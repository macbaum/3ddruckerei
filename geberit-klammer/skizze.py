#!/usr/bin/env python3
"""Erzeugt skizze.svg aus den Massen in generate.py."""
import generate as G
S = 40.0  # 40:1
ox, oy = 260, 500          # Ursprung (Unterkante aeusseres Bein)
X = lambda x: ox + x * S
Y = lambda y: oy - y * S
p = G.profil()
s = G.SCHLITZ + G.SPIEL
x1, x2, x3 = G.BEIN, G.BEIN + s, G.BEIN + s + G.BEIN_I
xn = G.BEIN + s + G.NASE_B
yo = G.HOEHE - G.TASCHE; yu = yo - G.NASE_D; ys = G.HOEHE - G.STEG_OBEN
o = []; A = o.append
A('<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="850" viewBox="0 0 1200 850" font-family="Arial, sans-serif">')
A('<defs><marker id="a" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,1 L10,5 L0,9 z" fill="#c00"/></marker>'
  '<pattern id="h" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="7" stroke="#1d7a3a" stroke-width="1.2"/></pattern></defs>')
A('<rect width="1200" height="850" fill="#fff"/><rect x="10" y="10" width="1180" height="830" fill="none" stroke="#000" stroke-width="2"/>')
A('<text x="600" y="50" font-size="26" font-weight="bold" text-anchor="middle">Klammer (grünes Teil) – nach Ihrer Skizze</text>')
A('<text x="600" y="78" font-size="16" text-anchor="middle" fill="#555">Querschnitt, Maßstab 40:1 · Maße in mm</text>')
# Becherwand im Schlitz, weisses Teil auf der Nase
A(f'<rect x="{X(G.BEIN):.1f}" y="{Y(G.HOEHE-G.STEG_OBEN):.1f}" width="{(G.SCHLITZ+G.SPIEL)*S:.1f}" height="{(G.HOEHE-G.STEG_OBEN+2)*S:.1f}" fill="#eee" stroke="#777" stroke-dasharray="6 3"/>')
A(f'<text x="{X(x1)-10:.1f}" y="{Y(-1.4):.1f}" font-size="15" fill="#666" text-anchor="end">Becherwand →</text>')
A(f'<rect x="{X(x3+0.15):.1f}" y="{Y(G.HOEHE+1.2):.1f}" width="{(xn-x3-0.3)*S:.1f}" height="{(G.HOEHE+1.2-yo)*S:.1f}" fill="#f4efe0" stroke="#777" stroke-dasharray="6 3"/>')
A(f'<text x="{X(xn)+12:.1f}" y="{Y(G.HOEHE+0.6):.1f}" font-size="15" fill="#666">weißes Teil liegt auf der Nase</text>')
A('<polygon points="' + " ".join(f"{X(x):.1f},{Y(y):.1f}" for x, y in p) + '" fill="url(#h)" stroke="#1d7a3a" stroke-width="3"/>')
def dim(x1_, y1_, x2_, y2_, t, tx, ty, anc="middle"):
    A(f'<line x1="{x1_:.1f}" y1="{y1_:.1f}" x2="{x2_:.1f}" y2="{y2_:.1f}" stroke="#c00" stroke-width="1.4" marker-start="url(#a)" marker-end="url(#a)"/>')
    A(f'<text x="{tx:.1f}" y="{ty:.1f}" font-size="18" fill="#c00" font-weight="bold" text-anchor="{anc}">{t}</text>')
def ext(x1_, y1_, x2_, y2_):
    A(f'<line x1="{x1_:.1f}" y1="{y1_:.1f}" x2="{x2_:.1f}" y2="{y2_:.1f}" stroke="#c00" stroke-width="0.6"/>')
# Hoehe 8
ext(X(0)-60, Y(0), X(0), Y(0)); ext(X(0)-60, Y(G.HOEHE), X(0), Y(G.HOEHE))
dim(X(0)-45, Y(0), X(0)-45, Y(G.HOEHE), f"{G.HOEHE:g}", X(0)-55, Y(G.HOEHE/2)+6, "end")
# Bein 1 (oben)
ext(X(0), Y(G.HOEHE), X(0), Y(G.HOEHE)-50); ext(X(x1), Y(G.HOEHE), X(x1), Y(G.HOEHE)-50)
dim(X(0), Y(G.HOEHE)-40, X(x1), Y(G.HOEHE)-40, f"{G.BEIN:g}", X(x1/2), Y(G.HOEHE)-50)
# Schlitz (unten)
ext(X(x1), Y(0), X(x1), Y(0)+60); ext(X(x2), Y(yu), X(x2), Y(0)+60)
dim(X(x1), Y(0)+50, X(x2), Y(0)+50, f"{G.SCHLITZ + G.SPIEL:g} (Wand 1,0)", X(x2)+10, Y(0)+56, "start")
# Nase 3 (unten)
ext(X(xn), Y(yu), X(xn), Y(0)+120); ext(X(x2), Y(0)+60, X(x2), Y(0)+120)
dim(X(x2), Y(0)+110, X(xn), Y(0)+110, f"{G.NASE_B:g}", X((x2+xn)/2), Y(0)+140)
# Tasche 6 und Nase 1 (rechts)
xr = X(xn) + 70
ext(X(x3), Y(G.HOEHE), xr + 10, Y(G.HOEHE)); ext(X(xn), Y(yo), xr + 80, Y(yo)); ext(X(xn), Y(yu), xr + 80, Y(yu))
dim(xr, Y(G.HOEHE), xr, Y(yo), f"{G.TASCHE:g}", xr + 12, Y((G.HOEHE+yo)/2)+6, "start")
dim(xr + 70, Y(yo), xr + 70, Y(yu), f"{G.NASE_D:g}", xr + 82, Y((yo+yu)/2)+6, "start")
A(f'<text x="{X(x1+s/2):.1f}" y="{Y(G.HOEHE)-80:.1f}" font-size="14" fill="#555" text-anchor="middle">innen/außen je nach Einbau</text>')
# Tabelle
rows = [("Gesamthöhe", f"{G.HOEHE:g}", "Skizze"), ("Bein außen", f"{G.BEIN:g}", "Skizze"),
        ("Schlitz (Klemmsitz)", f"{G.SCHLITZ + G.SPIEL:g}", "gemessen"),
        ("Nase (inkl. inneres Bein)", f"{G.NASE_B:g}", "Skizze"), ("Nasendicke", f"{G.NASE_D:g}", "Skizze"),
        ("Tasche über der Nase", f"{G.TASCHE:g}", "Skizze"),
        ("Steg über dem Schlitz", f"{G.STEG_OBEN:g}", "angenommen"), ("inneres Bein", f"{G.BEIN_I:g}", "angenommen"),
        ("Breite (Tiefe)", f"{G.BREITE:g}", "gemessen")]
y0 = 130
A(f'<rect x="760" y="{y0}" width="410" height="{36*len(rows)+10}" fill="none" stroke="#000"/>')
for i, (k, v, q) in enumerate(rows):
    y = y0 + 30 + i * 36
    col = "#c00" if q.startswith("FEHLT") else ("#b36b00" if q == "angenommen" else "#2a8a2a")
    A(f'<text x="775" y="{y}" font-size="16">{k}</text><text x="985" y="{y}" font-size="16" font-weight="bold">{v}</text>'
      f'<text x="1160" y="{y}" font-size="13" fill="{col}" text-anchor="end">{q}</text>')
A('<line x1="10" y1="700" x2="1190" y2="700" stroke="#000"/>')
A('<text x="35" y="738" font-size="17" font-weight="bold">Druck</text><text x="170" y="738" font-size="17">liegend (Querschnitt flach auf der Platte), PETG, 0,08–0,12 mm Schicht, 0,4-mm-Düse, 100 % Füllung, keine Stützen.</text>')
A('<text x="35" y="772" font-size="17" font-weight="bold">Hinweis</text><text x="170" y="772" font-size="17">1-mm-Wände sind am Limit (2 Linien à 0,45 mm) – Linienbreite im Slicer ggf. auf 0,42 mm stellen.</text>')
A('<text x="35" y="806" font-size="17" font-weight="bold">Datei</text><text x="170" y="806" font-size="17">klammer_2stk.stl · klammer.scad (Parametric Model Maker)</text>')
A('</svg>')
open("skizze.svg", "w").write("\n".join(o)); print("skizze.svg geschrieben")
