// Distanz-Clip fuer Geberit Heberglocke (AV02 / 5200.017) - parametrisch
// MakerWorld: "Parametric Model Maker" -> diese Datei hochladen.
// OpenSCAD: Werte rechts im Customizer aendern, F6 (Render), F7 (STL-Export).

/* [Masse] */
// Innendurchmesser = Durchmesser der Nut am Rohr [mm]
innen_d = 26; // [15:0.1:60]
// Aussendurchmesser [mm] (kleiner als Huelse Ø 35)
aussen_d = 33; // [18:0.1:70]
// Hoehe / Dicke = Breite der Nut [mm]
hoehe = 3; // [1:0.1:20]
// Druckertoleranz auf den Innendurchmesser [mm]
spiel = 0.2; // [0:0.05:1]

/* [Form] */
// Bauform
variante = "C"; // [C:C-Clip (ein Teil), H:2 Halbschalen]
// Umschlingung des C-Clips in Grad (mehr als 180 = schnappt ein)
c_winkel = 240; // [190:5:330]
// Kantenfase [mm]
fase = 0.6; // [0:0.1:1.5]
// Anzahl Clips auf der Platte
anzahl = 1; // [1:1:6]

/* [Hidden] */
$fn = 180;
ri = (innen_d + spiel) / 2;
ro = aussen_d / 2;

module profil() {
    c = min(fase, (ro - ri) / 3, hoehe / 3);
    polygon([[ri + c, 0], [ro - c, 0], [ro, c], [ro, hoehe - c], [ro - c, hoehe],
             [ri + c, hoehe], [ri, hoehe - c], [ri, c]]);
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
