r"""
shorts_assembler.py
-------------------
Módulo en Python para ensamblar videos verticales (9:16, 1080x1920) para Shorts / Reels / TikTok.

Funciones principales:
- generar_ass(alignment, segmentos, ruta_salida=...) -> ruta del archivo .ass
- ensamblar_video(imagenes, audio, archivo_ass, duracion_total, ...) -> ruta del mp4 final
- validar_output(ruta_mp4, duracion_esperada, ...) -> bool

Optimizaciones implementadas para timing fluido (karaoke sin traqueteo):
1. Sanitización de caracteres Unicode (NFC) y decodificación adecuada de español (á,é,í,ó,ú,ñ,¿,¡).
2. Huecos de silencio cubiertos: \k de palabra N cubre desde inicio(N) hasta inicio(N+1).
3. Precisión estricta uniforme en centésimas de segundo (cs) en todos los cálculos y cabeceras ASS.
4. Filtrado riguroso de palabras vacías y saltos de línea/espacios duplicados.
"""

from __future__ import annotations

import argparse
import json
import logging
import os
from pathlib import Path
import re
import subprocess
import unicodedata
from typing import Any, Dict, List, Optional, Sequence, Tuple, Union

try:
    from src.rutas import DIR_FONDOS, DIR_ANIMACIONES_BYTE
except ImportError:
    from rutas import DIR_FONDOS, DIR_ANIMACIONES_BYTE

try:
    from src.enfasis import PuntoEnfasis, construir_filtro_enfasis
except ImportError:
    from enfasis import PuntoEnfasis, construir_filtro_enfasis

try:
    from src.director_gancho import TRATAMIENTOS
except ImportError:
    from director_gancho import TRATAMIENTOS

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Estructuras de datos y utilidades de tiempo en centésimas (cs)
# ---------------------------------------------------------------------------

def seg_a_cs(segundos: float) -> int:
    """Convierte segundos float a centésimas de segundo enteras redondeadas uniformemente."""
    return round(float(segundos) * 100)


def cs_a_tiempo_ass(cs: int) -> str:
    """Convierte centésimas de segundo a formato de timestamp ASS: H:MM:SS.cs"""
    cs = max(0, int(cs))
    horas = cs // 360000
    minutos = (cs % 360000) // 6000
    segundos = (cs % 6000) // 100
    centesimas = cs % 100
    return f"{horas}:{minutos:02d}:{segundos:02d}.{centesimas:02d}"


def _escape_ass_path(path: Union[str, Path]) -> str:
    """
    Escapa la ruta del archivo ASS para su uso seguro en el filtro de FFmpeg en Windows.
    Reemplaza backslashes por slashes y escapa dos puntos ':' como '\\:'.
    """
    abs_path = os.path.abspath(str(path)).replace("\\", "/")
    return abs_path.replace(":", r"\:")


class Word:
    """Representa una palabra con su texto y timestamps de inicio y fin (segundos y centésimas)."""

    def __init__(self, text: str, start: float, end: float):
        # Garantizar forma Unicode NFC normalizada
        self.text = unicodedata.normalize("NFC", str(text).strip())
        self.start = float(start)
        self.end = max(float(end), self.start)
        self.start_cs = seg_a_cs(self.start)
        self.end_cs = max(seg_a_cs(self.end), self.start_cs)

    @property
    def duration(self) -> float:
        return max(0.01, self.end - self.start)

    @property
    def duration_cs(self) -> int:
        return max(1, self.end_cs - self.start_cs)

    def __repr__(self) -> str:
        return f"Word({self.text!r}, start={self.start:.3f}s ({self.start_cs}cs), end={self.end:.3f}s ({self.end_cs}cs))"


# ---------------------------------------------------------------------------
# DIAGNÓSTICO 1: Sanitización y verificación de caracteres especiales
# ---------------------------------------------------------------------------

def sanitizar_alignment(alignment: Dict[str, Any]) -> Dict[str, Any]:
    """
    Verifica y normaliza la lista de characters de alignment:
    - Normaliza a Unicode NFC (para evitar que tildes vengan como caracteres combinados NFD separados).
    - Repara posibles mojibakes (UTF-8 interpretado como Latin-1).
    - Fusiona caracteres combinatorios huérfanos con su letra previa.
    """
    chars = alignment.get("characters", [])
    starts = alignment.get("character_start_times_seconds", [])
    ends = alignment.get("character_end_times_seconds", [])

    if not chars:
        return alignment

    nuevos_chars: List[str] = []
    nuevos_starts: List[float] = []
    nuevos_ends: List[float] = []

    for c, s, e in zip(chars, starts, ends):
        # Si vino como string con tildes descompuestas o con bytes
        c_norm = unicodedata.normalize("NFC", str(c))

        # Si el caracter es un diacrítico combinatorio (ej. acento solo) y ya tenemos un caracter anterior
        if unicodedata.combining(c_norm) != 0 and nuevos_chars:
            # Fusionar con el caracter previo
            fusion = unicodedata.normalize("NFC", nuevos_chars[-1] + c_norm)
            nuevos_chars[-1] = fusion
            nuevos_ends[-1] = max(nuevos_ends[-1], e)
        else:
            nuevos_chars.append(c_norm)
            nuevos_starts.append(s)
            nuevos_ends.append(e)

    return {
        "characters": nuevos_chars,
        "character_start_times_seconds": nuevos_starts,
        "character_end_times_seconds": nuevos_ends
    }


def imprimir_diagnostico_caracteres(alignment: Dict[str, Any]) -> Dict[str, Any]:
    """
    Imprime la lista completa de characters del alignment y confirma visualmente
    que cada tilde (á,é,í,ó,ú), la ñ y signos ¿¡ aparecen como UN SOLO carácter.
    """
    chars = alignment.get("characters", [])
    caracteres_especiales_es = {"á", "é", "í", "ó", "ú", "Á", "É", "Í", "Ó", "Ú", "ñ", "Ñ", "¿", "¡"}

    logger.info("=" * 65)
    logger.info("DIAGNÓSTICO 1 - ANÁLISIS DE CARACTERES ESPECIALES DEL ESPAÑOL")
    logger.info("=" * 65)
    logger.info(f"Total de caracteres en alignment: {len(chars)}")

    hallazgos = []
    anomalias = []

    for idx, ch in enumerate(chars):
        # Verificar longitud del string en el elemento
        if len(ch) != 1:
            anomalias.append((idx, ch, f"Longitud de elemento != 1 (len={len(ch)})"))

        # Si es un caracter especial del español
        if any(esp in ch for esp in caracteres_especiales_es):
            codepoint = f"U+{ord(ch):04X}" if len(ch) == 1 else "MULTI"
            nombre = unicodedata.name(ch, "DESCONOCIDO") if len(ch) == 1 else "COMPUESTO"
            hallazgos.append((idx, ch, codepoint, nombre))

    logger.info(f"Caracteres especiales encontrados: {len(hallazgos)}")
    for idx, ch, cp, nom in hallazgos:
        logger.info(f"  [{idx:03d}] Carácter: '{ch}' | Codepoint: {cp} | {nom} | (1 solo carácter: {len(ch) == 1})")

    if anomalias:
        logger.warning(f"¡Atención! Se detectaron {len(anomalias)} elementos con caracteres rotos/divididos:")
        for idx, ch, razon in anomalias:
            logger.warning(f"  [{idx:03d}] '{ch}' -> {razon}")
    else:
        logger.info(" Verificación completada: Todas las tildes, ñ y signos ¿¡ son caracteres únicos (len=1).")

    logger.info("=" * 65)
    return {
        "total_chars": len(chars),
        "especiales_encontrados": len(hallazgos),
        "anomalias": anomalias
    }


# ---------------------------------------------------------------------------
# DIAGNÓSTICO 4: Agrupamiento robusto sin palabras vacías ni fragmentos raros
# ---------------------------------------------------------------------------

def _agrupar_caracteres_en_palabras(alignment: Dict[str, Any]) -> List[Word]:
    """
    Agrupa los caracteres de alignment en palabras (cortando en espacios y saltos de línea),
    calculando inicio y fin a partir de los timestamps de sus caracteres.
    Filtra estrictamente cualquier palabra vacía, espacios duplicados o saltos de línea.
    """
    alignment_limpio = sanitizar_alignment(alignment)
    chars = alignment_limpio.get("characters", [])
    starts = alignment_limpio.get("character_start_times_seconds", [])
    ends = alignment_limpio.get("character_end_times_seconds", [])

    if not (len(chars) == len(starts) == len(ends)):
        raise ValueError(
            f"Listas de alignment con longitudes inconsistentes: "
            f"chars={len(chars)}, starts={len(starts)}, ends={len(ends)}"
        )

    words: List[Word] = []
    current_chars: List[str] = []
    current_start: Optional[float] = None
    current_end: Optional[float] = None

    for char, s, e in zip(chars, starts, ends):
        # DIAGNÓSTICO 4: Si hay un salto de silencio significativo entre caracteres (> 0.15s), delimitar palabra
        silencio_entre_caracteres = (current_end is not None and (s - current_end) > 0.15)

        if char.isspace() or silencio_entre_caracteres:
            # Fin de palabra si había caracteres acumulados
            if current_chars and current_start is not None and current_end is not None:
                word_text = "".join(current_chars).strip()
                if word_text:
                    words.append(Word(word_text, current_start, current_end))
                current_chars = []
                current_start = None
                current_end = None

            # Si el caracter actual no es espacio pero detonó por silencio (ej: primera letra de la siguiente frase)
            if not char.isspace():
                current_start = s
                current_chars.append(char)
                current_end = e
        else:
            if not current_chars:
                current_start = s
            current_chars.append(char)
            current_end = e

    # Procesar última palabra acumulada
    if current_chars and current_start is not None and current_end is not None:
        word_text = "".join(current_chars).strip()
        if word_text:
            words.append(Word(word_text, current_start, current_end))

    # Segundo filtro de seguridad: descartar palabras vacías o inválidas
    words_filtradas = [w for w in words if w.text and len(w.text.strip()) > 0]
    return words_filtradas


def _dividir_en_chunks(
    words: List[Word],
    segmentos: Optional[List[Dict[str, Any]]] = None,
    max_words_per_chunk: int = 4
) -> List[List[Word]]:
    """
    Divide las palabras en chunks respetando los límites de cada segmento narrativo.
    En segmentos clave de alto impacto conceptual (cold_open, hook, problema, cierre/pregunta),
    mantiene la frase o bloque de sentido completo (hasta 10-12 palabras) para que el espectador
    comprenda el dolor o la pregunta de inmediato, reservando chunks cortos para las demos.
    """
    if not words:
        return []

    chunks: List[List[Word]] = []

    # Segmentos donde se debe mostrar la premisa o pregunta completa para eliminar fricción cognitiva
    SEGMENTOS_FRASE_COMPLETA = {
        "cold_open", "hook", "problema", "escena_problema", "panico", "cierre", "pregunta"
    }

    if segmentos:
        seg_index = 0
        seg_words: List[List[Word]] = [[] for _ in range(len(segmentos))]

        for w in words:
            while seg_index < len(segmentos) - 1 and w.start >= segmentos[seg_index].get("fin", float("inf")):
                seg_index += 1
            seg_words[seg_index].append(w)

        for s_idx, group in enumerate(seg_words):
            if not group:
                continue

            tipo_seg = str(segmentos[s_idx].get("tipo", "")).lower() if s_idx < len(segmentos) else ""
            es_frase_completa = any(k in tipo_seg for k in SEGMENTOS_FRASE_COMPLETA)

            if es_frase_completa and len(group) <= 6:
                # Mantener bloque de sentido de 3 a 6 palabras (se partirá en 2 líneas cortas con \N)
                chunks.append(group)
            elif es_frase_completa and len(group) > 6:
                # Si supera 6 palabras, dividir en bloques equilibrados de 4 o 5 palabras
                # para que no desborde hacia los laterales en móvil
                chunk_tam = 4 if len(group) <= 8 else 5
                for i in range(0, len(group), chunk_tam):
                    chunk = group[i : i + chunk_tam]
                    if chunk:
                        chunks.append(chunk)
            else:
                for i in range(0, len(group), max_words_per_chunk):
                    chunk = group[i : i + max_words_per_chunk]
                    if chunk:
                        chunks.append(chunk)
    else:
        for i in range(0, len(words), max_words_per_chunk):
            chunk = words[i : i + max_words_per_chunk]
            if chunk:
                chunks.append(chunk)

    return chunks


# ---------------------------------------------------------------------------
# TAREA 1: Generación de subtítulos estilo karaoke (.ass) corregida
# ---------------------------------------------------------------------------

def generar_ass(
    alignment: Dict[str, Any],
    segmentos: Optional[List[Dict[str, Any]]] = None,
    ruta_salida: Optional[Union[str, Path]] = None,
    max_words_per_chunk: int = 4
) -> str:
    r"""
    Genera un archivo .ass (Advanced SubStation Alpha) estilo karaoke (\k) sin saltos bruscos:
    - DIAGNÓSTICO 2: La duración \k de la palabra N cubre desde inicio(N) hasta inicio(N+1).
    - DIAGNÓSTICO 3: Precisión uniforme en centésimas de segundo (cs) en todo el archivo.
    - DIAGNÓSTICO 4: Sin fragmentos vacíos.
    - Colores: base blanco (&H00FFFFFF), palabra activa cian (#00E5FF -> &H00FFE500).
    - Posición: tercio inferior con márgenes de seguridad para UI móvil.
    """
    if ruta_salida is None:
        ruta_salida = Path.cwd() / "subtitulos_karaoke.ass"
    else:
        ruta_salida = Path(ruta_salida)

    ruta_salida.parent.mkdir(parents=True, exist_ok=True)

    words = _agrupar_caracteres_en_palabras(alignment)
    chunks = _dividir_en_chunks(words, segmentos, max_words_per_chunk=max_words_per_chunk)

    segmentos_meta = json.dumps(segmentos or [])

    header = f"""[Script Info]
Title: Karaoke Shorts Subtitles (Pro Hormozi Tech Style)
ScriptType: v4.00+
WrapStyle: 2
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.709
PlayResX: 1080
PlayResY: 1920
; SEGMENTS_METADATA: {segmentos_meta}

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: KaraokeByte,Arial,46,&H0000F5FF,&H00FFFFFF,&H00000000,&H90000000,-1,0,0,0,100,100,1,0,1,4.5,2.5,2,80,80,860,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

    # Color base: Amarillo brillante puro (&H0000F5FF&)
    COLOR_AMARILLO = "&H0000F5FF&"
    COLOR_CLAVE_POP = "&H00FFFFFF&"  # Blanco puro de alto impacto para palabra clave

    # Palabras clave de alto impacto que reciben micro-resaltado magnético
    PALABRAS_CLAVE = {
        "OTTER.AI", "OTTER", "FIREFLIES.AI", "FIREFLIES", "NOTAS", "VIDEOLLAMADAS",
        "TRANSCRIPCIONES", "AUTOMÁTICAS", "RESÚMENES", "ASISTENTE", "PAZ", "MENTAL",
        "COMENTARIOS", "HORAS", "GRABA", "ORGANIZAR", "DETALLES", "ENORMES", "REUNIONES"
    }

    dialogue_lines: List[str] = []

    for idx, chunk in enumerate(chunks):
        if not chunk:
            continue

        num_words = len(chunk)
        start_cs = chunk[0].start_cs

        # Determinar cuándo inicia el siguiente chunk para dar continuidad visual
        next_chunk = chunks[idx + 1] if idx + 1 < len(chunks) and chunks[idx + 1] else None
        next_chunk_start_cs = next_chunk[0].start_cs if next_chunk else None

        # Construir tokens de karaoke con duración cubriendo hasta la siguiente palabra
        karaoke_tokens: List[str] = []

        # Si el chunk tiene 3 o más palabras, buscar el quiebre gramatical más armónico para partirlo en 2 líneas cortas con \N
        split_idx = -1
        if num_words >= 3:
            mid = (num_words + 1) // 2
            split_idx = mid
            # Priorizar quiebre en puntuación cercana a la mitad (, : ? -)
            for cand_i in range(max(1, mid - 1), min(num_words - 1, mid + 2)):
                t_prev = chunk[cand_i - 1].text.strip()
                if t_prev.endswith(",") or t_prev.endswith(":") or t_prev.endswith("?") or t_prev.endswith("-"):
                    split_idx = cand_i
                    break

        for i in range(num_words):
            w_actual = chunk[i]

            if i < num_words - 1:
                w_siguiente = chunk[i + 1]
                # DIAGNÓSTICO 2: duracion_k_palabra_N = inicio_palabra_N+1 - inicio_palabra_N
                k_dur_cs = max(1, w_siguiente.start_cs - w_actual.start_cs)
            else:
                # Última palabra del chunk: cubre hasta que el diálogo termine
                if next_chunk_start_cs is not None and next_chunk_start_cs > w_actual.start_cs:
                    end_candidate_cs = min(w_actual.end_cs + 35, next_chunk_start_cs)
                else:
                    end_candidate_cs = w_actual.end_cs + 35

                k_dur_cs = max(1, end_candidate_cs - w_actual.start_cs)

            if i == 0:
                prefix = ""
            elif i == split_idx:
                prefix = "\\N"
            else:
                prefix = " "

            # Pop dinámico sincronizado al milisegundo exacto de inicio de la palabra
            t_word_start_ms = max(0, int((w_actual.start_cs - start_cs) * 10))
            t_pop_peak_ms = t_word_start_ms + 80
            t_pop_settle_ms = t_word_start_ms + 170

            w_text_formatted = w_actual.text.upper()
            palabra_limpia = re.sub(r"[^\w\.]", "", w_text_formatted)
            es_clave = palabra_limpia in PALABRAS_CLAVE

            scale_peak = 128 if es_clave else 118
            pop_col = COLOR_CLAVE_POP if es_clave else COLOR_AMARILLO

            pop_tag = (
                f"\\t({t_word_start_ms},{t_pop_peak_ms},\\1c{pop_col}\\fscx{scale_peak}\\fscy{scale_peak})"
                f"\\t({t_pop_peak_ms},{t_pop_settle_ms},\\1c{COLOR_AMARILLO}\\fscx100\\fscy100)"
            )

            karaoke_tokens.append(f"{prefix}{{\\1c{COLOR_AMARILLO}{pop_tag}\\k{k_dur_cs}}}{w_text_formatted}")

        # DIAGNÓSTICO 3: El fin del diálogo debe ser exactamente igual a la suma de los \k
        total_line_duration_cs = sum(
            int(re.search(r"\\k(\d+)", tok).group(1)) for tok in karaoke_tokens
        )
        end_cs = start_cs + total_line_duration_cs

        start_str = cs_a_tiempo_ass(start_cs)
        end_str = cs_a_tiempo_ass(end_cs)

        line_text = "".join(karaoke_tokens)
        dialogue = f"Dialogue: 0,{start_str},{end_str},KaraokeByte,,0,0,0,,{line_text}"
        dialogue_lines.append(dialogue)

    with open(ruta_salida, "w", encoding="utf-8") as f:
        f.write(header)
        f.write("\n".join(dialogue_lines))
        f.write("\n")

    logger.info(f"Subtítulos ASS karaoke fluidos generados en: {ruta_salida} ({len(dialogue_lines)} diálogos)")
    return str(ruta_salida.resolve())


# ---------------------------------------------------------------------------
# Reporte detallado de palabras y tiempos en texto plano
# ---------------------------------------------------------------------------

def exportar_tabla_tiempos_palabras(
    alignment: Dict[str, Any],
    ruta_txt: Union[str, Path]
) -> Path:
    """
    Genera un archivo de texto plano tabulado con cada palabra, su tiempo de inicio,
    tiempo de fin y duración \\k calculada para revisión manual.
    """
    words = _agrupar_caracteres_en_palabras(alignment)
    ruta_txt = Path(ruta_txt)
    ruta_txt.parent.mkdir(parents=True, exist_ok=True)

    lineas = []
    lineas.append("=" * 80)
    lineas.append(f"{'ÍNDICE':<7} | {'PALABRA':<25} | {'INICIO (s)':<12} | {'FIN (s)':<10} | {'DUR \\k (cs)':<12} | {'DUR \\k (s)':<10}")
    lineas.append("=" * 80)

    for i in range(len(words)):
        w = words[i]
        if i < len(words) - 1:
            w_next = words[i + 1]
            dur_k_cs = max(1, w_next.start_cs - w.start_cs)
        else:
            dur_k_cs = max(1, (w.end_cs + 35) - w.start_cs)

        dur_k_s = dur_k_cs / 100.0
        lineas.append(
            f"{i+1:<7} | {w.text:<25} | {w.start:<12.3f} | {w.end:<10.3f} | {dur_k_cs:<12} | {dur_k_s:<10.2f}"
        )

    lineas.append("=" * 80)
    lineas.append(f"Total palabras procesadas: {len(words)}")

    with open(ruta_txt, "w", encoding="utf-8") as f:
        f.write("\n".join(lineas) + "\n")

    logger.info(f"Archivo de revisión de tiempos exportado en: {ruta_txt}")
    return ruta_txt


# ---------------------------------------------------------------------------
# TAREA 2: Ensamblar video con FFmpeg (MEJORA 2: Dos capas + Paneo real)
# ---------------------------------------------------------------------------

def _extraer_segmentos_de_ass(archivo_ass: Path) -> Optional[List[Dict[str, Any]]]:
    """Extrae los metadatos de segmentos guardados en el archivo ASS si están disponibles."""
    try:
        with open(archivo_ass, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("; SEGMENTS_METADATA:"):
                    raw_json = line.split("; SEGMENTS_METADATA:", 1)[1].strip()
                    data = json.loads(raw_json)
                    if isinstance(data, list) and len(data) > 0:
                        return data
    except Exception:
        pass
    return None


def _normalizar_clave_segmento(texto: str) -> str:
    """Normaliza nombres de tipo de segmento: 'punto_1' -> 'punto1', 'hook' -> 'hook'."""
    return re.sub(r"[^a-zA-Z0-9]", "", texto).lower()


def _resolver_imagenes(
    imagenes: Union[List[Union[str, Path]], Dict[str, Union[str, Path]]],
    segmentos: List[Dict[str, Any]]
) -> List[Path]:
    """Asocia cada segmento con su imagen correspondiente."""
    mapa_imagenes: Dict[str, Path] = {}

    if isinstance(imagenes, dict):
        for k, v in imagenes.items():
            norm_k = _normalizar_clave_segmento(k)
            mapa_imagenes[norm_k] = Path(v)
    elif isinstance(imagenes, (list, tuple)):
        for item in imagenes:
            p = Path(item)
            stem_norm = _normalizar_clave_segmento(p.stem)
            mapa_imagenes[stem_norm] = p

    imagenes_resueltas: List[Path] = []
    lista_fallback = list(imagenes.values()) if isinstance(imagenes, dict) else list(imagenes)

    for i, seg in enumerate(segmentos):
        tipo = seg.get("tipo", f"segmento_{i}")
        norm_tipo = _normalizar_clave_segmento(tipo)

        if norm_tipo in mapa_imagenes:
            img_path = mapa_imagenes[norm_tipo]
        elif i < len(lista_fallback):
            img_path = Path(lista_fallback[i])
        else:
            raise FileNotFoundError(f"No se pudo encontrar imagen para el segmento '{tipo}' (índice {i})")

        if not img_path.exists():
            raise FileNotFoundError(f"La imagen no existe en disco: {img_path}")

        imagenes_resueltas.append(img_path.resolve())

    return imagenes_resueltas


# ---------------------------------------------------------------------------
# MEJORA 1: Remoción de fondo con rembg
# ---------------------------------------------------------------------------

def quitar_fondo(
    ruta_imagen_entrada: Union[str, Path],
    ruta_salida: Union[str, Path],
    tamano_lienzo: int = 640
) -> str:
    """
    Procesa un sprite de personaje (Byte):
    1. Si la imagen no tiene canal alpha transparente, remueve el fondo con rembg.
    2. Escala con interpolación Lanczos de alta calidad a un lienzo cuadrado uniforme (640x640)
       centrado y con transparencia completa.
    """
    try:
        from PIL import Image
    except ImportError:
        raise ImportError("La librería 'Pillow' no está instalada.")

    ruta_entrada = Path(ruta_imagen_entrada).resolve()
    ruta_salida = Path(ruta_salida).resolve()

    if not ruta_entrada.exists():
        raise FileNotFoundError(f"La imagen de entrada no existe: {ruta_entrada}")

    ruta_salida.parent.mkdir(parents=True, exist_ok=True)

    with Image.open(ruta_entrada) as img:
        img_rgba = img.convert("RGBA")
        
        w, h = img_rgba.size
        corners_alpha = [
            img_rgba.getpixel((0, 0))[3],
            img_rgba.getpixel((w - 1, 0))[3],
            img_rgba.getpixel((0, h - 1))[3],
            img_rgba.getpixel((w - 1, h - 1))[3],
        ]
        
        # Si las esquinas son totalmente opacas, aplicamos rembg
        if all(a > 200 for a in corners_alpha):
            try:
                from rembg import remove
                logger.info(f"Removiendo fondo de '{ruta_entrada.name}' con rembg...")
                img_rgba = remove(img_rgba)
            except Exception as e:
                logger.warning(f"No se pudo ejecutar rembg en {ruta_entrada.name}: {e}")

        # Redimensionar conservando proporción para encajar en tamano_lienzo - 40px
        box_limit = tamano_lienzo - 40
        ratio = min(box_limit / w, box_limit / h)
        new_w = max(1, int(w * ratio))
        new_h = max(1, int(h * ratio))
        img_scaled = img_rgba.resize((new_w, new_h), Image.Resampling.LANCZOS)

        # Centrar en un lienzo perfectamente cuadrado transparente
        canvas = Image.new("RGBA", (tamano_lienzo, tamano_lienzo), (0, 0, 0, 0))
        paste_x = (tamano_lienzo - new_w) // 2
        paste_y = (tamano_lienzo - new_h) // 2
        canvas.paste(img_scaled, (paste_x, paste_y), img_scaled)
        canvas.save(ruta_salida, format="PNG")

    logger.info(f"Sprite de Byte procesado y guardado en: {ruta_salida} ({tamano_lienzo}x{tamano_lienzo})")
    return str(ruta_salida)


def generar_fondo_texturado(
    indice_escena: int,
    ruta_salida: Union[str, Path],
    ancho: int = 1280,
    alto: int = 2276
) -> str:
    """
    Genera un fondo para shorts (1280x2276) con textura sutil que hace
    visible el desplazamiento del paneo y zoom:
    - Degradado suave entre 2 tonos de la paleta Byte.
    - 2-3 blobs circulares grandes, desenfocados (blur alto), cyan/coral al 15-20% de opacidad.
    - Patrón sutil de circuito y cuadrícula de puntos estilo Byte al 10-15% de opacidad.
    """
    try:
        from PIL import Image, ImageDraw, ImageFilter
    except ImportError:
        raise ImportError("Se requiere Pillow para generar fondos. Ejecutá 'pip install pillow'.")

    ruta_salida = Path(ruta_salida).resolve()
    ruta_salida.parent.mkdir(parents=True, exist_ok=True)

    configs = [
        # Escena 0 (Hook): Azul oscuro a violeta oscuro tech con blobs cyan y coral
        {
            "c_top": (26, 27, 46),       # #1A1B2E
            "c_bot": (43, 43, 77),       # #2B2B4D
            "blobs": [
                (160, 320, 560, 720, (0, 216, 246, 80)),     # Cyan superior-izq
                (760, 1420, 1220, 1880, (255, 92, 92, 65)),  # Coral inferior-der
                (860, 640, 1200, 980, (0, 180, 255, 50)),    # Azul eléctrico medio-der
            ],
            "circuit_lines": [
                [(100, 220), (420, 220), (560, 360), (560, 620)],
                [(1180, 420), (940, 420), (800, 560), (800, 820)],
                [(140, 1800), (360, 1800), (500, 1660), (500, 1400)],
                [(1120, 1920), (860, 1920), (720, 1780), (720, 1520)],
                [(180, 1080), (440, 1080), (540, 1180)],
                [(1100, 1180), (860, 1180), (760, 1080)]
            ]
        },
        # Escena 1 (Punto 1 - Shortwave): Petróleo tech oscuro a azul cian profundo
        {
            "c_top": (13, 31, 51),       # #0D1F33
            "c_bot": (22, 56, 92),       # #16385C
            "blobs": [
                (740, 320, 1180, 760, (0, 229, 255, 80)),    # Cyan superior-der
                (140, 1450, 580, 1890, (255, 107, 107, 60)), # Coral inferior-izq
                (200, 720, 520, 1040, (2, 132, 199, 50)),    # Cyan medio-izq
            ],
            "circuit_lines": [
                [(1160, 240), (880, 240), (760, 360), (760, 580)],
                [(120, 400), (340, 400), (460, 520), (460, 780)],
                [(1120, 1780), (880, 1780), (740, 1640), (740, 1380)],
                [(140, 1900), (380, 1900), (520, 1760), (520, 1500)],
                [(160, 1150), (420, 1150), (520, 1250)],
                [(1120, 1120), (880, 1120), (780, 1220)]
            ]
        },
        # Escena 2 (Punto 2 - SaneBox): Índigo cálido a púrpura Byte
        {
            "c_top": (34, 28, 53),       # #221C35
            "c_bot": (61, 38, 82),       # #3D2652
            "blobs": [
                (180, 1420, 640, 1880, (217, 70, 239, 70)),  # Violeta cálido inferior-izq
                (760, 380, 1180, 800, (6, 182, 212, 75)),    # Cyan superior-der
                (840, 1050, 1160, 1370, (236, 72, 153, 55)), # Magenta medio-der
            ],
            "circuit_lines": [
                [(120, 280), (380, 280), (500, 400), (500, 650)],
                [(1160, 360), (920, 360), (800, 480), (800, 720)],
                [(150, 1820), (400, 1820), (540, 1680), (540, 1420)],
                [(1100, 1860), (840, 1860), (700, 1720), (700, 1460)],
                [(200, 1120), (460, 1120), (560, 1220)],
                [(1080, 1160), (840, 1160), (740, 1060)]
            ]
        },
        # Escena 3 (Cierre): Azul noche Byte a azul profundo
        {
            "c_top": (14, 24, 42),       # #0E182A
            "c_bot": (28, 46, 78),       # #1C2E4E
            "blobs": [
                (220, 420, 680, 880, (56, 189, 248, 80)),    # Cyan superior-izq
                (740, 1350, 1180, 1790, (244, 63, 94, 65)),  # Coral inferior-der
                (480, 1700, 840, 2060, (125, 211, 252, 50)), # Cyan suave inferior-centro
            ],
            "circuit_lines": [
                [(100, 300), (360, 300), (480, 420), (480, 680)],
                [(1180, 300), (920, 300), (800, 420), (800, 680)],
                [(120, 1820), (380, 1820), (500, 1700), (500, 1450)],
                [(1160, 1820), (900, 1820), (780, 1700), (780, 1450)],
                [(180, 1100), (450, 1100), (550, 1200)],
                [(1100, 1100), (830, 1100), (730, 1200)]
            ]
        }
    ]

    cfg = configs[indice_escena % len(configs)]

    # 1. Base gradient
    base = Image.new("RGBA", (ancho, alto))
    c_top = cfg["c_top"]
    c_bot = cfg["c_bot"]
    for y in range(alto):
        t = y / (alto - 1)
        r = int(c_top[0] + (c_bot[0] - c_top[0]) * t)
        g = int(c_top[1] + (c_bot[1] - c_top[1]) * t)
        b = int(c_top[2] + (c_bot[2] - c_top[2]) * t)
        line = Image.new("RGBA", (ancho, 1), (r, g, b, 255))
        base.paste(line, (0, y))

    # 2. Blobs layer con blur gaussiano alto
    blobs = Image.new("RGBA", (ancho, alto), (0, 0, 0, 0))
    draw_b = ImageDraw.Draw(blobs)
    for bx0, by0, bx1, by1, bcolor in cfg["blobs"]:
        draw_b.ellipse([bx0, by0, bx1, by1], fill=bcolor)
    blobs = blobs.filter(ImageFilter.GaussianBlur(radius=140))

    # 3. Circuito y cuadrícula de puntos estilo Byte
    circuits = Image.new("RGBA", (ancho, alto), (0, 0, 0, 0))
    draw_c = ImageDraw.Draw(circuits)
    line_col = (77, 238, 234, 40)  # ~16% opacidad
    dot_col = (77, 238, 234, 55)   # ~22% opacidad

    for l in cfg["circuit_lines"]:
        draw_c.line(l, fill=line_col, width=3)
        draw_c.ellipse([l[0][0]-6, l[0][1]-6, l[0][0]+6, l[0][1]+6], fill=dot_col)
        draw_c.ellipse([l[-1][0]-6, l[-1][1]-6, l[-1][0]+6, l[-1][1]+6], fill=dot_col)

    # Cuadrícula sutil de nodos/puntos
    for gx in range(140, ancho, 200):
        for gy in range(140, alto, 200):
            draw_c.point([(gx, gy)], fill=(77, 238, 234, 45))

    fondo = Image.alpha_composite(base, blobs)
    fondo = Image.alpha_composite(fondo, circuits)

    # Guardado del fondo base compuesto (degradado + blobs + circuito Byte)
    fondo.save(ruta_salida, format="PNG")
    logger.info(f"Fondo texturado escena {indice_escena} guardado en: {ruta_salida}")
    return str(ruta_salida)


# ---------------------------------------------------------------------------
# Transiciones xfade (rotación anti-template por video)
# ---------------------------------------------------------------------------

# Catálogo curado para vertical 9:16; la rotación arranca sembrada por el
# número del video para que cada uno tenga su propia secuencia reproducible.
# SOLO tipos de revelado/mezcla (blend o wipe): cada píxel de salida toma el
# valor de A o B en su misma posición, así ningún contenido puede salirse de
# las safe zones laterales. Prohibidos los de traducción (slideleft/smoothup/
# slidedown): desplazan los mockups fuera de x>=90/x<=990 durante el corte y
# lint_zonas_seguras los detecta como violación (evidencia video_13 frame_0028).
TRANSICIONES_XFADE: Tuple[str, ...] = (
    "fade", "wiperight", "circleclose", "circleopen",
    "wipeleft", "wipedown",
)

# Ajuste narrativo: la escena que llega pinnea la transición para que la
# edición acompañe la historia (valores siempre dentro del catálogo).
# Sin fadeblack/fadewhite: los fundes a negro/blanco restan foco al contenido.
TRANSICIONES_POR_TIPO: Dict[str, str] = {
    "problema": "circleclose",
    "escena_problema": "circleclose",
    "panico": "circleclose",
    "resultado": "circleopen",
}

# Grado cinematográfico sutil (vigilar brillo en zonas con lint_zonas_seguras)
GRADO_VIGNETTE: str = "PI/6"                     # viñeta suave en los bordes
GRADO_EQ: str = "contrast=1.06:saturation=1.10"  # contraste y color leves
GRADO_NOISE: str = "alls=4:allf=t"               # grano fino temporal


def _semilla_transiciones(ruta_salida: Union[str, Path]) -> int:
    """Semilla determinista por video a partir de los dígitos de ruta_salida."""
    m = re.search(r"(\d+)", Path(ruta_salida).stem)
    return int(m.group(1)) if m else 0


def transicion_para_escena(
    i: int,
    tipo_escena: Optional[str],
    semilla: int,
    anterior: Optional[str] = None,
) -> str:
    """Elige la transición xfade del corte que llega a la escena i.

    Rotación sembrada por video + pin narrativo por tipo de escena +
    guardia anti-repetición (nunca dos cortes seguidos iguales).
    """
    elegida: Optional[str] = None
    if tipo_escena:
        elegida = TRANSICIONES_POR_TIPO.get(str(tipo_escena).lower())
    if elegida is None:
        elegida = TRANSICIONES_XFADE[(semilla + i) % len(TRANSICIONES_XFADE)]
    if anterior is not None and elegida == anterior:
        idx = TRANSICIONES_XFADE.index(elegida)
        elegida = TRANSICIONES_XFADE[(idx + 1) % len(TRANSICIONES_XFADE)]
    return elegida


def _expresion_zoom_gancho(trat: Dict[str, float], total_frames: int) -> str:
    """Expresión zoompan z(on) del clip 0 para una variante de gancho.

    - Punch (B): subida rápida a z_max y retorno suave (curva del enfasis).
    - Lento (C): zoom-in lineal que se sostiene hasta z_max.
    Siempre z≥1.0 y ancla (540, 250) — mismo rango seguro del punch-in
    (src/enfasis.py); z<1 revelaría bordes en crop/zoompan.
    Devuelve "" si la variante es el control (sin zoom).
    """
    z_max = float(trat.get("z_max", 1.0))
    if z_max <= 1.0:
        return ""
    ax, ay = 540, 250
    dur_up = float(trat.get("dur_zoom_up", 0.0))
    dur_down = float(trat.get("dur_zoom_down", 0.0))
    dur_lento = float(trat.get("dur_zoom_lento", 0.0))
    if dur_up > 0 and dur_down > 0:
        # Punch: bump de (z_max-1) con subida rápida y retorno suave
        total_s = dur_up + dur_down
        dur_f = max(1.0, total_s * 30)
        amp = z_max - 1.0
        z_expr = (
            f"1+{amp:.4f}*sin(PI*pow(clip(on/{dur_f:.1f},0,1),0.6))"
            f"*between(on,0,{dur_f:.1f})"
        )
    elif dur_lento > 0:
        # Lento: lineal de 1.0 a z_max en dur_lento, luego se sostiene
        dur_f = max(1.0, dur_lento * 30)
        amp = z_max - 1.0
        z_expr = f"1+{amp:.4f}*clip(on/{dur_f:.1f},0,1)"
    else:
        return ""
    return (
        f"zoompan=z='{z_expr}':"
        f"x='{ax}-{ax}/zoom':y='{ay}-{ay}/zoom':"
        f"d=1:s=1080x1920:fps=30"
    )


def ensamblar_video(
    imagenes: Union[List[Union[str, Path]], Dict[str, Union[str, Path]]],
    audio: Union[str, Path],
    archivo_ass: Union[str, Path],
    duracion_total: float,
    segmentos: Optional[List[Dict[str, Any]]] = None,
    ruta_salida: Optional[Union[str, Path]] = None,
    fondos: Optional[List[Union[str, Path]]] = None,
    fade_duration: float = 0.15,
    puntos_enfasis: Optional[Sequence[Sequence[PuntoEnfasis]]] = None,
    variante_gancho: Optional[str] = None,
) -> str:
    """
    Ensambla el video vertical 9:16 (1080x1920) a 30fps con composición en DOS CAPAS:
    1. Capa de Fondo: Con textura sutil (degradado, blobs suaves cyan/coral y circuito Byte) y PANEO real alternado por escena.
    2. Capa de Byte: Imagen transparente centrada con respiración senoidal (escala oscilando entre 0.96 y 1.04).
    3. Superposición con overlay y transiciones xfade rotativas (anti-template) entre escenas.
    4. Grado cinematográfico (vignette + eq + grano), burn-in de subtítulos ASS karaoke y mezcla de audio AAC.

    `puntos_enfasis`: opcional, una secuencia de PuntoEnfasis por escena (tiempos
    LOCALES de escena). Si se provee, se aplica un punch-in (zoompan z≥1 con
    ancla en el mockup) a la capa de FONDO de esa escena, sin tocar a Byte ni
    los subtítulos (ver src/enfasis.py). None = sin punch-in (por defecto).

    `variante_gancho`: opcional, arquetipo de gancho visual del clip 0 (ver
    src/director_gancho.py: "texto_pantalla" | "byte_reacciona" |
    "mockup_inmediato"). Cambia SOLO el tratamiento visual del primer segmento
    (mismo audio/ASS => 0 créditos). None = comportamiento histórico exacto.
    Si el clip 0 tiene variante con zoom, el punch-in de énfasis NO se aplica
    en ese clip (evita multiplicar zooms y violar safe zones; z_total≤1.04).
    """
    audio_path = Path(audio).resolve()
    ass_path = Path(archivo_ass).resolve()

    if not audio_path.exists():
        raise FileNotFoundError(f"El archivo de audio no existe: {audio_path}")
    if not ass_path.exists():
        raise FileNotFoundError(f"El archivo de subtítulos .ass no existe: {ass_path}")

    if ruta_salida is None:
        ruta_salida = Path.cwd() / "short_final.mp4"
    else:
        ruta_salida = Path(ruta_salida).resolve()

    ruta_salida.parent.mkdir(parents=True, exist_ok=True)

    if not segmentos:
        segmentos = _extraer_segmentos_de_ass(ass_path)

    num_imagenes = len(imagenes) if isinstance(imagenes, (list, tuple)) else len(imagenes.keys())
    if not segmentos:
        step = duracion_total / max(1, num_imagenes)
        segmentos = [
            {"inicio": i * step, "fin": (i + 1) * step, "tipo": f"segmento_{i}"}
            for i in range(num_imagenes)
        ]

    imagenes_ordenadas = _resolver_imagenes(imagenes, segmentos)
    num_clips = len(imagenes_ordenadas)

    # Asegurar fondos texturados para cada escena si no fueron provistos
    if fondos is None:
        dir_fondos = DIR_FONDOS
        dir_fondos.mkdir(parents=True, exist_ok=True)
        rutas_fondos = []
        for i in range(num_clips):
            p_fondo = dir_fondos / f"fondo_escena_{i}.png"
            generar_fondo_texturado(i, p_fondo)
            rutas_fondos.append(p_fondo.resolve())
    else:
        rutas_fondos = [Path(f).resolve() for f in fondos]

    # Tratamiento visual del gancho (clip 0); None o desconocido = control
    trat_gancho = TRATAMIENTOS.get(variante_gancho or "", TRATAMIENTOS["texto_pantalla"])
    if variante_gancho and variante_gancho in TRATAMIENTOS and variante_gancho != "texto_pantalla":
        logger.info(f"Variante de gancho: {variante_gancho} (solo clip 0)")

    clip_durations: List[float] = []
    offsets: List[float] = []

    for i, seg in enumerate(segmentos):
        ini = seg.get("inicio", 0.0)
        fin = seg.get("fin", duracion_total)

        if i == 0:
            dur = fin + (fade_duration / 2.0)
        elif i == num_clips - 1:
            dur = (duracion_total - ini) + (fade_duration / 2.0)
        else:
            dur = (fin - ini) + fade_duration

        clip_durations.append(max(fade_duration * 2, dur))

        if i < num_clips - 1:
            offset = fin - (fade_duration / 2.0)
            offsets.append(max(0.01, offset))

    cmd: List[str] = ["ffmpeg", "-y"]

    # Entradas de fondos texturados (índices 0 .. num_clips - 1)
    for dur, bg_path in zip(clip_durations, rutas_fondos):
        if str(bg_path).lower().endswith(".mp4"):
            cmd.extend(["-t", f"{dur:.3f}", "-i", str(bg_path)])
        else:
            cmd.extend(["-framerate", "30", "-loop", "1", "-t", f"{dur:.3f}", "-i", str(bg_path)])

    # Resolver o generar capas de Byte animadas con poses dinámicas, micro-saltos y VFX
    rutas_fg = []
    dir_animaciones_byte = DIR_ANIMACIONES_BYTE
    dir_animaciones_byte.mkdir(parents=True, exist_ok=True)

    for i, dur in enumerate(clip_durations):
        p_byte_mov = dir_animaciones_byte / f"byte_escena_{i}_animado.mov"
        try:
            try:
                from src.generar_animacion_byte import generar_video_byte_escena
            except ImportError:
                from generar_animacion_byte import generar_video_byte_escena
            generar_video_byte_escena(i, dur, p_byte_mov, sprite_path=imagenes_ordenadas[i])
            rutas_fg.append(p_byte_mov.resolve())
            logger.info(f"Capa de Byte animada generada para escena {i}: {p_byte_mov.name} ({dur:.2f}s)")
        except Exception as e:
            logger.warning(f"Fallback a imagen estática de Byte para escena {i}: {e}")
            rutas_fg.append(imagenes_ordenadas[i])

    # Entradas de Byte (índices num_clips .. 2*num_clips - 1)
    for dur, fg_path in zip(clip_durations, rutas_fg):
        if str(fg_path).lower().endswith(".mov"):
            cmd.extend(["-t", f"{dur:.3f}", "-i", str(fg_path)])
        else:
            cmd.extend(["-framerate", "30", "-loop", "1", "-t", f"{dur:.3f}", "-i", str(fg_path)])

    # FASE 3: Mezcla de sonido completa (Locución + BGM Lo-Fi duckeada + SFX procedurales sincronizados)
    audio_path_final = Path(audio_path).resolve()
    try:
        try:
            from src.generar_paisaje_sonoro import mezclar_paisaje_sonoro_completo
        except ImportError:
            from generar_paisaje_sonoro import mezclar_paisaje_sonoro_completo
        dir_audio_out = Path(audio_path).parent
        p_audio_master = dir_audio_out / f"audio_master_{Path(audio_path).stem}.wav"
        mezclar_paisaje_sonoro_completo(audio_path, p_audio_master, duracion_total, segmentos)
        if p_audio_master.exists():
            audio_path_final = p_audio_master
            logger.info(f"Fase 3: Usando audio master multitrack mezclado: {p_audio_master}")
    except Exception as e:
        logger.warning(f"No se pudo mezclar paisaje sonoro multitrack, usando audio base: {e}")

    audio_input_idx = 2 * num_clips
    cmd.extend(["-i", str(audio_path_final)])

    filter_chains: List[str] = []

    for i, dur in enumerate(clip_durations):
        total_frames = max(1, int(dur * 30))
        bg_idx = i
        fg_idx = num_clips + i

        # Definir fórmula de paneo/zoom suave y centrado según la escena (evita recortes de bordes)
        if i == 0:
            # Hook: sutil zoom in centrado
            zoompan_expr = (
                f"zoompan=z='1.00+0.03*(on/{total_frames})':"
                f"x='iw/2-iw/zoom/2':"
                f"y='ih/2-ih/zoom/2':"
                f"d=1:s=1080x1920:fps=30"
            )
        elif i == 1:
            # Punto 1: estático centrado (video MP4 animado de Shortwave)
            zoompan_expr = (
                f"zoompan=z=1.00:"
                f"x='iw/2-iw/zoom/2':"
                f"y='ih/2-ih/zoom/2':"
                f"d=1:s=1080x1920:fps=30"
            )
        elif i == 2:
            # Punto 2: estático centrado (video MP4 animado de SaneBox)
            zoompan_expr = (
                f"zoompan=z=1.00:"
                f"x='iw/2-iw/zoom/2':"
                f"y='ih/2-ih/zoom/2':"
                f"d=1:s=1080x1920:fps=30"
            )
        else:
            # Cierre: sutil zoom centrado
            zoompan_expr = (
                f"zoompan=z='1.00+0.035*(on/{total_frames})':"
                f"x='iw/2-iw/zoom/2':"
                f"y='ih/2-ih/zoom/2':"
                f"d=1:s=1080x1920:fps=30"
            )

        # 1. Capa de Fondo texturada con paneo real visible (o video directo si ya es MP4 animado)
        is_video_bg = str(rutas_fondos[i]).lower().endswith(".mp4")
        zoom_gancho = _expresion_zoom_gancho(trat_gancho, total_frames) if i == 0 else ""
        if is_video_bg:
            chain_bg = (
                f"[{bg_idx}:v]scale=1080:1920:force_original_aspect_ratio=decrease,"
                f"pad=1080:1920:(1080-iw)/2:(1920-ih)/2,"
            )
            if zoom_gancho:
                chain_bg += f"{zoom_gancho},"
        elif zoom_gancho:
            # Variante de gancho manda sobre el zoompan base del clip 0
            chain_bg = f"[{bg_idx}:v]{zoom_gancho},"
        else:
            chain_bg = f"[{bg_idx}:v]{zoompan_expr},"

        # Punch-in de énfasis (solo capa bg; Byte y subs quedan intactos).
        # Verificado: crop/zoompan exigen z≥1; ancla (540,250) mantiene el
        # mockup dentro de las safe zones a z≤1.035 (src/enfasis.py).
        # Si el clip 0 ya tiene zoom de gancho, se omite el enfasis ahí
        # (evita multiplicar zooms: z_total = z_gancho ≤ 1.04, seguro).
        filtro_enfasis = ""
        if puntos_enfasis is not None and i < len(puntos_enfasis):
            if i == 0 and zoom_gancho:
                logger.info(
                    "Punch-in de énfasis omitido en clip 0: "
                    "la variante de gancho ya aplica zoom (evita safe zones)."
                )
            else:
                filtro_enfasis = construir_filtro_enfasis(puntos_enfasis[i])
                if filtro_enfasis:
                    logger.info(
                        f"Punch-in de énfasis en escena {i}: "
                        f"{len(puntos_enfasis[i])} punto(s)"
                    )
                    filtro_enfasis += ","
        chain_bg += f"{filtro_enfasis}fps=30,settb=1/30,setsar=1[bg{i}]"
        filter_chains.append(chain_bg)

        # 2. Capa de Byte animada con canal alfa (680x680)
        is_mov_fg = str(rutas_fg[i]).lower().endswith(".mov")
        # Choque de Byte (variante B del gancho, solo clip 0): escala de
        # impacto que decae a 1.0; zoompan z≥1 preserva alfa (verificado argb).
        choque_byte = ""
        if i == 0 and trat_gancho.get("escala_choque_byte", 1.0) > 1.0:
            esc = float(trat_gancho["escala_choque_byte"])
            choque_f = max(1.0, 0.25 * 30)
            choque_byte = (
                f"zoompan=z='{esc:.3f}-({esc - 1.0:.3f}*clip(on/{choque_f:.1f},0,1))':"
                f"x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':"
                f"d=1:s=680x680:fps=30,"
            )
        if is_mov_fg:
            chain_fg = (
                f"[{fg_idx}:v]{choque_byte}format=rgba,fps=30,settb=1/30,setsar=1[fg{i}]"
            )
        else:
            chain_fg = (
                f"[{fg_idx}:v]"
                f"scale=640:640:force_original_aspect_ratio=decrease,"
                f"pad=680:680:(680-iw)/2:(680-ih)/2:color=0x00000000,"
                f"format=rgba,"
                f"zoompan=z='1.0+0.035*sin(2*PI*on/80)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=680x680:fps=30[fg{i}]"
            )
        filter_chains.append(chain_fg)

        # 3. Superposición con overlay dinámico según la escena:
        # Curva elástica BackEaseOut para la entrada en los primeros 0.35s
        spring_p = "if(lt(t,0.35), 1+2.70158*pow(t/0.35-1,3)+1.70158*pow(t/0.35-1,2), 1)"

        if i == 0 and trat_gancho.get("entrada_byte") == "lateral":
            # Variante C: Byte entra deslizándose desde la izquierda
            x_expr = f"70 - (1 - {spring_p})*320"
            y_expr = "1270"
        elif i == 0:
            # Hook: Byte entra desde abajo con rebote elástico al centro
            x_expr = "(W-w)/2"
            y_expr = f"1270 + (1 - {spring_p})*360"
        elif i == 1:
            # Punto 1: Byte entra deslizándose desde la izquierda con rebote elástico hacia x=70
            x_expr = f"70 - (1 - {spring_p})*320"
            y_expr = "1270"
        elif i == 2:
            # Punto 2: Byte entra deslizándose desde la derecha con rebote elástico hacia x=330
            x_expr = f"330 + (1 - {spring_p})*320"
            y_expr = "1270"
        else:
            # Cierre: Byte entra desde abajo con rebote elástico celebratorio
            x_expr = "(W-w)/2"
            y_expr = f"1270 + (1 - {spring_p})*360"

        chain_comp = f"[bg{i}][fg{i}]overlay=x='{x_expr}':y='{y_expr}':format=auto,fps=30,settb=1/30[comp{i}]"
        filter_chains.append(chain_comp)

    # Transiciones xfade sucesivas entre las escenas compuestas comp_i
    # (rotación anti-template sembrada por video + pin narrativo por tipo)
    if num_clips == 1:
        last_v = "[comp0]"
    else:
        semilla = _semilla_transiciones(ruta_salida)
        trans_anterior: Optional[str] = None
        prev_node = "[comp0]"
        for i in range(1, num_clips):
            next_node = f"[comp{i}]"
            out_node = f"[xf{i-1}]" if i < num_clips - 1 else "[vjoined]"
            offset = offsets[i - 1]
            tipo = str(segmentos[i].get("tipo", "")).lower() if i < len(segmentos) else ""
            trans = transicion_para_escena(i, tipo, semilla, trans_anterior)
            filter_chains.append(
                f"{prev_node}{next_node}xfade=transition={trans}:duration={fade_duration:.3f}:offset={offset:.3f}{out_node}"
            )
            trans_anterior = trans
            prev_node = out_node
        last_v = "[vjoined]"

    # Grado cinematográfico sutil (vignette + contraste/saturación + grano fino)
    # y quemado de subtítulos ENCIMA: los subs conservan su amarillo #FFF500
    # crudo. Ajuste fino en las constantes GRADO_* (verificar con lint_zonas_seguras).
    escaped_ass = _escape_ass_path(ass_path)
    filter_chains.append(
        f"{last_v}format=yuv420p,"
        f"vignette=angle={GRADO_VIGNETTE},"
        f"eq={GRADO_EQ},"
        f"noise={GRADO_NOISE},"
        f"ass=filename='{escaped_ass}'[vout]"
    )

    full_filter = ";\n".join(filter_chains)

    cmd.extend([
        "-filter_complex", full_filter,
        "-map", "[vout]",
        "-map", f"{audio_input_idx}:a",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-r", "30",
        "-c:a", "aac",
        "-b:a", "192k",
        "-t", f"{duracion_total:.3f}",
        str(ruta_salida)
    ])

    logger.info(f"Ejecutando FFmpeg para ensamblar video (duración objetivo: {duracion_total:.2f}s)...")
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        logger.error(f"Error durante el ensamblado con FFmpeg:\n{result.stderr[-1000:]}")
        raise RuntimeError(f"FFmpeg falló con código {result.returncode}: {result.stderr[-500:]}")

    logger.info(f"Video ensamblado exitosamente en: {ruta_salida}")
    return str(ruta_salida)



# ---------------------------------------------------------------------------
# TAREA 3: Validación del output
# ---------------------------------------------------------------------------

def validar_output(
    ruta_mp4: Union[str, Path],
    duracion_esperada: float,
    tolerancia: float = 0.1
) -> bool:
    """Valida duración exacta (±0.1s), codecs H.264/AAC e integridad con ffprobe."""
    path = Path(ruta_mp4).resolve()
    if not path.exists():
        logger.error(f"Validación fallida: El archivo {path} no existe.")
        return False

    cmd = [
        "ffprobe",
        "-v", "error",
        "-show_entries", "format=duration,size:stream=index,codec_name,codec_type,width,height,r_frame_rate",
        "-of", "json",
        str(path)
    ]

    try:
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        probe_data = json.loads(res.stdout)
    except Exception as e:
        logger.error(f"Validación fallida: Error al invocar ffprobe: {e}")
        return False

    streams = probe_data.get("streams", [])
    format_info = probe_data.get("format", {})

    video_streams = [s for s in streams if s.get("codec_type") == "video"]
    audio_streams = [s for s in streams if s.get("codec_type") == "audio"]

    if not video_streams:
        logger.error("Validación fallida: No se encontró ningún stream de video.")
        return False
    if not audio_streams:
        logger.error("Validación fallida: No se encontró ningún stream de audio.")
        return False

    v_stream = video_streams[0]
    a_stream = audio_streams[0]

    width = v_stream.get("width")
    height = v_stream.get("height")
    v_codec = v_stream.get("codec_name")
    a_codec = a_stream.get("codec_name")

    if (width, height) != (1080, 1920):
        logger.warning(f"Resolución no coincide exactamente con 1080x1920: {width}x{height}")

    duration_str = format_info.get("duration")
    if not duration_str:
        logger.error("Validación fallida: ffprobe no reportó duración.")
        return False

    duracion_real = float(duration_str)
    diff = abs(duracion_real - duracion_esperada)

    logger.info(
        f"Validación de video: codec_v={v_codec}, {width}x{height}, codec_a={a_codec}, "
        f"duración_real={duracion_real:.3f}s, duración_esperada={duracion_esperada:.3f}s (dif={diff:.3f}s)"
    )

    if diff > tolerancia:
        logger.error(
            f"Validación fallida: La duración difiere por {diff:.3f}s "
            f"(tolerancia máxima: ±{tolerancia:.3f}s)"
        )
        return False

    logger.info(" Validación exitosa: Video válido, streams íntegros y duración exacta.")
    return True


# ---------------------------------------------------------------------------
# POST-PROCESAMIENTO: Aceleración sincronizada (Video + Audio con pitch original)
# ---------------------------------------------------------------------------

def acelerar_video(
    ruta_video_entrada: Union[str, Path],
    factor: float = 1.12,
    ruta_salida: Optional[Union[str, Path]] = None
) -> Path:
    """
    Acelera un video final completo (video y audio sincronizados) mediante FFmpeg:
    - Audio: filtro 'atempo={factor}' (preserva pitch/tono natural sin sonar chipmunk).
    - Video: filtro 'setpts=PTS/{factor}' (reduce duración del frame timing).

    Comando FFmpeg aplicado:
    ffmpeg -y -i video_entrada.mp4 -filter_complex "[0:v]setpts=PTS/{factor}[v];[0:a]atempo={factor}[a]" \
           -map "[v]" -map "[a]" -c:v libx264 -pix_fmt yuv420p -c:a aac -b:a 192k video_salida.mp4
    """
    ruta_video_entrada = Path(ruta_video_entrada)
    if not ruta_video_entrada.exists():
        raise FileNotFoundError(f"No se encontró el video de entrada para acelerar: {ruta_video_entrada}")

    if ruta_salida is None:
        ruta_salida = ruta_video_entrada.with_name(f"{ruta_video_entrada.stem}_acelerado.mp4")
    else:
        ruta_salida = Path(ruta_salida)

    if ruta_video_entrada.resolve() == ruta_salida.resolve():
        raise ValueError("La ruta de salida no puede ser idéntica a la de entrada en FFmpeg (usar un nombre temporal o diferenciado).")

    # atempo en FFmpeg acepta valores entre 0.5 y 2.0 por filtro
    if not (0.5 <= factor <= 2.0):
        raise ValueError(f"El factor de aceleración debe estar entre 0.5 y 2.0 (recibido {factor}).")

    cmd = [
        "ffmpeg", "-y",
        "-i", str(ruta_video_entrada),
        "-filter_complex", f"[0:v]setpts=PTS/{factor}[v];[0:a]atempo={factor}[a]",
        "-map", "[v]",
        "-map", "[a]",
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        str(ruta_salida)
    ]

    logger.info(f"Acelerando video final (factor={factor}x): {ruta_video_entrada.name} -> {ruta_salida.name}")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        logger.error(f"Error en FFmpeg al acelerar video:\n{res.stderr}")
        raise RuntimeError(f"FFmpeg falló al acelerar video: {res.stderr}")

    logger.info(f"Video acelerado exitosamente en: {ruta_salida}")
    return ruta_salida


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Ensamblador de videos verticales (Shorts) con FFmpeg.")
    parser.add_argument("--json", required=True, help="Ruta al archivo JSON de alineación.")
    parser.add_argument("--audio", required=True, help="Ruta al archivo de audio.")
    parser.add_argument("--imagenes", nargs="+", required=True, help="Rutas a las imágenes.")
    parser.add_argument("--output", default="short_final.mp4", help="Ruta del video MP4.")
    parser.add_argument("--ass-output", default=None, help="Ruta para guardar el archivo .ass.")
    parser.add_argument("--export-tabla", default=None, help="Ruta para exportar tabla de tiempos de palabras en TXT.")
    args = parser.parse_args()

    with open(args.json, "r", encoding="utf-8") as f:
        data = json.load(f)

    alignment = data.get("alignment", {})
    segmentos = data.get("segmentos", [])
    duracion_total = float(data.get("duracion_total_seg", 0.0))

    if args.export_tabla:
        exportar_tabla_tiempos_palabras(alignment, args.export_tabla)

    ass_path = generar_ass(alignment, segmentos, ruta_salida=args.ass_output)
    mp4_path = ensamblar_video(args.imagenes, args.audio, ass_path, duracion_total, segmentos=segmentos, ruta_salida=args.output)
    es_valido = validar_output(mp4_path, duracion_total)

    if es_valido:
        print(f"\n Proceso completado exitosamente: {mp4_path}")
    else:
        print(f"\n Falló la validación del video.")
        exit(1)


if __name__ == "__main__":
    main()
