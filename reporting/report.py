from docx import Document
from docx.shared import Cm

def create_word_report(summary_df, png_paths, output_path):
    doc=Document(); doc.add_heading("Analyse incendie sous la passerelle - V1.1",0)
    doc.add_paragraph("Rapport automatique de calcul. Les hypotheses V1.1 et leurs limites doivent etre validees avant usage de justification.")
    doc.add_heading("Synthese",level=1)
    table=doc.add_table(rows=1,cols=len(summary_df.columns)); table.style="Table Grid"
    for i,c in enumerate(summary_df.columns): table.rows[0].cells[i].text=str(c)
    for _,row in summary_df.iterrows():
        cells=table.add_row().cells
        for i,v in enumerate(row): cells[i].text=str(v)
    doc.add_heading("Graphiques",level=1)
    for p in png_paths:
        doc.add_picture(str(p),width=Cm(16)); doc.add_paragraph(p.stem)
    doc.save(output_path)
