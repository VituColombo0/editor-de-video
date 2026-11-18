import json,subprocess,sys
C=json.load(open("vo/cues.json"))
for v,c in C.items():
  ins=[];flt=[]
  for i,s in enumerate(c["starts"],1):
    ins+=["-i",f"vo/trim/{v}_{i:02d}.wav"]; ms=int(s*1000); flt.append(f"[{i-1}]adelay={ms}|{ms}[a{i}]")
  n=len(c["starts"])
  f=";".join(flt)+";"+"".join(f"[a{i}]" for i in range(1,n+1))+f"amix=inputs={n}:normalize=0,apad=whole_dur={c['dur']},atrim=0:{c['dur']}[o]"
  subprocess.run(["ffmpeg","-nostdin","-loglevel","error","-y",*ins,"-filter_complex",f,"-map","[o]","-ar","48000","-ac","2",f"vo/narracao_{v}.wav"],check=True)
  # check overlaps
  for i,s in enumerate(c["starts"],1):
    d=float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f"vo/trim/{v}_{i:02d}.wav"]))
    nxt=c["starts"][i] if i<n else c["dur"]
    print(v,i,s,round(s+d,2),"OK" if s+d<nxt-0.2 else "!! OVERLAP/TIGHT")
