"""Rapport Word V1.5_A autonome avec équations OMML et annexes."""
from pathlib import Path
from datetime import datetime
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm,Pt,Mm,RGBColor

def rr(x):o=OxmlElement('m:r');t=OxmlElement('m:t');t.text=x;o.append(t);return o
def sub(b,s):o=OxmlElement('m:sSub');e=OxmlElement('m:e');e.append(rr(b));q=OxmlElement('m:sub');q.append(rr(s));o.extend([e,q]);return o
def sup(b,s):o=OxmlElement('m:sSup');e=OxmlElement('m:e');e.append(rr(b));q=OxmlElement('m:sup');q.append(rr(s));o.extend([e,q]);return o
def frac(n,d):o=OxmlElement('m:f');a=OxmlElement('m:num');b=OxmlElement('m:den');[a.append(x) for x in n];[b.append(x) for x in d];o.extend([a,b]);return o
def eq(doc,els):
 p=doc.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER;mp=OxmlElement('m:oMathPara');m=OxmlElement('m:oMath');[m.append(x) for x in els];mp.append(m);p._p.append(mp)
def q(s):return sub('q',s)
def th(s):return sub('θ',s)
def shade(cell,fill='D9EAF7'):
 tc=cell._tc.get_or_add_tcPr();sh=OxmlElement('w:shd');sh.set(qn('w:fill'),fill);tc.append(sh)
def img(doc,path,cap,w=16):
 path=Path(path)
 if not path.exists():raise FileNotFoundError(path)
 doc.add_picture(str(path),width=Cm(w));doc.paragraphs[-1].alignment=WD_ALIGN_PARAGRAPH.CENTER
 p=doc.add_paragraph(cap);p.alignment=WD_ALIGN_PARAGRAPH.CENTER;p.paragraph_format.keep_with_next=False;p.runs[0].italic=True
def tbl(doc,rows,widths=None):
 if not rows:return None
 hs=list(rows[0]);t=doc.add_table(rows=1,cols=len(hs));t.style='Table Grid';t.alignment=WD_TABLE_ALIGNMENT.CENTER
 for i,h in enumerate(hs):
  c=t.rows[0].cells[i];c.text=h;c.paragraphs[0].runs[0].bold=True;shade(c);c.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
 for row in rows:
  cells=t.add_row().cells
  for i,h in enumerate(hs):cells[i].text=str(row[h]);cells[i].vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
 return t
def f(v,n=2):return f'{v:.{n}f}'.replace('.',',')
def setup(d):
 s=d.sections[0];s.top_margin=s.bottom_margin=Mm(18);s.left_margin=s.right_margin=Mm(20)
 d.styles['Normal'].font.name='Aptos';d.styles['Normal'].font.size=Pt(10.5)
 for n,z,c in [('Title',24,'17365D'),('Heading 1',16,'17365D'),('Heading 2',13,'2F5597')]:
  st=d.styles[n];st.font.name='Aptos Display';st.font.size=Pt(z);st.font.color.rgb=RGBColor.from_string(c)
def equations(d):
 d.add_heading('Équations utilisées',2)
 d.add_paragraph('Courbe CN - ISO 834, NF EN 1991-1-2, § 3.2.1 :');eq(d,[th('g'),rr('(t) = 20 + 345 '),sub('log','10'),rr('(8t + 1)')])
 d.add_paragraph('Courbe de feu extérieur, NF EN 1991-1-2, § 3.2.2 :');eq(d,[th('g'),rr('(t) = 660[1 - 0,687 '),sup('e','-0,32t'),rr(' - 0,313 '),sup('e','-3,8t'),rr('] + 20')])
 d.add_paragraph('Flux convectif net, NF EN 1991-1-2, § 3.1 :');eq(d,[q('conv'),rr(' = '),sub('α','c'),rr('('),th('g'),rr(' - '),th('a'),rr(')')])
 d.add_paragraph('Flux radiatif net, NF EN 1991-1-2, § 3.1 :');eq(d,[q('rad'),rr(' = Φ '),sub('ε','m'),rr(' '),sub('ε','f'),rr(' σ ['),sup('(θg + 273,15)','4'),rr(' - '),sup('(θa + 273,15)','4'),rr(']')])
 d.add_paragraph('Facteur de section :');eq(d,[frac([sub('A','m')],[rr('V')]),rr(' = '),sub('η','exp'),rr(' '),frac([rr('4')],[rr('D')])])
 d.add_paragraph("Incrément de température, NF EN 1993-1-2, § 4.2.5.1 :");eq(d,[rr('Δ'),th('a,t'),rr(' = '),frac([sub('k','sh'),rr(' '),frac([sub('A','m')],[rr('V')]),rr(' '),q('net'),rr(' Δt')],[sub('ρ','a'),rr(' '),sub('c','a'),rr('('),th('a'),rr(')')])])
def build(path,assets,sections,params,summary,figures,case,appendix,integration_figure,fire_curve_figure,geometry_figure):
 d=Document();setup(d)
 p=d.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER;p.paragraph_format.space_before=Pt(55);x=p.add_run("ANALYSE THERMIQUE D'UN INCENDIE\nSOUS LA PASSERELLE");x.bold=True;x.font.size=Pt(23)
 p=d.add_paragraph('Passerelle Gerland - La Saulaie\nVersion V1.5_A autonome');p.alignment=WD_ALIGN_PARAGRAPH.CENTER
 p=d.add_paragraph('Rapport généré le '+datetime.now().strftime('%d/%m/%Y à %H:%M'));p.alignment=WD_ALIGN_PARAGRAPH.CENTER;d.add_page_break()
 d.add_heading("1. Objet et présentation du projet",1);d.add_paragraph("L'étude évalue l'évolution de la température de l'intrados, des suspentes secondaires et des câbles principaux lors d'un incendie sur la M7 sous la passerelle.")
 img(d,assets/'ZZ extrait vue en plan generale.png','Figure 1 - Vue en plan générale.');img(d,assets/'ZZ extrait plan suspension.png','Figure 2 - Élévation et plan du système de suspension.');img(d,assets/'Zz extrait coupe long generale.png','Figure 3 - Coupe longitudinale générale.');img(d,assets/'ZZ coupe transv.png','Figure 4 - Coupe transversale type du tablier.')
 d.add_heading('2. Références',1)
 for z in ['NF EN 1991-1-2, § 3.1, § 3.2.1 et § 3.2.2.','NF EN 1993-1-2, § 3.4.1 et § 4.2.5.1.',"Cerema, Résistance à l'incendie des ponts routiers, guide méthodologique, 2018.",'Note SAU_AVP_NTE_069_A_FeuM7.']:d.add_paragraph(z,style='List Bullet')
 d.add_heading('3. Choix de la courbe de feu',1)
 d.add_paragraph("Le choix des scénarios thermiques est établi en appui du guide Cerema « Résistance à l'incendie des ponts routiers », notamment de son passage consacré au choix des courbes de feu. Deux calculs indépendants sont menés : l'un avec la courbe CN - ISO 834 et l'autre avec la courbe de feu extérieur. Les résultats sont ensuite comparés et l'enveloppe est retenue pour la poursuite de l'analyse.")
 d.add_paragraph("Ce choix constitue l'hypothèse de la présente étude thermique. Il appartient néanmoins au maître d'ouvrage ou à son assistant à maîtrise d'ouvrage de confirmer à la maîtrise d'œuvre le scénario contre lequel l'ouvrage doit être protégé et, en particulier, de préciser si une courbe hydrocarbure HC doit également être étudiée. Le guide Cerema indique, dans la définition des responsabilités du maître d'ouvrage, que celui-ci doit définir le scénario de feu contre lequel il souhaite protéger l'ouvrage.")
 d.add_paragraph("Les hauteurs de flammes retenues pour le cadrage géométrique, jusqu'à 15 m, ainsi que les courbes CN et feu extérieur utilisées ici ne couvrent pas explicitement un feu de citerne d'hydrocarbures. Une telle situation devra faire l'objet d'une décision spécifique du maître d'ouvrage et, si elle est retenue, d'un scénario HC et d'hypothèses de foyer adaptées.")
 equations(d);img(d,fire_curve_figure,'Figure 5 - Courbes nominales température-temps.')
 d.add_heading('4. Géométrie simplifiée et positions de feu',1);d.add_paragraph("Trois coupes successives sont étudiées le long de l'axe de la passerelle au franchissement de la M7 : bord ouest, axe M7 et bord est.")
 tbl(d,[{'Coupe':s.code,'Position':s.label,'Intrados (m)':f(s.intrados_m,3),'Naissance suspente (m)':f(s.intrados_m+.82,3),'Axe câble (m)':f(s.cable_m,3)} for s in sections])
 img(d,assets/'ZZ_coupe longit partielle zone M7.png','Figure 6 - Hauteurs sur les trois coupes.');img(d,assets/'ZZ_vue en plan cotée zone M7.png','Figure 7 - Largeurs de la M7.');img(d,assets/'ZZ_demie coupe tablier et approx intrados.png',"Figure 8 - Demi-coupe et approximation de l'intrados par 2 segments de droite")
 d.add_paragraph("F1 correspond à la position ouest, F2 à la position centrale et F3 à la position est. Ces repères sont repris dans les tableaux et figures. Chaque position est associée à la coupe de référence la plus proche pour le contrôle de la distance tridimensionnelle.")
 img(d,geometry_figure,'Figure 9 - Trois coupes géométriques de référence et positions F1, F2 et F3.')
 d.add_heading('5. Choix des paramètres et hypothèses',1)
 d.add_paragraph("Le véhicule est représenté par un poids lourd de 16,0 m de longueur, 2,50 m de largeur et 4,00 m de hauteur, immobilisé sous l'ouvrage. Trois longueurs de foyer, 10 m, 15 m et 20 m, sont paramétrées en vue d'une analyse de sensibilité. La durée maximale du calcul est de 120 min, avec lectures à 15, 30, 60, 90 et 120 min ; la phase de refroidissement est ignorée.")
 tbl(d,[{'Paramètre et référence':k,'Valeur retenue':v} for k,v in params])
 d.add_heading('5.1 Chaleur spécifique de l’acier',2)
 d.add_paragraph("La chaleur spécifique c_a n'est pas supposée constante. À chaque pas, le programme l'évalue à partir de la température d'acier θ_a,i au début du pas, en appliquant la loi par morceaux de la NF EN 1993-1-2, § 3.4.1.2 : domaine 20 à 600 °C, domaine 600 à 735 °C, domaine 735 à 900 °C, puis valeur constante au-delà de 900 °C. Cette mise à jour est intégrée avant le calcul de l'incrément de température du pas considéré.")
 d.add_heading('5.2 Facteur de configuration radiatif Φ',2)
 d.add_paragraph("Dans l'expression du flux radiatif, Φ représente la part du rayonnement émis par la source qui atteint la surface réceptrice. Son évaluation dépend de la taille de la source, de la distance entre source et récepteur, de leurs orientations relatives et de la visibilité de la source. Le cadre Eurocode prévoit la détermination de facteurs de forme à partir de la géométrie des flammes et des éléments exposés.")
 d.add_paragraph("La V1.5_A retient Φ = 1,0. Ce choix est volontairement enveloppe : aucune réduction n'est admise tant qu'un calcul géométrique documenté n'a pas été réalisé. Au stade actuel, retenir Φ < 1 serait insuffisamment justifié. En outre, le poids lourd de 16 m est plus long que la largeur courante de 7,40 m du tablier et le foyer est situé à faible distance verticale de l'ouvrage ; ces dimensions ne garantissent pas, à elles seules, une réduction significative de l'exposition des éléments proches. Cette dernière appréciation constitue une hypothèse prudente de modélisation et non une valeur normative. Une réduction de Φ pourra être examinée ultérieurement à partir d'une représentation géométrique de la flamme, des masquages et des surfaces réceptrices.")
 d.add_heading('6. Résultats de synthèse',1);tbl(d,summary)
 for cap,p in figures:img(d,p,cap)
 d.add_paragraph("Certaines courbes se superposent exactement du fait de Φ = 1,0, de l'exposition uniforme et de l'absence d'atténuation géométrique. Les légendes conservent l'ensemble des cas calculés. Cette superposition traduit le caractère enveloppe de la V1.5_A plutôt qu'une impossibilité physique de différencier ultérieurement les positions.")
 d.add_heading('7. Impact structurel et poursuite de l’analyse',1)
 d.add_paragraph("Les historiques θ_a(t) constituent les données d'entrée de la vérification structurelle en situation d'incendie. La prochaine étape consistera à associer, pour chaque temps de lecture, les propriétés mécaniques réduites de l'acier à la température calculée, puis à vérifier les éléments tendus avec les efforts axiaux communiqués par le modèle global. Les efforts de référence seront a priori issus de l'ELS quasi permanent, sous réserve de la définition finale de la combinaison accidentelle et des actions concomitantes.")
 d.add_paragraph("L'analyse devra distinguer les câbles principaux et les suspentes secondaires. Elle portera notamment sur la réduction de résistance et de rigidité, l'allongement thermique, l'évolution de la tension, les redistributions entre suspentes, ainsi que les scénarios accidentels de perte d'une ou plusieurs suspentes. Les efforts axiaux dans les câbles principaux et les suspentes secondaires restent à renseigner avant d'effectuer ces vérifications.")
 d.add_heading('8. Limites et portée de la V1.5_A',1)
 d.add_paragraph("La distance tridimensionnelle est calculée à titre de contrôle et Φ = 1,0 est conservé comme hypothèse enveloppe. L'absence actuelle de facteur de forme détaillé ne fragilise donc pas le calcul par une réduction arbitraire ; elle conduit au contraire à ne créditer aucun effet favorable de distance, d'orientation ou de masquage. L'affinement géométrique permettra surtout de quantifier d'éventuelles réductions justifiables et de différencier les positions F1, F2 et F3.")
 d.add_page_break();d.add_heading('Annexe A - Calcul détaillé du cas critique à 30 min',1)
 d.add_paragraph(f"Cas retenu : {case['fire']} - {case['position']} - coupe {case['section']} - {case['element']} - foyer {f(case['L'],1)} m.")
 tbl(d,[{'Grandeur':k,'Valeur':v} for k,v in case['values']])
 d.add_heading('A.1 Principe de l’intégration temporelle',2)
 d.add_paragraph("Le calcul progresse par pas constants Δt = 5 s. Pour chaque indice i, la température obtenue au pas précédent est utilisée pour mettre à jour les propriétés thermiques et les flux avant de calculer la température du pas suivant.")
 tbl(d,[{'Étape':'1','Opération':'Lecture de θ_a,i','Résultat':'Température d’acier au début du pas'}, {'Étape':'2','Opération':'Calcul de c_a(θ_a,i)','Résultat':'Chaleur spécifique par la loi NF EN 1993-1-2'}, {'Étape':'3','Opération':'Calcul des flux','Résultat':'q_conv,i, q_rad,i et q_net,i'}, {'Étape':'4','Opération':'Calcul de Δθ_a,i','Résultat':'Bilan énergétique sur Δt'}, {'Étape':'5','Opération':'Mise à jour','Résultat':'θ_a,i+1 = θ_a,i + Δθ_a,i'}, {'Étape':'6','Opération':'Itération','Résultat':'Répétition jusqu’à 30 min puis 120 min'}])
 img(d,integration_figure,'Figure A.1 - Intégration temporelle du cas critique jusqu’à 30 min.')
 d.add_heading('A.2 Calcul du dernier pas avant 30 min',2)
 eq(d,[q('conv'),rr(' = '),sub('α','c'),rr('('),th('g'),rr(' - '),th('a'),rr(') = '+f(case['qc'],1)+' W/m²')]);eq(d,[q('rad'),rr(' = Φ '),sub('ε','m'),rr(' '),sub('ε','f'),rr(' σ ['),sup('(θg + 273,15)','4'),rr(' - '),sup('(θa + 273,15)','4'),rr('] = '+f(case['qr'],1)+' W/m²')]);eq(d,[q('net'),rr(' = '),q('conv'),rr(' + '),q('rad'),rr(' = '+f(case['qn'],1)+' W/m²')])
 d.add_heading('A.3 Incrément de température',2);eq(d,[rr('Δ'),th('a,t'),rr(' = '),frac([sub('k','sh'),rr(' '),frac([sub('A','m')],[rr('V')]),rr(' '),q('net'),rr(' Δt')],[sub('ρ','a'),rr(' '),sub('c','a'),rr('('),th('a'),rr(')')]),rr(' = '+f(case['dta'],4)+' °C')]);d.add_paragraph(f"La température passe de {f(case['ta0'],2)} °C à {f(case['ta1'],2)} °C pendant le dernier pas de 5 s. La température à 30 min résulte de l'intégration de tous les pas depuis t = 0.")
 d.add_page_break();d.add_heading('Annexe B - Courbes de tous les cas étudiés',1);d.add_paragraph("Les figures suivantes couvrent 2 courbes de feu × 3 positions × 3 longueurs de foyer × 2 familles d'éléments.")
 for cap,p in appendix:img(d,p,cap)
 p=Path(path);p.parent.mkdir(parents=True,exist_ok=True);d.save(p);return p
