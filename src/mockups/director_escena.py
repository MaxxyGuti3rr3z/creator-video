"""
director_escena.py
------------------
Fachada del Director de Escena para 'Byte el Zorrito'.

El codigo vive ahora en src/mockups/planos/:
  comunes, arquetipos, video_07_excel, video_08_busqueda,
  pestanias_navegador, video_09_flyers, video_10_cotizacion,
  video_11_archivos, video_12_ciberseguridad, video_13_noticias,
  router (MAPA_ARQUETIPOS + cinematico) y wrappers (videos 06-13).
Este modulo solo reexporta todo para mantener la API publica estable.
"""

from src.mockups.planos.comunes import (
    dibujar_icono_alerta,
    dibujar_icono_cruz,
    dibujar_icono_candado,
    dibujar_icono_lupa,
)
from src.mockups.planos.arquetipos import (
    renderizar_plano_hero_caos,
    renderizar_plano_showcase_panoramico,
    renderizar_plano_split_before_after,
    renderizar_plano_deck_3d,
    renderizar_plano_host_community,
    renderizar_plano_panico_reloj,
)
from src.mockups.planos.video_07_excel import (
    renderizar_plano_julius_dashboard,
    renderizar_plano_gamma_slides,
    renderizar_plano_laptop_finde,
)
from src.mockups.planos.video_08_busqueda import (
    renderizar_plano_perplexity_search,
    renderizar_plano_notebooklm_docs,
)
from src.mockups.planos.pestanias_navegador import (
    renderizar_plano_browser_tabs_caos,
    renderizar_plano_single_tab_zen,
    renderizar_plano_battle_vs,
)
from src.mockups.planos.video_09_flyers import (
    renderizar_plano_flyer_paint_caos,
    renderizar_plano_canva_magic_design,
    renderizar_plano_remove_bg,
    renderizar_plano_flyer_showcase_zen,
    renderizar_plano_chat_flyer_urgente,
    renderizar_plano_photoshop_freeze,
    renderizar_plano_lienzo_blanco_bloqueo,
    renderizar_plano_remove_bg_laser,
    renderizar_plano_smartphone_instagram_feed,
)
from src.mockups.planos.video_10_cotizacion import (
    renderizar_plano_whatsapp_pedido_remeras,
    renderizar_plano_byte_pase_ia,
    renderizar_plano_tabla_presupuesto_extraccion,
    renderizar_plano_tabla_cotizar_ordenada,
    renderizar_plano_cotizacion_formal_pdf,
    renderizar_plano_cierre_pregunta_automatizar,
)
from src.mockups.planos.video_11_archivos import (
    renderizar_plano_cincuenta_archivos_caos,
    renderizar_plano_byte_rechazo_manual,
    renderizar_plano_drag_drop_ia_analisis,
    renderizar_plano_rag_resultado_citas,
    renderizar_plano_humor_sufrir_gratis,
    renderizar_plano_cierre_archivos_acumulados,
)
from src.mockups.planos.video_12_ciberseguridad import (
    renderizar_plano_google_ads_busqueda_trampa,
    renderizar_plano_alerta_sitio_clonado,
    renderizar_plano_mecanica_anuncio_pagado,
    renderizar_plano_inspeccion_url_lupa,
    renderizar_plano_split_anuncio_vs_organico,
    renderizar_plano_escudo_ciberseguridad,
    renderizar_plano_cierre_debate_estafas,
)
from src.mockups.planos.video_13_noticias import (
    renderizar_plano_noticias_mito_chat,
    renderizar_plano_noticias_breaking_impacto,
    renderizar_plano_noticias_transformacion_silenciosa,
    renderizar_plano_noticias_medicina_diagnostico,
    renderizar_plano_noticias_ciencia_clima_materiales,
    renderizar_plano_noticias_aceleracion_editorial,
    renderizar_plano_noticias_cierre_encuesta_futuro,
)

from src.mockups.planos.router import (
    MAPA_ARQUETIPOS,
    renderizar_escena_por_arquetipo,
    generar_video_cinematico_escena,
)
from src.mockups.planos.wrappers import (
    CONFIGS_ATENCION_CLIENTES,
    CONFIGS_EXCEL_REPORTES,
    CONFIGS_BUSQUEDA_INVESTIGACION,
    CONFIGS_DISENO_FLYERS,
    CONFIGS_COTIZACION_AUTOMATICA,
    CONFIGS_CINCUENTA_ARCHIVOS,
    CONFIGS_CIBERSEGURIDAD_GOOGLE_ADS,
    CONFIGS_NOTICIAS_IA_REALIDAD,
    CONFIGS_AGUA_IA,
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

__all__ = [
    "dibujar_icono_alerta",
    "dibujar_icono_cruz",
    "dibujar_icono_candado",
    "dibujar_icono_lupa",
    "renderizar_plano_hero_caos",
    "renderizar_plano_showcase_panoramico",
    "renderizar_plano_split_before_after",
    "renderizar_plano_deck_3d",
    "renderizar_plano_host_community",
    "renderizar_plano_panico_reloj",
    "renderizar_plano_julius_dashboard",
    "renderizar_plano_gamma_slides",
    "renderizar_plano_laptop_finde",
    "renderizar_plano_perplexity_search",
    "renderizar_plano_notebooklm_docs",
    "renderizar_plano_browser_tabs_caos",
    "renderizar_plano_single_tab_zen",
    "renderizar_plano_battle_vs",
    "renderizar_plano_flyer_paint_caos",
    "renderizar_plano_canva_magic_design",
    "renderizar_plano_remove_bg",
    "renderizar_plano_flyer_showcase_zen",
    "renderizar_plano_chat_flyer_urgente",
    "renderizar_plano_photoshop_freeze",
    "renderizar_plano_lienzo_blanco_bloqueo",
    "renderizar_plano_remove_bg_laser",
    "renderizar_plano_smartphone_instagram_feed",
    "renderizar_plano_whatsapp_pedido_remeras",
    "renderizar_plano_byte_pase_ia",
    "renderizar_plano_tabla_presupuesto_extraccion",
    "renderizar_plano_tabla_cotizar_ordenada",
    "renderizar_plano_cotizacion_formal_pdf",
    "renderizar_plano_cierre_pregunta_automatizar",
    "renderizar_plano_cincuenta_archivos_caos",
    "renderizar_plano_byte_rechazo_manual",
    "renderizar_plano_drag_drop_ia_analisis",
    "renderizar_plano_rag_resultado_citas",
    "renderizar_plano_humor_sufrir_gratis",
    "renderizar_plano_cierre_archivos_acumulados",
    "renderizar_plano_google_ads_busqueda_trampa",
    "renderizar_plano_alerta_sitio_clonado",
    "renderizar_plano_mecanica_anuncio_pagado",
    "renderizar_plano_inspeccion_url_lupa",
    "renderizar_plano_split_anuncio_vs_organico",
    "renderizar_plano_escudo_ciberseguridad",
    "renderizar_plano_cierre_debate_estafas",
    "renderizar_plano_noticias_mito_chat",
    "renderizar_plano_noticias_breaking_impacto",
    "renderizar_plano_noticias_transformacion_silenciosa",
    "renderizar_plano_noticias_medicina_diagnostico",
    "renderizar_plano_noticias_ciencia_clima_materiales",
    "renderizar_plano_noticias_aceleracion_editorial",
    "renderizar_plano_noticias_cierre_encuesta_futuro",
    "MAPA_ARQUETIPOS",
    "renderizar_escena_por_arquetipo",
    "generar_video_cinematico_escena",
    "CONFIGS_ATENCION_CLIENTES",
    "CONFIGS_EXCEL_REPORTES",
    "CONFIGS_BUSQUEDA_INVESTIGACION",
    "CONFIGS_DISENO_FLYERS",
    "CONFIGS_COTIZACION_AUTOMATICA",
    "CONFIGS_CINCUENTA_ARCHIVOS",
    "CONFIGS_CIBERSEGURIDAD_GOOGLE_ADS",
    "CONFIGS_NOTICIAS_IA_REALIDAD",
    "CONFIGS_AGUA_IA",
    "generar_video_interactivo_atencion_clientes",
    "generar_video_interactivo_excel_reportes",
    "generar_video_interactivo_busqueda_investigacion",
    "generar_video_interactivo_diseno_flyers",
    "generar_video_interactivo_cotizacion_automatica",
    "generar_video_interactivo_cincuenta_archivos",
    "generar_video_interactivo_ciberseguridad_google_ads",
    "generar_video_interactivo_noticias_ia_realidad",
    "generar_video_interactivo_agua_ia",
    "dibujar_icono_alerta",
    "dibujar_icono_cruz",
    "dibujar_icono_candado",
    "dibujar_icono_lupa",
]
