"""
test_previews_video_15.py
-------------------------
Genera capturas PNG de vista previa para las 7 micro-escenas de Video 15 (IA en tu celular),
verificando la Safe Zone (y >= 250, ancho 880px, x 100..980) y la zona de Byte (base <= y1650).
"""

from pathlib import Path
import sys

DIR_RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DIR_RAIZ))

from src.mockups.director_escena import (
    renderizar_escena_por_arquetipo,
    CONFIGS_CELULAR_IA
)
from src.rutas import ruta_video

def main():
    v_paths = ruta_video("video_15_ia_celular")
    dir_previews = v_paths["intermedios"] / "previews_director"
    dir_previews.mkdir(parents=True, exist_ok=True)

    print("=" * 65)
    print("GENERANDO PREVIEWS CINEMATOGRÁFICAS PARA VIDEO 15 (IA EN TU CELULAR)")
    print("=" * 65)

    escenas = [
        ("01_cold_open_celu_popup_sospecha", "cold_open"),
        ("02_hook_celu_popup_sospecha", "hook"),
        ("03_problema_wake_word", "problema"),
        ("04_punto_1_circle_to_search", "punto_1"),
        ("05_punto_2_ios_resumen_notif", "punto_2"),
        ("06_resultado_celu_primero_nube", "resultado"),
        ("07_cierre_cierre_rara_frase", "cierre"),
    ]

    for prefijo, clave in escenas:
        arquetipo, cfg = CONFIGS_CELULAR_IA[clave]
        print(f"Renderizando '{prefijo}' -> [{arquetipo}]...")
        img = renderizar_escena_por_arquetipo(
            arquetipo=arquetipo,
            ancho=1080,
            alto=1920,
            t_sec=1.5,
            duracion=4.0,
            config=cfg
        )
        ruta_out = dir_previews / f"{prefijo}.png"
        img.save(ruta_out, "PNG")
        print(f"  [OK] Guardado en: {ruta_out.name}")

    print("\nTodas las previews del Video 15 fueron generadas exitosamente!")
    print(f"Carpeta: {dir_previews.resolve()}")

if __name__ == "__main__":
    main()
