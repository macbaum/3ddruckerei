// Distanz-Clip fuer Geberit Heberglocke (AV02 / 5200.017) – parametrisch
// Oeffnen mit OpenSCAD (openscad.org) oder MakerWorld "Parametric Model Maker",
// Werte anpassen, F6 (Render), dann F7 (Export als STL).

innen_d  = 26;   // Innendurchmesser = Rohrdurchmesser [mm]
aussen_d = 33;   // Aussendurchmesser [mm]
hoehe    = 3;    // Hoehe / Dicke [mm]
spiel    = 0.2;  // Druckertoleranz auf den Innendurchmesser [mm]
variante = "C";  // "C" = C-Clip (Schnappclip), "H" = 2 Halbschalen
c_winkel = 240;  // Umschlingung des C-Clips in Grad (>180 = schnappt ein)
fase     = 0.6;  // Kantenfase [mm]

$fn = 180;
ri = (innen_d + spiel) / 2;
ro = aussen_d / 2;

module profil() {
    c = min(fase, (ro - ri) / 3, hoehe / 3);
    polygon([[ri+c,0],[ro-c,0],[ro,c],[ro,hoehe-c],[ro-c,hoehe],
             [ri+c,hoehe],[ri,hoehe-c],[ri,c]]);
}
module segment(w) rotate([0,0,-w/2]) rotate_extrude(angle = w) profil();

if (variante == "C") {
    segment(c_winkel);
} else {
    translate([-2, 0, 0]) rotate([0,0,180]) segment(179);
    translate([ 2, 0, 0]) segment(179);
}
