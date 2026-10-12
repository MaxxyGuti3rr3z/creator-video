r"""
bloques_narrativos.py
---------------------
Construcción de los bloques narrativos de un guion y concatenación del texto
completo de narración para ElevenLabs.

Extraído verbatim de `pruebas/prueba_end_to_end.py` (PASO 1) durante la
partición del monolito; sin cambios de comportamiento.
"""

from __future__ import annotations

from typing import Any, Dict, List


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
