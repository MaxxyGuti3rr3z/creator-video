r"""
segmentacion.py
---------------
Cálculo de segmentos visuales a partir del alignment carácter-por-carácter y
extracción de frames de preview del video final.

Extraído verbatim de `pruebas/prueba_end_to_end.py` (PASO 3 y PASO 7) durante
la partición del monolito; sin cambios de comportamiento.
"""

from __future__ import annotations

import re
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional


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
