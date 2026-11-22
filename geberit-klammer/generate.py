#!/usr/bin/env python3
"""U-Klammer (gruenes Teil) fuer die Geberit Heberglocke AV02 / 5200.017.
Wird ueber den Rand des Gehaeusebechers gesteckt; der Kragen des Rohrs liegt oben auf.
Erzeugt klammer_2stk.stl (2 Stueck, liegend gedruckt).   python3 generate.py
"""
import math, struct

# ---------------- MASSE (mm) – aus der Handskizze des Originals ----------------
HOEHE     = 8.0    # Gesamthoehe (aeusseres Bein)
BEIN      = 1.0    # Dicke aeusseres Bein
SCHLITZ   = 1.0    # Schlitzbreite (Becherwand) laut Skizze
SPIEL     = 0.15   # zusaetzliche Luft im Schlitz
STEG_OBEN = 1.0    # Dicke ueber dem Schlitz (angenommen)
BEIN_I    = 1.0    # Dicke inneres Bein (angenommen)
NASE_B    = 3.0    # Breite der Nase ab Aussenkante inneres Bein (inkl. Bein)
NASE_D    = 1.0    # Dicke der Nase
TASCHE    = 6.0    # Abstand Oberkante -> Oberseite Nase (Auflage weisses Teil)
BREITE    = 8.0    # Breite der Klammer (in die Tiefe) – noch nicht gemessen
ANZAHL    = 2
# -----------------------------------------------------------------------------


def profil():
    """Querschnitt, gegen den Uhrzeigersinn. y=0 = Unterkante aeusseres Bein."""
    s = SCHLITZ + SPIEL
    x1, x2, x3 = BEIN, BEIN + s, BEIN + s + BEIN_I
    xn = BEIN + s + NASE_B
    y_nase_oben = HOEHE - TASCHE
    y_nase_unten = max(0.0, y_nase_oben - NASE_D)
    y_schlitz = HOEHE - STEG_OBEN
    return [(0, 0), (x1, 0), (x1, y_schlitz), (x2, y_schlitz), (x2, y_nase_unten),
            (xn, y_nase_unten), (xn, y_nase_oben), (x3, y_nase_oben), (x3, HOEHE), (0, HOEHE)]


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
