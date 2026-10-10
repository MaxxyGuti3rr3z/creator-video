"""
rutas.py
--------
Módulo centralizado de resolución de rutas para el proyecto 'Byte el Zorrito'.
Garantiza portabilidad y elimina rutas hardcodeadas en los scripts del motor,
mockups, pruebas y pipeline end-to-end.
"""

from pathlib import Path
from typing import Dict, Union, Optional
import os
import re

# ---------------------------------------------------------------------------
# Directorios Principales
# ---------------------------------------------------------------------------
DIR_RAIZ = Path(__file__).resolve().parent.parent

DIR_SRC = DIR_RAIZ / "src"
DIR_MOCKUPS = DIR_SRC / "mockups"

DIR_ASSETS = DIR_RAIZ / "assets"
DIR_BYTE = DIR_ASSETS / "byte"
DIR_BYTE_TRANSPARENTES = DIR_BYTE / "transparentes"
DIR_BYTE_ILUSTRACIONES = DIR_BYTE / "ilustraciones_originales"
DIR_AUDIO = DIR_ASSETS / "audio"
DIR_FONDOS = DIR_ASSETS / "fondos"
DIR_VFX = DIR_ASSETS / "vfx"

DIR_GUIONES = DIR_RAIZ / "guiones"
DIR_VIDEOS = DIR_RAIZ / "videos"

DIR_CACHE = DIR_RAIZ / "cache" / "cache_audio"
DIR_CACHE_INDEX = DIR_CACHE / "cache_audio_index.json"

DIR_PRUEBAS = DIR_RAIZ / "pruebas"
DIR_ARCHIVO = DIR_RAIZ / "_archivo"


# ---------------------------------------------------------------------------
# Funciones de Resolución
# ---------------------------------------------------------------------------

def normalizar_id_video(identificador: Union[int, str]) -> str:
    """Convierte un número o nombre a formato estándar (ej: 2 -> 'video_02', 'video_02_reuniones' -> 'video_02_reuniones')."""
    if isinstance(identificador, int):
        return f"video_{identificador:02d}"
    txt = str(identificador).strip().replace("\\", "/").rstrip("/")
    if "/" in txt:
        txt = txt.split("/")[-1]
    return txt


def ruta_video(identificador: Union[int, str]) -> Dict[str, Path]:
    """
    Resuelve y retorna el mapa de carpetas estructuradas para un video:
    - base:        videos/video_XX_nombre/
    - entrada:     videos/video_XX_nombre/entrada/
    - intermedios: videos/video_XX_nombre/intermedios/
    - final:       videos/video_XX_nombre/final/
    """
    id_str = normalizar_id_video(identificador)
    
    # Buscar si ya existe una carpeta que coincida
    carpeta_base = None
    if (DIR_VIDEOS / id_str).exists():
        carpeta_base = DIR_VIDEOS / id_str
    else:
        # Buscar por prefijo numérico (ej: 'video_02' matchea 'video_02_reuniones')
        m = re.match(r"(video_\d{2})", id_str)
        if m:
            prefijo = m.group(1)
            for d in DIR_VIDEOS.iterdir():
                if d.is_dir() and d.name.startswith(prefijo):
                    carpeta_base = d
                    break
        if carpeta_base is None:
            carpeta_base = DIR_VIDEOS / id_str

    dir_entrada = carpeta_base / "entrada"
    dir_intermedios = carpeta_base / "intermedios"
    dir_final = carpeta_base / "final"

    # Garantizar existencia
    dir_entrada.mkdir(parents=True, exist_ok=True)
    dir_intermedios.mkdir(parents=True, exist_ok=True)
    dir_final.mkdir(parents=True, exist_ok=True)

    return {
        "base": carpeta_base,
        "entrada": dir_entrada,
        "intermedios": dir_intermedios,
        "final": dir_final
    }


def ruta_guion(nombre_o_numero: Union[int, str]) -> Optional[Path]:
    """Busca y retorna la ruta a un guion JSON (en guiones/ o en videos/video_XX/entrada/)."""
    if isinstance(nombre_o_numero, int):
        patron = f"guion_{nombre_o_numero:02d}*.json"
        encontrados = list(DIR_GUIONES.glob(patron))
        if encontrados:
            return encontrados[0]
        # Buscar en videos/
        v_paths = ruta_video(nombre_o_numero)
        encontrados_v = list(v_paths["entrada"].glob(patron))
        if encontrados_v:
            return encontrados_v[0]
        return None

    p = Path(nombre_o_numero)
    if p.exists():
        return p.resolve()
    
    en_guiones = DIR_GUIONES / p.name
    if en_guiones.exists():
        return en_guiones.resolve()
        
    return None


def ruta_sprite_byte(nombre_sprite: str) -> Path:
    """Retorna la ruta al sprite transparente de Byte."""
    return DIR_BYTE_TRANSPARENTES / nombre_sprite


def ruta_sfx(nombre_sfx: str) -> Path:
    """Retorna la ruta a un SFX base."""
    return DIR_AUDIO / nombre_sfx


def ruta_vfx(nombre_vfx: str) -> Path:
    """Retorna la ruta a un efecto visual en assets/vfx/."""
    return DIR_VFX / nombre_vfx
