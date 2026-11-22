// Klickring fuer Geberit Heberglocke (AV02 / 5200.017) - parametrisch
// Der Ring hat innen eine Nut. Er wird auf den geschlitzten Wulst (Ø 30) am Rohr
// gedrueckt; der Wulst federt ein und schnappt in die Nut.
// MakerWorld: "Parametric Model Maker" -> diese Datei hochladen.
// OpenSCAD: Werte im Customizer aendern, F6 (Render), F7 (STL-Export).

/* [Wulst am Rohr] */
// Ø des geschlitzten Wulsts [mm] (gemessen: 30)
wulst_d = 30; // [15:0.1:60]
// Breite des Wulsts in Laengsrichtung [mm]
wulst_b = 2.5; // [0.5:0.1:10]
// Ø des Rohrs direkt neben dem Wulst = Ringbohrung [mm]
sitz_d = 28.5; // [12:0.1:59]

/* [Ring] */
// Aussen-Ø des Rings [mm]
aussen_d = 40; // [20:0.1:80]
// Gesamthoehe des Rings [mm]
hoehe = 6; // [2:0.1:30]
// Abstand Ringunterkante bis Nut [mm]
nut_abst = 1.5; // [0:0.1:20]
// Druckertoleranz auf die Durchmesser [mm]
spiel = 0.2; // [0:0.05:1]

/* [Form] */
// Bauform
variante = "O"; // [O:geschlossener Ring, C:C-Ring (offen), H:2 Halbschalen]
// Umschlingung des C-Rings in Grad
c_winkel = 260; // [190:5:330]
// Kantenfase aussen [mm]
fase = 0.6; // [0:0.1:1.5]
// Anzahl Ringe auf der Platte
anzahl = 1; // [1:1:6]

/* [Hidden] */
$fn = 180;
rb = (sitz_d + spiel) / 2;
rg = (wulst_d + 2 * spiel) / 2;
ro = aussen_d / 2;
d  = rg - rb;
z0 = max(nut_abst, d + 0.2);
z1 = min(z0 + wulst_b + spiel, hoehe - d - 0.4);
c  = min(fase, (ro - rg) / 3, hoehe / 4);

module profil() {
    polygon([[rg, 0], [ro - c, 0], [ro, c], [ro, hoehe - c], [ro - c, hoehe],
             [rb + c, hoehe], [rb, hoehe - c],
             [rb, z1 + d], [rg, z1], [rg, z0], [rb, z0],
             [rb, d]]);
}

module segment(w) rotate([0, 0, -w / 2]) rotate_extrude(angle = w) profil();

module ein_satz() {
    if (variante == "O") {
        rotate_extrude() profil();
    } else if (variante == "C") {
        segment(c_winkel);
    } else {
        translate([-2, 0, 0]) rotate([0, 0, 180]) segment(179);
        translate([ 2, 0, 0]) segment(179);
    }
}

abstand = aussen_d + 8;
for (i = [0 : anzahl - 1])
    translate([(i % 3) * abstand, floor(i / 3) * abstand, 0]) ein_satz();
