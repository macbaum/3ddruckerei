#!/usr/bin/env python3
"""Erzeugt zeichnung.svg fuer den Klickring (Masse aus generate.py)."""
import math
import generate as G

OD, H, W = G.AUSSEN_D, G.HOEHE, G.C_WINKEL
out = []
A = out.append
A('<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="850" viewBox="0 0 1200 850" font-family="Arial, sans-serif">')
A('<defs><marker id="a" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,1 L10,5 L0,9 z" fill="#c00"/></marker>'
  '<pattern id="h" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="6" stroke="#333" stroke-width="1"/></pattern></defs>')
A('<rect width="1200" height="850" fill="white"/><rect x="10" y="10" width="1180" height="830" fill="none" stroke="#000" stroke-width="2"/>')


def dim(x1, y1, x2, y2, txt, tx, ty, size=16):
    A(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#c00" stroke-width="1.3" marker-start="url(#a)" marker-end="url(#a)"/>')
    A(f'<text x="{tx:.1f}" y="{ty:.1f}" fill="#c00" font-size="{size}" text-anchor="middle">{txt}</text>')


# ---------- Draufsicht C-Ring (5:1)
S = 5.0
cx, cy = 230, 300
rb, ro = (G.ROHR_D + G.SPIEL) / 2 * S, OD / 2 * S
rn = (G.NUT_D + G.SPIEL) / 2 * S
def arcpath(r1, r2, a0, a1):
    p = lambda r, a: (cx + r * math.cos(math.radians(a)), cy - r * math.sin(math.radians(a)))
    lg = 1 if (a1 - a0) > 180 else 0
    (x1, y1), (x2, y2), (x3, y3), (x4, y4) = p(r2, a0), p(r2, a1), p(r1, a1), p(r1, a0)
    return (f'M{x1:.1f},{y1:.1f} A{r2},{r2} 0 {lg} 0 {x2:.1f},{y2:.1f} L{x3:.1f},{y3:.1f} '
            f'A{r1},{r1} 0 {lg} 1 {x4:.1f},{y4:.1f} Z')
A(f'<text x="{cx}" y="60" font-size="20" font-weight="bold" text-anchor="middle">Draufsicht C-Ring (5:1)</text>')
A(f'<path d="{arcpath(rb, ro, -W/2, W/2)}" fill="#dfe8f7" stroke="#000" stroke-width="2"/>')
A(f'<path d="{arcpath(rn, rb, -W/2, W/2)}" fill="none" stroke="#000" stroke-width="1" stroke-dasharray="5 4"/>')
A(f'<line x1="{cx-ro-25}" y1="{cy}" x2="{cx+ro+25}" y2="{cy}" stroke="#555" stroke-dasharray="12 4 2 4"/>'
  f'<line x1="{cx}" y1="{cy-ro-25}" x2="{cx}" y2="{cy+ro+25}" stroke="#555" stroke-dasharray="12 4 2 4"/>')
dim(cx - ro, cy + ro + 40, cx + ro, cy + ro + 40, f"Ø {OD:g}", cx, cy + ro + 65)
gap = 2 * (rn / S) * math.sin(math.radians((360 - W) / 2))
A(f'<text x="{cx}" y="{cy+ro+95}" font-size="15" text-anchor="middle">Umschlingung {W:g}° · Öffnung an der Rippe ≈ {gap:.1f} mm</text>')
A(f'<text x="{cx}" y="{cy+ro+117}" font-size="15" text-anchor="middle">gestrichelt = Innenrippe</text>')

# ---------- Schnitt mit Rohr (25:1)
S2 = 25.0
sx, sy = 640, 545  # sx = Rohrachse liegt links ausserhalb; Bezug r = ROHR_D/2 bei x = sx
r0 = G.ROHR_D / 2
X = lambda r: sx + (r - r0) * S2 + 80
Y = lambda z: sy - z * S2
A(f'<text x="850" y="60" font-size="20" font-weight="bold" text-anchor="middle">Schnitt A–A durch Ring und Rohr (25:1)</text>')
# Rohr mit Nut (grau, gestrichelt)
rN = G.NUT_D / 2
z0 = max(G.NUT_ABST, (G.ROHR_D - G.NUT_D) / 2 + 0.1)
z1 = z0 + G.NUT_B
tube = [(X(r0 - 3), Y(-1.5)), (X(r0), Y(-1.5)), (X(r0), Y(z0)), (X(rN), Y(z0)), (X(rN), Y(z1)),
        (X(r0), Y(z1)), (X(r0), Y(H + 3)), (X(r0 - 3), Y(H + 3))]
A('<polygon points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in tube) + '" fill="#eee" stroke="#777" stroke-width="1.5" stroke-dasharray="6 3"/>')
A(f'<text x="{X(r0-1.5):.1f}" y="{Y(H+1):.1f}" font-size="14" fill="#666" text-anchor="middle" transform="rotate(-90 {X(r0-1.5):.1f} {Y(H+1):.1f})">Rohr Ø {G.ROHR_D:g}</text>')
# Ringprofil
pts = [(X(r), Y(z)) for r, z in G.profil()]
A('<polygon points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in pts) + '" fill="url(#h)" stroke="#000" stroke-width="2"/>')
# Masse
xr = X(OD / 2)
dim(xr + 30, Y(0), xr + 30, Y(H), f"{H:g}", xr + 55, Y(H / 2) + 6)
dim(xr + 90, Y(z0), xr + 90, Y(z1), f"Nut {G.NUT_B:g}", xr + 130, Y((z0 + z1) / 2) + 6, 15)
A(f'<line x1="{X(rN):.1f}" y1="{Y(z1):.1f}" x2="{xr+100:.1f}" y2="{Y(z1):.1f}" stroke="#c00" stroke-width="0.7"/>'
  f'<line x1="{X(rN):.1f}" y1="{Y(z0):.1f}" x2="{xr+100:.1f}" y2="{Y(z0):.1f}" stroke="#c00" stroke-width="0.7"/>')
dim(xr + 150, Y(0), xr + 150, Y(z0), f"{z0:g}", xr + 172, Y(z0 / 2) + 6, 15)
dim(X(r0), Y(H + 1.2), X(OD / 2), Y(H + 1.2), f"Wand {(OD-G.ROHR_D)/2:g}", (X(r0) + xr) / 2, Y(H + 1.2) - 10, 15)
A(f'<text x="{X(r0-3)-10:.1f}" y="{Y((z0+z1)/2)+5:.1f}" font-size="15" fill="#c00" text-anchor="end">Rippe Ø {G.NUT_D:g}</text>')
A(f'<text x="{X(r0-3)-10:.1f}" y="{Y(H*0.85):.1f}" font-size="15" fill="#c00" text-anchor="end">Bohrung Ø {G.ROHR_D:g}</text>')

# ---------- Tabelle
ty = 640
A(f'<line x1="10" y1="{ty-45}" x2="1190" y2="{ty-45}" stroke="#000"/>')
rows = [("Teil", "Klickring für Geberit Heberglocke (Spülventil AV02, Glocke 5200.017) – rastet in die Nut am Rohr Ø 30"),
        ("Maße", f"Bohrung Ø {G.ROHR_D:g} · Rippe Ø {G.NUT_D:g} · Ø außen {OD:g} · Höhe {H:g} · Spiel +{G.SPIEL:g} · Maße in mm"),
        ("WICHTIG", "Nur Ø 30 gemessen. Nut-Ø, Nutbreite, Nutabstand, Ø außen und Höhe sind geschätzt – siehe Messskizze."),
        ("Material", "PETG (wasserfest, zäh) – alternativ PLA."),
        ("Druck", "flach liegend, 0,12 mm Schicht, 4 Wände, 100 % Füllung, keine Stützen (Rippe hat 45°-Schrägen).")]
for i, (k, v) in enumerate(rows):
    A(f'<text x="35" y="{ty+i*36}" font-size="17" font-weight="bold">{k}</text><text x="170" y="{ty+i*36}" font-size="17">{v}</text>')
A('<text x="1175" y="825" font-size="13" text-anchor="end" fill="#666">clip_C.stl · halbschalen_2stk.stl · clip.scad</text>')
A('</svg>')
open("zeichnung.svg", "w").write("\n".join(out))
print("zeichnung.svg geschrieben")
