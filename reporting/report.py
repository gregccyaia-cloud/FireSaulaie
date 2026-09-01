from docx import Document
from docx.shared import Cm,Pt,RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT,WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.section import WD_SECTION
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def shade(c,color):
 p=c._tc.get_or_add_tcPr();s=OxmlElement('w:shd');s.set(qn('w:fill'),color);p.append(s)
def add_table(d,headers,rows,font=8.5):
 t=d.add_table(rows=1,cols=len(headers));t.style='Table Grid';t.alignment=WD_TABLE_ALIGNMENT.CENTER
 for i,h in enumerate(headers):
  c=t.rows[0].cells[i];c.text=str(h);shade(c,'1F4E78')
  for r in c.paragraphs[0].runs:r.font.bold=True;r.font.color.rgb=RGBColor(255,255,255);r.font.size=Pt(font)
 for row in rows:
  cells=t.add_row().cells
  for i,v in enumerate(row):
   cells[i].text=str(v);cells[i].vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
   for r in cells[i].paragraphs[0].runs:r.font.size=Pt(font)
 return t
def add_figure(d,p,caption,num,w=15.5):
 if not p.exists():return num
 q=d.add_paragraph();q.alignment=WD_ALIGN_PARAGRAPH.CENTER;q.add_run().add_picture(str(p),width=Cm(w))
 c=d.add_paragraph(f'Figure {num} - {caption}');c.alignment=WD_ALIGN_PARAGRAPH.CENTER;c.style='Caption';return num+1
def build_report(ctx,path):
 path.parent.mkdir(parents=True,exist_ok=True);d=Document();sec=d.sections[0];sec.top_margin=Cm(1.7);sec.bottom_margin=Cm(1.7);sec.left_margin=Cm(2);sec.right_margin=Cm(2)
 d.styles['Normal'].font.name='Arial';d.styles['Normal'].font.size=Pt(9.5)
 for n in ('Title','Heading 1','Heading 2','Heading 3'):d.styles[n].font.name='Arial';d.styles[n].font.color.rgb=RGBColor(31,78,120)
 p=d.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER;r=p.add_run('ANALYSE THERMIQUE D’UN INCENDIE SOUS LA PASSERELLE');r.bold=True;r.font.size=Pt(18);r.font.color.rgb=RGBColor(31,78,120)
 p=d.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER;p.add_run('Passerelle Gerland - La Saulaie | Modèle Python V1.4 consolidé').bold=True
 d.add_paragraph('Document de travail pour validation du modèle thermique. Les coefficients d’exposition et le facteur de massiveté de l’intrados restent provisoires.')
 d.add_page_break();n=1
 # Coupe déplacée juste avant le paragraphe 2
 if ctx['coupe'].exists():n=add_figure(d,ctx['coupe'],'Coupe transversale type.',n)
 d.add_heading('1. Objet et périmètre',1);d.add_paragraph('Le calcul évalue l’évolution de la température de l’intrados métallique, des suspentes secondaires et du câble principal. Deux courbes de feu sont calculées séparément puis comparées. Les résultats ne constituent pas encore une vérification structurelle.')
 d.add_heading('2. Données du projet et géométrie',1);add_table(d,['Paramètre','Valeur'],ctx['project'])
 d.add_paragraph('Le profil transversal de l’intrados est approché par deux segments symétriques à partir de l’axe du tablier : une remontée de 0,19 m à 1,91 m de l’axe, puis une remontée totale de 0,61 m au bord du tablier, à 3,70 m de l’axe. La naissance inférieure des suspentes est située à 0,82 m au-dessus du point bas de l’intrados.')
 if ctx['demicoupe'].exists():n=add_figure(d,ctx['demicoupe'],'Demi-coupe et approximation de l’intrados par 2 segments de droite.',n)
 d.add_heading('3. Choix des paramètres et hypothèses',1)
 d.add_paragraph('Les positions de foyer sont introduites comme suit : F1 correspond à un foyer placé dans la zone ouest du franchissement, F2 à un foyer placé à l’axe de la M7 et F3 à un foyer placé dans la zone est. Ces repères sont utilisés dans les tableaux et graphiques suivants.')
 add_table(d,['Famille','Hypothèse retenue','Statut'],ctx['hypotheses'])
 d.add_heading('4. Scénarios de feu',1);d.add_paragraph('Les deux lois sont évaluées de 0 à 120 minutes. La variable t est exprimée en minutes et la température en degrés Celsius.')
 n=add_figure(d,ctx['eq_png'],'Formules des courbes de feu.',n);n=add_figure(d,ctx['fire_png'],'Comparaison des températures nominales des gaz.',n)
 d.add_heading('5. Principes et résultats thermiques',1);d.add_paragraph('Le modèle capacitif suppose une température uniforme dans chaque section. À chaque pas de 5 s, le bilan énergétique combine convection et rayonnement. Les indices et exposants des expressions suivantes sont rendus sous forme mathématique.')
 n=add_figure(d,ctx['principles_png'],'Formulation des flux thermiques et du facteur de section.',n)
 add_table(d,['Grandeur','Valeur'],ctx['thermal'])
 d.add_heading('5.1 Échauffement de la suspente secondaire',2);n=add_figure(d,ctx['hanger_png'],'Échauffement de la suspente secondaire pour H = 15 m : six courbes correspondant aux deux feux et aux positions F1, F2 et F3.',n)
 d.add_heading('5.2 Échauffement du câble principal clos',2);n=add_figure(d,ctx['cable_png'],'Échauffement du câble principal clos pour H = 15 m : six courbes correspondant aux deux feux et aux positions F1, F2 et F3.',n)
 d.add_heading('6. Synthèse des 18 cas',1);add_table(d,list(ctx['summary'].columns),ctx['summary'].values.tolist(),7.5)
 d.add_heading('7. Cas le plus défavorable à 30 minutes',1);w=ctx['worst'];d.add_paragraph(f"Le cas retenu est {w['case']} pour l’élément {w['element']}. À 30 min, la température calculée est {w['T_end']:.2f} °C.")
 add_table(d,['Donnée','Valeur'],ctx['worst_rows'])
 d.add_paragraph('Vérification du dernier incrément avant 30 min :');d.add_paragraph(ctx['worst_equation'])
 n=add_figure(d,w['png'],f"Évolution thermique du cas {w['case']}.",n)
 d.add_heading('8. Conclusions et limites',1)
 for x in ctx['conclusions']:d.add_paragraph(x,style='List Bullet')
 d.add_page_break();d.add_heading('Annexe A - Données détaillées du cas défavorable à 30 minutes',1);add_table(d,['Grandeur','Valeur'],ctx['worst_rows']);d.add_paragraph(ctx['worst_equation'])
 d.add_page_break();d.add_heading('Annexe B - Courbes de tous les cas étudiés',1)
 for item in ctx['all_figures']:n=add_figure(d,item[0],item[1],n,14.5)
 d.save(str(path));return path
