"""
test_previews_video_10.py
-------------------------
Genera capturas PNG de vista previa para las 7 micro-escenas de Video 10 (Cotización Automática de Pedidos),
verificando la jerarquía de 4 zonas y la asimilación visual en 1 segundo.
"""

from pathlib import Path
import sys

DIR_RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(DIR_RAIZ))

from src.mockups.director_escena import (
    renderizar_escena_por_arquetipo,
    CONFIGS_COTIZACION_AUTOMATICA
)
from src.rutas import ruta_video

def main():
    v_paths = ruta_video("video_10_cotizacion_automatica")
    dir_previews = v_paths["intermedios"] / "previews_director"
    dir_previews.mkdir(parents=True, exist_ok=True)

    print("=" * 65)
    print("GENERANDO PREVIEWS CINEMATOGRÁFICAS PARA VIDEO 10 (COTIZACIÓN AUTOMÁTICA)")
    print("=" * 65)

    escenas = [
        ("01_cold_open_whatsapp_cliente", "cold_open"),
        ("02_hook_no_calcular_a_mano", "hook"),
        ("03_problema_pase_ia", "problema"),
        ("04_punto_1_extraccion_datos", "punto_1"),
        ("05_punto_2_presupuesto_ordenado", "punto_2"),
        ("06_resultado_cotizacion_formal", "resultado"),
        ("07_cierre_pregunta_comunidad", "cierre"),
    ]

    for prefijo, clave in escenas:
        arquetipo, cfg = CONFIGS_COTIZACION_AUTOMATICA[clave]
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

    print("\nTodas las previews del Video 10 fueron generadas exitosamente!")
    print(f"Carpeta: {dir_previews.resolve()}")

if __name__ == "__main__":
    main()
