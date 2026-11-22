#!/usr/bin/env python3
"""Klickring fuer die Geberit Heberglocke (AV02 / 5200.017).
Der Ring sitzt auf dem Rohr (Ø 30) und rastet mit einer Innenrippe in die
umlaufende Nut ein.  Nur Python-Standardbibliothek noetig:
    python3 generate.py
"""
import math, struct

# ---------------- MASSE (in mm) ----------------
ROHR_D     = 30.0   # Ø des Rohrs, auf dem der Ring sitzt (gemessen)
NUT_D      = 28.0   # Ø im Nutgrund (geschaetzt – messen!)
NUT_B      = 2.0    # Breite der Nut in Laengsrichtung (geschaetzt – messen!)
NUT_ABST   = 2.0    # Abstand Ringunterkante -> Nut (geschaetzt)
AUSSEN_D   = 40.0   # Aussen-Ø des Rings (Anschlag; geschaetzt)
HOEHE      = 6.0    # Gesamthoehe des Rings (geschaetzt)
SPIEL      = 0.2    # Druckertoleranz (auf Durchmesser)
C_WINKEL   = 260.0  # Umschlingung des C-Rings in Grad
FASE       = 0.6    # Kantenfase
SEG        = 180
# -----------------------------------------------


def profil():
    """Querschnitt (r, z) gegen den Uhrzeigersinn, mit Innenrippe."""
    rb = (ROHR_D + SPIEL) / 2           # Bohrung
    rn = (NUT_D + SPIEL) / 2            # Rippe (greift in die Nut)
    ro = AUSSEN_D / 2
    d = rb - rn                          # 45°-Schraegen an der Rippe
    z0 = max(NUT_ABST, d + 0.1)
    z1 = min(z0 + NUT_B, HOEHE - d - 0.1)
    c = min(FASE, (ro - rb) / 3, HOEHE / 4)
    return [(rb + c, 0), (ro - c, 0), (ro, c), (ro, HOEHE - c), (ro - c, HOEHE),
            (rb + c, HOEHE), (rb, HOEHE - c),
            (rb, z1 + d), (rn, z1), (rn, z0), (rb, z0 - d),
            (rb, c)]


def ring_sector(angle_deg):
    prof = profil()
    m = len(prof)
    n = max(4, int(SEG * angle_deg / 360))
    a0, da = math.radians(-angle_deg / 2), math.radians(angle_deg) / n
    rings = []
    for i in range(n + 1):
        a = a0 + i * da
        rings.append([(r * math.cos(a), r * math.sin(a), z) for r, z in prof])
    tris = []
    for i in range(n):
        A, B = rings[i], rings[i + 1]
        for j in range(m):
            k = (j + 1) % m
            tris += [(A[j], B[j], B[k]), (A[j], B[k], A[k])]
    # Endkappen: Faecher von einem Punkt, von dem aus das Profil sternfoermig ist
    ro = AUSSEN_D / 2
    for R, a, flip in ((rings[0], a0, False), (rings[-1], a0 + n * da, True)):
        cpt = ((ro - 0.4) * math.cos(a), (ro - 0.4) * math.sin(a), HOEHE / 2)
        for j in range(m):
            t = (cpt, R[j], R[(j + 1) % m])
            tris.append(t if not flip else (t[0], t[2], t[1]))
    return tris


def orient(tris):
    vol = sum(a[0]*(b[1]*c[2]-b[2]*c[1]) - a[1]*(b[0]*c[2]-b[2]*c[0]) + a[2]*(b[0]*c[1]-b[1]*c[0])
              for a, b, c in tris)
    return tris if vol > 0 else [(a, c, b) for a, b, c in tris]


def move(tris, dx, dy, mirror=False):
    out = []
    for t in tris:
        if mirror:
            t = tuple((-p[0], p[1], p[2]) for p in (t[0], t[2], t[1]))
        out.append(tuple((p[0] + dx, p[1] + dy, p[2]) for p in t))
    return out


def write_stl(path, tris):
    with open(path, "wb") as f:
        f.write(b"Geberit Klickring".ljust(80, b" "))
        f.write(struct.pack("<I", len(tris)))
        for a, b, c in tris:
            u = [b[i] - a[i] for i in range(3)]; v = [c[i] - a[i] for i in range(3)]
            nx, ny, nz = u[1]*v[2]-u[2]*v[1], u[2]*v[0]-u[0]*v[2], u[0]*v[1]-u[1]*v[0]
            l = math.sqrt(nx*nx + ny*ny + nz*nz) or 1
            f.write(struct.pack("<3f", nx/l, ny/l, nz/l))
            for p in (a, b, c):
                f.write(struct.pack("<3f", *p))
            f.write(b"\0\0")
    print(f"{path}: {len(tris)} Dreiecke")


if __name__ == "__main__":
    write_stl("clip_C.stl", orient(ring_sector(C_WINKEL)))
    half = orient(ring_sector(179.0))
    ro = AUSSEN_D / 2
    write_stl("halbschalen_2stk.stl", move(half, -ro - 2, 0) + move(half, ro + 2, 0, mirror=True))
