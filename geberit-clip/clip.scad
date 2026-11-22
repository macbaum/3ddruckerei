// Klickring fuer Geberit Heberglocke (AV02 / 5200.017) - parametrisch
// Ring sitzt auf dem Rohr (Ø 30) und rastet mit einer Innenrippe in die Nut ein.
// MakerWorld: "Parametric Model Maker" -> diese Datei hochladen.
// OpenSCAD: Werte im Customizer aendern, F6 (Render), F7 (STL-Export).

/* [Rohr und Nut] */
// Ø des Rohrs, auf dem der Ring sitzt [mm]
rohr_d = 30; // [15:0.1:60]
// Ø im Nutgrund [mm] (kleiner als rohr_d)
nut_d = 28; // [12:0.1:59]
// Breite der Nut in Laengsrichtung [mm]
nut_b = 2; // [0.5:0.1:10]
// Abstand Ringunterkante bis Nut [mm]
nut_abst = 2; // [0:0.1:20]

/* [Ring] */
// Aussen-Ø des Rings [mm]
aussen_d = 40; // [20:0.1:80]
// Gesamthoehe des Rings [mm]
hoehe = 6; // [2:0.1:30]
// Druckertoleranz auf die Durchmesser [mm]
spiel = 0.2; // [0:0.05:1]

/* [Form] */
// Bauform
variante = "C"; // [C:C-Ring (ein Teil), H:2 Halbschalen]
// Umschlingung des C-Rings in Grad
c_winkel = 260; // [190:5:330]
// Kantenfase [mm]
fase = 0.6; // [0:0.1:1.5]
// Anzahl Ringe auf der Platte
anzahl = 1; // [1:1:6]

/* [Hidden] */
$fn = 180;
rb = (rohr_d + spiel) / 2;
rn = (nut_d + spiel) / 2;
ro = aussen_d / 2;
d  = rb - rn;
z0 = max(nut_abst, d + 0.1);
z1 = min(z0 + nut_b, hoehe - d - 0.1);
c  = min(fase, (ro - rb) / 3, hoehe / 4);

module profil() {
    polygon([[rb + c, 0], [ro - c, 0], [ro, c], [ro, hoehe - c], [ro - c, hoehe],
             [rb + c, hoehe], [rb, hoehe - c],
             [rb, z1 + d], [rn, z1], [rn, z0], [rb, z0 - d],
             [rb, c]]);
}

module segment(w) rotate([0, 0, -w / 2]) rotate_extrude(angle = w) profil();

module ein_satz() {
    if (variante == "C") {
        segment(c_winkel);
    } else {
        translate([-2, 0, 0]) rotate([0, 0, 180]) segment(179);
        translate([ 2, 0, 0]) segment(179);
    }
}

abstand = aussen_d + 8;
for (i = [0 : anzahl - 1])
    translate([(i % 3) * abstand, floor(i / 3) * abstand, 0]) ein_satz();
