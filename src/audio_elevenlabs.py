r"""
audio_elevenlabs.py
-------------------
Audio y alignment de ElevenLabs con sistema de caché inteligente (SHA-256)
y fallback sintético sin API key.

Extraído verbatim de `pruebas/prueba_end_to_end.py` (PASO 2) durante la
partición del monolito; sin cambios de comportamiento.

La función `generar_audio_con_timestamps_elevenlabs` solo llama a la API
(gasta créditos) cuando el hash NO está en la caché; con caché en disco
reutiliza el MP3 y alignment existentes.
"""

from __future__ import annotations

import base64
import datetime
import hashlib
import json
import logging
import shutil
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

import requests

from src.rutas import DIR_RAIZ, DIR_CACHE, DIR_CACHE_INDEX

logger = logging.getLogger(__name__)

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
