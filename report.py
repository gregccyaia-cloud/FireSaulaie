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
def build(path,A,S,params,summary,res_summary,figs,resfigs,case,appendix,integ,firefig,geomfig):
 d=Document();sec=d.sections[0];sec.top_margin=sec.bottom_margin=Mm(18);sec.left_margin=sec.right_margin=Mm(20);d.styles['Normal'].font.name='Aptos';d.styles['Normal'].font.size=Pt(10.5)
 p=d.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER;x=p.add_run("ANALYSE THERMIQUE D'UN INCENDIE\nSOUS LA PASSERELLE");x.bold=True;x.font.size=Pt(23);p=d.add_paragraph('Passerelle Gerland - La Saulaie\nVersion V1.5_I autonome');p.alignment=WD_ALIGN_PARAGRAPH.CENTER;d.add_page_break()
 d.add_heading('1. Objet et projet',1);d.add_paragraph("Étude de l'évolution thermique de l'intrados, des suspentes secondaires et de la suspension principale par câble clos.");img(d,A/'ZZ extrait vue en plan generale.png','Figure 1 - Vue en plan générale.');img(d,A/'ZZ extrait plan suspension.png','Figure 2 - Système de suspension.');img(d,A/'Zz extrait coupe long generale.png','Figure 3 - Coupe longitudinale générale.');img(d,A/'ZZ coupe transv.png','Figure 4 - Coupe transversale type.')
 d.add_heading('2. Références',1)
 for x in ['NF EN 1991-1-2, § 3.1, § 3.2.1 et § 3.2.2.','NF EN 1993-1-2, § 3.4.1 et § 4.2.5.1.','NF EN 1993-1-11, structures à câbles ou éléments tendus.',"Cerema, Résistance à l'incendie des ponts routiers, 2018."]:d.add_paragraph(x,style='List Bullet')
 d.add_heading('3. Choix des courbes',1);d.add_paragraph("Feu 1 correspond à la courbe CN - ISO 834, représentée en pointillés. Feu 2 correspond à la courbe de feu extérieur, représentée en trait plein. Le MOA ou son AMO doit confirmer si un scénario HC doit être ajouté.");img(d,A/'extrait_cerema_choix_courbes.png','Figure 5 - Extrait Cerema relatif au choix des courbes.');img(d,firefig,'Figure 6 - Courbes nominales température-temps.')
 d.add_heading('4. Géométrie et positions',1);tbl(d,[{'Coupe':s.code,'Position':s.label,'Intrados (m)':f(s.intrados_m,3),'Naissance suspente (m)':f(s.intrados_m+.82,3),'Axe câble (m)':f(s.cable_m,3)} for s in S]);img(d,A/'ZZ_coupe longit partielle zone M7.png','Figure 7 - Hauteurs sur les trois coupes.');img(d,A/'ZZ_vue en plan cotée zone M7.png','Figure 8 - Largeurs de la M7.');img(d,A/'ZZ_demie coupe tablier et approx intrados.png',"Figure 9 - Approximation de l'intrados par 2 segments.");d.add_paragraph('F1 : ouest ; F2 : centre ; F3 : est.');img(d,geomfig,'Figure 10 - Trois coupes géométriques.')
 d.add_heading('5. Paramètres',1);tbl(d,[{'Paramètre':k,'Valeur':v} for k,v in params])
 d.add_heading('6. Résultats thermiques',1);d.add_paragraph('Convention graphique : feu 1 en pointillés ; feu 2 en trait plein. Les couleurs distinguent F1, F2 et F3.');tbl(d,summary)
 for c,p in figs:img(d,p,c)
 d.add_heading('7. Pré-analyse de résistance',1);d.add_paragraph("Même convention graphique : feu 1 en pointillés et feu 2 en trait plein. F_t,Rd,20 vaut 11 897 kN pour la suspension principale et 541 kN pour une suspente secondaire. La loi k_y,θ est un proxy à confirmer.");tbl(d,res_summary)
 for c,p in resfigs:img(d,p,c)
 d.add_paragraph("Aucun taux de travail n'est calculé faute d'efforts N_Ed.")
 d.add_page_break();d.add_heading('Annexe A - Calcul détaillé et comparaison des suspensions à 30 min',1);d.add_paragraph(f"Cas critique : {case['fire']} ; {case['position']} ; coupe {case['section']} ; foyer {f(case['L'],1)} m.");tbl(d,[{'Grandeur':k,'Valeur':v} for k,v in case['values']]);d.add_heading('A.1 Processus d’intégration',2);tbl(d,[{'Étape':'1','Calcul':'θ_a,i'},{'Étape':'2','Calcul':'c_a(θ_a,i)'},{'Étape':'3','Calcul':'q_conv,i, q_rad,i et q_net,i'},{'Étape':'4','Calcul':'Δθ_a,i'},{'Étape':'5','Calcul':'θ_a,i+1 = θ_a,i + Δθ_a,i'}]);img(d,integ,"Figure A.1 - Gaz, suspente secondaire et suspension principale jusqu'à 30 min.");d.add_heading('A.2 Dernier pas du cas critique',2);tbl(d,[{'Grandeur':'q_conv','Valeur':f(case['qc'],1)+' W/m²'},{'Grandeur':'q_rad','Valeur':f(case['qr'],1)+' W/m²'},{'Grandeur':'q_net','Valeur':f(case['qn'],1)+' W/m²'},{'Grandeur':'Δθ_a','Valeur':f(case['dta'],4)+' °C'},{'Grandeur':'θ_a,i → θ_a,i+1','Valeur':f(case['ta0'],2)+' → '+f(case['ta1'],2)+' °C'}])
 d.add_page_break();d.add_heading('Annexe B - Tous les cas et enveloppes',1);d.add_paragraph("Chaque graphique contient explicitement les 18 séries de l'élément considéré : 2 feux × 3 positions × 3 longueurs. Le faisceau min-max et ses enveloppes sont superposés. Avec Φ = 1,0, plusieurs séries coïncident exactement ; des marqueurs décalés permettent néanmoins de constater leur présence. Si l'enveloppe a une épaisseur nulle, cela traduit le modèle actuel et non une omission de cas.")
 for c,p in appendix:img(d,p,c)
 path=Path(path);d.save(path);return path
