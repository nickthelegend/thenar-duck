import build_duck_B as b
b.eyes(False);b.base_and_sides();b.chest_lights();b.a.coupons()
for p in b.parts:
 try:
  m,fix=b.prepare_mesh(p['mesh']);print(p['name'],m.is_watertight,round(m.volume,2),flush=True)
 except Exception as e:print('FAILED',p['name'],e,flush=True);raise
