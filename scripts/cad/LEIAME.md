# Converter CAD (STEP) para o vídeo

Ambiente: `uv venv ~/.local/share/step-venv && uv pip install --python ~/.local/share/step-venv/bin/python gmsh trimesh numpy fast-simplification`
(rode os scripts com `python -I` e fora da pasta deles).

1. `step_para_glb.py arquivo.step bruto.glb` — malha o STEP (mm → m) com gmsh, agrupando peças (arco / pilares / suportes; parafusos ignorados). ~7 min, ~1,3 GB RAM.
2. `reduzir_malha.py bruto.glb lite.glb` — reduz para ~145 mil triângulos.
3. `glb_para_js.py lite.glb projetos/<nome>/assets/lib/arco-scanner.js` — gera `window.ARCO_SCANNER` (base64) para carregar no Three.js sem fetch.
