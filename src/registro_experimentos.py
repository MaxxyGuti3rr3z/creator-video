"""
src.registro_experimentos
 ---------------------------------------------------------------------------
 Registro histórico de experimentos del pipeline (A/B test de ganchos y
 otras variables). Cada variante renderizada agrega una fila a un CSV
 append-only rastreado por git (datos/experimentos.csv).

 La fila deja trazable: qué variante se produjo, con qué tratamiento de
 gancho, si llevó punch-in de énfasis, y a qué ruta de MP4 correspondió.
 El CSV es un REGISTRO (no un estado): solo se agrega, nunca se reescribe.

 Escritura mínima y controlada (append con cabecera si no existe). La
 lógica de formato (dataclass, columnas, conversión de fila) es pura y se
 prueba sin tocar disco.
"""

from __future__ import annotations

import csv
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional, Union

# Orden fijo de columnas del CSV (si se añade una, va al final)
COLUMNAS: tuple[str, ...] = (
    "fecha_utc",
    "video",
    "variante_id",
    "arquetipo_gancho",
    "punch_enfasis",
    "ruta_mp4",
    "notas",
)


@dataclass(frozen=True)
class Experimento:
    """Una fila del registro de experimentos.

    - fecha_utc: ISO-8601 con Z (hora UTC); si es None se usa la actual.
    - video: número entero del video (ej. 15).
    - variante_id: "A"/"B"/"C" (o "-" si no hay A/B test).
    - arquetipo_gancho: arquetipo visual del gancho (ver src/director_gancho.py)
      o "-" si es el control histórico.
    - punch_enfasis: True si la variante llevó punch-in de énfasis.
    - ruta_mp4: ruta del MP4 producido (como string, portable).
    - notas: texto libre corto (contexto del experimento).
    """

    video: int
    variante_id: str
    arquetipo_gancho: str
    punch_enfasis: bool
    ruta_mp4: str
    notas: str = ""
    fecha_utc: Optional[str] = None


def _fecha_actual_utc() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def formatear_fila(exp: Experimento) -> List[str]:
    """Convierte un Experimento en las celdas del CSV, en orden COLUMNAS."""
    fecha = exp.fecha_utc or _fecha_actual_utc()
    d = asdict(exp)
    d["fecha_utc"] = fecha
    d["punch_enfasis"] = "si" if exp.punch_enfasis else "no"
    return [str(d[col]) for col in COLUMNAS]


def registrar_experimento(
    ruta_csv: Union[str, Path],
    exp: Experimento,
) -> Path:
    """Agrega una fila al CSV (crea el archivo con cabecera si no existe).

    No valida ni bloquea: es un registro histórico append-only. Devuelve la
    ruta resuelta del CSV.
    """
    ruta = Path(ruta_csv).resolve()
    ruta.parent.mkdir(parents=True, exist_ok=True)
    existe = ruta.exists() and ruta.stat().st_size > 0
    with open(ruta, "a", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f)
        if not existe:
            escritor.writerow(COLUMNAS)
        escritor.writerow(formatear_fila(exp))
    return ruta


def leer_experimentos(ruta_csv: Union[str, Path]) -> List[Dict[str, str]]:
    """Lee todas las filas del CSV como dicts (para auditorías/tests)."""
    ruta = Path(ruta_csv)
    if not ruta.exists():
        return []
    with open(ruta, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))
