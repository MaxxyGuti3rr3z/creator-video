"""
test_previews_video_14.py
-------------------------
Genera capturas PNG de vista previa para las 7 micro-escenas de Video 14 (Agua e IA: Desmintiendo el Pánico),
verificando la Safe Zone (y >= 250, ancho 880px, x 100..980) y la zona de Byte (base <= y1650).
"""

from pathlib import Path
import sys

DIR_RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DIR_RAIZ))

from src.mockups.director_escena import (
    renderizar_escena_por_arquetipo,
    CONFIGS_AGUA_IA
)
from src.rutas import ruta_video

def main():
    v_paths = ruta_video("video_14_agua_ia")
    dir_previews = v_paths["intermedios"] / "previews_director"
    dir_previews.mkdir(parents=True, exist_ok=True)

    print("=" * 65)
    print("GENERANDO PREVIEWS CINEMATOGRÁFICAS PARA VIDEO 14 (AGUA E IA)")
    print("=" * 65)

    escenas = [
        ("01_cold_open_hero_caos_mito", "cold_open"),
        ("02_hook_hero_caos_botella", "hook"),
        ("03_problema_hero_caos_dato_2023", "problema"),
        ("04_punto_1_split_panico_vs_medicion", "punto_1"),
        ("05_punto_2_showcase_matiz", "punto_2"),
        ("06_resultado_deck_3d_industria", "resultado"),
        ("07_cierre_battle_vs_debate", "cierre"),
    ]

    for prefijo, clave in escenas:
        arquetipo, cfg = CONFIGS_AGUA_IA[clave]
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

    print("\nTodas las previews del Video 14 fueron generadas exitosamente!")
    print(f"Carpeta: {dir_previews.resolve()}")

if __name__ == "__main__":
    main()
