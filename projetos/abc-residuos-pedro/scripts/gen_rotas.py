import math
N=[(225,120,30),(525,120,82),(825,120,45),(1125,120,90),(1425,270,25),(1125,420,70),(825,420,20),(525,420,88),(225,420,35),(225,720,76),(525,720,40),(825,720,85),(1125,720,15),(1425,720,72)]
D=(75,570)
def manh(pts):
    out=[pts[0]]
    for a,b in zip(pts,pts[1:]):
        if a[0]!=b[0] and a[1]!=b[1]: out.append((b[0],a[1]))
        out.append(b)
    return out
fixed=[D,N[8][:2],N[0][:2],N[1][:2],N[2][:2],N[3][:2],N[4][:2],N[5][:2],N[6][:2],N[7][:2],N[10][:2],N[9][:2],(225,720),N[11][:2],N[12][:2],N[13][:2],(1425,870),(75,870),D]
# fixed: depois do 9 (225,720) segue 10 (525,720) etc. reorganiza ordem serpenteando
fixed=[D,(225,570),N[8][:2],N[0][:2],N[1][:2],N[2][:2],N[3][:2],N[4][:2],N[5][:2],N[6][:2],N[7][:2],(525,570),(225,570),N[9][:2],N[10][:2],N[11][:2],N[12][:2],N[13][:2],(1425,870),(75,870),D]
data=[D,(525,570),N[7][:2],N[1][:2],N[3][:2],N[5][:2],(1425,420),N[13][:2],N[11][:2],N[9][:2],(75,720),D]
F=manh(fixed); G=manh(data)
def path(p): return "M"+" L".join(f"{x} {y}" for x,y in p)
def keys(p,total):
    L=[math.dist(a,b) for a,b in zip(p,p[1:])]; S=sum(L)
    return ",".join(f'{{x:{b[0]-p[0][0]},y:{b[1]-p[0][1]},duration:{total*l/S:.3f}}}' for (a,b),l in zip(zip(p,p[1:]),L) if l>0), S
kf,sf=keys(F,4.2); kg,sg=keys(G,3.6)
col=lambda f:"#43e3b0" if f<40 else ("#ffb547" if f<70 else "#ff6b5a")
nodes="".join(f'<div class="cn {"hi" if f>=70 else "lo"}" id="rt-n{i}" style="left:{x}px;top:{y}px;--c:{col(f)}"><span>{f}%</span></div>' for i,(x,y,f) in enumerate(N))
streets="".join(f'<line x1="{x}" y1="40" x2="{x}" y2="900"/>' for x in range(75,1500,150))+"".join(f'<line x1="20" y1="{y}" x2="1480" y2="{y}"/>' for y in range(120,900,150))
t=open("/home/vitu/Claude/EditorDeVideo/projetos/abc-residuos-pedro/scripts/tpl_rotas.html").read()
for k,v in {"__STREETS__":streets,"__NODES__":nodes,"__PF__":path(F),"__PG__":path(G),"__KF__":kf,"__KG__":kg,"__DX__":str(D[0]),"__DY__":str(D[1]),"__NF__":str(len(N)),"__NG__":str(sum(1 for n in N if n[2]>=70))}.items(): t=t.replace(k,v)
open("/home/vitu/Claude/EditorDeVideo/projetos/abc-residuos-pedro/pedro-03/compositions/rotas.html","w").write(t)
print(round(sf),round(sg))
