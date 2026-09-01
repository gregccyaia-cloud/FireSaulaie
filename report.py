from pathlib import Path
from datetime import datetime
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.shared import Cm,Pt,Mm

def run(text): o=OxmlElement('m:r');t=OxmlElement('m:t');t.text=text;o.append(t);return o
def script(tag,base_elements,script_elements):
    o=OxmlElement('m:'+tag);e=OxmlElement('m:e');s=OxmlElement('m:sub' if tag=='sSub' else 'm:sup')
    for x in base_elements:e.append(x)
    for x in script_elements:s.append(x)
    o.extend([e,s]);return o
def sub_text(base,sub):return script('sSub',[run(base)],[run(sub)])
def sup_text(base,sup):return script('sSup',[run(base)],[run(sup)])
def frac(num,den):
    o=OxmlElement('m:f');n=OxmlElement('m:num');d=OxmlElement('m:den')
    for x in num:n.append(x)
    for x in den:d.append(x)
    o.extend([n,d]);return o
def eq(doc,els):
    p=doc.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER;mp=OxmlElement('m:oMathPara');m=OxmlElement('m:oMath')
    for x in els:m.append(x)
    mp.append(m);p._p.append(mp)
def q(s):return sub_text('q',s)
def th(s):return sub_text('θ',s)
def image(doc,path,caption,w=16):
    path=Path(path)
    if not path.exists():return 0
    doc.add_picture(str(path),width=Cm(w));doc.paragraphs[-1].alignment=WD_ALIGN_PARAGRAPH.CENTER
    p=doc.add_paragraph(caption);p.alignment=WD_ALIGN_PARAGRAPH.CENTER;p.runs[0].italic=True;return 1
def table(doc,rows):
    if not rows:return
    hs=list(rows[0]);t=doc.add_table(rows=1,cols=len(hs));t.style='Table Grid'
    for i,h in enumerate(hs):t.rows[0].cells[i].text=h;t.rows[0].cells[i].paragraphs[0].runs[0].bold=True
    for row in rows:
        c=t.add_row().cells
        for i,h in enumerate(hs):c[i].text=str(row[h])
def f(v,n=2):return f'{v:.{n}f}'.replace('.',',')
def equations(doc):
    doc.add_heading('Équations utilisées',2)
    doc.add_paragraph('Courbe CN - ISO 834, NF EN 1991-1-2, § 3.2.1 :');eq(doc,[th('g'),run('(t) = 20 + 345 '),sub_text('log','10'),run('(8t + 1)')])
    doc.add_paragraph('Courbe de feu extérieur, NF EN 1991-1-2, § 3.2.2 :');eq(doc,[th('g'),run('(t) = 660[1 - 0,687 '),sup_text('e','-0,32t'),run(' - 0,313 '),sup_text('e','-3,8t'),run('] + 20')])
    doc.add_paragraph('Flux convectif net, NF EN 1991-1-2, § 3.1 :');eq(doc,[q('conv'),run(' = '),sub_text('α','c'),run('('),th('g'),run(' - '),th('a'),run(')')])
    doc.add_paragraph('Flux radiatif net, NF EN 1991-1-2, § 3.1 :');eq(doc,[q('rad'),run(' = Φ '),sub_text('ε','m'),run(' '),sub_text('ε','f'),run(' σ ['),sup_text('(θg + 273,15)','4'),run(' - '),sup_text('(θa + 273,15)','4'),run(']')])
    doc.add_paragraph('Flux thermique net :');eq(doc,[q('net'),run(' = '),q('conv'),run(' + '),q('rad')])
    doc.add_paragraph('Facteur de section :');eq(doc,[frac([sub_text('A','m')],[run('V')]),run(' = '),sub_text('η','exp'),run(' '),frac([run('4')],[run('D')])])
    doc.add_paragraph("Incrément de température, NF EN 1993-1-2, § 4.2.5.1 :");eq(doc,[run('Δ'),th('a,t'),run(' = '),frac([sub_text('k','sh'),run(' '),frac([sub_text('A','m')],[run('V')]),run(' '),q('net'),run(' Δt')],[sub_text('ρ','a'),run(' '),sub_text('c','a'),run('('),th('a'),run(')')])])
def build(path,figures,summary,case,assets,sections,parameters,appendix_figures):
    d=Document();s=d.sections[0];s.top_margin=s.bottom_margin=Mm(18);s.left_margin=s.right_margin=Mm(20);d.styles['Normal'].font.name='Aptos';d.styles['Normal'].font.size=Pt(10.5)
    p=d.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER;p.paragraph_format.space_before=Pt(55);x=p.add_run("ANALYSE THERMIQUE D'UN INCENDIE\nSOUS LA PASSERELLE");x.bold=True;x.font.size=Pt(23)
    p=d.add_paragraph('Passerelle Gerland - La Saulaie\nVersion V1.4 - Révision A');p.alignment=WD_ALIGN_PARAGRAPH.CENTER
    p=d.add_paragraph('Rapport généré le '+datetime.now().strftime('%d/%m/%Y à %H:%M'));p.alignment=WD_ALIGN_PARAGRAPH.CENTER;d.add_page_break()
    d.add_heading("1. Objet et présentation du projet",1);d.add_paragraph("L'étude évalue l'évolution de la température de l'intrados, des suspentes et des câbles principaux lors d'un incendie sur la M7. Les courbes ISO 834 et feu extérieur sont calculées séparément, puis comparées.")
    ins=0;ins+=image(d,assets/'ZZ extrait vue en plan generale.png','Figure 1 - Vue en plan générale.');ins+=image(d,assets/'ZZ extrait plan suspension.png','Figure 2 - Élévation et plan du système de suspension.');ins+=image(d,assets/'Zz extrait coupe long generale.png','Figure 3 - Coupe longitudinale générale.');ins+=image(d,assets/'ZZ coupe transv.png','Figure 4 - Coupe transversale type du tablier.')
    d.add_heading('2. Références',1)
    for z in ['NF EN 1991-1-2, § 3.1, § 3.2.1 et § 3.2.2.','NF EN 1993-1-2, § 3.4.1 et § 4.2.5.1.',"Cerema, Résistance à l'incendie des ponts routiers, guide 2018.",'Note SAU_AVP_NTE_069_A_FeuM7.']:d.add_paragraph(z,style='List Bullet')
    d.add_heading('3. Géométrie simplifiée et positions de feu',1);d.add_paragraph("Trois coupes successives sont étudiées le long de l'axe de la passerelle au franchissement de la M7 : bord ouest, axe M7 et bord est.")
    rows=[{'Coupe':s.code,'Position':s.label,'Intrados (m)':f(s.intrados_m,3),'Naissance suspente (m)':f(s.intrados_m+.82,3),'Axe câble (m)':f(s.cable_m,3)} for s in sections];table(d,rows)
    ins+=image(d,assets/'ZZ_coupe longit partielle zone M7.png','Figure 5 - Hauteurs sur les trois coupes.');ins+=image(d,assets/'ZZ_vue en plan cotée zone M7.png','Figure 6 - Largeurs de la M7.');ins+=image(d,assets/'ZZ_demie coupe tablier et approx intrados.png',"Figure 7 - Demi-coupe et approximation de l'intrados par 2 segments de droite")
    d.add_paragraph("Les positions de feu sont introduites comme suit : F1 correspond à la position ouest, F2 à la position centrale et F3 à la position est. Chaque position est associée à la coupe géométrique de référence la plus proche pour les contrôles de distance tridimensionnelle. Ces repères sont ensuite repris dans les tableaux et figures de résultats.")
    d.add_heading('4. Choix des paramètres et hypothèses',1)
    d.add_paragraph("Le véhicule est représenté par un poids lourd de 16,0 m de longueur, 2,50 m de largeur et 4,00 m de hauteur. Le véhicule est supposé immobilisé sous la passerelle pendant toute la durée du feu. Trois longueurs de foyer sont paramétrées, soit 10 m, 15 m et 20 m, afin de préparer l'analyse de sensibilité. Dans la présente version, le facteur de configuration radiatif Φ est uniforme et égal à 1,0 ; les trois longueurs de foyer ne modifient donc pas encore le flux thermique. Elles sont néanmoins conservées dans les scénarios et dans l'annexe B. La durée maximale de calcul est de 120 min, avec des lectures à 15, 30, 60, 90 et 120 min. La phase de refroidissement est ignorée.")
    table(d,[{'Paramètre':k,'Valeur retenue':v} for k,v in parameters])
    equations(d)
    d.add_heading('5. Résultats de synthèse',1);table(d,summary)
    for title,pth in figures:ins+=image(d,pth,title)
    d.add_paragraph("Pour les graphiques d'échauffement, certaines courbes se superposent exactement. Cette superposition résulte des hypothèses de la V1.4 : Φ = 1,0, exposition uniforme et absence d'atténuation liée à la position ou à la longueur du foyer. Les légendes recensent néanmoins l'ensemble des cas calculés.")
    d.add_heading('6. Limites',1);d.add_paragraph("Le facteur de configuration Φ vaut 1,0. Les longueurs de foyer sont paramétrées, mais elles ne modifient pas encore le flux tant qu'un facteur de forme géométrique n'est pas introduit.")
    d.add_page_break();d.add_heading('Annexe A - Calcul détaillé du cas critique à 30 min',1)
    d.add_paragraph(f"Cas retenu : {case['fire']} - {case['position']} - coupe {case['section']} - {case['element']} - foyer {f(case['fire_length'],1)} m.")
    table(d,[{'Grandeur':k,'Valeur':v} for k,v in case['values']])
    d.add_heading('A.1 Calcul des flux',2);eq(d,[q('conv'),run(' = '),sub_text('α','c'),run('('),th('g'),run(' - '),th('a'),run(') = '+f(case['qc'],1)+' W/m²')]);eq(d,[q('rad'),run(' = Φ '),sub_text('ε','m'),run(' '),sub_text('ε','f'),run(' σ ['),sup_text('(θg + 273,15)','4'),run(' - '),sup_text('(θa + 273,15)','4'),run('] = '+f(case['qr'],1)+' W/m²')]);eq(d,[q('net'),run(' = '),q('conv'),run(' + '),q('rad'),run(' = '+f(case['qn'],1)+' W/m²')])
    d.add_heading('A.2 Incrément de température',2);eq(d,[run('Δ'),th('a,t'),run(' = '),frac([sub_text('k','sh'),run(' '),frac([sub_text('A','m')],[run('V')]),run(' '),q('net'),run(' Δt')],[sub_text('ρ','a'),run(' '),sub_text('c','a'),run('('),th('a'),run(')')]),run(' = '+f(case['dta'],4)+' °C')]);d.add_paragraph(f"La température passe de {f(case['ta0'],2)} °C à {f(case['ta1'],2)} °C pendant le dernier pas de 5 s. La température à 30 min résulte de l'intégration de tous les pas depuis t = 0.")
    d.add_page_break();d.add_heading('Annexe B - Courbes de tous les cas étudiés',1);d.add_paragraph("Les figures suivantes présentent les 36 combinaisons calculées : 2 courbes de feu × 3 positions de foyer × 3 longueurs de foyer × 2 familles d'éléments. Chaque figure regroupe les neuf cas de position et de longueur pour une courbe de feu et une famille d'éléments.")
    for title,pth in appendix_figures:ins+=image(d,pth,title)
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True);d.save(path);return {'path':path.resolve(),'figures':ins}
