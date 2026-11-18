# Gera a versão SEM NARRAÇÃO: refaz a mistura (trilha + efeitos) a partir do index.html
# e junta com o vídeo já renderizado (vídeo copiado, sem re-encode).
import re,subprocess,sys,os
proj,video,out=sys.argv[1:4]
html=open(os.path.join(proj,"index.html")).read()
root_d=float(re.search(r'id="root"[^>]*data-duration="([\d.]+)"',html).group(1))
ins=[];flt=[];labels=[]
for m in re.finditer(r'<audio ([^>]*)>',html):
    a=dict(re.findall(r'([\w-]+)="([^"]*)"',m.group(1)))
    if a["id"]=="vo": continue
    i=len(ins)//2; ins+=["-i",os.path.join(proj,a["src"])]
    st=float(a["data-start"]); vol=float(a.get("data-volume",1)); f=[]
    if "data-duration" in a: f.append(f"atrim=0:{a['data-duration']}")
    d=float(a.get("data-duration",0)) or None
    if "data-fade-in" in a: f.append(f"afade=t=in:st=0:d={a['data-fade-in']}")
    if "data-fade-out" in a and d: f.append(f"afade=t=out:st={d-float(a['data-fade-out'])}:d={a['data-fade-out']}")
    f+= [f"volume={vol}", f"adelay={int(st*1000)}|{int(st*1000)}"]
    flt.append(f"[{i}:a]aformat=sample_rates=48000:channel_layouts=stereo,"+",".join(f)+f"[a{i}]"); labels.append(f"[a{i}]")
fc=";".join(flt)+";"+"".join(labels)+f"amix=inputs={len(labels)}:normalize=0,atrim=0:{root_d},alimiter=limit=0.89[m]"
subprocess.run(["ffmpeg","-nostdin","-loglevel","error","-y",*ins,"-i",video,"-filter_complex",fc,"-map",f"{len(labels)}:v","-map","[m]","-c:v","copy","-c:a","aac","-b:a","256k","-shortest",out],check=True)
print("ok",out)
