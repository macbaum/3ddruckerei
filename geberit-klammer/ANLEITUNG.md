# U-Klammer (grünes Teil) – Geberit Heberglocke AV02 / 5200.017

![Skizze](skizze.png)

Die zwei grünen U-Klammern werden über den Rand des Gehäusebechers gesteckt.
Oben steht innen eine **Nase** über, auf der der weiße Kragen des Rohrs aufliegt; die Dicke **O** bestimmt also die Höhe des Rohrs.

## Dateien
- `klammer_2stk.stl` – 2 Klammern, fertig zum Drucken (Standardmaße, geschätzt)
- `klammer.scad` – zum Anpassen (MakerWorld Parametric Model Maker oder OpenSCAD)
- `generate.py` – erzeugt die STL neu (`python3 generate.py`)

## Maße (geschätzt – bitte am Original messen)
| | Maß | Standard |
|---|---|---|
| S | Wandstärke Becherrand | 2,0 mm (+0,3 Spiel) |
| B | Breite | 8 mm |
| O | Dicke über dem Rand | 4 mm |
| A | Bein außen | 12 mm |
| I | Bein innen | 8 mm |
| T | Dicke der Beine | 2 mm |
| N | Überstand der Nase nach innen (Auflage für den Kragen) | 3 mm (Dicke 2 mm) |

## Drucken (Bambu Studio / MakerWorld)
1. `klammer_2stk.stl` importieren – die Klammern liegen bereits flach (Profil auf der Platte).
2. PETG, 0,12–0,16 mm Schicht, 4 Wände, 100 % Füllung, **keine Stützen**.
3. Slicen → an den A1 mini senden. Druckzeit wenige Minuten.

Tipp: Sitzt die Klammer zu stramm auf dem Rand → `spiel` erhöhen. Zu locker → verringern.
