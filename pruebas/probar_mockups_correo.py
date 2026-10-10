"""
pruebas/probar_mockups_correo.py
--------------------------------
Genera frames de previsualización para las dos nuevas plantillas de correo (Video 4):
1. correo_hilo_resumen
2. correo_chat_generico
"""

import sys
from pathlib import Path

raiz_proyecto = Path(__file__).resolve().parent.parent
if str(raiz_proyecto) not in sys.path:
    sys.path.insert(0, str(raiz_proyecto))

from src.mockups.motor import (
    renderizar_mockup_por_nombre,
    generar_frame_completo_escena
)
from src.rutas import DIR_VIDEOS, DIR_ASSETS

DIR_BYTE = DIR_ASSETS / "byte" / "transparentes"
DIR_SALIDA = DIR_VIDEOS / "video_04_correo" / "intermedios" / "preview_frames"
DIR_SALIDA.mkdir(parents=True, exist_ok=True)

def main():
    print("=== Probando nuevas plantillas de Video 4 (correo) ===")
    
    # 1. Hilo de correo con resumen y panel borrador (etapa 2 para ver todo desplegado)
    m_hilo = renderizar_mockup_por_nombre(
        "correo_hilo_resumen",
        ancho=940,
        alto=560,
        progreso=0.9,
        tiempo_segundos=5.5,
        tipo_mockup="ilustrativo"
    )
    p_hilo = DIR_SALIDA / "preview_correo_hilo_resumen.png"
    generar_frame_completo_escena(
        tipo_escena="punto_1",
        mockup_img=m_hilo,
        ruta_byte_transparente=DIR_BYTE / "punto_1_guion_03_transparente.png",
        texto_subtitulo="Resumí hilos largos en un segundo",
        ruta_salida=p_hilo
    )

    # 2. Chat genérico sin marcas de terceros
    m_chat = renderizar_mockup_por_nombre(
        "correo_chat_generico",
        ancho=940,
        alto=560,
        progreso=0.9,
        tiempo_segundos=5.5,
        tipo_mockup="ilustrativo"
    )
    p_chat = DIR_SALIDA / "preview_correo_chat_generico.png"
    generar_frame_completo_escena(
        tipo_escena="punto_2",
        mockup_img=m_chat,
        ruta_byte_transparente=DIR_BYTE / "punto_2_guion_03_transparente.png",
        texto_subtitulo="Pegá el mail y pedí tu borrador listo",
        ruta_salida=p_chat
    )

    print("[OK] Previews de correo generados con éxito en:", DIR_SALIDA)

if __name__ == "__main__":
    main()
