r"""
chequeos_pipeline.py
--------------------
Integración de las validaciones automáticas al pipeline end-to-end.

pre_vuelo (ANTES de gastar créditos ElevenLabs):
  1. validar_guion: puntos en narración o términos prohibidos bloquean el
     arranque (corrige el guion o gasta créditos con audio malo).
  2. lint_obsoleto sobre la carpeta destino (cheques fondos + sprites):
     caché vencida bloquea para no renderizar con artefactos viejos
     (el bug que hizo salir el video 14 con el layout anterior).

PASO 5 (DESPUÉS de generar_ass, ANTES de ensamblar_video):
  3. lint_subtitulos sobre el .ass: estilo 46px / color amarillo / chunks
     y \N correctos (bloquea el render si el subtítulo está mal).

post_vuelo (DESPUÉS del render, antes de publicar):
  4. lint_zonas_seguras sobre el MP4 final: contenido en zonas prohibidas
     de TikTok/Reels marca "no publicar" (exit code != 0).

Todas las funciones devuelven 0 (continuar) o 1 (bloquear) y son de solo
lectura. Escape: --saltar-validacion (pre y ASS) y --sin-chequeo-final
(post) en pruebas/prueba_end_to_end.py.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import List, Optional

DIR_RAIZ = Path(__file__).resolve().parent.parent
if str(DIR_RAIZ) not in sys.path:
    sys.path.insert(0, str(DIR_RAIZ))

from src.validar_guion import validar_guion  # noqa: E402
from pruebas.lint_obsoleto import main as _lint_obsoleto_main  # noqa: E402
from pruebas.lint_zonas_seguras import main as _lint_zonas_main  # noqa: E402
from pruebas.lint_subtitulos import main as _lint_subtitulos_main  # noqa: E402

_SEPARADOR = "=" * 65


def _ejecutar(funcion, argv: List[str]) -> int:
    """Ejecuta el main() de un linter y normaliza su código de salida."""
    try:
        return int(funcion(argv) or 0)
    except SystemExit as e:
        return int(e.code or 0)


def pre_vuelo(
    ruta_guion: Optional[Path],
    carpeta_video: Optional[Path],
) -> int:
    """
    Validaciones previas a ElevenLabs. Devuelve 0 si se puede continuar,
    1 si hay que abortar (errores de guion o caché vencida en la carpeta).
    """
    bloqueos = 0

    print(f"\n{_SEPARADOR}")
    print(" [PRE-VUELO] Validaciones antes de gastar créditos")
    print(_SEPARADOR)

    if ruta_guion is not None and Path(ruta_guion).exists():
        resultado = validar_guion(Path(ruta_guion))
        for advertencia in resultado["advertencias"]:
            print(f"  [AVISO] guion: {advertencia}")
        if resultado["valido"]:
            palabras = resultado["detalles"]["total_palabras"]
            dur = resultado["detalles"]["duracion_estimada_seg"]
            print(f"  [OK]    guion: {Path(ruta_guion).name} sin errores ({palabras} palabras, ~{dur}s)")
        else:
            bloqueos += 1
            for error in resultado["errores"]:
                print(f"  [FAIL]  guion: {error}")
    else:
        print("  [ -- ]  guion: sin archivo para validar (se omite)")

    if carpeta_video is not None and Path(carpeta_video).is_dir():
        rc = _ejecutar(
            _lint_obsoleto_main,
            [str(carpeta_video), "--solo", "fondos", "--solo", "sprites"],
        )
        bloqueos += rc
    else:
        print("  [ -- ]  artefactos: carpeta inexistente (se omite)")

    if bloqueos:
        print(f"\n[PRE-VUELO] BLOQUEADO ({bloqueos} cheque(s) fallaron).")
        print("  Corrige los errores y vuelve a correr; o forzá la salida con")
        print("  --saltar-validacion bajo tu responsabilidad.")
        return 1

    print("\n[PRE-VUELO] OK — se puede gastar el audio con confianza.")
    return 0


def post_vuelo(ruta_mp4: Optional[Path], guardar_evidencia: bool = True) -> int:
    """
    Chequeo post-render sobre el MP4 final. Devuelve 0 si es publicable,
    1 si hay contenido en zonas prohibidas (no publicar / re-renderizar).
    """
    print(f"\n{_SEPARADOR}")
    print(" [POST-VUELO] Safe Zones sobre el video final")
    print(_SEPARADOR)

    if ruta_mp4 is None or not Path(ruta_mp4).exists():
        print("  [ -- ]  sin MP4 final para verificar (se omite)")
        return 0

    argv = [str(ruta_mp4)]
    if not guardar_evidencia:
        argv.append("--sin-evidencia")
    rc = _ejecutar(_lint_zonas_main, argv)

    if rc:
        print("\n[POST-VUELO] NO PUBLICAR — el video tiene contenido en zonas prohibidas.")
        print("  Corrige los mockups (ver detalle arriba y test_artifacts/lint_evidencia/) y re-renderizá.")
        return 1

    print("\n[POST-VUELO] OK — zonas seguras, el video es publicable.")
    return 0


def chequear_ass(ruta_ass: Path) -> int:
    r"""
    Valida el .ass recién generado contra la especificación (estilo 46px,
    color amarillo, chunks y \N). Devuelve 0 (continuar a ensamblar) o 1
    (bloquear: el estilo o los chunks no son correctos).
    """
    print(f"\n{_SEPARADOR}")
    print(" [CHEQUEO ASS] Subtítulos conformes a especificación")
    print(_SEPARADOR)

    if ruta_ass is None or not Path(ruta_ass).exists():
        print("  [ -- ]  sin .ass para verificar (se omite)")
        return 0

    rc = _ejecutar(_lint_subtitulos_main, [str(ruta_ass)])

    if rc:
        print("\n[CHEQUEO ASS] BLOQUEADO — subtítulos fuera de especificación.")
        print("  Corrige generar_ass / chunks (ver detalle arriba) y reintentá.")
        return 1

    print("\n[CHEQUEO ASS] OK — subtítulos conformes, se puede ensamblar.")
    return 0
