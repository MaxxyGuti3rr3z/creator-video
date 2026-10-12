"""
src.mockups
-----------
Motor unificado de renderizado de mockups y plantillas para 'Byte el Zorrito'.
"""

from .motor import (
    dibujar_ventana_base,
    evaluar_etapa_visual,
    generar_fondo_tech_base,
    generar_video_interactivo,
    generar_frame_completo_escena,
    renderizar_mockup_por_nombre,
    generar_video_interactivo_tareas,
    generar_video_interactivo_reunion,
    generar_video_interactivo_correo,
    generar_video_interactivo_presentaciones,
    PALETAS_EMOCIONALES,
    obtener_fuente,
)
from .director_escena import (
    renderizar_escena_por_arquetipo,
    generar_video_cinematico_escena,
    generar_video_interactivo_atencion_clientes,
    generar_video_interactivo_excel_reportes,
    generar_video_interactivo_busqueda_investigacion,
    generar_video_interactivo_diseno_flyers,
    generar_video_interactivo_cotizacion_automatica,
    generar_video_interactivo_cincuenta_archivos,
    generar_video_interactivo_ciberseguridad_google_ads,
    generar_video_interactivo_noticias_ia_realidad,
    generar_video_interactivo_agua_ia,
)
from .plantillas import PLANTILLAS, ALIAS_ESCENAS, obtener_plantilla

__all__ = [
    "dibujar_ventana_base",
    "evaluar_etapa_visual",
    "generar_fondo_tech_base",
    "generar_video_interactivo",
    "generar_frame_completo_escena",
    "renderizar_mockup_por_nombre",
    "generar_video_interactivo_tareas",
    "generar_video_interactivo_reunion",
    "generar_video_interactivo_correo",
    "generar_video_interactivo_presentaciones",
    "generar_video_interactivo_atencion_clientes",
    "generar_video_interactivo_excel_reportes",
    "generar_video_interactivo_busqueda_investigacion",
    "generar_video_interactivo_diseno_flyers",
    "generar_video_interactivo_cotizacion_automatica",
    "generar_video_interactivo_cincuenta_archivos",
    "generar_video_interactivo_ciberseguridad_google_ads",
    "generar_video_interactivo_noticias_ia_realidad",
    "generar_video_interactivo_agua_ia",
    "generar_video_cinematico_escena",
    "renderizar_escena_por_arquetipo",
    "PALETAS_EMOCIONALES",
    "obtener_fuente",
    "PLANTILLAS",
    "ALIAS_ESCENAS",
    "obtener_plantilla",
]

