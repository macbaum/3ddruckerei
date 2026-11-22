#!/usr/bin/env python3
"""Erzeugt zeichnung.svg fuer den Klickring mit Innennut (Masse aus generate.py)."""
import generate as G

OD, H = G.AUSSEN_D, G.HOEHE
rb_mm, rg_mm, d_mm, z0, z1 = G.nutmasse()
out = []
A = out.append
A('<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="850" viewBox="0 0 1200 850" font-family="Arial, sans-serif">')
A('<defs><marker id="a" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,1 L10,5 L0,9 z" fill="#c00"/></marker>'
  '<pattern id="h" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="6" stroke="#333" stroke-width="1"/></pattern></defs>')
A('<rect width="1200" height="850" fill="white"/><rect x="10" y="10" width="1180" height="830" fill="none" stroke="#000" stroke-width="2"/>')


def dim(x1, y1, x2, y2, txt, tx, ty, size=16, anchor="middle"):
    A(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#c00" stroke-width="1.3" marker-start="url(#a)" marker-end="url(#a)"/>')
    A(f'<text x="{tx:.1f}" y="{ty:.1f}" fill="#c00" font-size="{size}" text-anchor="{anchor}">{txt}</text>')


def line(x1, y1, x2, y2, w=0.7):
    A(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#c00" stroke-width="{w}"/>')


# ---------- Draufsicht (5:1)
S = 5.0
cx, cy = 230, 300
ro, rb, rg = OD / 2 * S, rb_mm * S, rg_mm * S
A(f'<text x="{cx}" y="60" font-size="20" font-weight="bold" text-anchor="middle">Draufsicht Ring (5:1)</text>')
A(f'<path d="M{cx-ro},{cy} a{ro},{ro} 0 1,0 {2*ro},0 a{ro},{ro} 0 1,0 {-2*ro},0 Z '
  f'M{cx-rb},{cy} a{rb},{rb} 0 1,1 {2*rb},0 a{rb},{rb} 0 1,1 {-2*rb},0 Z" fill="#dfe8f7" fill-rule="evenodd" stroke="#000" stroke-width="2"/>')
A(f'<circle cx="{cx}" cy="{cy}" r="{rg}" fill="none" stroke="#000" stroke-width="1" stroke-dasharray="5 4"/>')
A(f'<line x1="{cx-ro-25}" y1="{cy}" x2="{cx+ro+25}" y2="{cy}" stroke="#555" stroke-dasharray="12 4 2 4"/>'
  f'<line x1="{cx}" y1="{cy-ro-25}" x2="{cx}" y2="{cy+ro+25}" stroke="#555" stroke-dasharray="12 4 2 4"/>')
dim(cx - ro, cy + ro + 40, cx + ro, cy + ro + 40, f"Ø {OD:g}", cx, cy + ro + 65)
A(f'<text x="{cx}" y="{cy+ro+95}" font-size="15" text-anchor="middle">geschlossener Ring · gestrichelt = Innennut</text>')
A(f'<text x="{cx}" y="{cy+ro+117}" font-size="15" text-anchor="middle">(Varianten C-Ring / Halbschalen in clip.scad)</text>')

# ---------- Schnitt mit Rohr und Wulst (25:1)
S2 = 25.0
rs = G.SITZ_D / 2
rw = G.WULST_D / 2
X = lambda r: 720 + (r - rs) * S2
Y = lambda z: 545 - z * S2
A('<text x="850" y="60" font-size="20" font-weight="bold" text-anchor="middle">Schnitt A–A durch Ring und Rohr (25:1)</text>')
# Rohr mit Wulst (grau, gestrichelt)
wz0, wz1 = z0 + G.SPIEL / 2, z0 + G.SPIEL / 2 + G.WULST_B
tube = [(X(rs - 2.5), Y(-1.5)), (X(rs), Y(-1.5)), (X(rs), Y(wz0)), (X(rw), Y(wz0)), (X(rw), Y(wz1)),
        (X(rs), Y(wz1)), (X(rs), Y(H + 3)), (X(rs - 2.5), Y(H + 3))]
A('<polygon points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in tube) + '" fill="#eee" stroke="#777" stroke-width="1.5" stroke-dasharray="6 3"/>')
A(f'<text x="{X(rs-1.25):.1f}" y="{Y(H+1.2):.1f}" font-size="14" fill="#666" text-anchor="middle" transform="rotate(-90 {X(rs-1.25):.1f} {Y(H+1.2):.1f})">Rohr</text>')
# Ringprofil
pts = [(X(r), Y(z)) for r, z in G.profil()]
A('<polygon points="' + " ".join(f"{x:.1f},{y:.1f}" for x, y in pts) + '" fill="url(#h)" stroke="#000" stroke-width="2"/>')
xr = X(OD / 2)
# Masse rechts
dim(xr + 30, Y(0), xr + 30, Y(H), f"{H:g}", xr + 50, Y(H / 2) + 6, anchor="start")
line(X(rg_mm), Y(z0), xr + 100, Y(z0)); line(X(rg_mm), Y(z1), xr + 100, Y(z1))
dim(xr + 90, Y(z0), xr + 90, Y(z1), f"Nut {z1 - z0:.1f}", xr + 100, Y((z0 + z1) / 2) + 6, 15, "start")
dim(xr + 160, Y(0), xr + 160, Y(z0), f"{z0:g}", xr + 170, Y(z0 / 2) + 6, 15, "start")
dim(X(rs), Y(H + 1.2), X(OD / 2), Y(H + 1.2), f"Wand {(OD-G.SITZ_D)/2:g}", (X(rs) + xr) / 2, Y(H + 1.2) - 10, 15)
# Beschriftung links
A(f'<text x="{X(rs-2.5)-10:.1f}" y="{Y(H*0.85):.1f}" font-size="15" fill="#c00" text-anchor="end">Bohrung Ø {G.SITZ_D:g}</text>')
A(f'<text x="{X(rs-2.5)-10:.1f}" y="{Y((z0+z1)/2)+5:.1f}" font-size="15" fill="#c00" text-anchor="end">Nutgrund Ø {G.WULST_D + 2*G.SPIEL:g}</text>')
A(f'<text x="{X(rs-2.5)-10:.1f}" y="{Y((z0+z1)/2)+25:.1f}" font-size="14" fill="#666" text-anchor="end">(Wulst Ø {G.WULST_D:g} schnappt ein)</text>')
A(f'<text x="{X(rs-2.5)-10:.1f}" y="{Y(0.3):.1f}" font-size="14" fill="#666" text-anchor="end">45°-Einführschräge</text>')

# ---------- Tabelle
ty = 640
A(f'<line x1="10" y1="{ty-45}" x2="1190" y2="{ty-45}" stroke="#000"/>')
rows = [("Teil", "Klickring mit Innennut für Geberit Heberglocke (AV02, Glocke 5200.017) – wird auf den Wulst Ø 30 gedrückt"),
        ("Maße", f"Bohrung Ø {G.SITZ_D:g} · Nutgrund Ø {G.WULST_D + 2*G.SPIEL:g} · Nut {z1-z0:.1f} breit · Ø außen {OD:g} · Höhe {H:g} · mm"),
        ("WICHTIG", "Nur Wulst Ø 30 gemessen. Wulstbreite, Rohr-Ø neben dem Wulst, Ø außen und Höhe sind geschätzt."),
        ("Material", "PETG (wasserfest, zäh) – alternativ PLA."),
        ("Druck", "Einführschräge nach unten (wie gezeichnet), 0,12 mm Schicht, 4 Wände, 100 % Füllung, keine Stützen.")]
for i, (k, v) in enumerate(rows):
    A(f'<text x="35" y="{ty+i*36}" font-size="17" font-weight="bold">{k}</text><text x="170" y="{ty+i*36}" font-size="17">{v}</text>')
A('<text x="1175" y="825" font-size="13" text-anchor="end" fill="#666">ring.stl · halbschalen_2stk.stl · clip.scad</text>')
A('</svg>')
open("zeichnung.svg", "w").write("\n".join(out))
print("zeichnung.svg geschrieben")
