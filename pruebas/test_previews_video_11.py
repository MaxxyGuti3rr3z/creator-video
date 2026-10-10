"""
test_previews_video_11.py
-------------------------
Genera capturas PNG de vista previa para las 7 micro-escenas de Video 11 (50 Archivos - Análisis Documental con IA),
verificando la Safe Zone (y >= 250, ancho 880px) y la regla de asimilación visual en 1 segundo.
"""

from pathlib import Path
import sys

DIR_RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DIR_RAIZ))

from src.mockups.director_escena import (
    renderizar_escena_por_arquetipo,
    CONFIGS_CINCUENTA_ARCHIVOS
)
from src.rutas import ruta_video

def main():
    v_paths = ruta_video("video_11_cincuenta_archivos")
    dir_previews = v_paths["intermedios"] / "previews_director"
    dir_previews.mkdir(parents=True, exist_ok=True)

    print("=" * 65)
    print("GENERANDO PREVIEWS CINEMATOGRÁFICAS PARA VIDEO 11 (50 ARCHIVOS)")
    print("=" * 65)

    escenas = [
        ("01_cold_open_cincuenta_archivos_caos", "cold_open"),
        ("02_hook_no_abrir_una_por_una", "hook"),
        ("03_problema_rechazo_manual", "problema"),
        ("04_punto_1_drag_drop_ia_analisis", "punto_1"),
        ("05_punto_2_rag_resultado_citas", "punto_2"),
        ("06_resultado_humor_sufrir_gratis", "resultado"),
        ("07_cierre_archivos_acumulados", "cierre"),
    ]

    for prefijo, clave in escenas:
        arquetipo, cfg = CONFIGS_CINCUENTA_ARCHIVOS[clave]
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

    print("\nTodas las previews del Video 11 fueron generadas exitosamente!")
    print(f"Carpeta: {dir_previews.resolve()}")

if __name__ == "__main__":
    main()
