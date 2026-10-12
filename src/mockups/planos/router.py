"""
src.mockups.planos.router
---------------------------------------------------------------------------
MAPA_ARQUETIPOS, despacho por arquetipo y generador MP4 de escenas cinematicas.
"""

from typing import Dict, Any, Optional, Tuple, List, Union
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

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


MAPA_ARQUETIPOS = {

    "PLANO_HERO_CAOS": renderizar_plano_hero_caos,
    "PLANO_SHOWCASE_PANORAMICO": renderizar_plano_showcase_panoramico,
    "PLANO_SPLIT_BEFORE_AFTER": renderizar_plano_split_before_after,
    "PLANO_DECK_3D": renderizar_plano_deck_3d,
    "PLANO_HOST_COMMUNITY": renderizar_plano_host_community,
    "PLANO_PANICO_RELOJ": renderizar_plano_panico_reloj,
    "PLANO_JULIUS_DASHBOARD": renderizar_plano_julius_dashboard,
    "PLANO_GAMMA_SLIDES": renderizar_plano_gamma_slides,
    "PLANO_LAPTOP_CERRADA": renderizar_plano_laptop_finde,
    "PLANO_PERPLEXITY_SEARCH": renderizar_plano_perplexity_search,
    "PLANO_NOTEBOOKLM_DOCS": renderizar_plano_notebooklm_docs,
    "PLANO_BROWSER_TABS_CAOS": renderizar_plano_browser_tabs_caos,
    "PLANO_SINGLE_TAB_ZEN": renderizar_plano_single_tab_zen,
    "PLANO_BATTLE_VS": renderizar_plano_battle_vs,
    "PLANO_FLYER_PAINT_CAOS": renderizar_plano_flyer_paint_caos,
    "PLANO_CANVA_MAGIC_DESIGN": renderizar_plano_canva_magic_design,
    "PLANO_REMOVE_BG": renderizar_plano_remove_bg,
    "PLANO_FLYER_SHOWCASE_ZEN": renderizar_plano_flyer_showcase_zen,
    "PLANO_CHAT_FLYER_URGENTE": renderizar_plano_chat_flyer_urgente,
    "PLANO_PHOTOSHOP_FREEZE": renderizar_plano_photoshop_freeze,
    "PLANO_LIENZO_BLANCO_BLOQUEO": renderizar_plano_lienzo_blanco_bloqueo,
    "PLANO_REMOVE_BG_LASER": renderizar_plano_remove_bg_laser,
    "PLANO_SMARTPHONE_INSTAGRAM_FEED": renderizar_plano_smartphone_instagram_feed,
    "PLANO_WHATSAPP_PEDIDO_REMERAS": renderizar_plano_whatsapp_pedido_remeras,
    "PLANO_BYTE_PASE_IA": renderizar_plano_byte_pase_ia,
    "PLANO_TABLA_PRESUPUESTO_EXTRACCION": renderizar_plano_tabla_presupuesto_extraccion,
    "PLANO_TABLA_COTIZAR_ORDENADA": renderizar_plano_tabla_cotizar_ordenada,
    "PLANO_COTIZACION_FORMAL_PDF": renderizar_plano_cotizacion_formal_pdf,
    "PLANO_CIERRE_PREGUNTA_AUTOMATIZAR": renderizar_plano_cierre_pregunta_automatizar,
    "PLANO_CINCUENTA_ARCHIVOS_CAOS": renderizar_plano_cincuenta_archivos_caos,
    "PLANO_BYTE_RECHAZO_MANUAL": renderizar_plano_byte_rechazo_manual,
    "PLANO_DRAG_DROP_IA_ANALISIS": renderizar_plano_drag_drop_ia_analisis,
    "PLANO_RAG_RESULTADO_CITAS": renderizar_plano_rag_resultado_citas,
    "PLANO_HUMOR_SUFRIR_GRATIS": renderizar_plano_humor_sufrir_gratis,
    "PLANO_CIERRE_ARCHIVOS_ACUMULADOS": renderizar_plano_cierre_archivos_acumulados,
    "PLANO_GOOGLE_ADS_BUSQUEDA_TRAMPA": renderizar_plano_google_ads_busqueda_trampa,
    "PLANO_ALERTA_SITIO_CLONADO": renderizar_plano_alerta_sitio_clonado,
    "PLANO_MECANICA_ANUNCIO_PAGADO": renderizar_plano_mecanica_anuncio_pagado,
    "PLANO_INSPECCION_URL_LUPA": renderizar_plano_inspeccion_url_lupa,
    "PLANO_SPLIT_ANUNCIO_VS_ORGANICO": renderizar_plano_split_anuncio_vs_organico,
    "PLANO_ESCUDO_CIBERSEGURIDAD": renderizar_plano_escudo_ciberseguridad,
    "PLANO_CIERRE_DEBATE_ESTAFAS": renderizar_plano_cierre_debate_estafas,
    "PLANO_NOTICIAS_MITO_CHAT": renderizar_plano_noticias_mito_chat,
    "PLANO_NOTICIAS_BREAKING_IMPACTO": renderizar_plano_noticias_breaking_impacto,
    "PLANO_NOTICIAS_TRANSFORMACION_SILENCIOSA": renderizar_plano_noticias_transformacion_silenciosa,
    "PLANO_NOTICIAS_MEDICINA_DIAGNOSTICO": renderizar_plano_noticias_medicina_diagnostico,
    "PLANO_NOTICIAS_CIENCIA_CLIMA_MATERIALES": renderizar_plano_noticias_ciencia_clima_materiales,
    "PLANO_NOTICIAS_ACELERACION_EDITORIAL": renderizar_plano_noticias_aceleracion_editorial,
    "PLANO_NOTICIAS_CIERRE_ENCUESTA_FUTURO": renderizar_plano_noticias_cierre_encuesta_futuro,
}


def renderizar_escena_por_arquetipo(
    arquetipo: str,
    ancho: int = 1080,
    alto: int = 1920,
    t_sec: float = 0.0,
    duracion: float = 5.0,
    config: Optional[Dict[str, Any]] = None
) -> Image.Image:
    """Invoca la función del arquetipo cinematográfico correspondiente."""
    fn = MAPA_ARQUETIPOS.get(arquetipo)
    if not fn:
        # Fallback inteligente según nombre
        if "caos" in arquetipo.lower() or "problema" in arquetipo.lower():
            fn = renderizar_plano_hero_caos
        elif "showcase" in arquetipo.lower() or "gamma" in arquetipo.lower():
            fn = renderizar_plano_showcase_panoramico
        elif "split" in arquetipo.lower() or "canva" in arquetipo.lower():
            fn = renderizar_plano_split_before_after
        elif "3d" in arquetipo.lower() or "resultado" in arquetipo.lower():
            fn = renderizar_plano_deck_3d
        else:
            fn = renderizar_plano_host_community

    return fn(ancho=ancho, alto=alto, t_sec=t_sec, duracion=duracion, config=config)


# ---------------------------------------------------------------------------
# Generador de Video MP4 para Escenas Cinematográficas
# ---------------------------------------------------------------------------
import subprocess

def generar_video_cinematico_escena(
    arquetipo: str,
    duracion_segundos: float,
    ruta_salida: Union[str, Path],
    config: Optional[Dict[str, Any]] = None,
    fps: int = 30,
    ancho: int = 1080,
    alto: int = 1920
) -> Path:
    """Renderiza un video animado completo en base a un arquetipo cinematográfico enviando frames a FFmpeg."""
    ruta_salida = Path(ruta_salida)
    ruta_salida.parent.mkdir(parents=True, exist_ok=True)
    total_frames = max(1, int(duracion_segundos * fps))

    cmd = [
        "ffmpeg", "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-s", f"{ancho}x{alto}",
        "-pix_fmt", "rgba",
        "-r", str(fps),
        "-i", "-",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-preset", "veryfast",
        "-crf", "18",
        str(ruta_salida)
    ]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        for f_idx in range(total_frames):
            if f_idx % 60 == 0 or f_idx == total_frames - 1:
                print(f"  [{arquetipo}] Frame {f_idx + 1}/{total_frames} ({((f_idx + 1) / total_frames) * 100:.0f}%)...", flush=True)

            t_sec = f_idx / float(fps)
            frame_img = renderizar_escena_por_arquetipo(
                arquetipo=arquetipo,
                ancho=ancho,
                alto=alto,
                t_sec=t_sec,
                duracion=duracion_segundos,
                config=config
            )
            proc.stdin.write(frame_img.tobytes())
        proc.stdin.close()
        proc.wait()
    except Exception as e:
        proc.kill()
        raise e

    print(f"Video cinematográfico generado en: {ruta_salida} ({total_frames} frames)")
    return ruta_salida
