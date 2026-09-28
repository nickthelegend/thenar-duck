# Dimensional evidence

All dimensions are millimetres. Published specifications are not physical measurements of the user's individual parts.

| Component | Evidence used | Qualification |
|---|---|---|
| Battery | [BONKA BK-4200/35-3S](https://www.bonkapower.com/ru/helicopterairplane-lipo-batteries/533252.html): 137 × 44 × 27, 320 g, XT60/JST-XH | Model inferred from “BK 4200 3S”; larger sled capacity and rear lead bay supplied. |
| Pi 4B | [Official mechanical drawing](https://datasheets.raspberrypi.com/rpi4/raspberry-pi-4-mechanical-drawing.pdf): 85 × 56, 58 × 49 mounting pitch, Ø2.75 holes | Pi board pattern used directly. Port housings are simplified; accessory plugs are not exact vendor models. |
| DFRobot SEN0374 | [Official product wiki and dimension drawing](https://wiki.dfrobot.com/sen0374): 19 × 21, two Ø2 holes on one edge, 16 pitch | Mounted rotated 90° in the XY plane; configure the sensor-to-robot axis transform in software. |
| ST3215 C018 | [Waveshare ST3215 servo](https://www.waveshare.com/st3215-servo.htm), vendor STEP in `../vendor/` | Exact vendor solid reference used for nominal case/horn interference checks; supplied hardware and cable routing require assembly trials. |
| Bus Servo Adapter (A) | [Waveshare documentation](https://docs.waveshare.com/Bus_Servo_Adapter_A): 42 × 33, 37 × 28 hole pitch | Assumed final adapter after the user's correction; not the 7.2 V buck product in the first cart. |
| xcluma PDB | [Matek PDB-XT60 manual](https://www.mateksys.com/downloads/pdb-xt60_manual_en.pdf): 50 × 36 × 4, 30.5 hole pitch | Reference family only; clone identity/dimensions not asserted. Slots provide 28–33 pitch adjustment. |
| ReadyToSky UBEC | [Manufacturer product page](https://www.readytosky.com/e_productshow/?951-Readytosky-2-6S-5V3A-and-12V3A-Switchable-UBEC-951.html=) | Accessible manufacturer page gave no dimensional drawing; 45 × 22 × 15 is the **mount's capacity**. |
| KW10-DZ2P075 | [Daier microswitch catalogue](https://www.chinadaier.com/wp-content/uploads/2017/08/Micro-switch.pdf) | Catalogue body, hole spacing and lever dimensions used; cassette allows operating-height adjustment. |
| Main switch | [Finglai KCD1 family](https://www.finglai.com/products/switches/rocker-switches/KCD1-19x13/KCD1-101.html) illustrates the common 19 × 13 class | Actual switch identity unknown. Default cutout 19.4 × 13.2 and three alternatives are design options, not a claim that all switches fit. CAD fit does not establish a switch's DC current rating. |
| Inserts, LED boards and fuse holder | User's cart and explicitly stated design capacities | No exact outside-diameter or PCB drawing invented; coupons, interchangeable sleeves, removable carriers and straps used. |
| Joint mechanism | [Pinned Open Duck Mini repository](https://github.com/apirrone/Open_Duck_Mini/tree/b23317a485b3cec7d8417f352478778b3475173c) | 14 retained joint axes, 78.65 mm leg links, three 6804 bearings. Old Pi Zero/power/lighting installation is superseded by B. |

## Electrical boundary of this CAD

The mechanical layout does not establish a current budget, fuse value, wire gauge, servo bus topology, battery runtime or thermal performance. Keep the Pi on regulated 5 V; a 3S pack must not connect directly to it. The ReadyToSky product's 12 V mode requires 4–6S according to its manufacturer. A 3 A rail has not been shown sufficient for a Pi 4B plus all LEDs at full brightness. The signal adapter must not be presumed to carry all fourteen servos' combined current. These are unresolved electrical design checks, not dimensions inferred from the enclosure.
