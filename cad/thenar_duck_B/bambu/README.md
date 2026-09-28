# P1S printing package

Open **Thenar_Duck_B_P1S_ALL_PARTS.3mf** as a Bambu Studio project. Keep the named plates, full-size models and object colors. The project targets P1S / 0.4 mm / Textured PEI and uses generic PETG/TPU presets; select the actual spool and plate profiles and re-slice before printing.

- **19 plates / 94 objects:** 79 installed pieces, 6 fit coupons, 9 optional replacements.
- **Plate 1:** fit tests; establish insert, bearing and servo fit first.
- **Plates 2–15:** structural PETG, white/dark grey/blue.
- **Plate 16:** translucent PETG diffusers and lightpipe.
- **Plate 17:** black TPU soles, **external spool, AMS disabled for this job**.
- **Plates 18–19:** optional switch lids and eye-sleeve pairs. Select only the needed replacement; disable its default counterpart.

Map virtual filaments 1–4 to the actual AMS slots for the PETG plates. Filament 5 is the TPU role, not an AMS slot. Each plate is one color/material. No mid-layer color changes or prime tower are required by the delivered arrangement.

Read the [complete build guide](../../../README.md), [plate overview](plate_overview.png), [per-object inventory](plate_manifest.csv), [slice estimates](slice_estimates.csv) and [release checks](RELEASE_CHECKS.md).

The primary `.3mf` is the native Bambu Studio export. The `_source.3mf` and resolved JSON are regeneration inputs; `sample/` and `validation/` hold development evidence. The temporary validation G-code is not the print deliverable. The project contains printed pieces only; use the separate GLB/STEP/SolidWorks files to review the assembled robot and hardware.

First printing and physical fit checks remain necessary. No print was sent to a printer.
