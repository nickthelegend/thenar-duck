# Hardware and fasteners — revision B

## Installed hardware

| Item | Installed | From stated cart/ownership |
|---|---:|---|
| Waveshare ST3215 C018 12 V servo | 14 | 14 |
| Raspberry Pi 4B | 1 | Owned |
| BK 4200 mAh 3S | 1 | Owned; BONKA dimensional reference used |
| DFRobot SEN0374 BNO055 | 1 | Replacement selected |
| Waveshare Bus Servo Adapter (A) | 1 | Assumed corrected interface; distinct from 7.2 V buck |
| PDB and UBEC | 1 each | Cart |
| Inline fuse holder + fuse / DC main switch | 1 each | User reported corrections; exact models not supplied |
| 6804 ZZ bearing | 3 | 4; one spare |
| KW10 microswitch | 4 | 6; two spare |
| 16-pixel ring | 2 | 3; one spare |
| 4×4 LED matrix | 1 | Cart |
| Bare 2020 pixel | 1 | Cart; needs 10 × 10 mm solder carrier |

## Screws for the custom mounting system

These quantities include the four foot-contact cassettes, torso, lights and board mounts. **Add the retained servo mechanism's kit screws and core fasteners separately.** Screw length is measured under the head.

| Screw | Quantity |
|---|---:|
| M2 × 10 mm | 2 |
| M2 × 14 mm | 8 |
| M2.5 × 12 mm | 8 |
| M3 × 6 mm | 32 |
| M3 × 8 mm | 46 |
| M3 × 10 mm | 6 |
| M3 × 12 mm | 4 |

**Ordinary nuts for these custom mounts:** M3 **6**, M2.5 **8**, M2 **10**. Inserts already provide a nut at insert joints; do not buy one extra nut per insert. M3 nuts go to the PDB (4) and IMU bridge (2); M2.5 nuts go to Pi/adapter; M2 nuts go to sensor/foot switches.

**M3 flat washers:** 46 at **1 mm thickness**, 34 at **0.5 mm thickness**, for the explicitly washer-specified custom joints. Do not substitute arbitrary thickness at the short insert joints. PCB bolts use the individual stack specified in `reports/fasteners_custom_parts.csv`; the Pi M2.5×12 stack has no extra washer.

The B enclosure, eyes and light mounts contain **62 M3 insert positions**. The retained foot-contact changes add **16**, making **78 custom insert positions**, plus the original core's retained inserts (including four used to attach B01). The total inherited consumption is not reconciled; 100 owned inserts is not a verified whole-robot total. Alternative lids reuse the same installed inserts.

## Assembly materials

- Two 20 mm hook-and-loop battery straps and 2 mm nonabrasive pad.
- Insulating spacers B19 are printed; add ties for the UBEC/fuse, wire insulation and a grommet/sleeve for the 14 mm pass-through.
- Matching serial-bus cables, suitable power wires/connectors, Pi power lead and board/header leads. Cart PWM extension cables are not assumed to fit the bus servos.
- Thin removable insulating adhesive pads for LED PCB backs and diffuser retention; small 10 × 10 mm solder carrier for the bare pixel.
- PETG structural prints, compliant TPU/rubber sole provision and translucent diffuser material.

Electrical current budget, fuse rating, wire size and switch DC rating are outside this geometric BOM and have not been approved by the CAD fit check.
