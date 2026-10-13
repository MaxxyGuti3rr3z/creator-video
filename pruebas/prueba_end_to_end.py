r"""
prueba_end_to_end.py
--------------------
Pipeline multi-guion de extremo a extremo (orquestador).

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

    --sin-enfasis    Desactiva el punch-in de énfasis (zoom breve sobre el
                      fondo+mockup en el inicio de palabra de cada escena; ver
                      src/enfasis.py). Activo por defecto en videos NO
                      cinemáticos (los cinemáticos tienen Byte horneado en el
                      bg y quedan excluidos para no escalarlo).

    --variantes-gancho=N   Renderiza N variantes VISUALES del gancho (clip 0)
                      con el mismo audio y ASS (0 créditos; ver
                      src/director_gancho.py). Default N=1 (solo la variante
                      de producción). Con N>1 las variantes extra quedan en
                      intermedios/variantes/ como material de A/B test; el
                      video de final/ es siempre la variante de producción.

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

Este archivo es solo el ORQUESTADOR (flags, PASO 1-7 y validaciones). La
lógica reutilizable vive en módulos extraídos durante la partición del monolito:
    src/bloques_narrativos.py   bloques narrativos y texto completo
    src/audio_elevenlabs.py     caché SHA-256, API ElevenLabs, fallback
    src/segmentacion.py         segmentos visuales y frames de preview
"""

from __future__ import annotations

import json
import logging
import os
from pathlib import Path
import subprocess
import sys
from typing import Any, Dict, Optional, Tuple, Union
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
    DIR_BYTE_TRANSPARENTES,
    DIR_GUIONES,
    RUTA_EXPERIMENTOS,
    ruta_video,
    ruta_guion,
)

from src.registro_experimentos import Experimento, registrar_experimento

from src.shorts_assembler import (
    generar_ass,
    quitar_fondo,
    ensamblar_video,
    acelerar_video,
    validar_output,
    exportar_tabla_tiempos_palabras,
    imprimir_diagnostico_caracteres,
)

from src.registro_videos import (
    resolver_carpeta,
    sprites_para,
    config_de_fondos,
    overlay_vacio,
    generar_fondos_del_video,
)

from src.chequeos_pipeline import pre_vuelo, post_vuelo, chequear_ass

from src.bloques_narrativos import (
    construir_bloques_narrativos,
    concatenar_texto_completo,
)

from src.audio_elevenlabs import (
    VOICE_SETTINGS_DEFAULT,
    calcular_hash_audio,
    cargar_indice_cache,
    generar_audio_con_timestamps_elevenlabs,
    sintetizar_audio_y_alignment_fallback,
)

from src.segmentacion import calcular_segmentos_reales, extraer_frames_preview

from src.enfasis import seleccionar_puntos_enfasis
from src.eventos_voz import palabras_de_segmento
from src.director_gancho import seleccionar_para_produccion, variantes_gancho

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
    # Punch-in de énfasis (zoom breve sobre bg+mockup; se desactiva con flag)
    sin_enfasis = "--sin-enfasis" in sys.argv

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
        rutas_fondos = generar_fondos_del_video(
            cfg_fondos, segmentos_reales, dir_fondos, forzar=forzar_fondos, alignment=alignment
        )


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

    # Punch-in de énfasis: solo en videos NO cinemáticos (en los cinemáticos
    # Byte está horneado en el bg y el zoom lo escalaría fuera de safe zones).
    # Candidatos: inicios de palabra (≥4 letras) de cada escena, tiempo local.
    puntos_enfasis: Optional[list] = None
    if sin_enfasis:
        logger.info("Punch-in de énfasis DESACTIVADO (--sin-enfasis).")
    elif overlay_vacio(nombre_base):
        logger.info(
            "Punch-in de énfasis omitido: video cinemático "
            "(Byte horneado en el fondo; el zoom lo escaló fuera de safe zones)."
        )
    else:
        puntos_enfasis = []
        for seg in segmentos_reales:
            inicio_seg = float(seg.get("inicio", 0.0))
            dur_seg = max(0.0, float(seg.get("fin", inicio_seg)) - inicio_seg)
            candidatos = [
                max(0.0, t_ini - inicio_seg)
                for palabra, t_ini, _t_fin in palabras_de_segmento(seg, alignment)
                if len(palabra) >= 4
            ]
            puntos = seleccionar_puntos_enfasis(candidatos, dur_seg)
            puntos_enfasis.append(puntos)
            if puntos:
                logger.info(
                    f"Enfasis escena {seg.get('tipo', '?')}: "
                    f"{len(puntos)} punch-in en t={[round(p.t_inicio, 2) for p in puntos]}"
                )

    # Variantes VISUALES del gancho (mismo audio/ASS => 0 créditos). La
    # variante de producción (A, o la preferida en ConfigVideo.gancho_preferido)
    # va a final/; con N>1 las demás quedan en intermedios/variantes/.
    variantes_gancho_n = 1
    for _arg in sys.argv:
        if _arg.startswith("--variantes-gancho="):
            try:
                variantes_gancho_n = max(1, int(_arg.split("=", 1)[1]))
            except ValueError:
                logger.warning(f"Valor inválido en --variantes-gancho: {_arg}")

    numero_video = int(guion.get("video", 0) or 0)
    preferido_gancho = getattr(cfg_fondos, "gancho_preferido", None) if cfg_fondos else None
    variantes = variantes_gancho(numero_video, arquetipo_preferido=preferido_gancho)
    prod_gancho = seleccionar_para_produccion(variantes)
    if variantes_gancho_n > 1 and len(variantes) > 1:
        variantes_a_render = list(variantes[:variantes_gancho_n])
    else:
        variantes_a_render = [prod_gancho]

    factor_aceleracion = 1.12
    duracion_esperada_acelerada = duracion_audio / factor_aceleracion
    ppm_acelerado = num_palabras / (duracion_esperada_acelerada / 60.0)
    ruta_mp4 = dir_final / f"video_{nombre_base}.mp4"
    es_valido = True

    for v in variantes_a_render:
        es_prod = (v is None) or (prod_gancho is not None and v.id == prod_gancho.id)
        # La variante de producción usa el nombre histórico del base (lo espera
        # lint_obsoleto); las demás llevan sufijo de variante.
        sufijo = "" if es_prod else f"_{v.id}"
        ruta_base_v = dir_intermedios / f"video_{nombre_base}_base{sufijo}.mp4"
        var_param = None if (v is None or v.arquetipo == "texto_pantalla") else v.arquetipo

        ensamblar_video(
            imagenes=rutas_imagenes_overlay,
            audio=ruta_audio,
            archivo_ass=ruta_ass,
            duracion_total=duracion_audio,
            segmentos=segmentos_reales,
            ruta_salida=ruta_base_v,
            fondos=rutas_fondos if rutas_fondos else None,
            fade_duration=0.15,
            puntos_enfasis=puntos_enfasis,
            variante_gancho=var_param
        )

        # -------------------------------------------------------------
        # PASO 6: Post-procesamiento: aceleración sincronizada (1.12x)
        # -------------------------------------------------------------
        if es_prod:
            ruta_out_v = ruta_mp4
        else:
            dir_variantes = dir_intermedios / "variantes"
            dir_variantes.mkdir(parents=True, exist_ok=True)
            ruta_out_v = dir_variantes / f"video_{nombre_base}_var_{v.id}.mp4"
        acelerar_video(
            ruta_video_entrada=ruta_base_v,
            factor=factor_aceleracion,
            ruta_salida=ruta_out_v
        )

        # -------------------------------------------------------------
        # PASO 7: Validación de la variante acelerada
        # -------------------------------------------------------------
        ok_v = validar_output(ruta_out_v, duracion_esperada=duracion_esperada_acelerada, tolerancia=0.15)
        etiqueta_v = f"{v.id} ({v.arquetipo})" if v else "única"
        print(f"\n[VARIANTE {etiqueta_v}] {'APROBADA' if ok_v else 'FALLIDA'} -> {ruta_out_v.name}")
        cod_v = 0
        if not sin_chequeo_final:
            cod_v = post_vuelo(ruta_out_v)
            if cod_v != 0:
                es_valido = False
        if es_prod:
            es_valido = es_valido and ok_v

        # Registro histórico del experimento (append-only, git-rastreable)
        try:
            registrar_experimento(
                RUTA_EXPERIMENTOS,
                Experimento(
                    video=numero_video,
                    variante_id=v.id if v else "-",
                    arquetipo_gancho=v.arquetipo if v else "-",
                    punch_enfasis=bool(puntos_enfasis),
                    ruta_mp4=str(ruta_out_v),
                    notas=(
                        f"ffprobe={'ok' if ok_v else 'fail'};"
                        f"post_vuelo={'skip' if sin_chequeo_final else ('ok' if cod_v == 0 else 'fail')}"
                    ),
                ),
            )
            logger.info(f"Experimento registrado en {RUTA_EXPERIMENTOS.name}")
        except OSError as e:
            logger.warning(f"No se pudo registrar el experimento: {e}")

    print("\n" + "=" * 65)
    print(f" [POST-PROCESAMIENTO] Aceleración {factor_aceleracion}x aplicada con FFmpeg:")
    print(f"  • Duración base original  : {duracion_audio:.2f}s (PPM: {ppm:.1f})")
    print(f"  • Duración final acelerada: {duracion_esperada_acelerada:.2f}s (PPM: {ppm_acelerado:.1f})")
    print(f"  • Variantes de gancho     : {len(variantes_a_render)} (producción: "
          f"{prod_gancho.id if prod_gancho else 'única'})")
    print("=" * 65 + "\n")

    # -------------------------------------------------------------
    # PASO 7 (cont.): Captura de frames de la variante de producción
    # -------------------------------------------------------------
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

    codigo_final = 0 if es_valido else 1
    return codigo_final


if __name__ == "__main__":
    sys.exit(main())
