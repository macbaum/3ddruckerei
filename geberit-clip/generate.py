#!/usr/bin/env python3
"""Erzeugt STL-Dateien fuer den Distanz-Clip der Geberit Heberglocke (AV02 / 5200.017).
Nur Python-Standardbibliothek noetig.  Masse unten anpassen und erneut ausfuehren:
    python3 generate.py
"""
import math, struct

# ---------------- MASSE (in mm) – bitte am Original nachmessen ----------------
INNEN_D   = 26.0   # Innendurchmesser = Durchmesser des Rohrs, auf dem der Clip sitzt
AUSSEN_D  = 33.0   # Aussendurchmesser
HOEHE     = 3.0    # Hoehe/Dicke (= Abstand, der ueberbrueckt werden soll)
SPIEL     = 0.2    # Zugabe auf den Innendurchmesser (Druckertoleranz)
C_WINKEL  = 240.0  # Umschlingungswinkel des C-Clips in Grad (>180 = schnappt ein)
FASE      = 0.6    # Fase an den Kanten (erleichtert das Aufschieben)
SEG       = 180    # Aufloesung (Segmente pro 360 Grad)
# -----------------------------------------------------------------------------

def ring_sector(ri, ro, h, angle_deg, chamfer, seg_full=SEG):
    """Ringsegment (angle<360) als Dreiecksliste. Profil mit Fasen (Achteck-Querschnitt)."""
    c = min(chamfer, (ro - ri) / 3, h / 3)
    # Querschnittsprofil (r, z) gegen den Uhrzeigersinn
    prof = [(ri + c, 0), (ro - c, 0), (ro, c), (ro, h - c), (ro - c, h),
            (ri + c, h), (ri, h - c), (ri, c)]
    n = max(4, int(seg_full * angle_deg / 360))
    a0 = math.radians(-angle_deg / 2)
    da = math.radians(angle_deg) / n
    rings = []
    for i in range(n + 1):
        a = a0 + i * da
        ca, sa = math.cos(a), math.sin(a)
        rings.append([(r * ca, r * sa, z) for r, z in prof])
    tris = []
    m = len(prof)
    for i in range(n):
        A, B = rings[i], rings[i + 1]
        for j in range(m):
            k = (j + 1) % m
            tris.append((A[j], B[j], B[k]))
            tris.append((A[j], B[k], A[k]))
    # Endkappen (konvexes Profil -> Faecher)
    def cap(R, flip):
        for j in range(1, m - 1):
            t = (R[0], R[j], R[j + 1])
            tris.append(t if not flip else (t[0], t[2], t[1]))
    cap(rings[0], False)
    cap(rings[-1], True)
    return tris

def fix_orientation(tris):
    # Normalen nach aussen ausrichten anhand des Volumen-Vorzeichens
    vol = sum(a[0]*(b[1]*c[2]-b[2]*c[1]) - a[1]*(b[0]*c[2]-b[2]*c[0]) + a[2]*(b[0]*c[1]-b[1]*c[0])
              for a, b, c in tris)
    return tris if vol > 0 else [(a, c, b) for a, b, c in tris]

def translate(tris, dx, dy):
    return [tuple((p[0] + dx, p[1] + dy, p[2]) for p in t) for t in tris]

def write_stl(path, tris):
    with open(path, "wb") as f:
        f.write(b"Geberit Clip".ljust(80, b" "))
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

ri = (INNEN_D + SPIEL) / 2
ro = AUSSEN_D / 2

# Variante A: C-Clip (ein Teil, wird seitlich aufgeschnappt)
write_stl("clip_C.stl", fix_orientation(ring_sector(ri, ro, HOEHE, C_WINKEL, FASE)))

# Variante B: zwei Halbschalen (je 180 Grad), nebeneinander fuer einen Druckvorgang
half = fix_orientation(ring_sector(ri, ro, HOEHE, 179.0, FASE))
write_stl("halbschalen_2stk.stl", translate(half, -ro - 2, 0) + translate(
    [tuple((-p[0], p[1], p[2]) for p in (t[0], t[2], t[1])) for t in half], ro + 2, 0))
