import json, math
def proj(lon,lat,clon,clat,z):
    W=512*2**z
    f=lambda lo,la:((lo+180)/360*W,(1-math.log(math.tan(math.radians(la))+1/math.cos(math.radians(la)))/math.pi)/2*W)
    x,y=f(lon,lat); cx,cy=f(clon,clat); return round(x-cx+960,1),round(y-cy+540,1)
R=json.load(open("assets/mapas/abc-regiao.json")); SA=json.load(open("assets/mapas/sa-aterro.json")); LA=json.load(open("assets/mapas/lara.json"))
cities=["São Caetano do Sul","Diadema","São Bernardo do Campo","Santo André","Mauá","Ribeirão Pires","Rio Grande da Serra"]
lab={"São Caetano do Sul":(-46.572,-23.617),"Diadema":(-46.625,-23.684),"São Bernardo do Campo":(-46.57,-23.725),"Santo André":(-46.53,-23.655),"Mauá":(-46.455,-23.664),"Ribeirão Pires":(-46.408,-23.713),"Rio Grande da Serra":(-46.397,-23.748)}
c=R["center"]; z=R["zoom"]
paths="".join(f'<path class="mp-city" id="mp-c{i}" d="{R["shapes"][n]["d"]}" pathLength="100"/>' for i,n in enumerate(cities))
hi="".join(f'<path class="mp-hi" id="mp-h{i}" d="{R["shapes"][n]["d"]}"/>' for i,n in enumerate(["Santo André","Mauá"]))
labels=""
for i,n in enumerate(cities):
    x,y=proj(*lab[n],c[0],c[1],z); labels+=f'<div class="mp-lab" id="mp-l{i}" style="left:{x}px;top:{y}px">{n}</div>'
pa=R["shapes"]["Aterro Sanitário de Santo André"]; pl=R["shapes"]["Lara Central de Tratamento de Resíduos"]
html=open("scripts/tpl_mapa_v1.html").read()
for k,v in {"__PATHS__":paths,"__HI__":hi,"__LABELS__":labels,"__PAX__":str(pa["cx"]),"__PAY__":str(pa["cy"]),"__PLX__":str(pl["cx"]),"__PLY__":str(pl["cy"]),
 "__SA_D__":SA["shapes"]["Aterro Sanitário de Santo André"]["d"],"__LA_D__":LA["shapes"]["Lara Central de Tratamento de Resíduos"]["d"]}.items(): html=html.replace(k,v)
open("pedro-01/compositions/mapa.html","w").write(html)
print("ok", proj(-46.4852,-23.6807,c[0],c[1],z), pa["cx"],pa["cy"])
