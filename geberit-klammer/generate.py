#!/usr/bin/env python3
"""U-Klammer (gruenes Teil) fuer die Geberit Heberglocke AV02 / 5200.017.
Wird ueber den Rand des Gehaeusebechers gesteckt; der Kragen des Rohrs liegt oben auf.
Erzeugt klammer_2stk.stl (2 Stueck, liegend gedruckt).   python3 generate.py
"""
import math, struct

# ---------------- MASSE (mm) – alle geschaetzt, bitte messen ----------------
WAND      = 2.0    # Wandstaerke des Becherrands (Schlitz = WAND + SPIEL)
SPIEL     = 0.3    # Luft im Schlitz
BREITE    = 8.0    # Breite der Klammer (entlang des Rands)
OBEN      = 4.0    # Dicke ueber dem Rand = Abstandshoehe fuer den Kragen
BEIN_A    = 12.0   # Laenge aeusseres Bein (ab Rand nach unten)
BEIN_I    = 8.0    # Laenge inneres Bein (ab Rand nach unten)
STEG      = 2.0    # Dicke der Beine
NASE_L    = 3.0    # wie weit die Nase nach innen uebersteht (Auflage fuer den Kragen)
NASE_H    = 2.0    # Dicke der Nase
ANZAHL    = 2
# -----------------------------------------------------------------------------


def profil():
    s = WAND + SPIEL
    t = STEG
    top = BEIN_A + OBEN
    xi = 2 * t + s
    nh = min(NASE_H, top - (BEIN_A - BEIN_I))
    pts = [(0, 0), (t, 0), (t, BEIN_A), (t + s, BEIN_A), (t + s, BEIN_A - BEIN_I), (xi, BEIN_A - BEIN_I)]
    if NASE_L > 0:
        pts += [(xi, top - nh), (xi + NASE_L, top - nh), (xi + NASE_L, top)]
    else:
        pts += [(xi, top)]
    return pts + [(0, top)]


def earclip(poly):
    idx = list(range(len(poly)))
    tris = []
    cross = lambda o, a, b: (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])
    def inside(p, a, b, c):
        return cross(a, b, p) >= 0 and cross(b, c, p) >= 0 and cross(c, a, p) >= 0
    while len(idx) > 3:
        for k in range(len(idx)):
            i0, i1, i2 = idx[k - 1], idx[k], idx[(k + 1) % len(idx)]
            a, b, c = poly[i0], poly[i1], poly[i2]
            if cross(a, b, c) <= 1e-9:
                continue
            if any(inside(poly[j], a, b, c) for j in idx if j not in (i0, i1, i2)):
                continue
            tris.append((i0, i1, i2)); idx.pop(k); break
    tris.append(tuple(idx))
    return tris


def extrude(poly, h, dx=0.0):
    n = len(poly)
    lo = [(x + dx, y, 0.0) for x, y in poly]
    hi = [(x + dx, y, h) for x, y in poly]
    tris = []
    for a, b, c in earclip(poly):
        tris.append((lo[a], lo[c], lo[b]))   # Boden (Normale nach unten)
        tris.append((hi[a], hi[b], hi[c]))   # Deckel
    for i in range(n):
        j = (i + 1) % n
        tris.append((lo[i], lo[j], hi[j])); tris.append((lo[i], hi[j], hi[i]))
    return tris


def write_stl(path, tris):
    with open(path, "wb") as f:
        f.write(b"Geberit U-Klammer".ljust(80, b" ")); f.write(struct.pack("<I", len(tris)))
        for a, b, c in tris:
            u = [b[i]-a[i] for i in range(3)]; v = [c[i]-a[i] for i in range(3)]
            n = (u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0])
            l = math.sqrt(sum(x*x for x in n)) or 1
            f.write(struct.pack("<3f", *(x/l for x in n)))
            for p in (a, b, c): f.write(struct.pack("<3f", *p))
            f.write(b"\0\0")
    print(f"{path}: {len(tris)} Dreiecke")


if __name__ == "__main__":
    p = profil()
    w = max(x for x, _ in p)
    tris = []
    for k in range(ANZAHL):
        tris += extrude(p, BREITE, dx=k * (w + 5))
    write_stl("klammer_2stk.stl", tris)
