import json,subprocess,re,textwrap
F=json.load(open("vo/falas.json")); C=json.load(open("vo/cues.json"))
NAMES={"v1":"PEDRO_01_INFRAESTRUTURA_LIMPEZA_URBANA","v2":"PEDRO_02_MATERIAS_PRIMAS_SECUNDARIAS","v3":"PEDRO_03_SMART_CITIES_RESIDUOS"}
def ts(t):
    h=int(t//3600); m=int(t%3600//60); s=t%60
    return f"{h:02d}:{m:02d}:{int(s):02d},{int(round((s-int(s))*1000)):03d}"
def dur(v,i): return float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f"vo/trim/{v}_{i:02d}.wav"]))
def chunks(t):
    # quebra em pedaços de até ~84 caracteres em vírgulas/dois-pontos/espaços
    if len(t)<=84: return [t]
    parts=re.split(r"(?<=[,:;])\s+",t); out=[]; cur=""
    for p in parts:
        if len(cur)+len(p)+1<=84: cur=(cur+" "+p).strip()
        else:
            if cur: out.append(cur)
            while len(p)>84:
                cut=p.rfind(" ",0,84); out.append(p[:cut]); p=p[cut+1:]
            cur=p
    if cur: out.append(cur)
    return out
for v,lines in F.items():
    n=1; srt=[]
    for i,(t,s) in enumerate(zip(lines,C[v]["starts"]),1):
        d=dur(v,i); cs=chunks(t); tot=sum(len(c) for c in cs); a=s
        for c in cs:
            b=a+d*len(c)/tot
            srt.append(f"{n}\n{ts(a)} --> {ts(b)}\n"+"\n".join(textwrap.wrap(c,42))+"\n"); n+=1; a=b
    open(f"entregas/{NAMES[v]}.srt","w").write("\n".join(srt))
    print(v,n-1,"legendas")
