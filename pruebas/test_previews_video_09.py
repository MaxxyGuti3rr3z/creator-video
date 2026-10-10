"""
test_previews_video_09.py
-------------------------
Genera previews en PNG de los arquetipos cinematográficos para el Guion 09 (Diseño de Flyers: Canva y Remove.bg).
Permite verificar la composición visual, legibilidad en 1 segundo y zonas verticales antes de renderizar el video completo.
"""

import sys
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass
from pathlib import Path
DIR_RAIZ = Path(__file__).resolve().parent.parent
if str(DIR_RAIZ) not in sys.path:
    sys.path.insert(0, str(DIR_RAIZ))

from PIL import Image
from src.rutas import DIR_VIDEOS, DIR_BYTE_TRANSPARENTES
from src.mockups.director_escena import (
    renderizar_escena_por_arquetipo,
    CONFIGS_DISENO_FLYERS
)

DIR_OUT = DIR_VIDEOS / "video_09_diseno_flyers" / "intermedios" / "previews_director"
DIR_OUT.mkdir(parents=True, exist_ok=True)

ESCENAS = [
    ("01_cold_open_chat", "cold_open", 1.0, 2.5),
    ("02_hook_ps_freeze", "hook", 1.0, 2.5),
    ("03_problema_lienzo_blanco", "problema", 1.0, 3.0),
    ("04_punto_1_canva", "punto_1", 2.0, 5.0),
    ("05_punto_2_removebg_laser", "punto_2", 2.0, 4.5),
    ("06_resultado_smartphone_feed", "resultado", 2.0, 4.8),
    ("07_cierre_debate_vs", "cierre", 2.0, 4.5),
]

def main():
    print(f"=== GENERANDO PREVIEWS PARA VIDEO 09 (DISEÑO FLYERS) ===")
    for nombre_archivo, clave_cfg, t_sec, duracion in ESCENAS:
        arquetipo, cfg = CONFIGS_DISENO_FLYERS[clave_cfg]
        print(f"Renderizando {nombre_archivo} ({arquetipo})...")
        img = renderizar_escena_por_arquetipo(
            arquetipo=arquetipo,
            ancho=1080,
            alto=1920,
            t_sec=t_sec,
            duracion=duracion,
            config=cfg
        )
        p_salida = DIR_OUT / f"{nombre_archivo}.png"
        img.save(p_salida, format="PNG")
        print(f"  -> Guardado: {p_salida}")

    print("\nPreviews completados con éxito.")

if __name__ == "__main__":
    main()
