from datetime import datetime,timezone
import os,time
from docx import Document
from docx.shared import Cm,Pt,RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
def fig(d,p,c,w=15.5):d.add_picture(str(p),width=Cm(w));d.paragraphs[-1].alignment=WD_ALIGN_PARAGRAPH.CENTER;q=d.add_paragraph(c);q.style='Caption';q.alignment=WD_ALIGN_PARAGRAPH.CENTER
def table(d,df,fs=7.5):
 t=d.add_table(rows=1,cols=len(df.columns));t.style='Table Grid'
 for i,x in enumerate(df.columns):t.rows[0].cells[i].text=str(x)
 for _,r in df.iterrows():
  c=t.add_row().cells
  for i,x in enumerate(r):c[i].text=str(x)
 for row in t.rows:
  for c in row.cells:
   for p in c.paragraphs:
    for r in p.runs:r.font.size=Pt(fs)
def toc(p):
 r=p.add_run();b=OxmlElement('w:fldChar');b.set(qn('w:fldCharType'),'begin');i=OxmlElement('w:instrText');i.set(qn('xml:space'),'preserve');i.text=' TOC \\o "1-3" \\h \\z ';s=OxmlElement('w:fldChar');s.set(qn('w:fldCharType'),'separate');t=OxmlElement('w:t');t.text='Mettre à jour le sommaire : Ctrl+A, F9.';e=OxmlElement('w:fldChar');e.set(qn('w:fldCharType'),'end');[r._r.append(x) for x in (b,i,s,t,e)]
def build(c,out):
 d=Document();d.styles['Normal'].font.name='Arial';d.styles['Normal'].font.size=Pt(9.5)
 for n in ('Title','Heading 1','Heading 2'):d.styles[n].font.color.rgb=RGBColor(31,78,120)
 p=d.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER;r=p.add_run('ANALYSE THERMIQUE D’UN INCENDIE SOUS LA PASSERELLE');r.bold=True;r.font.size=Pt(18);p=d.add_paragraph('Passerelle Gerland - La Saulaie');p.alignment=WD_ALIGN_PARAGRAPH.CENTER;p=d.add_paragraph('Rapport du '+datetime.now().strftime('%d/%m/%Y'));p.alignment=WD_ALIGN_PARAGRAPH.CENTER;d.add_page_break();d.add_heading('Sommaire',1);toc(d.add_paragraph());d.add_page_break()
 d.add_heading('1. Objet et présentation du projet',1);d.add_paragraph('L’étude évalue sous Python l’évolution temporelle des températures des suspentes secondaires et du câble principal lors d’un incendie sur la M7.')
 for p,cap,w in c['assets']:fig(d,p,cap,w)
 d.add_heading('2. Références',1);d.add_paragraph('NF EN 1991-1-2 ; NF EN 1993-1-2 ; guide Cerema Résistance à l’incendie des ponts routiers ; note SAU_AVP_NTE_069_A_FeuM7.')
 d.add_heading('3. Choix des courbes de feu',1);d.add_paragraph('Les courbes ISO 834, feu extérieur et HC sont étudiées séparément puis comparées. La courbe HC est ajoutée du fait de la proximité signalée d’une station Esso, située à environ 2 km de l’ouvrage. Ce choix prudent pourra être rediscuté avec la MOA et son AMO. Le guide Cerema rappelle que le maître d’ouvrage doit définir le scénario de feu contre lequel il souhaite protéger l’ouvrage.');fig(d,c['cerema'],'Figure 5 - Extrait du guide Cerema : choix des courbes.',15);fig(d,c['fire'],'Figure 6 - Courbes nominales température-temps.',15)
 d.add_heading('4. Géométrie simplifiée et positions de feu',1);table(d,c['geomtab']);fig(d,c['geom'],'Figure 7 - Trois coupes géométriques de référence et positions F1, F2 et F3.',15);fig(d,c['intrados'],'Figure 8 - Approximation de l’intrados par deux segments de droite.',14)
 d.add_heading('5. Choix des paramètres et hypothèses',1);table(d,c['params'])
 d.add_heading('6. Méthode de calcul',1);d.add_paragraph('Pour chaque courbe, position et longueur de foyer, Python calcule la température des gaz, le facteur de forme, la chaleur spécifique, les flux et l’incrément de température par pas de 5 s.')
 d.add_heading('7. Résultats thermiques',1);table(d,c['temps']);fig(d,c['f12'],'Figure 12 - Température de la suspente secondaire - foyer 20 m.');fig(d,c['f13'],'Figure 13 - Température du câble principal clos - foyer 20 m.')
 d.add_heading('8. Impact structurel',1);d.add_paragraph('Les résistances à chaud sont estimées par Ft,Rd,θ = ky,θ × Ft,Rd et les ratios par ηfi = NQP / Ft,Rd,θ. Les valeurs de Ft,Rd proviennent de la note SAU_AVP_NDC_062_A_JustifOADéfi.');table(d,c['struct'],6.8);d.add_paragraph(c['maxtext']);fig(d,c['f14'],'Figure 14 - Ratio de vérification de la suspente secondaire.');fig(d,c['f15'],'Figure 15 - Ratio de vérification du câble principal clos.')
 d.add_heading('9. Portée et limites',1);d.add_paragraph('L’approche est enveloppe et ne crédite pas complètement les masquages. Pour les suspentes, le bec de tablier peut créer un masque partiel, mais un rayonnement latéral demeure possible.')
 d.add_page_break();d.add_heading('Annexe B - Courbes de tous les cas étudiés',1)
 for p,cap in c['annex']:fig(d,p,cap,15)
 now=datetime.now(timezone.utc);d.core_properties.created=now;d.core_properties.modified=now;d.core_properties.last_modified_by='AIA Ingénierie';u=OxmlElement('w:updateFields');u.set(qn('w:val'),'true');d.settings._element.append(u);out.parent.mkdir(parents=True,exist_ok=True);d.save(out);os.utime(out,(time.time(),time.time()));return out
