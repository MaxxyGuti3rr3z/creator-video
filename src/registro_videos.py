"""
Registro central de videos del pipeline "Byte el Zorrito".

Una fila por video: carpetas, nombre_base, alias de búsqueda, generador de
fondos, etiqueta de consola y set de sprites de Byte.

Reemplaza los tres encadenamientos if/elif que vivían en
`pruebas/prueba_end_to_end.py` y que obligaban a tocar 3 lugares por cada
video nuevo; hoy el orquestador los invoca vía resolver_carpeta (~161),
sprites_para (~285) y config_de_fondos (~313).

Para agregar un video nuevo:
  1. Agregar una fila a CONFIGS (abajo).
  2. Crear la función `generar_video_interactivo_<clave>` en src/mockups/.
  3. Agregar sus planos en src/mockups/director_escena.py.

Nota de equivalencia: la condición histórica del video 03 en el bloque de
fondos era `"03" in nombre_base and "04" not in nombre_base`; aquí se
expresa como clave "03" + mockup "gestor_tareas", que cubre todos los
guiones reales (02-13).
"""
from __future__ import annotations

import importlib
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, List, Optional, Tuple

from src.rutas import DIR_BYTE_ILUSTRACIONES, DIR_BYTE_TRANSPARENTES

# Bloques narrativos reconocidos en los sprites de Byte
BLOQUES = (
    "cold_open", "hook", "escena_problema", "problema",
    "punto_1", "punto_2", "punto1", "punto2", "resultado", "cierre",
)

Sprite = Tuple[str, Path]


@dataclass(frozen=True)
class ConfigVideo:
    """Fila de configuración de un video del catálogo."""

    id: str
    # Palabras clave contra el stem del archivo del guion (bloque de carpetas)
    claves: Tuple[str, ...]
    # Valores de guion["mockup_sugerido"] que seleccionan este video
    claves_mockup: Tuple[str, ...]
    # nombre_base literal; None => se usa el stem del archivo del guion
    nombre_base: Optional[str]
    # Carpeta bajo videos/; None => f"video_{stem}"
    carpeta: Optional[str]
    # Función de src.mockups que genera los fondos; None => sin fondos dedicados
    generador_fondos: Optional[str]
    # Etiqueta impresa en consola al generar los fondos
    etiqueta_fondos: str
    # Sprites de Byte por bloque narrativo
    sprites: Tuple[Sprite, ...]
    # Palabras clave del nombre_base que seleccionan estos sprites
    # (vacío = solo se selecciona por claves_mockup, como en el bloque 02/03)
    claves_sprites: Tuple[str, ...] = ()
    # Palabras clave del nombre_base que activan el generador de fondos
    # (vacío = solo se selecciona por claves_mockup, como en el video 02)
    claves_fondos: Tuple[str, ...] = ()
    # Palabras clave del nombre_base que activan el overlay cinematográfico;
    # si se omiten se usan claves_sprites (caso idéntico en los videos 06-13)
    claves_overlay: Tuple[str, ...] = ()
    # True: arquetipo cinematográfico -> capa de overlay FFmpeg transparente
    cinematico: bool = False


def _sprites(base: Path, *pares: Tuple[str, str]) -> Tuple[Sprite, ...]:
    return tuple((bloque, base / archivo) for bloque, archivo in pares)


# --- Sets de sprites -------------------------------------------------------

# Videos 03/04/05/06: ilustraciones originales de Byte (5 bloques)
_SPRITES_GENERICOS = _sprites(
    DIR_BYTE_ILUSTRACIONES,
    ("escena_problema", "byte_estresado.png"),
    ("punto_1", "byte_ojos_estrella.png"),
    ("punto_2", "Byte_enojado_computadora.png"),
    ("resultado", "byte_pacifico_rodeados_archivos.png"),
    ("cierre", "byte_saltando_feliz.png"),
)

# Video 02 (reuniones): ilustraciones originales (4 bloques)
_SPRITES_REUNION = _sprites(
    DIR_BYTE_ILUSTRACIONES,
    ("hook", "byte_estresado.png"),
    ("punto1", "byte_ojos_estrella.png"),
    ("punto2", "byte_pacifico_rodeados_archivos.png"),
    ("cierre", "byte_saltando_feliz.png"),
)

# Fallback: ilustraciones originales (4 bloques)
_SPRITES_GENERICO_FINAL = _sprites(
    DIR_BYTE_ILUSTRACIONES,
    ("hook", "Byte_enojado_computadora.png"),
    ("punto1", "byte_ojos_estrella.png"),
    ("punto2", "byte_pacifico_rodeados_archivos.png"),
    ("cierre", "byte_señalando_serio.png"),
)

_SPRITES_07 = _sprites(
    DIR_BYTE_TRANSPARENTES,
    ("cold_open", "byte_cortocircuito_transparente.png"),
    ("hook", "hook_guion_07_transparente.png"),
    ("problema", "problema_guion_07_transparente.png"),
    ("punto_1", "punto_1_guion_07_transparente.png"),
    ("punto_2", "punto_2_guion_07_transparente.png"),
    ("resultado", "resultado_guion_07_transparente.png"),
    ("cierre", "cierre_guion_07_transparente.png"),
)

_SPRITES_08 = _sprites(
    DIR_BYTE_TRANSPARENTES,
    ("cold_open", "cold_open_guion_08_busqueda_investigacion_transparente.png"),
    ("hook", "hook_guion_08_busqueda_investigacion_transparente.png"),
    ("problema", "problema_guion_08_busqueda_investigacion_transparente.png"),
    ("punto_1", "punto_1_guion_08_busqueda_investigacion_transparente.png"),
    ("punto_2", "punto_2_guion_08_busqueda_investigacion_transparente.png"),
    ("resultado", "resultado_guion_08_busqueda_investigacion_transparente.png"),
    ("cierre", "cierre_guion_08_busqueda_investigacion_transparente.png"),
)

_SPRITES_09 = _sprites(
    DIR_BYTE_TRANSPARENTES,
    ("cold_open", "byte_agotado_transparente.png"),
    ("hook", "punto_2_guion_04_transparente.png"),
    ("problema", "byte_cortocircuito_transparente.png"),
    ("punto_1", "punto_1_guion_04_transparente.png"),
    ("punto_2", "cierre_transparente.png"),
    ("resultado", "cierre_guion_04_transparente.png"),
    ("cierre", "cierre_guion_08_busqueda_investigacion_transparente.png"),
)

_SPRITES_10 = _sprites(
    DIR_BYTE_TRANSPARENTES,
    ("cold_open", "cierre_transparente.png"),
    ("hook", "punto_2_guion_04_transparente.png"),
    ("problema", "byte_computadora_feliz_transparente.png"),
    ("punto_1", "punto_1_guion_04_transparente.png"),
    ("punto_2", "punto_2_guion_08_busqueda_investigacion_transparente.png"),
    ("resultado", "cierre_guion_04_transparente.png"),
    ("cierre", "cierre_saltando_transparente.png"),
)

_SPRITES_11 = _sprites(
    DIR_BYTE_TRANSPARENTES,
    ("cold_open", "escena_problema_guion_03_transparente.png"),
    ("hook", "punto_2_guion_10_cotizacion_automatica_transparente.png"),
    ("problema", "byte_cortocircuito_transparente.png"),
    ("punto_1", "byte_computadora_feliz_transparente.png"),
    ("punto_2", "resultado_guion_08_busqueda_investigacion_transparente.png"),
    ("resultado", "cierre_guion_07_transparente.png"),
    ("cierre", "cierre_saltando_transparente.png"),
)

_SPRITES_12 = _sprites(
    DIR_BYTE_TRANSPARENTES,
    ("cold_open", "punto_1_guion_08_busqueda_investigacion_transparente.png"),
    ("hook", "hook_estresado_transparente.png"),
    ("problema", "byte_cortocircuito_transparente.png"),
    ("punto_1", "punto_1_guion_08_busqueda_investigacion_transparente.png"),
    ("punto_2", "punto_2_guion_08_busqueda_investigacion_transparente.png"),
    ("resultado", "resultado_guion_10_cotizacion_automatica_transparente.png"),
    ("cierre", "cierre_saltando_transparente.png"),
)

_SPRITES_13 = _sprites(
    DIR_BYTE_TRANSPARENTES,
    ("cold_open", "cierre_transparente.png"),
    ("hook", "punto1_feliz_transparente.png"),
    ("problema", "punto_1_guion_08_busqueda_investigacion_transparente.png"),
    ("punto_1", "punto_2_guion_08_busqueda_investigacion_transparente.png"),
    ("punto_2", "punto_2_guion_08_busqueda_investigacion_transparente.png"),
    ("resultado", "resultado_guion_10_cotizacion_automatica_transparente.png"),
    ("cierre", "cierre_saltando_transparente.png"),
)

# Video 14 (agua e IA): rotación de poses (estresado, cortocircuito, feliz)
# sin repetir byte_agotado; sprites dedicados del video 13 para el bloque medio
_SPRITES_14 = _sprites(
    DIR_BYTE_TRANSPARENTES,
    ("cold_open", "hook_estresado_transparente.png"),
    ("hook", "byte_cortocircuito_transparente.png"),
    ("problema", "punto_1_guion_13_noticias_ia_realidad_transparente.png"),
    ("punto_1", "punto1_feliz_transparente.png"),
    ("punto_2", "punto_2_guion_13_noticias_ia_realidad_transparente.png"),
    ("resultado", "byte_computadora_feliz_transparente.png"),
    ("cierre", "cierre_guion_13_noticias_ia_realidad_transparente.png"),
)


# --- Catálogo --------------------------------------------------------------

CONFIGS: Tuple[ConfigVideo, ...] = (
    ConfigVideo(
        id="01",
        claves=("01", "bandeja"),
        claves_mockup=(),
        nombre_base="prueba_real",
        carpeta="video_01_bandeja_correo",
        generador_fondos=None,
        etiqueta_fondos="",
        sprites=_SPRITES_GENERICO_FINAL,
    ),
    ConfigVideo(
        id="02",
        claves=("02", "reuniones"),
        claves_mockup=("reunion_transcripcion",),
        nombre_base="guion_02",
        carpeta="video_02_reuniones",
        generador_fondos="generar_video_interactivo_reunion",
        etiqueta_fondos="Sala Andes (reunion_transcripcion)",
        sprites=_SPRITES_REUNION,
    ),
    ConfigVideo(
        id="03",
        claves=("03", "tareas"),
        claves_mockup=("gestor_tareas",),
        nombre_base="guion_03",
        carpeta="video_03_tareas",
        claves_fondos=("03",),
        generador_fondos="generar_video_interactivo_tareas",
        etiqueta_fondos="Lista Andes (gestor_tareas)",
        sprites=_SPRITES_GENERICOS,
    ),
    ConfigVideo(
        id="04",
        claves=("04", "correo"),
        claves_mockup=("asistente_correo",),
        nombre_base="guion_04",
        carpeta="video_04_correo",
        claves_fondos=("04", "correo"),
        generador_fondos="generar_video_interactivo_correo",
        etiqueta_fondos="Correo (Video 04)",
        sprites=_SPRITES_GENERICOS,
        claves_sprites=("04", "correo"),
    ),
    ConfigVideo(
        id="05",
        claves=("05", "presentaciones"),
        claves_mockup=("presentaciones",),
        nombre_base="guion_05",
        carpeta="video_05_presentaciones",
        claves_fondos=("05", "presentaciones"),
        generador_fondos="generar_video_interactivo_presentaciones",
        etiqueta_fondos="Presentaciones (Video 05 - Gamma/Canva)",
        sprites=_SPRITES_GENERICOS,
        claves_sprites=("05", "presentaciones"),
    ),
    ConfigVideo(
        id="06",
        claves=("06", "atencion", "soporte"),
        claves_mockup=("atencion_clientes",),
        nombre_base="guion_06",
        carpeta="video_06_atencion_clientes",
        claves_fondos=("06", "atencion"),
        generador_fondos="generar_video_interactivo_atencion_clientes",
        etiqueta_fondos="Atención al Cliente (Video 06 - Fin/Lyro)",
        sprites=_SPRITES_GENERICOS,
        claves_sprites=("06", "atencion"),
        cinematico=True,
    ),
    ConfigVideo(
        id="07",
        claves=("07", "excel", "reportes"),
        claves_mockup=("excel_reportes", "dinamico_con_memes"),
        nombre_base="guion_07",
        carpeta="video_07_excel_reportes",
        claves_fondos=("07", "excel"),
        generador_fondos="generar_video_interactivo_excel_reportes",
        etiqueta_fondos="Excel y Reportes con memes (Video 07)",
        sprites=_SPRITES_07,
        claves_sprites=("07", "excel"),
        cinematico=True,
    ),
    ConfigVideo(
        id="08",
        claves=("08", "busqueda", "investigacion"),
        claves_mockup=("busqueda_investigacion",),
        nombre_base="guion_08_busqueda_investigacion",
        carpeta="video_08_busqueda_investigacion",
        claves_fondos=("08", "busqueda", "investigacion"),
        generador_fondos="generar_video_interactivo_busqueda_investigacion",
        etiqueta_fondos="Búsqueda e Investigación (Video 08 - Perplexity/NotebookLM)",
        sprites=_SPRITES_08,
        claves_sprites=("08", "busqueda", "investigacion"),
        cinematico=True,
    ),
    ConfigVideo(
        id="09",
        claves=("09", "diseno", "flyers"),
        claves_mockup=("diseno_flyers", "flyers"),
        nombre_base="guion_09_diseno_flyers",
        carpeta="video_09_diseno_flyers",
        claves_fondos=("09", "diseno", "flyers"),
        generador_fondos="generar_video_interactivo_diseno_flyers",
        etiqueta_fondos="Diseño de Flyers (Video 09 - Canva/Remove.bg)",
        sprites=_SPRITES_09,
        claves_sprites=("09", "diseno", "flyers"),
        cinematico=True,
    ),
    ConfigVideo(
        id="10",
        claves=("10", "cotizacion", "presupuesto"),
        claves_mockup=("cotizacion_automatica", "cotizacion"),
        nombre_base="guion_10_cotizacion_automatica",
        carpeta="video_10_cotizacion_automatica",
        claves_fondos=("10", "cotizacion"),
        generador_fondos="generar_video_interactivo_cotizacion_automatica",
        etiqueta_fondos="Cotización Automática (Video 10)",
        sprites=_SPRITES_10,
        claves_sprites=("10", "cotizacion", "presupuesto"),
        claves_overlay=("10", "cotizacion"),
        cinematico=True,
    ),
    ConfigVideo(
        id="11",
        claves=("11", "cincuenta", "archivos"),
        claves_mockup=("cincuenta_archivos", "archivos"),
        nombre_base="guion_11_cincuenta_archivos",
        carpeta="video_11_cincuenta_archivos",
        claves_fondos=("11", "cincuenta", "archivos"),
        generador_fondos="generar_video_interactivo_cincuenta_archivos",
        etiqueta_fondos="50 Archivos (Video 11 - Análisis Documental IA)",
        sprites=_SPRITES_11,
        claves_sprites=("11", "cincuenta", "archivos"),
        cinematico=True,
    ),
    ConfigVideo(
        id="12",
        claves=("12", "ciberseguridad", "google_ads"),
        claves_mockup=("ciberseguridad_google_ads", "ciberseguridad"),
        nombre_base=None,          # se usa el stem del guion (nombres de sprites/subtítulos)
        carpeta="video_12_ciberseguridad_google_ads",
        claves_fondos=("12", "ciberseguridad", "google_ads"),
        generador_fondos="generar_video_interactivo_ciberseguridad_google_ads",
        etiqueta_fondos="Ciberseguridad y Google Ads (Video 12)",
        sprites=_SPRITES_12,
        claves_sprites=("12", "ciberseguridad", "google_ads"),
        cinematico=True,
    ),
    ConfigVideo(
        id="13",
        claves=("13", "noticias"),
        claves_mockup=("noticias_ia_realidad", "noticias"),
        nombre_base=None,          # se usa el stem del guion (nombres de sprites/subtítulos)
        carpeta="video_13_noticias_ia_realidad",
        claves_fondos=("13", "noticias"),
        generador_fondos="generar_video_interactivo_noticias_ia_realidad",
        etiqueta_fondos="Noticias de IA (Video 13)",
        sprites=_SPRITES_13,
        claves_sprites=("13", "noticias"),
        cinematico=True,
    ),
    ConfigVideo(
        id="14",
        claves=("14", "agua"),
        claves_mockup=("agua_ia", "agua"),
        nombre_base=None,          # se usa el stem del guion (nombres de sprites/subtítulos)
        carpeta="video_14_agua_ia",
        claves_fondos=("14", "agua"),
        generador_fondos="generar_video_interactivo_agua_ia",
        etiqueta_fondos="Agua e IA (Video 14 - desmintiendo el pánico)",
        sprites=_SPRITES_14,
        claves_sprites=("14", "agua"),
        cinematico=True,
    ),
)

_POR_ID = {cfg.id: cfg for cfg in CONFIGS}

# Orden histórico de cada bloque (replica el if/elif original; 12/13 ahora
# tienen carpeta canónica explícita en su config; 14 se agrega al frente)
_ORDEN_CARPETA = ("14", "13", "12", "03", "02", "04", "05", "06", "07", "08", "10", "11", "09", "01")
_ORDEN_SPRITES = ("14", "13", "12", "11", "10", "09", "08", "07", "04", "05", "06", "03", "02", "01")
_ORDEN_FONDOS = ("14", "03", "04", "02", "05", "06", "07", "08", "09", "10", "11", "12", "13")


def _coincide(cfg: ConfigVideo, texto: str, claves: Tuple[str, ...],
              mockup_sugerido: Optional[str]) -> bool:
    """Coincidencia por palabra clave (subcadena) o por mockup_sugerido."""
    if claves and any(k in texto for k in claves):
        return True
    if mockup_sugerido and mockup_sugerido in cfg.claves_mockup:
        return True
    return False


def resolver_carpeta(stem: str) -> Tuple[str, str]:
    """
    Devuelve (nombre_base, carpeta) para el stem de un guion.
    Sustituye el bloque de if/elif de `cargar_guion()`.
    """
    for ident in _ORDEN_CARPETA:
        cfg = _POR_ID[ident]
        if any(k in stem for k in cfg.claves):
            return cfg.nombre_base or stem, cfg.carpeta or f"video_{stem}"
    return stem, f"video_{stem}"


def sprites_para(nombre_base: str, mockup_sugerido: Optional[str] = None) -> Tuple[Sprite, ...]:
    """
    Devuelve los sprites de Byte ((bloque, ruta_png), ...) para un video.
    Sustituye el bloque de if/elif de selección de imágenes en PASO 4.

    Los videos 02 y 03 solo se seleccionan por mockup_sugerido (así lo hacía
    la rama histórica); el resto por palabra clave del nombre_base.
    """
    texto = nombre_base or ""
    for ident in _ORDEN_SPRITES:
        cfg = _POR_ID[ident]
        if ident in ("02", "03"):
            if mockup_sugerido and mockup_sugerido in cfg.claves_mockup:
                return cfg.sprites
        elif any(k in texto for k in cfg.claves_sprites):
            return cfg.sprites
    return _SPRITES_GENERICO_FINAL


def config_de_fondos(nombre_base: str, mockup_sugerido: Optional[str] = None) -> Optional[ConfigVideo]:
    """
    Devuelve la ConfigVideo cuyo generador de fondos corresponde, o None.
    Sustituye el bloque de if/elif del PASO 4.1.
    """
    texto = nombre_base or ""
    for ident in _ORDEN_FONDOS:
        cfg = _POR_ID[ident]
        if cfg.generador_fondos and _coincide(cfg, texto, cfg.claves_fondos, mockup_sugerido):
            return cfg
    return None


def overlay_vacio(nombre_base: str) -> bool:
    """
    True si el video usa arquetipo cinematográfico (capa de overlay FFmpeg
    transparente). Sustituye la condición compuesta del PASO 4.
    """
    texto = nombre_base or ""
    return any(
        cfg.cinematico
        and any(k in texto for k in (cfg.claves_overlay or cfg.claves_sprites))
        for cfg in CONFIGS
    )


def obtener_generador(nombre: str) -> Callable[..., None]:
    """Resuelve `generar_video_interactivo_<x>` en src.mockups (fachada)."""
    for modulo in ("src.mockups", "src.mockups.motor", "src.mockups.director_escena"):
        try:
            mod = importlib.import_module(modulo)
        except ImportError:
            continue
        fn = getattr(mod, nombre, None)
        if callable(fn):
            return fn
    raise AttributeError(
        f"No existe el generador de fondos '{nombre}' en src.mockups "
        f"(agregue la función o la fila del video en src/registro_videos.py)"
    )


def generar_fondos_del_video(
    cfg: ConfigVideo,
    segmentos: List[dict],
    dir_fondos: Path,
    forzar: bool = False,
) -> List[Path]:
    """
    Genera (o reutiliza) un MP4 de fondo por escena con el generador del video.
    Devuelve la lista de rutas absolutas, en orden de escena.
    """
    generador = obtener_generador(cfg.generador_fondos)
    rutas: List[Path] = []
    for i, seg in enumerate(segmentos):
        tipo_escena = seg["tipo"]
        p_fondo = dir_fondos / f"fondo_escena_{i}_{tipo_escena}.mp4"
        dur_esc = (seg["fin"] - seg["inicio"]) + 0.15
        if forzar or not (p_fondo.exists() and p_fondo.stat().st_size > 50000):
            generador(tipo_escena, dur_esc, p_fondo)
        rutas.append(p_fondo.resolve())
    return rutas
