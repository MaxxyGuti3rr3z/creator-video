r"""
prueba_end_to_end.py
--------------------
Pipeline de prueba de extremo a extremo con el guion real de "Bandeja de entrada":

Uso:
    python pruebas/prueba_end_to_end.py [ruta_guion.json] [--forzar-fondos]
        [--saltar-validacion] [--sin-chequeo-final]

    --forzar-fondos   Regenera los MP4 de intermedios/fondos/ aunque existan.
                      Obligatorio tras editar arquetipos/configs de planos:
                      si no, el pipeline reusa la caché de fondos y el video
                      final queda con el aspecto ANTERIOR a los cambios
                      (el audio SÍ usa su propia caché y no gasta créditos).

    --saltar-validacion   Salta el PRE-VUELO (validar_guion + lint_obsoleto de
                      fondos/sprites de la carpeta destino). Sin este flag, el
                      pipeline ABORTA antes de gastar créditos si el guion tiene
                      errores o la carpeta tiene caché vencida.

    --sin-chequeo-final   Salta el POST-VUELO (lint_zonas_seguras sobre el MP4
                      final). Sin este flag, el pipeline termina con exit 1 si el
                      video tiene contenido en zonas prohibidas (no publicar).

1. Guion real estructurado.
2. Audio y alignment (ElevenLabs with timestamps o generador de alta fidelidad).
   DIAGNÓSTICO 1: Impresión completa de 'characters' y confirmación visual de caracteres españoles (á,é,í,ó,ú,ñ,¿,¡).
3. Segmentación real calculada según timestamps de alignment.
4. Mapeo de imágenes reales de Byte.
5. Ensamblado vertical con FFmpeg aplicando:
   - DIAGNÓSTICO 2: \k de palabra N cubre hasta inicio de palabra N+1 (sin saltos bruscos).
   - DIAGNÓSTICO 3: Precisión uniforme en centésimas de segundo (cs).
   - DIAGNÓSTICO 4: Filtrado estricto de palabras vacías y fragmentos anómalos.
6. Validación ffprobe, exportación de tabla TXT de tiempos \k y capturas PNG de frames.
"""

from __future__ import annotations

import base64
import datetime
import hashlib
import json
import logging
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import unicodedata
from typing import Any, Dict, List, Optional, Tuple
import requests
from PIL import Image
from dotenv import load_dotenv

load_dotenv()

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

DIR_RAIZ = Path(__file__).resolve().parent.parent
if str(DIR_RAIZ) not in sys.path:
    sys.path.insert(0, str(DIR_RAIZ))

from src.rutas import (
    DIR_RAIZ,
    DIR_SRC,
    DIR_ASSETS,
    DIR_BYTE_TRANSPARENTES,
    DIR_BYTE_ILUSTRACIONES,
    DIR_AUDIO,
    DIR_FONDOS,
    DIR_VFX,
    DIR_GUIONES,
    DIR_VIDEOS,
    DIR_CACHE,
    DIR_CACHE_INDEX,
    DIR_PRUEBAS,
    ruta_video,
    ruta_guion,
    ruta_sprite_byte
)

from src.shorts_assembler import (
    generar_ass,
    quitar_fondo,
    ensamblar_video,
    acelerar_video,
    validar_output,
    exportar_tabla_tiempos_palabras,
    imprimir_diagnostico_caracteres,
    sanitizar_alignment,
    _agrupar_caracteres_en_palabras
)

from src.registro_videos import (
    resolver_carpeta,
    sprites_para,
    config_de_fondos,
    overlay_vacio,
    generar_fondos_del_video,
)

from src.chequeos_pipeline import pre_vuelo, post_vuelo, chequear_ass

# Cargar explícitamente variables de entorno desde el .env del proyecto
from dotenv import load_dotenv
env_path = DIR_RAIZ / ".env"
load_dotenv(dotenv_path=env_path, override=True)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


# ===========================================================================
# PASO 1: Guion real fijo (Bandeja de entrada)
# ===========================================================================
GUION_REAL = {
    "hook": "¿Bandeja de entrada llena de mensajes repetitivos que te roban la energía?",
    "puntos": [
        {
            "herramienta_o_tip": "Shortwave",
            "explicacion": "Redacta borradores automáticos y resúmenes de tus correos usando inteligencia artificial.",
            "opinion_byte": "Me encanta cómo clava un tono natural sin sonar como un robot frío."
        },
        {
            "herramienta_o_tip": "SaneBox",
            "explicacion": "Filtra tus correos importantes y envía boletines o distracciones a carpetas secundarias.",
            "opinion_byte": "Al principio conviene revisar qué filtra, pero después te limpia todo el caos."
        }
    ],
    "cierre": "Comentá abajo cuántos correos sin leer acumulás hoy."
}


def construir_bloques_narrativos(guion: Dict[str, Any]) -> List[Dict[str, str]]:
    """Construye los bloques narrativos a partir del guion JSON."""
    if "problema" in guion and "demostracion" in guion:
        cold_open_text = guion.get("cold_open", "").strip()
        hook_text = guion["hook"].strip()
        problema_text = guion["problema"].strip()

        def _extraer_texto_demo(d: Any) -> str:
            if isinstance(d, dict):
                if "accion" in d:
                    return str(d["accion"]).strip()
                if "texto" in d:
                    return str(d["texto"]).strip()
                return f"{d.get('herramienta_o_tip', '')} {d.get('explicacion', '')} {d.get('opinion_byte', '')}".strip()
            return str(d).strip()

        demos = guion["demostracion"]
        if isinstance(demos, list) and len(demos) >= 2:
            p1_text = _extraer_texto_demo(demos[0])
            p2_text = _extraer_texto_demo(demos[1])
        elif isinstance(demos, list) and len(demos) == 1:
            p1_text = _extraer_texto_demo(demos[0])
            p2_text = ""
        else:
            p1_text = _extraer_texto_demo(demos)
            p2_text = ""

        resultado_text = guion.get("resultado", "").strip()
        cierre_text = guion["cierre"].strip()

        bloques = []
        if cold_open_text:
            bloques.append({"tipo": "cold_open", "texto": cold_open_text})
        bloques.extend([
            {"tipo": "hook", "texto": hook_text},
            {"tipo": "problema", "texto": problema_text},
            {"tipo": "punto_1", "texto": p1_text},
            {"tipo": "punto_2", "texto": p2_text},
            {"tipo": "resultado", "texto": resultado_text},
            {"tipo": "cierre", "texto": cierre_text}
        ])
        return [b for b in bloques if b["texto"]]

    # Fallback / compatibilidad con estructura previa de 4 bloques (guion 1 y 2)
    hook_text = guion["hook"].strip()
    p1 = guion["puntos"][0]
    p1_text = f"{p1.get('herramienta_o_tip', '')} {p1.get('explicacion', '')} {p1.get('opinion_byte', '')}".strip()
    p2 = guion["puntos"][1]
    p2_text = f"{p2.get('herramienta_o_tip', '')} {p2.get('explicacion', '')} {p2.get('opinion_byte', '')}".strip()
    cierre_text = guion["cierre"].strip()

    return [
        {"tipo": "hook", "texto": hook_text},
        {"tipo": "punto_1", "texto": p1_text},
        {"tipo": "punto_2", "texto": p2_text},
        {"tipo": "cierre", "texto": cierre_text}
    ]


def concatenar_texto_completo(bloques: List[Dict[str, str]]) -> str:
    """
    Concatena los bloques narrativos con fluidez.
    Si está presente 'cold_open', une todo de forma continua y veloz.
    Si están presentes 'hook' y 'problema', se concatenan como narración continua
    sin puntos intermedios para máxima fluidez en ElevenLabs.
    """
    if bloques and bloques[0]["tipo"] == "cold_open":
        return " ".join(b["texto"].strip() for b in bloques)

    if len(bloques) >= 2 and bloques[0]["tipo"] == "hook" and bloques[1]["tipo"] == "problema":
        h_txt = bloques[0]["texto"].strip()
        p_txt = bloques[1]["texto"].strip()
        if h_txt.endswith("?") or h_txt.endswith(",") or h_txt.endswith("!"):
            escena_prob_txt = f"{h_txt} {p_txt}"
        else:
            escena_prob_txt = f"{h_txt}, {p_txt}"

        resto_bloques = [escena_prob_txt] + [b["texto"].strip() for b in bloques[2:]]
        return "\n\n".join(resto_bloques)

    return "\n\n".join(b["texto"].strip() for b in bloques)


# ===========================================================================
# PASO 2: Audio y Alignment de ElevenLabs (con Sistema de Caché Inteligente)
# ===========================================================================
VOICE_SETTINGS_DEFAULT: Dict[str, Any] = {
    "stability": 0.45,
    "similarity_boost": 0.80,
    "style": 0.05,
    "use_speaker_boost": True,
    "speed": 1.15
}

CACHE_AUDIO_DIR = DIR_CACHE
CACHE_INDEX_FILE = DIR_CACHE_INDEX


def calcular_hash_audio(
    texto_completo: str,
    voice_id: str,
    model_id: str = "eleven_multilingual_v2",
    voice_settings: Optional[Dict[str, Any]] = None
) -> str:
    """
    Calcula un hash SHA-256 determinista con todos los factores que alteran el audio:
    - Texto completo del guion concatenado.
    - ID de la voz (voice_id).
    - Modelo usado (model_id).
    - Parámetros de la voz (speed, stability, style, etc.).
    """
    if voice_settings is None:
        voice_settings = VOICE_SETTINGS_DEFAULT

    payload_hash = {
        "text": texto_completo.strip(),
        "voice_id": str(voice_id).strip(),
        "model_id": str(model_id).strip(),
        "voice_settings": voice_settings
    }
    serializado = json.dumps(payload_hash, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(serializado.encode("utf-8")).hexdigest()


def cargar_indice_cache(ruta_indice: Path = CACHE_INDEX_FILE) -> Dict[str, Any]:
    """Carga el índice JSON de la caché si existe; si no, retorna dict vacío."""
    if ruta_indice.exists():
        try:
            with open(ruta_indice, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"No se pudo leer índice de caché {ruta_indice}: {e}")
    return {}


def guardar_indice_cache(indice: Dict[str, Any], ruta_indice: Path = CACHE_INDEX_FILE) -> None:
    """Guarda el índice JSON de la caché en disco."""
    ruta_indice.parent.mkdir(parents=True, exist_ok=True)
    with open(ruta_indice, "w", encoding="utf-8") as f:
        json.dump(indice, f, indent=2, ensure_ascii=False)


def generar_audio_con_timestamps_elevenlabs(
    texto_completo: str,
    voice_id: str,
    api_key: Optional[str] = None,
    model_id: str = "eleven_multilingual_v2",
    voice_settings: Optional[Dict[str, Any]] = None,
    ruta_audio: Union[str, Path] = "narracion_real.mp3",
    ruta_alignment: Union[str, Path] = "alignment_real.json",
    cache_dir: Union[str, Path] = CACHE_AUDIO_DIR
) -> Tuple[Path, Dict[str, Any]]:
    """
    Gestiona la obtención de audio y alignment con sistema de caché estricto:
    1. Calcula SHA-256 de (guion + voz + modelo + settings).
    2. Si existe en índice y archivos existen en disco -> USÓ CACHÉ (no gasta créditos).
    3. Si NO existe -> LLAMÓ A LA API (gasta créditos nuevos), guarda en caché y actualiza el índice.
    """
    ruta_audio = Path(ruta_audio)
    ruta_alignment = Path(ruta_alignment)
    cache_dir = Path(cache_dir)
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_index_path = cache_dir / "cache_audio_index.json"

    if voice_settings is None:
        voice_settings = VOICE_SETTINGS_DEFAULT

    # 1. Calcular hash determinista
    audio_hash = calcular_hash_audio(texto_completo, voice_id, model_id, voice_settings)
    indice = cargar_indice_cache(cache_index_path)

    cached_audio_path = cache_dir / f"{audio_hash}.mp3"
    cached_alignment_path = cache_dir / f"{audio_hash}_alignment.json"

    # 2. Comprobar si existe en caché y los archivos están en disco
    if audio_hash in indice:
        entry = indice[audio_hash]
        f_audio = Path(entry.get("archivo_audio", cached_audio_path))
        if not f_audio.is_absolute() and not f_audio.exists():
            f_audio = DIR_RAIZ / f_audio
        if not f_audio.exists():
            f_audio = cached_audio_path

        f_align = Path(entry.get("archivo_alignment", cached_alignment_path))
        if not f_align.is_absolute() and not f_align.exists():
            f_align = DIR_RAIZ / f_align
        if not f_align.exists():
            f_align = cached_alignment_path

        if f_audio.exists() and f_align.exists() and f_audio.stat().st_size > 10000:
            with open(f_align, "r", encoding="utf-8") as f:
                alignment = json.load(f)

            if f_audio.resolve() != ruta_audio.resolve():
                shutil.copyfile(f_audio, ruta_audio)
            if f_align.resolve() != ruta_alignment.resolve():
                shutil.copyfile(f_align, ruta_alignment)

            peso_kb = ruta_audio.stat().st_size / 1024.0

            # 5. MENSAJE EN CONSOLA BIEN VISIBLE: USÓ CACHÉ
            print("\n" + "=" * 78)
            print("  >>> [AUDIO CACHE] USO CACHE (no gasto creditos) <<<")
            print("=" * 78)
            print(f"  * Hash SHA-256 : {audio_hash}")
            print(f"  * Audio reusado: {f_audio.name} ({peso_kb:.2f} KB) -> {ruta_audio.name}")
            print(f"  * Alignment    : {f_align.name} -> {ruta_alignment.name}")
            dur_real = float(alignment["character_end_times_seconds"][-1]) if (alignment and "character_end_times_seconds" in alignment and alignment["character_end_times_seconds"]) else 0.0
            num_pal = len(texto_completo.split())
            ppm_cache = (num_pal / (dur_real / 60.0)) if dur_real > 0 else 0.0
            print(f"  * Duracion loc : {dur_real:.2f} s | {num_pal} palabras ({ppm_cache:.1f} PPM)")
            print(f"  * Configuracion: Voice={voice_id} | Speed={voice_settings.get('speed', 1.0)}")
            print("=" * 78 + "\n")
            logger.info(f"[AUDIO CACHE] Audio cargado desde cache (hash {audio_hash[:12]}...).")

            return ruta_audio, alignment

    # 4. SOLO llamar a la API real si el hash no existe todavía
    if not api_key:
        raise RuntimeError(
            "Se requiere ELEVENLABS_API_KEY para generar nuevo audio porque no se encontro en cache."
        )

    # 5. MENSAJE EN CONSOLA BIEN VISIBLE: LLAMÓ A LA API
    print("\n" + "=" * 78)
    print("  >>> [AUDIO API] LLAMO A LA API (gasto creditos nuevos) <<<")
    print("=" * 78)
    print(f"  * Hash nuevo   : {audio_hash}")
    print(f"  * Voice ID     : {voice_id} | Model: {model_id}")
    print(f"  * Settings     : {voice_settings}")
    print(f"  * Texto preview: {texto_completo[:70].replace(chr(10), ' ')}...")
    print("=" * 78 + "\n")

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/with-timestamps"
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json"
    }
    payload = {
        "text": texto_completo,
        "model_id": model_id,
        "voice_settings": voice_settings
    }

    logger.info(f"Llamando a ElevenLabs API ({url})...")
    response = requests.post(url, headers=headers, json=payload, timeout=90)

    print("\n" + "=" * 65)
    print(f"[ELEVENLABS] RESPUESTA HTTP: Codigo Status = {response.status_code}")
    print("=" * 65)

    if response.status_code != 200:
        logger.error(f"Error de autenticacion/llamada ElevenLabs [{response.status_code}]:\n{response.text}")
        raise RuntimeError(
            f"Fallo en ElevenLabs: HTTP {response.status_code} - {response.text}"
        )

    data = response.json()
    audio_base64 = data.get("audio_base64")
    alignment = data.get("alignment")

    if not audio_base64:
        raise RuntimeError("ElevenLabs respondio con status 200 pero sin campo 'audio_base64'.")

    audio_bytes = base64.b64decode(audio_base64)
    peso_kb = len(audio_bytes) / 1024.0

    print(f"[ELEVENLABS] AUDIO DESCARGADO: {peso_kb:.2f} KB")
    if peso_kb < 10.0:
        raise RuntimeError(f"El audio descargado pesa solo {peso_kb:.2f} KB (esperado > 50 KB para locución real).")

    # Calcular duración real y palabras por minuto (PPM)
    duracion_real = 0.0
    if alignment and "character_end_times_seconds" in alignment and alignment["character_end_times_seconds"]:
        duracion_real = float(alignment["character_end_times_seconds"][-1])
    num_palabras = len(texto_completo.split())
    ppm = (num_palabras / (duracion_real / 60.0)) if duracion_real > 0 else 0.0
    print(f"[ELEVENLABS] DURACION LOCUCION: {duracion_real:.2f} s")
    print(f"[ELEVENLABS] PALABRAS TOTALES : {num_palabras} palabras")
    print(f"[ELEVENLABS] PALABRAS POR MINUTO (PPM): {ppm:.1f} PPM")

    # Guardar en directorio de caché
    with open(cached_audio_path, "wb") as f:
        f.write(audio_bytes)

    with open(cached_alignment_path, "w", encoding="utf-8") as f:
        json.dump(alignment, f, indent=2, ensure_ascii=False)

    # Actualizar índice JSON
    indice[audio_hash] = {
        "archivo_audio": str(cached_audio_path.as_posix()),
        "archivo_alignment": str(cached_alignment_path.as_posix()),
        "fecha_creacion": datetime.datetime.now().isoformat(),
        "voice_id": voice_id,
        "model_id": model_id,
        "voice_settings": voice_settings,
        "texto_preview": texto_completo[:70].replace("\n", " ") + "..."
    }
    guardar_indice_cache(indice, cache_index_path)

    # Copiar a rutas finales solicitadas
    shutil.copyfile(cached_audio_path, ruta_audio)
    shutil.copyfile(cached_alignment_path, ruta_alignment)

    print(f"[AUDIO CACHE] Guardado nuevo audio en: {cached_audio_path.name}")
    print(f"[AUDIO CACHE] Índice actualizado: {cache_index_path.name}")
    logger.info(f"Audio real y alignment de ElevenLabs guardados exitosamente ({peso_kb:.2f} KB).")
    return ruta_audio, alignment


def sintetizar_audio_y_alignment_fallback(
    bloques: List[Dict[str, str]],
    ruta_audio: Path,
    ruta_alignment: Path
) -> Tuple[Path, Dict[str, Any]]:
    """
    Fallback explícito cuando no hay API Key de ElevenLabs configurada.
    Emite un warning muy visible para no confundir con una locución real.
    """
    print("\n" + "#" * 80)
    print("[!] [!] [!]   ADVERTENCIA CRITICA: USANDO AUDIO SINTETICO, NO ES VOZ REAL   [!] [!] [!]")
    print("No se encontro ELEVENLABS_API_KEY valida. El audio generado sera un tono de prueba.")
    print("#" * 80 + "\n")
    logger.warning("[!] USANDO AUDIO SINTETICO, NO ES VOZ REAL [!]")
    # Duraciones calibradas al ritmo de habla natural para cada bloque
    # Hook: ~4.5s, Punto 1: ~9.2s, Punto 2: ~9.5s, Cierre: ~3.8s -> Total ~27.0s
    duraciones_bloque = [4.5, 9.2, 9.5, 3.8]

    all_chars: List[str] = []
    all_starts: List[float] = []
    all_ends: List[float] = []

    t_cursor = 0.0

    for idx, (b, dur_b) in enumerate(zip(bloques, duraciones_bloque)):
        texto = b["texto"]
        # Pausa entre bloques de 0.35s con separación explícita de caracteres
        if idx > 0:
            all_chars.append(" ")
            all_starts.append(round(t_cursor, 3))
            t_cursor += 0.35
            all_ends.append(round(t_cursor, 3))

        t_inicio_bloque = t_cursor
        n = len(texto)
        dt = dur_b / max(1, n)

        for i, ch in enumerate(texto):
            s = t_inicio_bloque + (i * dt)
            e = s + dt
            all_chars.append(ch)
            all_starts.append(round(s, 3))
            all_ends.append(round(e, 3))

        t_cursor = t_inicio_bloque + dur_b

    duracion_total = round(t_cursor + 0.3, 3)

    # Generar audio de duración exacta con FFmpeg
    ruta_audio.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "ffmpeg", "-y",
        "-f", "lavfi",
        "-i", f"sine=frequency=440:beep_factor=3:sample_rate=44100:duration={duracion_total}",
        "-c:a", "libmp3lame",
        "-b:a", "192k",
        str(ruta_audio)
    ]
    subprocess.run(cmd, check=True, capture_output=True)

    alignment = {
        "characters": all_chars,
        "character_start_times_seconds": all_starts,
        "character_end_times_seconds": all_ends
    }

    with open(ruta_alignment, "w", encoding="utf-8") as f:
        json.dump(alignment, f, indent=2, ensure_ascii=False)

    logger.info(f"Audio y alignment generados: {ruta_audio.name} ({duracion_total:.2f}s)")
    return ruta_audio, alignment


# ===========================================================================
# PASO 3: Segmentación real
# ===========================================================================
def calcular_segmentos_reales(
    alignment: Dict[str, Any],
    bloques: List[Dict[str, str]],
    duracion_audio: float
) -> List[Dict[str, Any]]:
    """
    Calcula timestamps exactos de inicio/fin para las escenas visuales a partir de alignment.
    Si se reciben 6 bloques (hook, problema, punto_1, punto_2, resultado, cierre):
    - Mapea 'hook' + 'problema' a UNA sola escena visual ('escena_problema'),
      concatenando ambos textos como narración continua pero conservando
      sus tiempos individuales dentro del segmento para los subtítulos.
    - 'demostracion[0]' -> escena 'punto_1'
    - 'demostracion[1]' -> escena 'punto_2'
    - 'resultado' -> escena 'resultado' (nueva)
    - 'cierre' -> escena 'cierre'
    Generando exactamente 5 rangos de tiempo contiguos sin solapamientos.
    """
    chars = alignment.get("characters", [])
    starts = alignment.get("character_start_times_seconds", [])
    ends = alignment.get("character_end_times_seconds", [])

    full_aligned_text = "".join(chars)
    tiempos_bloques: List[Dict[str, Any]] = []

    pos_cursor = 0
    num_bloques = len(bloques)

    # 1. Hallar inicio y fin real de cada uno de los bloques narrativos
    for i, bloque in enumerate(bloques):
        tipo = bloque["tipo"]
        texto = bloque["texto"].strip()

        palabras = texto.split()
        p_inicio = re.sub(r"^[^\w]+", "", palabras[0])
        p_fin = re.sub(r"[^\w]+$", "", palabras[-1])

        idx_inicio = full_aligned_text.find(p_inicio, pos_cursor)
        if idx_inicio == -1:
            idx_inicio = pos_cursor

        idx_fin_palabra = full_aligned_text.find(p_fin, idx_inicio)
        if idx_fin_palabra != -1:
            idx_fin = idx_fin_palabra + len(p_fin)
        else:
            idx_fin = idx_inicio + len(texto)

        idx_fin = min(idx_fin, len(chars) - 1)

        t_inicio = starts[idx_inicio] if idx_inicio < len(starts) else 0.0
        t_fin = ends[idx_fin] if idx_fin < len(ends) else duracion_audio

        if i == 0:
            t_inicio = 0.0
        if i == num_bloques - 1:
            t_fin = max(t_fin, duracion_audio)

        pos_cursor = idx_fin

        tiempos_bloques.append({
            "tipo": tipo,
            "texto": texto,
            "inicio": round(t_inicio, 3),
            "fin": round(t_fin, 3)
        })

    # 2. Si es estructura con cold_open (7 bloques) -> Mantener 7 escenas cortas e hiperdinámicas
    if len(tiempos_bloques) == 7 and tiempos_bloques[0]["tipo"] == "cold_open":
        segmentos_detectados = tiempos_bloques
        for j in range(len(segmentos_detectados) - 1):
            actual = segmentos_detectados[j]
            siguiente = segmentos_detectados[j + 1]
            corte = round((actual["fin"] + siguiente["inicio"]) / 2.0, 3)
            actual["fin"] = corte
            siguiente["inicio"] = corte
        segmentos_detectados[0]["inicio"] = 0.0
        segmentos_detectados[-1]["fin"] = round(duracion_audio, 3)
        return segmentos_detectados

    # 3. Si es la estructura de 6 bloques -> Convertir a las 5 escenas visuales
    if len(tiempos_bloques) == 6 and tiempos_bloques[0]["tipo"] == "hook" and tiempos_bloques[1]["tipo"] == "problema":
        b_hook = tiempos_bloques[0]
        b_prob = tiempos_bloques[1]
        b_p1 = tiempos_bloques[2]
        b_p2 = tiempos_bloques[3]
        b_res = tiempos_bloques[4]
        b_cie = tiempos_bloques[5]

        # Cortes equidistantes entre bloques contiguos
        corte_prob_p1 = round((b_prob["fin"] + b_p1["inicio"]) / 2.0, 3)
        corte_p1_p2 = round((b_p1["fin"] + b_p2["inicio"]) / 2.0, 3)
        corte_p2_res = round((b_p2["fin"] + b_res["inicio"]) / 2.0, 3)
        corte_res_cie = round((b_res["fin"] + b_cie["inicio"]) / 2.0, 3)

        segmentos_finales = [
            {
                "tipo": "escena_problema",
                "texto": f"{b_hook['texto']} {b_prob['texto']}",
                "inicio": 0.0,
                "fin": corte_prob_p1,
                "bloques_internos": [b_hook, b_prob]
            },
            {
                "tipo": "punto_1",
                "texto": b_p1["texto"],
                "inicio": corte_prob_p1,
                "fin": corte_p1_p2
            },
            {
                "tipo": "punto_2",
                "texto": b_p2["texto"],
                "inicio": corte_p1_p2,
                "fin": corte_p2_res
            },
            {
                "tipo": "resultado",
                "texto": b_res["texto"],
                "inicio": corte_p2_res,
                "fin": corte_res_cie
            },
            {
                "tipo": "cierre",
                "texto": b_cie["texto"],
                "inicio": corte_res_cie,
                "fin": round(duracion_audio, 3)
            }
        ]
        return segmentos_finales

    # 3. Fallback / compatibilidad para guiones de 4 bloques (Video 1 y 2)
    segmentos_detectados = tiempos_bloques
    for j in range(len(segmentos_detectados) - 1):
        actual = segmentos_detectados[j]
        siguiente = segmentos_detectados[j + 1]
        corte = round((actual["fin"] + siguiente["inicio"]) / 2.0, 3)
        actual["fin"] = corte
        siguiente["inicio"] = corte

    segmentos_detectados[-1]["fin"] = round(duracion_audio, 3)
    return segmentos_detectados


def extraer_frames_preview(
    ruta_mp4: Path,
    duracion_total: float,
    output_dir: Path,
    segmentos: Optional[List[Dict[str, Any]]] = None
) -> List[Path]:
    """Extrae capturas clave para validar las animaciones de cada escena."""
    output_dir.mkdir(parents=True, exist_ok=True)
    puntos = []

    if segmentos and len(segmentos) >= 5:
        # Estructura de 5 escenas visuales
        for i, seg in enumerate(segmentos):
            t_ini = seg["inicio"]
            tipo_nom = seg["tipo"]
            dur_seg = seg["fin"] - t_ini
            puntos.append((f"frame_{i+1:02d}_{tipo_nom}_entrada.png", round(t_ini + min(0.20, dur_seg * 0.1), 2)))
            puntos.append((f"frame_{i+1:02d}_{tipo_nom}_reposo.png", round(t_ini + min(2.00, dur_seg * 0.6), 2)))
    elif segmentos and len(segmentos) >= 4:
        puntos.append(("frame_01_hook_entrada_bounce.png", 0.20))
        puntos.append(("frame_02_hook_flotando.png", 2.20))
        t_p1 = segmentos[1]["inicio"]
        puntos.append(("frame_03_punto1_slide_in.png", round(t_p1 + 0.20, 2)))
        puntos.append(("frame_04_punto1_flotando.png", round(t_p1 + 2.20, 2)))
        t_p2 = segmentos[2]["inicio"]
        puntos.append(("frame_05_punto2_slide_in.png", round(t_p2 + 0.20, 2)))
        puntos.append(("frame_06_punto2_flotando.png", round(t_p2 + 2.20, 2)))
        t_cierre = segmentos[3]["inicio"]
        puntos.append(("frame_07_cierre_rebote.png", round(t_cierre + 0.20, 2)))
    else:
        puntos.append(("frame_mitad.png", duracion_total / 2.0))
        puntos.append(("frame_final.png", max(0.5, duracion_total - 1.0)))

    rutas = []
    for nom, t in puntos:
        out = output_dir / nom
        cmd = ["ffmpeg", "-y", "-ss", f"{t:.3f}", "-i", str(ruta_mp4), "-frames:v", "1", "-update", "1", "-q:v", "2", str(out)]
        subprocess.run(cmd, check=True, capture_output=True)
        rutas.append(out)
    return rutas


def cargar_guion(ruta_arg: Optional[Union[str, Path]] = None) -> Tuple[Dict[str, Any], Dict[str, Path], str, Optional[Path]]:
    """
    Carga el guión JSON y determina la estructura de carpetas (entrada, intermedios, final).
    Soporta rutas relativas/absolutas o autodetecta en guiones/ y videos/.
    Devuelve (guion, v_paths, nombre_base, ruta_guion_archivo); la ruta es
    None en el fallback de prueba_real (no hay archivo que validar).
    """
    import sys
    if ruta_arg is None:
        # Primer argumento posicional (ignora flags --xxx como --forzar-fondos)
        posicionales = [a for a in sys.argv[1:] if not a.startswith("-")]
        if posicionales:
            ruta_arg = posicionales[0]
        elif (DIR_GUIONES / "guion_03_tareas.json").exists():
            ruta_arg = DIR_GUIONES / "guion_03_tareas.json"
        elif (DIR_GUIONES / "guion_02_reuniones.json").exists():
            ruta_arg = DIR_GUIONES / "guion_02_reuniones.json"

    p = None
    if ruta_arg:
        p = ruta_guion(ruta_arg)
        if p is None and Path(ruta_arg).exists():
            p = Path(ruta_arg).resolve()

    if p and p.exists():
        with open(p, "r", encoding="utf-8") as f:
            guion = json.load(f)

        stem = p.stem
        nombre_base, carpeta_video = resolver_carpeta(stem)
        v_paths = ruta_video(carpeta_video)

        return guion, v_paths, nombre_base, p

    v_paths = ruta_video("video_01_bandeja_correo")
    return GUION_REAL, v_paths, "prueba_real", None


# ===========================================================================
# EJECUCIÓN PRINCIPAL MULTI-GUIÓN
# ===========================================================================
def main() -> int:
    logger.info("=================================================================")
    logger.info("EJECUTANDO PIPELINE MULTI-GUIÓN (AISLADO POR PROYECTO)")
    logger.info("=================================================================")

    api_key = os.environ.get("ELEVENLABS_API_KEY")
    voice_id = os.environ.get("ELEVENLABS_VOICE_ID", "nPczCjzI2devNBz1zQrb")

    guion, v_paths, nombre_base, ruta_guion_archivo = cargar_guion()
    dir_proyecto = v_paths["base"]
    dir_entrada = v_paths["entrada"]
    dir_intermedios = v_paths["intermedios"]
    dir_final = v_paths["final"]

    # Flags CLI: --forzar-fondos regenera los MP4 de fondo aunque existan en caché
    # (necesario tras editar planos/configs; el audio sigue usando su caché normal)
    forzar_fondos = "--forzar-fondos" in sys.argv
    # Escape de las validaciones automáticas (pre-vuelo/post-vuelo)
    saltar_validacion = "--saltar-validacion" in sys.argv
    sin_chequeo_final = "--sin-chequeo-final" in sys.argv

    mockup_sugerido = guion.get("mockup_sugerido", "bandeja_correo")

    print(f"\n[CONFIGURACIÓN DE PRODUCCIÓN]")
    print(f"  • Guión:            {nombre_base} ({mockup_sugerido})")
    print(f"  • Carpeta proyecto: {dir_proyecto.resolve()}")
    print(f"  • Entrada:          {dir_entrada.resolve()}")
    print(f"  • Intermedios:      {dir_intermedios.resolve()}")
    print(f"  • Video de salida:  {dir_final / f'video_{nombre_base}.mp4'}")
    print(f"  • Fondos:           {'FORZADOS (--forzar-fondos)' if forzar_fondos else 'caché si existen'}\n")

    if not saltar_validacion:
        if pre_vuelo(ruta_guion_archivo, dir_proyecto) != 0:
            print("\n[PIPELINE] Abortado por el PRE-VUELO (sin créditos gastados).")
            return 1

    bloques = construir_bloques_narrativos(guion)
    texto_completo = concatenar_texto_completo(bloques)

    ruta_audio = dir_entrada / f"narracion_{nombre_base}.mp3"
    ruta_alignment = dir_entrada / f"alignment_{nombre_base}.json"

    # 1. Obtener o generar audio y alignment (usando caché inteligente)
    audio_hash_preliminar = calcular_hash_audio(
        texto_completo=texto_completo,
        voice_id=voice_id,
        model_id="eleven_multilingual_v2",
        voice_settings=VOICE_SETTINGS_DEFAULT
    )
    cache_existente = cargar_indice_cache()
    cached_en_disco = audio_hash_preliminar in cache_existente

    if api_key or cached_en_disco or (ruta_audio.exists() and ruta_alignment.exists()):
        ruta_audio, alignment = generar_audio_con_timestamps_elevenlabs(
            texto_completo=texto_completo,
            voice_id=voice_id,
            api_key=api_key,
            model_id="eleven_multilingual_v2",
            voice_settings=VOICE_SETTINGS_DEFAULT,
            ruta_audio=ruta_audio,
            ruta_alignment=ruta_alignment
        )
    else:
        ruta_audio, alignment = sintetizar_audio_y_alignment_fallback(
            bloques=bloques,
            ruta_audio=ruta_audio,
            ruta_alignment=ruta_alignment
        )

    # -------------------------------------------------------------
    # DIAGNÓSTICO 1: Impresión y confirmación visual de caracteres
    # -------------------------------------------------------------
    reporte_chars = imprimir_diagnostico_caracteres(alignment)
    chars_list = alignment.get("characters", [])
    logger.info("Lista de primeros 80 caracteres de alignment:")
    logger.info(f"{chars_list[:80]}")

    # -------------------------------------------------------------
    # DIAGNÓSTICO 2, 3 y 4: Exportar tabla de tiempos en TXT
    # -------------------------------------------------------------
    ruta_txt_tiempos = dir_intermedios / f"tiempos_{nombre_base}.txt"
    exportar_tabla_tiempos_palabras(alignment, ruta_txt_tiempos)

    with open(ruta_txt_tiempos, "r", encoding="utf-8") as f:
        lineas_tabla = f.readlines()
    print("\n--- EXTRACTO DE LA TABLA DE TIEMPOS \\k CALCULADOS ---")
    for l in lineas_tabla[:22]:
        print(l.rstrip())
    print("...\n")

    # -------------------------------------------------------------
    # PASO 3: Segmentación real y métricas de ritmo
    # -------------------------------------------------------------
    probe_cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", str(ruta_audio)]
    p_res = subprocess.run(probe_cmd, capture_output=True, text=True, check=True)
    duracion_audio = float(json.loads(p_res.stdout)["format"]["duration"])
    num_palabras = len(texto_completo.split())
    duracion_min = duracion_audio / 60.0
    ppm = num_palabras / duracion_min if duracion_min > 0 else 0.0

    print("\n" + "=" * 65)
    print(f" [MÉTRICA VELOCIDAD] Palabras: {num_palabras} | Duración: {duracion_audio:.2f}s ({duracion_min:.3f} min) | PPM: {ppm:.1f}")
    print("=" * 65 + "\n")

    segmentos_reales = calcular_segmentos_reales(alignment, bloques, duracion_audio)

    # -------------------------------------------------------------
    # PASO 4: Imágenes de Byte y remoción de fondo
    # -------------------------------------------------------------
    dir_transparentes = DIR_BYTE_TRANSPARENTES
    dir_transparentes.mkdir(parents=True, exist_ok=True)

    imagenes_base = sprites_para(nombre_base, mockup_sugerido)

    rutas_imagenes = []
    for clave, ruta_in in imagenes_base:
        ruta_out = dir_transparentes / f"{clave}_{nombre_base}_transparente.png"
        if not (ruta_out.exists() and ruta_out.stat().st_size > 5000):
            logger.info(f"Procesando '{ruta_in.name}' -> '{ruta_out.name}'...")
            quitar_fondo(ruta_in, ruta_out)
        else:
            logger.info(f"Usando sprite existente '{ruta_out.name}'...")
        rutas_imagenes.append(ruta_out)

    # Si se usan arquetipos cinematográficos con Byte integrado, la capa de overlay de FFmpeg es transparente
    if overlay_vacio(nombre_base):
        p_vacio = dir_transparentes / "transparente_vacio.png"
        if not p_vacio.exists():
            Image.new("RGBA", (1080, 1920), (0, 0, 0, 0)).save(p_vacio)
        rutas_imagenes_overlay = [p_vacio for _ in rutas_imagenes]
    else:
        rutas_imagenes_overlay = rutas_imagenes

    # -------------------------------------------------------------
    # PASO 4.1: Generar fondos interactivos según plantilla
    # -------------------------------------------------------------
    rutas_fondos = []
    dir_fondos = dir_intermedios / "fondos"
    dir_fondos.mkdir(parents=True, exist_ok=True)

    cfg_fondos = config_de_fondos(nombre_base, mockup_sugerido)
    if cfg_fondos is not None:
        modo = "FORZADO" if forzar_fondos else "caché si existen"
        print(f"\n[MOCKUP] Generando fondos de {cfg_fondos.etiqueta_fondos} ({modo})...")
        rutas_fondos = generar_fondos_del_video(cfg_fondos, segmentos_reales, dir_fondos, forzar=forzar_fondos)


    # -------------------------------------------------------------
    # PASO 4.2: Actualizar animaciones de Byte para las duraciones reales
    # -------------------------------------------------------------
    try:
        try:
            from src.generar_animacion_byte import generar_video_byte_escena
        except ImportError:
            from generar_animacion_byte import generar_video_byte_escena
        dir_anim_byte = dir_intermedios / "animaciones_byte"
        dir_anim_byte.mkdir(parents=True, exist_ok=True)
        for i, seg in enumerate(segmentos_reales):
            dur_esc = (seg["fin"] - seg["inicio"]) + 0.15
            p_mov = dir_anim_byte / f"byte_escena_{i}_animado.mov"
            generar_video_byte_escena(i, dur_esc, p_mov, sprite_path=rutas_imagenes_overlay[i])
    except Exception as e:
        logger.warning(f"No se pudieron regenerar animaciones de Byte: {e}")

    # -------------------------------------------------------------
    # PASO 5: Generar subtítulos .ass en amarillo limpio y ensamblar video
    # -------------------------------------------------------------
    ruta_ass = dir_intermedios / f"subtitulos_{nombre_base}.ass"
    generar_ass(
        alignment=alignment,
        segmentos=segmentos_reales,
        ruta_salida=ruta_ass,
        max_words_per_chunk=3
    )

    if not saltar_validacion:
        if chequear_ass(ruta_ass) != 0:
            print("\n[PIPELINE] Abortado por el CHEQUEO ASS (subtítulos fuera de especificación).")
            return 1

    ruta_mp4_base = dir_intermedios / f"video_{nombre_base}_base.mp4"
    ensamblar_video(
        imagenes=rutas_imagenes_overlay,
        audio=ruta_audio,
        archivo_ass=ruta_ass,
        duracion_total=duracion_audio,
        segmentos=segmentos_reales,
        ruta_salida=ruta_mp4_base,
        fondos=rutas_fondos if rutas_fondos else None,
        fade_duration=0.15
    )

    # -------------------------------------------------------------
    # PASO 6: Post-procesamiento: aceleración sincronizada (1.12x)
    # -------------------------------------------------------------
    factor_aceleracion = 1.12
    ruta_mp4 = dir_final / f"video_{nombre_base}.mp4"
    acelerar_video(
        ruta_video_entrada=ruta_mp4_base,
        factor=factor_aceleracion,
        ruta_salida=ruta_mp4
    )

    duracion_esperada_acelerada = duracion_audio / factor_aceleracion
    ppm_acelerado = num_palabras / (duracion_esperada_acelerada / 60.0)

    print("\n" + "=" * 65)
    print(f" [POST-PROCESAMIENTO] Aceleración {factor_aceleracion}x aplicada con FFmpeg:")
    print(f"  • Duración base original  : {duracion_audio:.2f}s (PPM: {ppm:.1f})")
    print(f"  • Duración final acelerada: {duracion_esperada_acelerada:.2f}s (PPM: {ppm_acelerado:.1f})")
    print("=" * 65 + "\n")

    # -------------------------------------------------------------
    # PASO 7: Validación y Captura de frames del video acelerado
    # -------------------------------------------------------------
    es_valido = validar_output(ruta_mp4, duracion_esperada=duracion_esperada_acelerada, tolerancia=0.15)
    segmentos_acelerados = [
        {"tipo": s["tipo"], "inicio": s["inicio"] / factor_aceleracion, "fin": s["fin"] / factor_aceleracion}
        for s in segmentos_reales
    ]
    dir_capturas = dir_intermedios / "capturas_frames"
    dir_capturas.mkdir(parents=True, exist_ok=True)
    frames = extraer_frames_preview(
        ruta_mp4=ruta_mp4,
        duracion_total=duracion_esperada_acelerada,
        output_dir=dir_capturas,
        segmentos=segmentos_acelerados
    )

    print("\n" + "=" * 65)
    print("REPORTE FINAL END-TO-END:")
    print("=" * 65)
    print(f"  • Video de salida:   {ruta_mp4.resolve()}")
    print(f"  • Subtítulos ASS:    {Path(ruta_ass).resolve()}")
    print(f"  • Tabla de tiempos:  {ruta_txt_tiempos.resolve()}")
    print(f"  • Duración video:    {duracion_esperada_acelerada:.2f} segundos (factor={factor_aceleracion}x)")
    print(f"  • Ritmo resultante:  {ppm_acelerado:.1f} palabras por minuto (PPM)")
    print(f"  • Validación ffprobe:{'APROBADA ' if es_valido else 'FALLIDA '}")
    print("  • Capturas de frames extraídas:")
    for f in frames:
        print(f"      - {f.name} ({f.resolve()})")
    print("=" * 65)

    codigo_final = 0
    if not sin_chequeo_final:
        codigo_final = post_vuelo(ruta_mp4)
    return codigo_final


if __name__ == "__main__":
    sys.exit(main())
