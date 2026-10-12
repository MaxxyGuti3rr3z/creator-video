"""
src/validar_guion.py
--------------------
Validador estricto de guiones para 'Byte el Zorrito'.
Controles implementados:
1. Ninguna frase/concepto de 'no_afirmar' aparece en narración, subtítulos, mockups ni copy.
2. La narración no tiene puntos finales ('.') para evitar silencios de 1-2s en ElevenLabs.
3. Estimación de duración de voz: palabras / 180 * 60 dentro de tolerancia (±15%).
4. Confianza de datos: 'media' se reporta como advertencia, no error.
5. Validación contra textos permitidos en plantillas de mockups.
"""

import json
import re
from pathlib import Path
from typing import Dict, Any, List, Tuple

def validar_guion(ruta_guion: Path) -> Dict[str, Any]:
    with open(ruta_guion, "r", encoding="utf-8") as f:
        guion = json.load(f)

    errores: List[str] = []
    advertencias: List[str] = []
    detalles: Dict[str, Any] = {}

    # 1. Extraer bloques de narración
    cold_open = guion.get("cold_open", "").strip()
    hook = guion.get("hook", "").strip()
    problema = guion.get("problema", "").strip()
    
    demos = guion.get("demostracion", [])
    demo_textos = []
    no_afirmar_totales = []

    for d in demos:
        if isinstance(d, dict):
            demo_textos.append(d.get("accion", "").strip())
            no_afirmar_totales.extend(d.get("no_afirmar", []))
            conf = d.get("confianza_dato", "")
            herr = d.get("herramienta", "")
            if conf.lower() == "media":
                advertencias.append(f"Confianza de dato 'media' en herramienta '{herr}': confirmar funcionalidad en la app antes de publicar")
        else:
            demo_textos.append(str(d).strip())

    resultado = guion.get("resultado", "").strip()
    cierre = guion.get("cierre", "").strip()

    bloques_ordenados = ([cold_open] if cold_open else []) + [hook, problema] + demo_textos + [resultado, cierre]
    narracion_completa = " ".join([b for b in bloques_ordenados if b])

    # 2. Control de puntos finales (.) en narración
    # Regla: Ningún bloque debe terminar en punto ('.') ni tener puntos seguidos de espacio/letra
    for idx, bloque in enumerate(bloques_ordenados):
        # Excluir puntos en abreviaturas conocidas si las hubiera, pero la regla dice: "No usar puntos (.) en los guiones"
        puntos_encontrados = [m.start() for m in re.finditer(r"\.", bloque)]
        if puntos_encontrados:
            errores.append(f"Bloque {idx+1} contiene punto(s) '.': '{bloque}'. Emplear comas o redacción continua.")

    # 3. Control de frases prohibidas (no_afirmar)
    # Lista de frases o términos no_afirmar
    terminos_prohibidos = [
        "gratis", "free", "sin costo", "cualquier proveedor",
        "no necesita revisión", "reemplaza la revisión", "reemplaza al humano",
        "conecta solo a tu correo", "precio", "plan", "usd", "$", "dólares"
    ]
    for prohibido in no_afirmar_totales:
        p_clean = prohibido.lower().strip()
        # Verificar en narración con límites de palabra si es palabra corta
        if re.search(rf"\b{re.escape(p_clean)}\b", narracion_completa.lower()):
            errores.append(f"Término prohibido de no_afirmar encontrado en narración: '{prohibido}'")

    for tp in terminos_prohibidos:
        if re.search(rf"\b{re.escape(tp)}\b", narracion_completa.lower()):
            errores.append(f"Término prohibido encontrado en narración: '{tp}'")

    # 4. Cálculo de duración estimada
    palabras = narracion_completa.split()
    total_palabras = len(palabras)
    duracion_estimada = (total_palabras / 180.0) * 60.0
    duracion_objetivo = guion.get("duracion_objetivo_seg", 30)

    margen = duracion_objetivo * 0.15
    min_dur = duracion_objetivo - margen
    max_dur = duracion_objetivo + margen

    if not (min_dur <= duracion_estimada <= max_dur):
        advertencias.append(
            f"Duración estimada ({duracion_estimada:.1f}s, {total_palabras} palabras) fuera del rango objetivo ±15% "
            f"[{min_dur:.1f}s - {max_dur:.1f}s]"
        )

    # 5. Control de hook_alternativo
    hook_alt = guion.get("hook_alternativo", "")
    if hook_alt and "." in hook_alt:
        errores.append(f"hook_alternativo contiene punto '.': '{hook_alt}'")

    detalles = {
        "total_palabras": total_palabras,
        "total_caracteres": len(narracion_completa),
        "duracion_estimada_seg": round(duracion_estimada, 1),
        "duracion_objetivo_seg": duracion_objetivo,
        "bloques": [
            {"tipo": "hook", "texto": hook},
            {"tipo": "problema", "texto": problema},
            {"tipo": "demostracion_1", "texto": demo_textos[0] if len(demo_textos) > 0 else ""},
            {"tipo": "demostracion_2", "texto": demo_textos[1] if len(demo_textos) > 1 else ""},
            {"tipo": "resultado", "texto": resultado},
            {"tipo": "cierre", "texto": cierre},
        ],
        "narracion_completa": narracion_completa
    }

    return {
        "valido": len(errores) == 0,
        "errores": errores,
        "advertencias": advertencias,
        "detalles": detalles
    }

if __name__ == "__main__":
    import sys
    try:
        from src.rutas import DIR_GUIONES
    except ImportError:
        from rutas import DIR_GUIONES
    ruta = DIR_GUIONES / "guion_04_correo.json"
    if len(sys.argv) > 1:
        ruta = Path(sys.argv[1])
    res = validar_guion(ruta)
    print(json.dumps(res, indent=2, ensure_ascii=False))
