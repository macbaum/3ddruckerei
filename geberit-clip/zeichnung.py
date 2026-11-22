#!/usr/bin/env python3
"""Erzeugt zeichnung.svg (technische Zeichnung, Masse aus generate.py)."""
import math, re
src = open("generate.py").read()
g = lambda k: float(re.search(rf"^{k}\s*=\s*([\d.]+)", src, re.M).group(1))
ID, OD, H, W = g("INNEN_D"), g("AUSSEN_D"), g("HOEHE"), g("C_WINKEL")
S = 5.0  # Massstab 5:1  (px pro mm)
ri, ro = ID/2*S, OD/2*S
out = []
A = out.append
A('<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="850" viewBox="0 0 1200 850" font-family="Arial, sans-serif">')
A('<defs><marker id="a" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,1 L10,5 L0,9 z" fill="#c00"/></marker>'
  '<pattern id="h" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="6" stroke="#333" stroke-width="1"/></pattern></defs>')
A('<rect width="1200" height="850" fill="white"/><rect x="10" y="10" width="1180" height="830" fill="none" stroke="#000" stroke-width="2"/>')
def dim(x1,y1,x2,y2,txt,tx,ty,rot=0):
    A(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#c00" stroke-width="1.3" marker-start="url(#a)" marker-end="url(#a)"/>')
    A(f'<text x="{tx}" y="{ty}" fill="#c00" font-size="17" text-anchor="middle" transform="rotate({rot} {tx} {ty})">{txt}</text>')
def arc(cx,cy,r1,r2,a0,a1):
    # Ringsegment-Pfad (Grad, 0 = rechts, math. positiv nach oben)
    p=lambda r,a:(cx+r*math.cos(math.radians(a)), cy-r*math.sin(math.radians(a)))
    large = 1 if (a1-a0)>180 else 0
    (x1,y1),(x2,y2),(x3,y3),(x4,y4)=p(r2,a0),p(r2,a1),p(r1,a1),p(r1,a0)
    return (f'M{x1:.1f},{y1:.1f} A{r2},{r2} 0 {large} 0 {x2:.1f},{y2:.1f} L{x3:.1f},{y3:.1f} '
            f'A{r1},{r1} 0 {large} 1 {x4:.1f},{y4:.1f} Z')
# --- Ansicht 1: C-Clip Draufsicht
cx, cy = 230, 330
A(f'<text x="{cx}" y="70" font-size="20" font-weight="bold" text-anchor="middle">Variante A: C-Clip (Draufsicht)</text>')
A(f'<path d="{arc(cx,cy,ri,ro,180-W/2+180-180, 180+W/2-180+180)}" fill="#dfe8f7" stroke="#000" stroke-width="2"/>'.replace(
  arc(cx,cy,ri,ro,180-W/2+180-180, 180+W/2-180+180), arc(cx,cy,ri,ro,-W/2+180-180+0, W/2)))
A(f'<line x1="{cx-ro-25}" y1="{cy}" x2="{cx+ro+25}" y2="{cy}" stroke="#555" stroke-dasharray="12 4 2 4"/>'
  f'<line x1="{cx}" y1="{cy-ro-25}" x2="{cx}" y2="{cy+ro+25}" stroke="#555" stroke-dasharray="12 4 2 4"/>')
dim(cx-ro, cy+ro+45, cx+ro, cy+ro+45, f"Ø {OD:g} (außen)", cx, cy+ro+70)
dim(cx-ri*0.7071, cy-ri*0.7071, cx+ri*0.7071, cy+ri*0.7071, f"Ø {ID:g} (innen)", cx+5, cy-12, 0)
gap = 2*ri*math.sin(math.radians((360-W)/2))/S
A(f'<text x="{cx-ro-10}" y="{cy-ro-10}" font-size="15" text-anchor="middle">Öffnung ≈ {gap:.1f} mm</text>')
A(f'<text x="{cx}" y="{cy+ro+100}" font-size="15" text-anchor="middle">Umschlingung {W:g}° – schnappt seitlich auf das Rohr</text>')
# --- Ansicht 2: Halbschalen
cx2 = 640
A(f'<text x="{cx2}" y="70" font-size="20" font-weight="bold" text-anchor="middle">Variante B: 2 Halbschalen</text>')
A(f'<path d="{arc(cx2-8,cy,ri,ro,90.5,269.5)}" fill="#dfe8f7" stroke="#000" stroke-width="2"/>')
A(f'<path d="{arc(cx2+8,cy,ri,ro,-89.5,89.5)}" fill="#dfe8f7" stroke="#000" stroke-width="2"/>')
dim(cx2-ro-8, cy+ro+45, cx2+ro+8, cy+ro+45, f"Ø {OD:g}", cx2, cy+ro+70)
A(f'<text x="{cx2}" y="{cy+ro+100}" font-size="15" text-anchor="middle">je 180° – von beiden Seiten einlegen</text>')
# --- Ansicht 3: Schnitt
sx, sy = 1010, 250
A(f'<text x="{sx}" y="70" font-size="20" font-weight="bold" text-anchor="middle">Schnitt A–A (Profil)</text>')
w, h, c = (ro-ri), H*S, 0.6*S
for side in (-1,1):
    x0 = sx + side*(ri) if side>0 else sx - ro
    pts=[(x0+c,sy),(x0+w-c,sy),(x0+w,sy+c),(x0+w,sy+h-c),(x0+w-c,sy+h),(x0+c,sy+h),(x0,sy+h-c),(x0,sy+c)]
    A('<polygon points="'+" ".join(f"{x:.1f},{y:.1f}" for x,y in pts)+'" fill="url(#h)" stroke="#000" stroke-width="2"/>')
A(f'<line x1="{sx}" y1="{sy-30}" x2="{sx}" y2="{sy+h+30}" stroke="#555" stroke-dasharray="12 4 2 4"/>')
dim(sx+ro+20, sy, sx+ro+20, sy+h, f"{H:g}", sx+ro+45, sy+h/2+6)
dim(sx+ri, sy+h+30, sx+ro, sy+h+30, f"{(OD-ID)/2:g}", sx+(ri+ro)/2, sy+h+55)
A(f'<text x="{sx}" y="{sy+h+90}" font-size="15" text-anchor="middle">Kantenfase 0,6 × 45°</text>')
# --- Tabelle / Hinweise
ty = 640
A(f'<line x1="10" y1="{ty-45}" x2="1190" y2="{ty-45}" stroke="#000"/>')
rows = [("Teil","Distanz-/Höhenclip für Geberit Heberglocke (Spülventil AV02, Glocke 5200.017)"),
        ("Maße","Ø innen "+f"{ID:g}"+" mm (+0,2 Spiel) · Ø außen "+f"{OD:g}"+" mm · Höhe "+f"{H:g}"+" mm · Maßstab 5:1, Maße in mm"),
        ("WICHTIG","Ø innen 30 mm gemessen. Ø außen und Höhe geschätzt – Höhe des Spalts nachmessen, ggf. in clip.scad anpassen."),
        ("Material","PETG (wasserfest, zäh) – alternativ PLA; ASA/ABS geht auf dem A1 mini nur eingeschränkt (kein Gehäuse)."),
        ("Druck","flach liegend, 0,12–0,16 mm Schicht, 4 Wände, 100 % Füllung, keine Stützen.")]
for i,(k,v) in enumerate(rows):
    A(f'<text x="35" y="{ty+i*36}" font-size="17" font-weight="bold">{k}</text><text x="170" y="{ty+i*36}" font-size="17">{v}</text>')
A('<text x="1175" y="825" font-size="13" text-anchor="end" fill="#666">clip_C.stl · halbschalen_2stk.stl · clip.scad</text>')
A('</svg>')
open("zeichnung.svg","w").write("\n".join(out)); print("zeichnung.svg geschrieben")
