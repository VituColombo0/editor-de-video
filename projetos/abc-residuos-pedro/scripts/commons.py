# Busca/metadados no Wikimedia Commons. Uso:
#   python3 commons.py search <db.json> <bitmap|video> "consulta" ...
#   python3 commons.py titles <db.json> "File:Nome.jpg" ...
import sys,json,urllib.request,urllib.parse,time,re,os
UA={"User-Agent":"UniversityDocumentaryResearch/1.0 (educational, non-commercial)"}
mode,out=sys.argv[1],sys.argv[2]
db=json.load(open(out)) if os.path.exists(out) else {}
def call(p):
  for a in range(5):
    try: return json.load(urllib.request.urlopen(urllib.request.Request("https://commons.wikimedia.org/w/api.php?"+urllib.parse.urlencode(p),headers=UA)))
    except Exception: time.sleep(8*(a+1))
  return {}
def rec(pg,q=""):
  ii=pg["imageinfo"][0]; m=ii.get("extmetadata",{})
  g=lambda k:re.sub("<[^>]+>","",m.get(k,{}).get("value","") or "").strip()
  return dict(title=pg["title"],url=ii["url"],page=ii["descriptionurl"],thumb=ii.get("thumburl"),w=ii["width"],h=ii["height"],license=g("LicenseShortName"),licurl=g("LicenseUrl"),artist=g("Artist")[:120],credit=g("Credit")[:160],desc=g("ImageDescription")[:300],date=g("DateTimeOriginal")[:40],query=q)
base={"action":"query","format":"json","prop":"imageinfo","iiprop":"url|size|extmetadata|mime","iiurlwidth":"3840"}
if mode=="search":
  ft=sys.argv[3]
  for q in sys.argv[4:]:
    r=call({**base,"generator":"search","gsrsearch":f"{q} filetype:{ft}","gsrnamespace":"6","gsrlimit":"15"})
    print("===",q)
    for pg in sorted(r.get("query",{}).get("pages",{}).values(),key=lambda x:x.get("index",0)):
      x=rec(pg,q); db[x["title"]]=x
      print(f'{x["title"][5:][:70]:70} | {x["w"]}x{x["h"]} | {x["license"]} | {x["artist"][:22]} | {x["desc"][:55]}')
    time.sleep(4)
else:
  for t in sys.argv[3:]:
    r=call({**base,"titles":t})
    for pg in r.get("query",{}).get("pages",{}).values():
      if "imageinfo" in pg: x=rec(pg); db[x["title"]]=x; print(x["title"],x["license"],x["artist"][:40])
      else: print("MISSING",t)
    time.sleep(2)
json.dump(db,open(out,"w"),ensure_ascii=False,indent=1)
