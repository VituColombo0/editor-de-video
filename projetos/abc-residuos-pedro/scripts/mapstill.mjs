// mapstill.mjs — tira uma foto de satélite (Esri World Imagery) em 3840x2160 (DSF 2)
// e projeta polígonos/pontos para coordenadas CSS 1920x1080 do mesmo enquadramento.
// Uso: node mapstill.mjs <saida-sem-ext> <lng> <lat> <zoom> <poligonos.json> [bearing]
import { writeFileSync, readFileSync } from "node:fs";
const PPT = "/home/vitu/.nvm/versions/node/v22.23.4/lib/node_modules/hyperframes/node_modules/puppeteer-core/lib/puppeteer/puppeteer-core.js";
const { default: puppeteer } = await import(PPT);
const CHROME = "/home/vitu/.cache/hyperframes/chrome/chrome-headless-shell/linux-152.0.7977.30/chrome-headless-shell-linux64/chrome-headless-shell";
const [out, lng, lat, zoom, polyFile, bearing = "0"] = process.argv.slice(2);
const POLYS = JSON.parse(readFileSync(polyFile, "utf8"));
const TILES = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}";
const PAGE = `<!doctype html><html><head>
<link href="https://cdn.jsdelivr.net/npm/maplibre-gl@5.24.0/dist/maplibre-gl.css" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/maplibre-gl@5.24.0/dist/maplibre-gl.js"></script>
<style>*{margin:0}html,body{width:1920px;height:1080px;overflow:hidden}#map{position:absolute;inset:0}.maplibregl-control-container{display:none!important}</style>
</head><body><div id="map"></div><script>
var map=new maplibregl.Map({container:"map",style:{version:8,sources:{s:{type:"raster",tiles:["${TILES}"],tileSize:256,maxzoom:19}},
 layers:[{id:"bg",type:"background",paint:{"background-color":"#05070d"}},{id:"s",type:"raster",source:"s"}]},
 center:[${lng},${lat}],zoom:${zoom},bearing:${bearing},interactive:false,attributionControl:false,fadeDuration:0,preserveDrawingBuffer:true});
window.__ready=new Promise(r=>map.on("load",r));
window.__idle=()=>new Promise(res=>{const t0=performance.now();(function p(){if(map.loaded()&&map.areTilesLoaded()){requestAnimationFrame(()=>requestAnimationFrame(()=>res(true)));return;}
 if(performance.now()-t0>30000){res(false);return;}setTimeout(p,100);})();});
window.__proj=(polys)=>{const o={};for(const [n,rings] of Object.entries(polys)){
 o[n]={d:rings.map(r=>r.map((c,i)=>{const p=map.project(c);return (i?"L":"M")+p.x.toFixed(1)+" "+p.y.toFixed(1);}).join(" ")+"Z").join(" ")};
 let sx=0,sy=0,k=0;for(const r of rings)for(const c of r){const p=map.project(c);sx+=p.x;sy+=p.y;k++;}o[n].cx=+(sx/k).toFixed(1);o[n].cy=+(sy/k).toFixed(1);}
 return o;};
</script></body></html>`;
const b = await puppeteer.launch({ executablePath: CHROME, headless: true,
  args: ["--no-sandbox", "--use-gl=angle", "--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--window-size=1920,1080"] });
const pg = await b.newPage();
await pg.setViewport({ width: 1920, height: 1080, deviceScaleFactor: 2 });
await pg.setContent(PAGE, { waitUntil: "load" });
await pg.evaluate(() => window.__ready);
const ok = await pg.evaluate(() => window.__idle());
await pg.screenshot({ path: out + ".jpg", type: "jpeg", quality: 92 });
const proj = await pg.evaluate((p) => window.__proj(p), POLYS);
writeFileSync(out + ".json", JSON.stringify({ center: [+lng, +lat], zoom: +zoom, tilesComplete: ok, shapes: proj }, null, 1));
console.log(out, "tiles ok:", ok);
await b.close();
