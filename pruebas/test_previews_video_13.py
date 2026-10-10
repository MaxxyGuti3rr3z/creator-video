"""
test_previews_video_13.py
-------------------------
Genera capturas PNG de vista previa para las 7 micro-escenas de Video 13 (Portal de Noticias de IA - Qué Hace Realmente la IA),
verificando la Safe Zone (y >= 250, ancho 880px) y la regla de asimilación visual en 1 segundo.
"""

from pathlib import Path
import sys

DIR_RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DIR_RAIZ))

from src.mockups.director_escena import (
    renderizar_escena_por_arquetipo,
    CONFIGS_NOTICIAS_IA_REALIDAD
)
from src.rutas import ruta_video

def main():
    v_paths = ruta_video("video_13_noticias_ia_realidad")
    dir_previews = v_paths["intermedios"] / "previews_director"
    dir_previews.mkdir(parents=True, exist_ok=True)

    print("=" * 65)
    print("GENERANDO PREVIEWS CINEMATOGRÁFICAS PARA VIDEO 13 (NOTICIAS IA)")
    print("=" * 65)

    escenas = [
        ("01_cold_open_noticias_mito_chat", "cold_open"),
        ("02_hook_noticias_breaking_impacto", "hook"),
        ("03_problema_noticias_transformacion_silenciosa", "problema"),
        ("04_punto_1_noticias_medicina_diagnostico", "punto_1"),
        ("05_punto_2_noticias_ciencia_clima_materiales", "punto_2"),
        ("06_resultado_noticias_aceleracion_editorial", "resultado"),
        ("07_cierre_noticias_cierre_encuesta_futuro", "cierre"),
    ]

    for prefijo, clave in escenas:
        arquetipo, cfg = CONFIGS_NOTICIAS_IA_REALIDAD[clave]
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

    print("\nTodas las previews del Video 13 fueron generadas exitosamente!")
    print(f"Carpeta: {dir_previews.resolve()}")

if __name__ == "__main__":
    main()
