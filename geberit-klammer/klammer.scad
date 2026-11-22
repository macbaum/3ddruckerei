// U-Klammer (gruenes Teil) fuer Geberit Heberglocke AV02 / 5200.017 - parametrisch
// Wird ueber den Rand des Gehaeusebechers gesteckt; der Kragen des Rohrs liegt oben auf.
// MakerWorld: "Parametric Model Maker" -> diese Datei hochladen.

/* [Masse] */
// Wandstaerke des Becherrands [mm]
wand = 2.0; // [0.5:0.1:6]
// Luft im Schlitz [mm]
spiel = 0.3; // [0:0.05:1]
// Breite der Klammer entlang des Rands [mm]
breite = 8; // [3:0.5:30]
// Dicke ueber dem Rand = Abstandshoehe [mm]
oben = 4; // [1:0.1:20]
// Laenge aeusseres Bein [mm]
bein_a = 12; // [2:0.5:40]
// Laenge inneres Bein [mm]
bein_i = 8; // [0:0.5:40]
// Dicke der Beine [mm]
steg = 2; // [1:0.1:5]
// wie weit die Nase nach innen uebersteht [mm]
nase_l = 3; // [0:0.5:15]
// Dicke der Nase [mm]
nase_h = 2; // [0.5:0.1:10]
// Anzahl Klammern
anzahl = 2; // [1:1:8]

/* [Hidden] */
s = wand + spiel;
xi = 2 * steg + s;
top = bein_a + oben;
nh = min(nase_h, top - (bein_a - bein_i));
w = xi + nase_l;

module profil() {
    polygon(concat(
        [[0, 0], [steg, 0], [steg, bein_a], [steg + s, bein_a], [steg + s, bein_a - bein_i],
         [xi, bein_a - bein_i]],
        nase_l > 0 ? [[xi, top - nh], [xi + nase_l, top - nh], [xi + nase_l, top]] : [[xi, top]],
        [[0, top]]));
}

// liegend gedruckt: Profil in XY, Breite in Z
for (k = [0 : anzahl - 1])
    translate([k * (w + 5), 0, 0]) linear_extrude(height = breite) profil();
