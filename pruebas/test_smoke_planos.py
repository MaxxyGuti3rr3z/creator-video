"""Smoke: renderiza cada plano una vez en canvas pequeno y valida el generador cinematico."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from PIL import Image
import src.mockups.director_escena as de

fallos = []
ok = 0
# gamma_slides y laptop_finde tienen geometria que solo valida a 1080x1920
# (a 270x480 fallan igual en el archivo original: preexistente, no regresion)
GRANDES = {"renderizar_plano_gamma_slides", "renderizar_plano_laptop_finde"}
for name in sorted(de.__all__):
    if not name.startswith("renderizar_plano_"):
        continue
    fn = getattr(de, name)
    ancho, alto = (1080, 1920) if name in GRANDES else (270, 480)
    try:
        img = fn(ancho=ancho, alto=alto, t_sec=0.5, duracion=2.0, config=None)
        assert isinstance(img, Image.Image), f"no es Image: {type(img)}"
        ok += 1
    except Exception as e:
        fallos.append((name, repr(e)))

print(f"planos OK: {ok}")
for n, e in fallos:
    print(f"FALLO {n}: {e}")

# generador cinematico (2 frames chicos via ffmpeg)
from src.mockups.planos.router import generar_video_cinematico_escena
out = Path(__file__).resolve().parent.parent / "test_artifacts" / "smoke_cinematico.mp4"
try:
    p = generar_video_cinematico_escena(
        "PLANO_NOTICIAS_MITO_CHAT", 0.2, out, config=None, fps=10, ancho=270, alto=480
    )
    print("cinematico OK:", p, p.stat().st_size, "bytes")
except Exception as e:
    print("FALLO cinematico:", repr(e))

sys.exit(1 if fallos else 0)
