# P1S release checks

Native Bambu Studio 2.8.2.61 export and local slicing completed successfully. **19/19 plates, 94/94 objects, no remaining slicer warnings.** No physical print was started.

The initial full slice flagged a curved TPU rim. Both soles were flipped onto their flat mounting face; plate17 was re-sliced successfully without that warning. The other 18 plates were unchanged. The original and corrected result records are retained, and `release_validation.json` consolidates them.

Checks read the delivered native project back, including all meshes, scale, positions, plate membership and color assignments. Deposited model/support/brim paths, including XY arc extrema and line-width margins, remain within the stock bed and clear of the front cutter area. Vendor start/end purge moves are outside this geometric check. This is not a mechanical load test or physical fit guarantee.

SHA-256: `8624e12624046245f8490b283e31c98fe2edc13964bf31fcd8a3e0a5840e02da`

## Slicer estimates

These use generic filament profiles and include supports/brims. They are estimates; actual spools, calibration and printer overhead change the result. Optional parts are included only in their own total.

| Selection | Filament g | Estimated hours |
|---|---:|---:|
| coupon | 43.1 | 2.42 |
| installed | 1709.2 | 106.96 |
| alternative | 161.0 | 8.73 |

See `slice_estimates.csv` for each plate. Select actual material profiles and inspect Preview before printing. TPU uses the external spool; filament5 is a project role, not an AMS slot.
