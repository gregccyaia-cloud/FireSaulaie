from pathlib import Path
from datetime import datetime
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.shared import Cm,Mm,Pt

def r(x):o=OxmlElement('m:r');t=OxmlElement('m:t');t.text=x;o.append(t);return o
def sub(b,s):o=OxmlElement('m:sSub');e=OxmlElement('m:e');e.append(r(b));q=OxmlElement('m:sub');q.append(r(s));o.extend([e,q]);return o
def frac(n,d):o=OxmlElement('m:f');a=OxmlElement('m:num');b=OxmlElement('m:den');[a.append(x) for x in n];[b.append(x) for x in d];o.extend([a,b]);return o
def eq(d,e):p=d.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER;mp=OxmlElement('m:oMathPara');m=OxmlElement('m:oMath');[m.append(x) for x in e];mp.append(m);p._p.append(mp)
def q(s):return sub('q',s)
def th(s):return sub('θ',s)
def img(d,p,c,w=16):d.add_picture(str(p),width=Cm(w));d.paragraphs[-1].alignment=WD_ALIGN_PARAGRAPH.CENTER;x=d.add_paragraph(c);x.alignment=WD_ALIGN_PARAGRAPH.CENTER;x.runs[0].italic=True
def tbl(d,rows):
 if not rows:return
 hs=list(rows[0]);t=d.add_table(rows=1,cols=len(hs));t.style='Table Grid'
 for i,h in enumerate(hs):t.rows[0].cells[i].text=h;t.rows[0].cells[i].paragraphs[0].runs[0].bold=True
 for row in rows:
  c=t.add_row().cells
  for i,h in enumerate(hs):c[i].text=str(row[h])
def f(v,n=2):return f'{v:.{n}f}'.replace('.',',')
def build(path,A,sections,params,summary,res_summary,figs,resfigs,case,appendix,integ,firefig,geomfig):
 d=Document();s=d.sections[0];s.top_margin=s.bottom_margin=Mm(18);s.left_margin=s.right_margin=Mm(20);d.styles['Normal'].font.name='Aptos';d.styles['Normal'].font.size=Pt(10.5)
 p=d.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER;x=p.add_run("ANALYSE THERMIQUE D'UN INCENDIE\nSOUS LA PASSERELLE");x.bold=True;x.font.size=Pt(23);p=d.add_paragraph('Passerelle Gerland - La Saulaie\nVersion V1.5_H autonome');p.alignment=WD_ALIGN_PARAGRAPH.CENTER;d.add_page_break()
 d.add_heading('1. Objet et projet',1);d.add_paragraph("Étude de l'évolution thermique de l'intrados, des suspentes et des câbles principaux.");img(d,A/'ZZ extrait vue en plan generale.png','Figure 1 - Vue en plan générale.');img(d,A/'ZZ extrait plan suspension.png','Figure 2 - Système de suspension.');img(d,A/'Zz extrait coupe long generale.png','Figure 3 - Coupe longitudinale générale.');img(d,A/'ZZ coupe transv.png','Figure 4 - Coupe transversale type.')
 d.add_heading('2. Références',1)
 for x in ['NF EN 1991-1-2, § 3.1, § 3.2.1 et § 3.2.2.','NF EN 1993-1-2, § 3.4.1 et § 4.2.5.1.','NF EN 1993-1-11, structures à câbles ou éléments tendus.',"Cerema, Résistance à l'incendie des ponts routiers, 2018."]:d.add_paragraph(x,style='List Bullet')
 d.add_heading('3. Choix de la courbe de feu',1);d.add_paragraph("Les courbes CN - ISO 834 et feu extérieur sont calculées séparément. Le guide Cerema indique que la courbe HC peut être utilisée pour les feux d'hydrocarbures. Le MOA ou son AMO doit confirmer si ce scénario doit être ajouté.");img(d,A/'extrait_cerema_choix_courbes.png','Figure 5 - Extrait Cerema relatif au choix des courbes.');img(d,firefig,'Figure 6 - Courbes nominales température-temps.')
 d.add_heading('4. Géométrie et positions de feu',1);tbl(d,[{'Coupe':x.code,'Position':x.label,'Intrados (m)':f(x.intrados_m,3),'Naissance suspente (m)':f(x.intrados_m+.82,3),'Axe câble (m)':f(x.cable_m,3)} for x in sections]);img(d,A/'ZZ_coupe longit partielle zone M7.png','Figure 7 - Hauteurs sur les trois coupes.');img(d,A/'ZZ_vue en plan cotée zone M7.png','Figure 8 - Largeurs de la M7.');img(d,A/'ZZ_demie coupe tablier et approx intrados.png',"Figure 9 - Approximation de l'intrados par 2 segments.");d.add_paragraph('F1 : ouest ; F2 : centre ; F3 : est.');img(d,geomfig,'Figure 10 - Trois coupes géométriques.')
 d.add_heading('5. Paramètres et hypothèses',1);tbl(d,[{'Paramètre et référence':k,'Valeur':v} for k,v in params]);d.add_paragraph("Le facteur Φ vaut 1,0. La chaleur spécifique c_a(θ_a) est recalculée à chaque pas selon la NF EN 1993-1-2.")
 d.add_heading('6. Résultats thermiques',1);tbl(d,summary)
 for c,p in figs:img(d,p,c)
 d.add_heading('7. Pré-analyse de résistance',1);d.add_paragraph("F_t,Rd,20 vaut 11 897 kN pour le câble clos et 541 kN pour une suspente. La résistance indicative à chaud est F_t,Rd,θ = k_y,θ F_t,Rd,20. La loi k_y,θ de l'EN 1993-1-2 est utilisée comme proxy à confirmer pour les fils THR et la nuance 520.");tbl(d,res_summary)
 for c,p in resfigs:img(d,p,c)
 d.add_paragraph("Aucun taux de travail n'est calculé faute d'efforts N_Ed.")
 # ANNEXE A EXPLICITEMENT RESTAUREE
 d.add_page_break();d.add_heading('Annexe A - Calcul détaillé du cas critique à 30 min',1);d.add_paragraph(f"Cas : {case['fire']} ; {case['position']} ; coupe {case['section']} ; {case['element']} ; foyer {f(case['L'],1)} m.");tbl(d,[{'Grandeur':k,'Valeur':v} for k,v in case['values']]);d.add_heading('A.1 Processus d’intégration',2);tbl(d,[{'Étape':'1','Opération':'Lecture de θ_a,i','Résultat':'Température au début du pas'},{'Étape':'2','Opération':'Calcul de c_a(θ_a,i)','Résultat':'Chaleur spécifique actualisée'},{'Étape':'3','Opération':'Calcul des flux','Résultat':'q_conv,i, q_rad,i et q_net,i'},{'Étape':'4','Opération':'Calcul de Δθ_a,i','Résultat':'Incrément thermique'},{'Étape':'5','Opération':'Mise à jour','Résultat':'θ_a,i+1 = θ_a,i + Δθ_a,i'}]);img(d,integ,"Figure A.1 - Intégration temporelle jusqu'à 30 min.");d.add_heading('A.2 Dernier pas avant 30 min',2);eq(d,[q('conv'),r(' = '+f(case['qc'],1)+' W/m²')]);eq(d,[q('rad'),r(' = '+f(case['qr'],1)+' W/m²')]);eq(d,[q('net'),r(' = '+f(case['qn'],1)+' W/m²')]);eq(d,[r('Δ'),th('a,t'),r(' = '+f(case['dta'],4)+' °C')]);d.add_paragraph(f"La température passe de {f(case['ta0'],2)} °C à {f(case['ta1'],2)} °C sur le dernier pas de 5 s.")
 d.add_page_break();d.add_heading('Annexe B - Courbes de tous les cas étudiés',1)
 for c,p in appendix:img(d,p,c)
 path=Path(path);d.save(path);return path
