from docx import Document
from docx.shared import Cm,Pt,RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT,WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

def shade(c,color):
 p=c._tc.get_or_add_tcPr();s=OxmlElement('w:shd');s.set(qn('w:fill'),color);p.append(s)
def add_table(d,headers,rows):
 t=d.add_table(rows=1,cols=len(headers));t.style='Table Grid';t.alignment=WD_TABLE_ALIGNMENT.CENTER
 for i,h in enumerate(headers):
  c=t.rows[0].cells[i];c.text=str(h);shade(c,'1F4E78')
  for r in c.paragraphs[0].runs:r.font.bold=True;r.font.color.rgb=RGBColor(255,255,255)
 for row in rows:
  cells=t.add_row().cells
  for i,v in enumerate(row):cells[i].text=str(v);cells[i].vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
 return t
def fig(d,p,caption,w=15.5):
 if p.exists():
  q=d.add_paragraph();q.alignment=WD_ALIGN_PARAGRAPH.CENTER;q.add_run().add_picture(str(p),width=Cm(w));c=d.add_paragraph(caption);c.alignment=WD_ALIGN_PARAGRAPH.CENTER;c.style='Caption'
def build_report(ctx,path):
 path.parent.mkdir(parents=True,exist_ok=True);d=Document();sec=d.sections[0];sec.top_margin=Cm(1.7);sec.bottom_margin=Cm(1.7);sec.left_margin=Cm(2);sec.right_margin=Cm(2)
 d.styles['Normal'].font.name='Arial';d.styles['Normal'].font.size=Pt(9.5)
 for n in ('Title','Heading 1','Heading 2','Heading 3'):d.styles[n].font.name='Arial';d.styles[n].font.color.rgb=RGBColor(31,78,120)
 p=d.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER;r=p.add_run('ANALYSE THERMIQUE D’UN INCENDIE SOUS LA PASSERELLE');r.bold=True;r.font.size=Pt(18);r.font.color.rgb=RGBColor(31,78,120)
 p=d.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER;p.add_run('Passerelle Gerland - La Saulaie | Modèle Python V1.3 consolidé').bold=True
 d.add_paragraph('Document de travail pour validation du modèle thermique. Les coefficients d’exposition spatiale et le facteur de massiveté de l’intrados restent provisoires.')
 d.add_page_break()
 d.add_heading('1. Objet et limites',1);d.add_paragraph('Le calcul évalue l’évolution de la température de l’intrados métallique, des suspentes secondaires et du câble principal. Deux courbes de feu sont calculées séparément, puis comparées. Les résultats ne constituent pas encore une vérification structurelle.')
 d.add_heading('2. Données du projet',1);add_table(d,['Paramètre','Valeur'],ctx['project'])
 d.add_heading('3. Scénarios de feu',1);d.add_paragraph('Les deux lois sont évaluées de 0 à 120 minutes. La variable t est exprimée en minutes et la température en degrés Celsius.');fig(d,ctx['eq_png'],'Figure 1 - Formules des courbes de feu.');fig(d,ctx['fire_png'],'Figure 2 - Comparaison des températures nominales des gaz.')
 d.add_heading('4. Principes du calcul thermique',1);d.add_paragraph('Le modèle capacitif suppose une température uniforme dans chaque section. À chaque pas de 5 s, le bilan énergétique combine convection et rayonnement :')
 for e in ['q_conv = f_conv × α_c × (θ_g - θ_a)','q_rad = f_rad × ε_m × ε_f × σ × [(θ_g + 273,15)^4 - (θ_a + 273,15)^4]','Δθ_a = (A_m/V) × (q_conv + q_rad) × Δt / [ρ_a × c_a(θ_a)]']:
  p=d.add_paragraph();p.alignment=WD_ALIGN_PARAGRAPH.CENTER;p.add_run(e).bold=True
 add_table(d,['Grandeur','Valeur'],ctx['thermal'])
 d.add_heading('5. Séquence de calcul',1);add_table(d,['Étape','Calcul','Contrôle'],ctx['steps'])
 d.add_heading('6. Synthèse des 18 cas',1);add_table(d,list(ctx['summary'].columns),ctx['summary'].values.tolist())
 d.add_heading('7. Cas le plus défavorable à 30 minutes',1)
 w=ctx['worst'];d.add_paragraph(f"Le cas retenu est {w['case']} pour l’élément {w['element']}. À 30 min, la température calculée est {w['T_end']:.2f} °C.")
 add_table(d,['Donnée','Valeur'],[["Courbe de feu",w['fire']],["Position du camion",w['position']],["Hauteur de flamme",f"{w['hf']:.2f} m"],["Élément",w['element']],["A_m/V",f"{w['amv']:.3f} m⁻¹"],["f_rad",f"{w['fr']:.3f}"],["f_conv",f"{w['fc']:.3f}"],["Pas",f"{w['dt']:.1f} s"],["T_g à 29 min 55 s",f"{w['Tg_start']:.3f} °C"],["T_acier à 29 min 55 s",f"{w['T_start']:.3f} °C"],["c_a",f"{w['cp']:.3f} J/(kg·K)"],["q_conv",f"{w['qc']:.3f} W/m²"],["q_rad",f"{w['qr']:.3f} W/m²"],["q_net",f"{w['qc']+w['qr']:.3f} W/m²"],["ΔT du dernier pas",f"{w['dT']:.6f} °C"],["T_acier à 30 min",f"{w['T_end']:.3f} °C"]])
 d.add_paragraph('Vérification numérique du dernier incrément :')
 d.add_paragraph(f"ΔT = {w['amv']:.3f} × ({w['qc']:.3f} + {w['qr']:.3f}) × {w['dt']:.1f} / (7850 × {w['cp']:.3f}) = {w['dT']:.6f} °C")
 fig(d,w['png'],f"Figure 3 - Évolution thermique du cas {w['case']}.")
 d.add_heading('8. Conclusions de validation',1)
 for x in ctx['conclusions']:d.add_paragraph(x,style='List Bullet')
 d.save(str(path));return path
