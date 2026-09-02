from pathlib import Path
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Cm,Mm,Pt
def img(d,p,c,w=16):d.add_picture(str(p),width=Cm(w));d.paragraphs[-1].alignment=WD_ALIGN_PARAGRAPH.CENTER;x=d.add_paragraph(c);x.alignment=WD_ALIGN_PARAGRAPH.CENTER;x.runs[0].italic=True
def tbl(d,R):
 if not R:return
 H=list(R[0]);t=d.add_table(rows=1,cols=len(H));t.style='Table Grid'
 for i,h in enumerate(H):t.rows[0].cells[i].text=h;t.rows[0].cells[i].paragraphs[0].runs[0].bold=True
 for r in R:
  c=t.add_row().cells
  for i,h in enumerate(H):c[i].text=str(r[h])
def f(v,n=2):return f'{v:.{n}f}'.replace('.',',')
def build(path,A,S,params,summary,rs,figs,rfigs,case,appendix,integ,ff,gf):
 d=Document();sec=d.sections[0];sec.top_margin=sec.bottom_margin=Mm(18);sec.left_margin=sec.right_margin=Mm(20);d.styles['Normal'].font.name='Aptos';d.styles['Normal'].font.size=Pt(10.5)
 p=d.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER;x=p.add_run("ANALYSE THERMIQUE DE TROIS FEUX\nSOUS LA PASSERELLE");x.bold=True;x.font.size=Pt(23);p=d.add_paragraph('Passerelle Gerland - La Saulaie\nVersion V2.0 autonome');p.alignment=WD_ALIGN_PARAGRAPH.CENTER;d.add_page_break()
 d.add_heading('1. Objet',1);d.add_paragraph("La note compare les montées en température et les températures atteintes dans les suspentes secondaires et la suspension principale sous l'effet de trois feux nominaux : CN - ISO 834, feu extérieur et feu d'hydrocarbure HC. Les historiques obtenus préparent l'analyse structurelle et l'analyse des dommages, à poursuivre en échanges avec le maître d'ouvrage et son AMO.");img(d,A/'ZZ extrait vue en plan generale.png','Figure 1 - Vue en plan générale.');img(d,A/'ZZ extrait plan suspension.png','Figure 2 - Système de suspension.');img(d,A/'Zz extrait coupe long generale.png','Figure 3 - Coupe longitudinale générale.');img(d,A/'ZZ coupe transv.png','Figure 4 - Coupe transversale type.')
 d.add_heading('2. Références',1)
 for x in ['NF EN 1991-1-2, § 3.1 et § 3.2.1 à § 3.2.3.','NF EN 1993-1-2, § 3.4.1 et § 4.2.5.1.','NF EN 1993-1-11, éléments tendus.',"Cerema, Résistance à l'incendie des ponts routiers, 2018."]:d.add_paragraph(x,style='List Bullet')
 d.add_heading('3. Trois scénarios de feu',1);d.add_paragraph("Feu 1 : CN - ISO 834, pointillé. Feu 2 : feu extérieur, trait plein. Feu 3 : hydrocarbure HC non majoré, trait mixte. La courbe HC est ajoutée pour représenter un scénario d'hydrocarbures à montée rapide. La courbe HCM n'est pas étudiée.");img(d,A/'extrait_cerema_choix_courbes.png','Figure 5 - Extrait Cerema sur le choix des courbes.');img(d,A/'image.png','Figure 6 - Extrait Cerema : formulation de la courbe HC.');img(d,ff,'Figure 7 - Comparaison des trois courbes nominales.')
 d.add_heading('4. Géométrie',1);tbl(d,[{'Coupe':s.code,'Position':s.label,'Intrados (m)':f(s.intrados_m,3),'Naissance suspente (m)':f(s.intrados_m+.82,3),'Axe câble (m)':f(s.cable_m,3)} for s in S]);img(d,A/'ZZ_coupe longit partielle zone M7.png','Figure 8 - Hauteurs.');img(d,A/'ZZ_vue en plan cotée zone M7.png','Figure 9 - Largeurs de la M7.');img(d,A/'ZZ_demie coupe tablier et approx intrados.png',"Figure 10 - Approximation de l'intrados.");d.add_paragraph('F1 : ouest ; F2 : centre ; F3 : est.');img(d,gf,'Figure 11 - Trois coupes géométriques.')
 d.add_heading('5. Paramètres',1);tbl(d,[{'Paramètre':k,'Valeur':v} for k,v in params])
 d.add_heading('6. Résultats thermiques',1);d.add_paragraph('Convention : feud 1 pointillé, feu 2 plein, feu 3 trait mixte ; couleurs F1/F2/F3.');tbl(d,summary)
 for c,p in figs:img(d,p,c)
 d.add_heading('7. Pré-analyse de résistance',1);d.add_paragraph("Les résistances indicatives à chaud sont calculées pour les trois feux à partir de F_t,Rd,20 = 11 897 kN et 541 kN. La loi k_y,θ reste un proxy à confirmer pour les produits réels.");tbl(d,rs)
 for c,p in rfigs:img(d,p,c)
 d.add_heading('8. Poursuite de l’analyse',1);d.add_paragraph("Les températures issues des trois feux seront confrontées aux efforts axiaux et aux critères de dommage. Les échanges avec le MOA et son AMO devront préciser les situations de calcul, niveaux de dommage admissibles, réparabilité, scénarios de perte de suspentes et éventuelles protections.")
 d.add_page_break();d.add_heading('Annexe A - Cas critique à 30 min',1);d.add_paragraph(f"Le cas critique parmi les trois feux est : {case['fire']}, {case['position']}, coupe {case['section']}, foyer {f(case['L'],1)} m.");tbl(d,[{'Grandeur':k,'Valeur':v} for k,v in case['values']]);d.add_heading('A.1 Processus d’intégration',2);tbl(d,[{'Étape':'1','Calcul':'θ_a,i'},{'Étape':'2','Calcul':'c_a(θ_a,i)'},{'Étape':'3','Calcul':'q_conv,i, q_rad,i, q_net,i'},{'Étape':'4','Calcul':'Δθ_a,i'},{'Étape':'5','Calcul':'θ_a,i+1'}]);img(d,integ,'Figure A.1 - Cas critique : gaz, suspente secondaire et suspension principale.');d.add_heading('A.2 Dernier pas',2);tbl(d,[{'Grandeur':'q_conv','Valeur':f(case['qc'],1)+' W/m²'},{'Grandeur':'q_rad','Valeur':f(case['qr'],1)+' W/m²'},{'Grandeur':'q_net','Valeur':f(case['qn'],1)+' W/m²'},{'Grandeur':'Δθ_a','Valeur':f(case['dta'],4)+' °C'}])
 d.add_page_break();d.add_heading('Annexe B - Tous les cas et enveloppes des trois feux',1);d.add_paragraph("Chaque graphique regroupe 27 séries par élément : 3 feux × 3 positions × 3 longueurs, ainsi que le faisceau min-max et les enveloppes.")
 for c,p in appendix:img(d,p,c)
 path=Path(path);d.save(path);return path
