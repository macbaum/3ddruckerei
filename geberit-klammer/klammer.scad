// Klammer (gruenes Teil) fuer Geberit Heberglocke AV02 / 5200.017 - parametrisch
// Masse aus der Handskizze des Originals. Umgedrehtes U (Schlitz fuer die Becherwand)
// mit Nase unten innen; das weisse Teil liegt in der Tasche auf der Nase auf.
// MakerWorld: "Parametric Model Maker" -> diese Datei hochladen.

/* [Masse] */
// Gesamthoehe [mm]
hoehe = 8; // [3:0.1:30]
// Dicke aeusseres Bein [mm]
bein = 1; // [0.6:0.1:5]
// Schlitzbreite [mm] (0,9 bei 1-mm-Wand = Klemmsitz)
schlitz = 0.9; // [0.3:0.05:5]
// zusaetzliche Luft im Schlitz [mm]
spiel = 0; // [0:0.05:1]
// Dicke ueber dem Schlitz [mm]
steg_oben = 1; // [0.6:0.1:5]
// Dicke inneres Bein [mm]
bein_i = 1; // [0.6:0.1:5]
// Breite Nase ab Aussenkante inneres Bein (inkl. Bein) [mm]
nase_b = 3; // [1:0.1:15]
// Dicke der Nase [mm]
nase_d = 1; // [0.6:0.1:5]
// Abstand Oberkante bis Oberseite Nase [mm]
tasche = 6; // [1:0.1:29]
// Breite der Klammer (in die Tiefe) [mm]
breite = 10; // [2:0.5:30]
// Anzahl Klammern
anzahl = 2; // [1:1:8]

/* [Hidden] */
s  = schlitz + spiel;
x1 = bein; x2 = bein + s; x3 = bein + s + bein_i; xn = bein + s + nase_b;
yo = hoehe - tasche;
yu = max(0, yo - nase_d);
ys = hoehe - steg_oben;

module profil() {
    polygon([[0, 0], [x1, 0], [x1, ys], [x2, ys], [x2, yu], [xn, yu], [xn, yo],
             [x3, yo], [x3, hoehe], [0, hoehe]]);
}

// liegend gedruckt: Profil flach in XY, Breite in Z
for (k = [0 : anzahl - 1])
    translate([k * (xn + 4), 0, 0]) linear_extrude(height = breite) profil();
