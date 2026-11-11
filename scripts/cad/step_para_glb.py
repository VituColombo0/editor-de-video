import gmsh, sys, numpy as np, trimesh
gmsh.initialize(); gmsh.option.setNumber("General.Terminal",0)
gmsh.option.setNumber("Mesh.MeshSizeMax", 40)
gmsh.option.setNumber("Mesh.MeshSizeMin", 2)
gmsh.option.setNumber("Mesh.MeshSizeFromCurvature", 12)
gmsh.option.setNumber("Mesh.Algorithm", 6)
gmsh.model.occ.importShapes(sys.argv[1]); gmsh.model.occ.synchronize()
gmsh.model.mesh.generate(2)
def group(t):
    if 7<=t<=18: return None
    if 3<=t<=6: return "pilares"
    if t in (1,2): return "suportes"
    return "arco"
parts={}
for d,t in gmsh.model.getEntities(3):
    g=group(t)
    if g is None: continue
    _,surfs=gmsh.model.getAdjacencies(3,t)
    for s in surfs:
        types,_,nodes=gmsh.model.mesh.getElements(2,s)
        for ty,nd in zip(types,nodes):
            if ty!=2: continue
            parts.setdefault(g,[]).append(np.array(nd,dtype=np.int64).reshape(-1,3))
tags,coords,_=gmsh.model.mesh.getNodes()
idx={int(t):i for i,t in enumerate(tags)}; P=coords.reshape(-1,3)/1000.0
scene=trimesh.Scene()
for g,lst in parts.items():
    F=np.vstack(lst); F=np.vectorize(idx.get)(F)
    m=trimesh.Trimesh(P,F,process=True); m.remove_unreferenced_vertices(); m.merge_vertices()
    print(g,len(m.faces))
    scene.add_geometry(m,node_name=g,geom_name=g)
scene.export(sys.argv[2])
