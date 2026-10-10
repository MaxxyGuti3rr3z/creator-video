"""
pruebas/comparar_mockups_video_03.py
------------------------------------
Renderiza los 5 frames de prueba para el Video 3 utilizando el nuevo motor unificado
en src/mockups/motor.py y las plantillas en src/mockups/plantillas/.
Guarda las imágenes en videos/video_03_tareas/intermedios/preview_frames_nuevo/
para verificación de calidad, fidelidad y retrocompatibilidad.
"""

import sys
from pathlib import Path

# Asegurar raíz en PYTHONPATH
raiz_proyecto = Path(__file__).resolve().parent.parent
if str(raiz_proyecto) not in sys.path:
    sys.path.insert(0, str(raiz_proyecto))

from src.mockups.motor import (
    renderizar_mockup_por_nombre,
    generar_frame_completo_escena
)
from src.rutas import (
    DIR_VIDEOS,
    DIR_ASSETS
)

DIR_BYTE = DIR_ASSETS / "byte" / "transparentes"
DIR_SALIDA = DIR_VIDEOS / "video_03_tareas" / "intermedios" / "preview_frames_nuevo"
DIR_SALIDA.mkdir(parents=True, exist_ok=True)

ESCENAS_CONFIG = [
    {
        "nombre_archivo": "frame_1_escena_problema.png",
        "tipo_escena": "escena_problema",
        "plantilla": "tareas_problema",
        "subtitulo": "¿Tu lista de tareas es un caos infinito?",
        "sprite_byte": DIR_BYTE / "escena_problema_guion_03_transparente.png",
        "progreso": 0.5,
        "tiempo": 2.5
    },
    {
        "nombre_archivo": "frame_2_punto_1.png",
        "tipo_escena": "punto_1",
        "plantilla": "tareas_todoist",
        "subtitulo": "Con Todoist ordenás por prioridad",
        "sprite_byte": DIR_BYTE / "punto_1_guion_03_transparente.png",
        "progreso": 0.5,
        "tiempo": 2.5
    },
    {
        "nombre_archivo": "frame_3_punto_2.png",
        "tipo_escena": "punto_2",
        "plantilla": "tareas_calendario",
        "subtitulo": "Con Motion se agenda automáticamente",
        "sprite_byte": DIR_BYTE / "punto_2_guion_03_transparente.png",
        "progreso": 0.5,
        "tiempo": 2.5
    },
    {
        "nombre_archivo": "frame_4_resultado.png",
        "tipo_escena": "resultado",
        "plantilla": "tareas_resultado",
        "subtitulo": "Vas completando todo paso a paso",
        "sprite_byte": DIR_BYTE / "resultado_guion_03_transparente.png",
        "progreso": 1.0,
        "tiempo": 5.0
    },
    {
        "nombre_archivo": "frame_5_cierre.png",
        "tipo_escena": "cierre",
        "plantilla": "tareas_cierre",
        "subtitulo": "¿Qué app usás hoy para organizarte?",
        "sprite_byte": DIR_BYTE / "cierre_guion_03_transparente.png",
        "progreso": 1.0,
        "tiempo": 5.0
    }
]

def main():
    print(f"=== Renderizando 5 frames de muestra con el motor unificado ===")
    for conf in ESCENAS_CONFIG:
        mockup = renderizar_mockup_por_nombre(
            conf["plantilla"],
            ancho=940,
            alto=560,
            progreso=conf["progreso"],
            tiempo_segundos=conf["tiempo"],
            tipo_mockup="ilustrativo"
        )
        ruta_out = DIR_SALIDA / conf["nombre_archivo"]
        generar_frame_completo_escena(
            tipo_escena=conf["tipo_escena"],
            mockup_img=mockup,
            ruta_byte_transparente=conf["sprite_byte"],
            texto_subtitulo=conf["subtitulo"],
            ruta_salida=ruta_out
        )
    print("\n[OK] Todos los frames nuevos generados exitosamente.")

if __name__ == "__main__":
    main()
