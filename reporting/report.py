from docx import Document
from docx.shared import Cm
def create_report(summary,pngs,output_path):
 output_path.parent.mkdir(parents=True,exist_ok=True)
 d=Document();d.add_heading('Analyse incendie sous la passerelle - V1.1',0)
 d.add_paragraph('Rapport automatique. Les hypotheses V1.1 doivent etre validees avant utilisation pour une justification.')
 d.add_heading('Synthese des cas',1);t=d.add_table(rows=1,cols=len(summary.columns));t.style='Table Grid'
 for i,c in enumerate(summary.columns):t.rows[0].cells[i].text=str(c)
 for _,row in summary.iterrows():
  cells=t.add_row().cells
  for i,v in enumerate(row):cells[i].text=str(v)
 d.add_heading('Graphiques',1)
 for p in pngs:
  if p.exists():d.add_picture(str(p),width=Cm(15.5));d.add_paragraph(p.stem)
 d.save(str(output_path));return output_path
