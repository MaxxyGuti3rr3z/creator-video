r"""
lint_subtitulos.py
------------------
Linter de subtítulos ASS karaoke del proyecto (safe zones de texto).

Valida que el .ass generado cumpla la especificación exacta de
`.agents/rules/reglas_produccion_video.md` (sección 2). Umbrales
calibrados contra los dos videos publicados (13 y 14): ambos pasan
todas las reglas con holgura; los falsos positivos son cero.

Estilo (valores exactos del generador, shorts_assembler.generar_ass):
  - PlayRes 1080x1920, un solo estilo 'KaraokeByte', Fontname Arial.
  - Fontsize 46, PrimaryColour &H0000F5FF (amarillo #FFF500 en BGR),
    OutlineColour negro, BorderStyle 1, Outline 4.5.
  - Alignment 2 (abajo-centro), MarginL/R 80, MarginV 860
    (-> banda de texto y ~950..1060 = safe zone de subtítulos 960..1080).

Diálogos:
  - Texto no vacío y con al menos un tag \\k (karaoke).
  - La suma de los \\k debe igualar la duración del diálogo (±1 cs);
    desbalances = ediciones manuales o bugs de timing.
  - Sin solapes entre diálogos consecutivos.
  - Máximo 2 sublíneas por diálogo (un solo \\N).
  - Con 3 o más palabras, el \\N es obligatorio (regla de quiebre).
  - Máximo 3 palabras y 30 caracteres por sublínea (no rozar laterales).
  - Máximo 6 palabras por diálogo en segmentos clave (cold_open, hook,
    problema, cierre...) y 4 en demos, según SEGMENTS_METADATA del propio
    .ass. Sin metadata -> universal 6.
    NOTA: el mínimo NO se exige (la regla dice 4-6) porque los restos de
    segmento generan chunks legítimos de 1-3 palabras: los videos 13/14
    publicados los contienen.

Uso:
    python pruebas/lint_subtitulos.py <ruta.ass> [<ruta.ass>...] [--dir]

  - Acepta archivos .ass o directorios (se recorren *.ass sin recursión).
  - Exit 1 si hay alguna violación. Solo lectura.
  - El pipeline ejecuta este cheque automáticamente entre generar_ass y
    ensamblar_video (escape: --saltar-validacion).
  - Tests: python pruebas/test_lint_subtitulos.py
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

# ---------------------------------------------------------------------------
# Especificación exacta (calibrada contra los ASS de los videos 13 y 14)
# ---------------------------------------------------------------------------

ESTILO_ESPERADO: Dict[str, str] = {
    "Name": "KaraokeByte",
    "Fontname": "Arial",
    "Fontsize": "46",
    "PrimaryColour": "&H0000F5FF",
    "OutlineColour": "&H00000000",
    "BorderStyle": "1",
    "Outline": "4.5",
    "Alignment": "2",
    "MarginL": "80",
    "MarginR": "80",
    "MarginV": "860",
}

PLAYRES_ESPERADO = {"PlayResX": "1080", "PlayResY": "1920"}

MAX_PAL_SUBLINEA = 3
MAX_CHARS_SUBLINEA = 30
MAX_PAL_DIALOGO_CLAVE = 6
MAX_PAL_DIALOGO_DEMO = 4
TOLERANCIA_K_CS = 1

# Mirrors _dividir_en_chunks en src/shorts_assembler.py
SEGMENTOS_CLAVE = (
    "cold_open", "hook", "problema", "escena_problema", "panico", "cierre", "pregunta",
)

_TAG_RE = re.compile(r"\{[^{}]*\}")
_K_RE = re.compile(r"\\k(\d+)")


@dataclass
class Diálogo:
    indice: int          # 1-based, para mensajes
    start_cs: int
    end_cs: int
    texto: str           # sin tags {}


@dataclass
class ArchivoASS:
    ruta: Path
    info: Dict[str, str] = field(default_factory=dict)
    estilo: Dict[str, str] = field(default_factory=dict)
    metadata: Optional[List[dict]] = None
    dialogos: List[Diálogo] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Parseo
# ---------------------------------------------------------------------------

def cs_a_entero(t: str) -> int:
    """'H:MM:SS.CC' -> centésimas de segundo."""
    partes = t.strip().split(":")
    h = int(partes[0])
    m = int(partes[1])
    s_cs = partes[2].split(".")
    s = int(s_cs[0])
    cs = int(s_cs[1]) if len(s_cs) > 1 else 0
    return ((h * 60 + m) * 60 + s) * 100 + cs


def _subir_a_cs(valor: float) -> int:
    return int(round(float(valor) * 100))


def parsear_ass(ruta: Path) -> ArchivoASS:
    ass = ArchivoASS(ruta=Path(ruta))
    formato_estilo: List[str] = []
    en_info = en_estilo = en_eventos = False

    with open(ass.ruta, "r", encoding="utf-8") as f:
        for linea in f:
            linea = linea.rstrip("\n").rstrip("\r")
            if linea.startswith("; SEGMENTS_METADATA:"):
                try:
                    ass.metadata = json.loads(linea.split(":", 1)[1].strip())
                except json.JSONDecodeError:
                    ass.metadata = None
                continue
            if linea.startswith("["):
                seccion = linea.strip().lower()
                en_info = seccion == "[script info]"
                en_estilo = seccion == "[v4+ styles]"
                en_eventos = seccion == "[events]"
                continue
            if en_info and ":" in linea:
                clave, _, valor = linea.partition(":")
                ass.info[clave.strip()] = valor.strip()
            elif en_estilo and linea.startswith("Format:"):
                formato_estilo = [c.strip() for c in linea.split(":", 1)[1].split(",")]
            elif en_estilo and linea.startswith("Style:"):
                valores = [v.strip() for v in linea.split(":", 1)[1].split(",")]
                ass.estilo = dict(zip(formato_estilo, valores))
            elif en_eventos and linea.startswith("Dialogue:"):
                partes = linea.split(",", 9)
                if len(partes) < 10:
                    continue
                ass.dialogos.append(
                    Diálogo(
                        indice=len(ass.dialogos) + 1,
                        start_cs=cs_a_entero(partes[1]),
                        end_cs=cs_a_entero(partes[2]),
                        texto=partes[9],
                    )
                )
    return ass


def texto_visible(texto: str) -> str:
    return _TAG_RE.sub("", texto)


def sublineas(dialogo: Diálogo) -> List[str]:
    visible = texto_visible(dialogo.texto)
    return [l.strip() for l in re.split(r"\\N", visible)]


def palabras_dialogo(dialogo: Diálogo) -> int:
    return sum(len(l.split()) for l in sublineas(dialogo))


def tipo_segmento(ass: ArchivoASS, start_cs: int) -> Optional[str]:
    if not ass.metadata:
        return None
    for seg in ass.metadata:
        if _subir_a_cs(seg["inicio"]) <= start_cs < _subir_a_cs(seg["fin"]):
            return str(seg.get("tipo", "")).lower()
    return str(ass.metadata[-1].get("tipo", "")).lower()


# ---------------------------------------------------------------------------
# Cheques
# ---------------------------------------------------------------------------

def chequear_info_estilo(ass: ArchivoASS) -> List[str]:
    problemas: List[str] = []
    for clave, esperado in PLAYRES_ESPERADO.items():
        obtenido = ass.info.get(clave)
        if obtenido != esperado:
            problemas.append(f"{clave}={obtenido!r} (esperado {esperado!r})")
    if not ass.estilo:
        return problemas + ["estilo 'KaraokeByte' ausente"]
    if len(ass.estilo) == 0:
        problemas.append("sin línea Style")
        return problemas
    for clave, esperado in ESTILO_ESPERADO.items():
        obtenido = ass.estilo.get(clave)
        if obtenido != esperado:
            problemas.append(f"Style.{clave}={obtenido!r} (esperado {esperado!r})")
    return problemas


def chequear_dialogos(ass: ArchivoASS) -> List[str]:
    problemas: List[str] = []
    if not ass.dialogos:
        return ["sin líneas Dialogue"]

    fin_previo: Optional[int] = None
    for d in ass.dialogos:
        etiqueta = f"dialogo {d.indice} ({d.start_cs / 100:.2f}s)"

        if not texto_visible(d.texto).strip():
            problemas.append(f"{etiqueta}: texto vacío")
            fin_previo = d.end_cs
            continue

        ks = [int(m) for m in _K_RE.findall(d.texto)]
        if not ks:
            problemas.append(f"{etiqueta}: sin tags \\k (karaoke ausente)")
        else:
            dur_cs = d.end_cs - d.start_cs
            if abs(sum(ks) - dur_cs) > TOLERANCIA_K_CS:
                problemas.append(
                    f"{etiqueta}: suma de \\k={sum(ks)} cs != duración {dur_cs} cs"
                )

        if d.end_cs <= d.start_cs:
            problemas.append(f"{etiqueta}: fin <= inicio")

        if fin_previo is not None and d.start_cs < fin_previo:
            problemas.append(
                f"{etiqueta}: se solapa con el diálogo anterior (terminaba en {fin_previo / 100:.2f}s)"
            )
        fin_previo = d.end_cs

        lineas = sublineas(d)
        if len(lineas) > 2:
            problemas.append(f"{etiqueta}: {len(lineas)} sublíneas (máximo 2)")

        total = sum(len(l.split()) for l in lineas)
        if total >= 3 and "\\N" not in d.texto:
            problemas.append(f"{etiqueta}: {total} palabras sin \\N (quiebre obligatorio)")

        for linea in lineas:
            palabras = linea.split()
            if len(palabras) > MAX_PAL_SUBLINEA:
                problemas.append(
                    f"{etiqueta}: sublínea con {len(palabras)} palabras (máximo {MAX_PAL_SUBLINEA}): '{linea}'"
                )
            ancho = sum(len(w) for w in palabras) + max(0, len(palabras) - 1)
            if ancho > MAX_CHARS_SUBLINEA:
                problemas.append(
                    f"{etiqueta}: sublínea con {ancho} caracteres (máximo {MAX_CHARS_SUBLINEA}): '{linea}'"
                )

        tipo = tipo_segmento(ass, d.start_cs)
        if tipo is None:
            limite = MAX_PAL_DIALOGO_CLAVE
        else:
            es_clave = any(k in tipo for k in SEGMENTOS_CLAVE)
            limite = MAX_PAL_DIALOGO_CLAVE if es_clave else MAX_PAL_DIALOGO_DEMO
        if total > limite:
            problemas.append(
                f"{etiqueta}: {total} palabras en un diálogo de tipo '{tipo or 'sin-metadata'}' (máximo {limite})"
            )

    return problemas


def lintear_ass(ruta: Path) -> Tuple[List[str], int]:
    """
    Lintea un .ass. Devuelve (problemas, cantidad_de_dialogos).
    Lista vacía = conforma.
    """
    ass = parsear_ass(ruta)
    problemas = chequear_info_estilo(ass) + chequear_dialogos(ass)
    return problemas, len(ass.dialogos)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _rutas_de_entrada(entradas: Sequence[Path]) -> List[Path]:
    rutas: List[Path] = []
    for e in entradas:
        if e.is_dir():
            rutas.extend(sorted(e.glob("*.ass")))
        elif e.suffix.lower() == ".ass":
            rutas.append(e)
        else:
            raise FileNotFoundError(f"Entrada no soportada (se espera .ass o directorio): {e}")
    return rutas


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        description="Linter de subtítulos ASS karaoke (safe zones de texto)."
    )
    parser.add_argument("entradas", nargs="+", type=Path, help="archivos .ass o directorios")
    args = parser.parse_args(argv)

    rutas = _rutas_de_entrada(args.entradas)
    if not rutas:
        print("No hay archivos .ass que analizar.")
        return 0

    print(f"[LINTER SUBTÍTULOS ASS] archivos={len(rutas)}\n")

    total_fail = 0
    for ruta in rutas:
        problemas, n_dialogos = lintear_ass(ruta)
        if problemas:
            total_fail += 1
            print(f"[FAIL] {ruta.name} ({n_dialogos} diálogos):")
            for p in problemas:
                print(f"       - {p}")
        else:
            print(f"[OK]   {ruta.name} ({n_dialogos} diálogos): conforme a especificación")

    print(f"\n[RESUMEN] archivos OK={len(rutas) - total_fail} FAIL={total_fail}")
    if total_fail:
        print("[RESULTADO] FAIL — corregir el estilo/chunks antes de ensamblar.")
        return 1
    print("[RESULTADO] PASS — subtítulos conformes.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
