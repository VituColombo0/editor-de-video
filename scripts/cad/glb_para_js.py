import trimesh, sys, base64, numpy as np, json
sc=trimesh.load(sys.argv[1]); out={}
for name,g in sc.geometry.items():
    v=np.asarray(g.vertices,dtype=np.float32); f=np.asarray(g.faces)
    it=np.uint16 if len(v)<65536 else np.uint32
    out[name]={"p":base64.b64encode(v.tobytes()).decode(),"i":base64.b64encode(f.astype(it).tobytes()).decode(),"w":32 if it==np.uint32 else 16}
    print(name,len(v),len(f),it.__name__)
open(sys.argv[2],"w").write("window.ARCO_SCANNER="+json.dumps(out)+";\n")
