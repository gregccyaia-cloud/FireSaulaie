from datetime import datetime,timezone
from pathlib import Path
import os,time
from docx import Document
from docx.shared import Cm,Pt,RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def toc(p):
 r=p.add_run();b=OxmlElement('w:fldChar');b.set(qn('w:fldCharType'),'begin');i=OxmlElement('w:instrText');i.set(qn('xml:space'),'preserve');i.text=' TOC \\o "1-3" \\h \\z ';s=OxmlElement('w:fldChar');s.set(qn('w:fldCharType'),'separate');t=OxmlElement('w:t');t.text='Mettre à jour le sommaire dans Word : Ctrl+A, F9.';e=OxmlElement('w:fldChar');e.set(qn('w:fldCharType'),'end');[r._r.append(x) for x in (b,i,s,t,e)]
def table(d,h,rows,fs=8.5):
 t=d.add_table(rows=1,cols=len(h));t.style='Table Grid';t.alignment=WD_TABLE_ALIGNMENT.CENTER
 for j,x in enumerate(h):t.rows[0].cells[j].text=str(x)
 for row in rows:
  cells=t.add_row().cells
  for j,x in enumerate(row):cells[j].text=str(x)
 for row in t.rows:
  for c in row.cells:
   for p in c.paragraphs:
    for r in p.runs:r.font.size=Pt(fs)
 return t
def fig(d,p,caption,w=15.5):
 if not Path(p).exists():return
 q=d.add_paragraph();q.alignment=WD_ALIGN_PARAGRAPH.CENTER;q.add_run().add_picture(str(p),width=Cm(w));c=d.add_paragraph(caption);c.style='Caption';c.alignment=WD_ALIGN_PARAGRAPH.CENTER
def asset(d,p,caption,w=16):fig(d,p,caption,w)
def build(ctx,out):
 d=Document();sec=d.sections[0];sec.top_margin=Cm(1.6);sec.bottom_margin=Cm(1.6);sec.left_margin=Cm(2);sec.right_margin=Cm(2);d.styles['Normal'].font.name='Arial';d.styles['Normal'].font.size=Pt(9.5)
 for n in ('Title','Heading 1','Heading 2'):d.styles[n].font.name='Arial';d.styles[n].font.color.rgb=RGBColor(31,78,120)
 p=d.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER;r=p.add_run("ANALYSE THERMIQUE D’UN INCENDIE SOUS LA PASSERELLE");r.bold=True;r.font.size=Pt(18);r.font.color.rgb=RGBColor(31,78,120)
 p=d.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER;p.add_run('Passerelle Gerland - La Saulaie').bold=True
 p=d.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER;p.add_run('Rapport du '+datetime.now().strftime('%d/%m/%Y'))
 d.add_page_break();d.add_heading('Sommaire',1);toc(d.add_paragraph());d.add_page_break()
 d.add_heading('1. Objet et présentation du projet',1);d.add_paragraph("L’étude évalue l’évolution de la température des suspentes secondaires et des câbles principaux lors d’un incendie sur la M7 sous la passerelle.")
 for p,c,w in ctx['project_assets']:asset(d,p,c,w)
 d.add_heading('2. Références',1);d.add_paragraph('• NF EN 1991-1-2 : actions thermiques sur les structures exposées au feu.\n• NF EN 1993-1-2 : propriétés thermiques de l’acier et calcul au feu.\n• Cerema, Résistance à l’incendie des ponts routiers, guide méthodologique, 2018.\n• Note SAU_AVP_NTE_069_A_FeuM7.')
 d.add_heading('3. Choix de la courbe de feu',1);d.add_paragraph(ctx['choice']);fig(d,ctx['cerema'],'Figure 5 - Extrait du guide Cerema : choix des courbes.',15);d.add_paragraph(ctx['moa']);d.add_paragraph(ctx['tanker']);fig(d,ctx['fire'],'Figure 6 - Courbes nominales température-temps.')
 d.add_heading('4. Géométrie simplifiée et positions de feu',1);table(d,['Coupe','Intrados (m)','Naissance suspente (m)','Axe câble (m)'],ctx['geometry_rows']);d.add_paragraph('F1 correspond à la zone ouest, F2 à l’axe de la M7 et F3 à la zone est.');fig(d,ctx['geometry'],'Figure 7 - Trois coupes géométriques de référence et positions F1, F2 et F3.')
 d.add_heading('5. Choix des paramètres et hypothèses',1);table(d,['Paramètre','Valeur retenue'],ctx['params']);d.add_paragraph(ctx['cp_text'])
 d.add_heading('6. Méthode de calcul',1);d.add_paragraph(ctx['method']);d.add_paragraph('L’annexe A détaille le processus d’intégration, les grandeurs du dernier pas avant 30 min et la courbe d’intégration du cas critique.')
 d.add_heading('7. Résultats de synthèse',1);table(d,list(ctx['summary'].columns),ctx['summary'].values.tolist(),7.2);fig(d,ctx['f10'],'Figure 10 - Échauffement - Suspente secondaire - foyer 15 m.');fig(d,ctx['f11'],'Figure 11 - Échauffement - Câble principal clos - foyer 15 m.')
 d.add_heading('8. Impact structurel',1);d.add_paragraph(ctx['structural'])
 d.add_heading('9. Limites et domaine de validité',1);d.add_paragraph(ctx['limits'])
 d.add_page_break();d.add_heading('Annexe A - Calcul détaillé du cas critique à 30 min',1);table(d,['Étape','Opération','Résultat'],ctx['steps']);fig(d,ctx['integration'],'Figure A.1 - Intégration temporelle du cas critique.');table(d,['Grandeur','Valeur'],ctx['worst_rows']);d.add_paragraph(ctx['worst_eq'])
 d.add_page_break();d.add_heading('Annexe B - Courbes de tous les cas étudiés',1);d.add_paragraph('Chaque graphique représente les neuf cas F1/F2/F3 et L = 10/15/20 m, le domaine min.-max. et l’enveloppe maximale. Les courbes ne sont donc pas réduites à un cas unique.')
 for p,c in ctx['annex']:fig(d,p,c,15)
 now=datetime.now(timezone.utc);d.core_properties.created=now;d.core_properties.modified=now;d.core_properties.last_modified_by='AIA Ingénierie';u=OxmlElement('w:updateFields');u.set(qn('w:val'),'true');d.settings._element.append(u)
 out.parent.mkdir(parents=True,exist_ok=True);d.save(out);epoch=time.time();os.utime(out,(epoch,epoch));return out
