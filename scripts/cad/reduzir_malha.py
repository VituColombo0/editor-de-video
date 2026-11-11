import trimesh, sys, numpy as np
sc=trimesh.load(sys.argv[1]); out=trimesh.Scene()
tgt={"arco":90000,"pilares":45000,"suportes":10000}
for name,g in sc.geometry.items():
    m=g.simplify_quadric_decimation(face_count=tgt.get(name,20000))
    m.fix_normals() if False else None
    print(name,len(g.faces),"->",len(m.faces), m.bounds.round(3).tolist())
    out.add_geometry(m,node_name=name,geom_name=name)
out.export(sys.argv[2])
