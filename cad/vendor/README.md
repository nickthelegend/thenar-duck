# Vendor CAD: Feetech STS3215 serial bus servo

Reference geometry for the Feetech STS3215 (12 V variant sold by Waveshare as "ST3215";
Feetech part code ST-3215-C018). All files were downloaded 2026-09-26 and verified:
every `.step` starts with `ISO-10303-21`, both `.stl` are valid binary STL (watertight,
single body), PDFs open and render.

Feetech itself does not publish a STEP file: the product page only links the datasheet, and
the Feetech "Data Download" portal (doc.feetech.cn) only hosts memory tables, protocol
documents and SDKs. The closest thing to a vendor-official 3D model is the STEP that
Waveshare distributes for the ST3215 (Feetech-authored assembly, see below).
GrabCAD / Onshape / Printables copies were skipped (login-gated or community-made).

## Files

| File | Size | What it is | Source | License |
|---|---|---|---|---|
| `STS3215_Waveshare_ST3215.step` | 3,025,101 B | Full servo **assembly** (9 products: `SCS215 v5` root, case parts `ZK_122`, `SG-ZIJI_15`, `XG-ZIJI_16`, `GE_27`, `MOTOR-1723_3`, `PCB-CHAZUO_92`, drive horn "配属舵盘(驱动)", idler horn "配属舵盘(从动)"). STEP AP214, mm. Exported 2022-06-08 from Autodesk (Inventor/Fusion) via ST-Developer v19. Chinese part names and the `SCS215` root name indicate a Feetech factory model of the shared SCS215/STS3215 housing, redistributed by Waveshare. | Waveshare wiki "ST3215 Servo" -> 3D model: https://files.waveshare.com/upload/5/59/ST3215-3D.zip (page: https://www.waveshare.com/wiki/ST3215_Servo) | No explicit license stated. Product documentation published by Waveshare/Feetech for customers; use as reference geometry. |
| `STS3215_drawing.pdf` | 114,506 B | Official 2D dimension drawing, 3 views, title block "SCS215", drawn by WL Zhang 2022-06-08 (same housing as STS3215). | Waveshare wiki -> 2D drawing: https://files.waveshare.com/upload/0/08/ST3215-2D.zip | as above |
| `STS3215_drawing.dxf` | 458,208 B | Same drawing as DXF (from the same zip). | as above | as above |
| `STS3215_Feetech_datasheet_ST-3215-C018.pdf` | 580,754 B | Feetech product specification ST-3215-C018 rev A/0, 2023-07-20, 8 pages. Page 6, section 9 "Outside Dimension" is the official Feetech outline drawing. | Feetech product page https://www.feetechrc.com/525603.html -> https://www.feetechrc.com/Data/feetechrc/upload/file/20260622/6391772519923113075854851.pdf | (c) Shenzhen Feetech RC Model Co., Ltd. Public product specification. |
| `STS3215_drawing_feetech.jpg` | 71,861 B | The outline-drawing figure extracted from page 6 of the datasheet above (765 x 584 px). | as above | as above |
| `STS3215_SO-ARM100_03a.step` | 247,082 B | Single-part simplified servo model `STS3215_03a v1` used in the SO-100 / SO-101 arm CAD. STEP AP242, mm, Fusion 360 export 2025-01-27. Includes drive horn on the output side and the rear passive horn. | TheRobotStudio/SO-ARM100, `STEP/SO100/STS3215_03a.step` (commit `5f6d2b8`, 2026-09-23): https://raw.githubusercontent.com/TheRobotStudio/SO-ARM100/main/STEP/SO100/STS3215_03a.step | Apache-2.0 (repo LICENSE) |
| `STS3215_Passive_Horn_SO-ARM100.step` | 8,900 B | The passive (idler) horn that mounts on the servo's rear boss: Ø20 x 3.1 mm disc, Ø7 through-hole, Ø9 x 2.0 step. Small file because the part is trivially simple (below the 50 KB sanity threshold, but a valid STEP). | TheRobotStudio/SO-ARM100, `STEP/SO100/Passive_Horn_01.step`: https://raw.githubusercontent.com/TheRobotStudio/SO-ARM100/main/STEP/SO100/Passive_Horn_01.step | Apache-2.0 |
| `STS3215_SO-ARM100_03a_with_horn.stl` | 954,084 B | Binary STL mesh of the same model (19,080 facets, watertight). **Units: metres** (URDF/MJCF convention) -> scale x1000 for mm. | TheRobotStudio/SO-ARM100, `Simulation/SO101/assets/sts3215_03a_v1.stl` | Apache-2.0 |
| `STS3215_SO-ARM100_03a_no_horn.stl` | 865,884 B | Same mesh without the rear passive horn (17,316 facets, watertight). Units: metres. | TheRobotStudio/SO-ARM100, `Simulation/SO101/assets/sts3215_03a_no_horn_v1.stl` | Apache-2.0 |

SHA-256:

```
58e38e4dc49f97df738c5f229f9aa8a7dce64a0a1d01335486a52d53e6017e8a  STS3215_Waveshare_ST3215.step
3f28841c73dd21c4dc757bc25c40fc2a9f71f30a4cbf77a4d9a3546ccf35afa1  STS3215_drawing.pdf
b5fdce6c6bdce84ec6d47aff86dbbbe5abe919e18ebe6517c5413e4c276e0644  STS3215_drawing.dxf
d0a735a8ddc23585dd7fef40bf7ed87359b6234436103e00bb6e992b5ffe9f39  STS3215_Feetech_datasheet_ST-3215-C018.pdf
6e239a56c2d2f4ba3ab137c2ee32486e888e152aba1df0ff2962ec21261cc5c1  STS3215_drawing_feetech.jpg
cacd717c2f22bec856fdace2c3bc9fa58084d54b6e70378eae90562f34df93ef  STS3215_SO-ARM100_03a.step
616655137679da98b29950a03d0c555d9e604e1fef4feaa32bf163cc11a392f6  STS3215_Passive_Horn_SO-ARM100.step
a37c871fb502483ab96c256baf457d36f2e97afc9205313d9c5ab275ef941cd0  STS3215_SO-ARM100_03a_with_horn.stl
75ef3781b752e4065891aea855e34dc161a38a549549cd0970cedd07eae6f887  STS3215_SO-ARM100_03a_no_horn.stl
```

## Body dimensions (from the drawings)

Both drawings agree; Feetech datasheet section 6-1 states the size as 45.2 x 24.7 x 35 mm,
weight 55 +/- 1 g, horn 25T / OD 5.9 mm spline, horn screw M3 x 6, connector 5264 3P (2.54 mm).

| Feature | Waveshare drawing (`STS3215_drawing.pdf`) | Feetech datasheet p.6 |
|---|---|---|
| Housing length (along the long axis) | 45.22 | 45.23 |
| Housing width | 24.72 | 24.73 |
| Housing height along the shaft axis, rear Ø6 boss tip to output-side case face | 35 | 35 |
| Case rear face to output-side case face (excl. rear boss) | 32 | 32 |
| Full-footprint mid band (between top/bottom cover lips) | 29 | 29 |
| Overall incl. horns | 37.25 (with the thicker drive horn in the assembly) | 36.5 |
| Drive-horn stack above the case face | -- | 3.4 |
| Rear (idler) boss | -- | Ø6, protrudes 4.1 |
| Drive horn / boss diameter | Ø19.2 | (Ø20 boss on the case) |
| Output shaft centre from the near end face | 10.11 | 45.23/2 - 12.5 = 10.12 |
| Output shaft centre from housing mid-length | -- | 12.5 |
| Output shaft across the width | centred (24.72/2 = 12.36) | centred |
| Mounting-hole pitch across width (output face) | 14 (holes on Ø19.2 boss, 2 pairs) | 8 x PA2.0 self-tapping (4 per face) |
| Mounting holes along length (bottom face) | 6.11 / 20.7 / 18.41 from the end faces | -- |
| Output-face lugs | 20.5 across, 24.45 long region | -- |

The output shaft and the rear idler boss are coaxial (the passive horn goes on the rear boss).

## Shaft location as measured in `STS3215_SO-ARM100_03a.step` / the STL twins

Part frame: origin at the centre of the 45.4 x 24.8 mm housing footprint, X along the
length, Y across the width, Z = output shaft axis, +Z = output (drive horn) side.
Measured by slicing the STL (scaled to mm) and from circle entities in the STEP:

* Housing: X -22.7 .. +22.7 (45.4), Y -12.4 .. +12.4 (24.8); full footprint from Z -14.3 to
  +14.7 (29.0), cover lips out to Z -15.8 / +15.7.
* Output side: case face at Z ~ +16.2..16.7; Ø20 drive horn from Z +16.2 to +18.7
  (2.5 mm), spline / M3 screw head Ø5.4 to Z +20.2. Horn centre at **(X = +12.5, Y = 0)**,
  i.e. 10.2 mm from the +X end face and centred across the width.
* Rear side: case face at Z ~ -15.6; Ø6 boss to Z -18.3 (coaxial with the output, X = 12.5);
  in the `with_horn` variant the Ø20 x 2.1 mm passive horn sits at Z -15.6 .. -17.7;
  the 5264 connector block extends to Z -19.4 (X -2.6 .. +15.5, Y +/-8.6).
* Overall bbox: 45.4 x 24.8 x 39.6 mm (Z -19.4 .. +20.2).

These numbers match the Feetech/Waveshare drawings to within 0.2 mm (the SO-ARM100 model is
a simplified re-model by TheRobotStudio, not a Feetech-supplied solid).

## Notes on `STS3215_Waveshare_ST3215.step`

* It is an assembly with per-part coordinate systems and ITEM_DEFINED_TRANSFORMATION
  placements; a naive point-cloud bounding box of the file is meaningless. Import it as an
  assembly (or "merge into one body") and re-measure in the CAD tool before trusting a frame.
* Circle radii present in the file confirm the drawing: Ø19.2 (r 9.6) drive horn, Ø6.1
  (r 3.05) rear boss, Ø17.6 / Ø15.8 case bosses, Ø25 / Ø25.6 gear features, M2 / M3 holes.
* The drawing shipped with it is titled "SCS215" (the PWM-era sibling); Feetech's SCS215,
  STS3215 and ST3215 share the identical housing, so the dimensions apply.

## Not obtained

* No Feetech-published STEP/STL exists on feetechrc.com or doc.feetech.cn (checked 2026-09-26).
* GrabCAD "FEETECH_STS3215" and Onshape (Open Duck Mini) models require a login; Printables
  model 1477431 is a community re-model. None were downloaded.
