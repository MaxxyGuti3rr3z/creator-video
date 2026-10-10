from pathlib import Path
import re

p = Path("src/mockups/director_escena.py")
text = p.read_text(encoding="utf-8")

pos_v12 = text.find("def renderizar_plano_google_ads_busqueda_trampa")
pos_end = text.find("CONFIGS_CIBERSEGURIDAD_GOOGLE_ADS")
v12_code = text[pos_v12:pos_end]

simbolos = ["✓", "❌", "⚠️", "🛡️", "🔍", "🚨", "👀", "😱", "🤯", "👇", "💳", "↑", "↓", "<-"]
encontrados = []
for i, line in enumerate(v12_code.splitlines()):
    if "draw.text" in line:
        for s in simbolos:
            if s in line:
                encontrados.append((i, s, line.strip()))

print(f"Total encontrados: {len(encontrados)}")
for idx, s, l in encontrados:
    print(f"[{s}] {l}")
