"""
Test de equivalencia: lógica histórica (if/elif de prueba_end_to_end.py)
versus registro central src/registro_videos.py.

Las funciones `_vieja_*` son copias literales de los bloques originales del
monolito de pruebas/prueba_end_to_end.py; hoy el orquestador los invoca como
resolver_carpeta (~161), sprites_para (~285), overlay_vacio (~298) y
config_de_fondos (~313). Si este test pasa, el registro nuevo reproduce
exactamente el comportamiento anterior.

Ejecutar: python pruebas/test_registro_videos.py
"""
import sys
import unittest
from pathlib import Path

DIR_RAIZ = Path(__file__).resolve().parent.parent
if str(DIR_RAIZ) not in sys.path:
    sys.path.insert(0, str(DIR_RAIZ))

from src.rutas import DIR_GUIONES, DIR_BYTE_TRANSPARENTES, DIR_BYTE_ILUSTRACIONES
from src.registro_videos import (
    CONFIGS,
    config_de_fondos,
    obtener_generador,
    overlay_vacio,
    resolver_carpeta,
    sprites_para,
)

T = DIR_BYTE_TRANSPARENTES
I = DIR_BYTE_ILUSTRACIONES


def _set(base, *pares):
    return tuple((clave, base / nombre) for clave, nombre in pares)


# ---------------------------------------------------------------------------
# Copias literales de la lógica original
# ---------------------------------------------------------------------------

def _vieja_carpeta(stem: str):
    # 15 es nuevo (carpeta canónica desde su nacimiento); 14 igual;
    # 12/13 pasaron del fallback video_<stem> a carpeta canónica explícita
    if "15" in stem or "celular" in stem:
        return stem, "video_15_ia_celular"
    elif "14" in stem or "agua" in stem:
        return stem, "video_14_agua_ia"
    elif "13" in stem or "noticias" in stem:
        return stem, "video_13_noticias_ia_realidad"
    elif "12" in stem or "ciberseguridad" in stem or "google_ads" in stem:
        return stem, "video_12_ciberseguridad_google_ads"
    elif "03" in stem or "tareas" in stem:
        return "guion_03", "video_03_tareas"
    elif "02" in stem or "reuniones" in stem:
        return "guion_02", "video_02_reuniones"
    elif "04" in stem or "correo" in stem:
        return "guion_04", "video_04_correo"
    elif "05" in stem or "presentaciones" in stem:
        return "guion_05", "video_05_presentaciones"
    elif "06" in stem or "atencion" in stem or "soporte" in stem:
        return "guion_06", "video_06_atencion_clientes"
    elif "07" in stem or "excel" in stem or "reportes" in stem:
        return "guion_07", "video_07_excel_reportes"
    elif "08" in stem or "busqueda" in stem or "investigacion" in stem:
        return "guion_08_busqueda_investigacion", "video_08_busqueda_investigacion"
    elif "10" in stem or "cotizacion" in stem or "presupuesto" in stem:
        return "guion_10_cotizacion_automatica", "video_10_cotizacion_automatica"
    elif "11" in stem or "cincuenta" in stem or "archivos" in stem:
        return "guion_11_cincuenta_archivos", "video_11_cincuenta_archivos"
    elif "09" in stem or "diseno" in stem or "flyers" in stem:
        return "guion_09_diseno_flyers", "video_09_diseno_flyers"
    elif "01" in stem or "bandeja" in stem:
        return "prueba_real", "video_01_bandeja_correo"
    return stem, f"video_{stem}"


def _viejos_sprites(nombre_base, mockup_sugerido):
    if "15" in nombre_base or "celular" in nombre_base:
        return (
            ("cold_open", I / "byte_perfil.png"),
            ("hook", T / "byte_agotado_transparente.png"),
            ("problema", I / "byte_señalando_serio.png"),
            ("punto_1", T / "byte_computadora_feliz_transparente.png"),
            ("punto_2", T / "punto_2_guion_08_busqueda_investigacion_transparente.png"),
            ("resultado", T / "punto1_feliz_transparente.png"),
            ("cierre", T / "cierre_saltando_transparente.png"),
        )
    elif "14" in nombre_base or "agua" in nombre_base:
        return _set(
            T,
            ("cold_open", "hook_estresado_transparente.png"),
            ("hook", "byte_cortocircuito_transparente.png"),
            ("problema", "punto_1_guion_13_noticias_ia_realidad_transparente.png"),
            ("punto_1", "punto1_feliz_transparente.png"),
            ("punto_2", "punto_2_guion_13_noticias_ia_realidad_transparente.png"),
            ("resultado", "byte_computadora_feliz_transparente.png"),
            ("cierre", "cierre_guion_13_noticias_ia_realidad_transparente.png"),
        )
    elif "13" in nombre_base or "noticias" in nombre_base:
        return _set(
            T,
            ("cold_open", "cierre_transparente.png"),
            ("hook", "punto1_feliz_transparente.png"),
            ("problema", "punto_1_guion_08_busqueda_investigacion_transparente.png"),
            ("punto_1", "punto_2_guion_08_busqueda_investigacion_transparente.png"),
            ("punto_2", "punto_2_guion_08_busqueda_investigacion_transparente.png"),
            ("resultado", "resultado_guion_10_cotizacion_automatica_transparente.png"),
            ("cierre", "cierre_saltando_transparente.png"),
        )
    elif "12" in nombre_base or "ciberseguridad" in nombre_base or "google_ads" in nombre_base:
        return _set(
            T,
            ("cold_open", "punto_1_guion_08_busqueda_investigacion_transparente.png"),
            ("hook", "hook_estresado_transparente.png"),
            ("problema", "byte_cortocircuito_transparente.png"),
            ("punto_1", "punto_1_guion_08_busqueda_investigacion_transparente.png"),
            ("punto_2", "punto_2_guion_08_busqueda_investigacion_transparente.png"),
            ("resultado", "resultado_guion_10_cotizacion_automatica_transparente.png"),
            ("cierre", "cierre_saltando_transparente.png"),
        )
    elif "11" in nombre_base or "cincuenta" in nombre_base or "archivos" in nombre_base:
        return _set(
            T,
            ("cold_open", "escena_problema_guion_03_transparente.png"),
            ("hook", "punto_2_guion_10_cotizacion_automatica_transparente.png"),
            ("problema", "byte_cortocircuito_transparente.png"),
            ("punto_1", "byte_computadora_feliz_transparente.png"),
            ("punto_2", "resultado_guion_08_busqueda_investigacion_transparente.png"),
            ("resultado", "cierre_guion_07_transparente.png"),
            ("cierre", "cierre_saltando_transparente.png"),
        )
    elif "10" in nombre_base or "cotizacion" in nombre_base or "presupuesto" in nombre_base:
        return _set(
            T,
            ("cold_open", "cierre_transparente.png"),
            ("hook", "punto_2_guion_04_transparente.png"),
            ("problema", "byte_computadora_feliz_transparente.png"),
            ("punto_1", "punto_1_guion_04_transparente.png"),
            ("punto_2", "punto_2_guion_08_busqueda_investigacion_transparente.png"),
            ("resultado", "cierre_guion_04_transparente.png"),
            ("cierre", "cierre_saltando_transparente.png"),
        )
    elif "09" in nombre_base or "diseno" in nombre_base or "flyers" in nombre_base:
        return _set(
            T,
            ("cold_open", "byte_agotado_transparente.png"),
            ("hook", "punto_2_guion_04_transparente.png"),
            ("problema", "byte_cortocircuito_transparente.png"),
            ("punto_1", "punto_1_guion_04_transparente.png"),
            ("punto_2", "cierre_transparente.png"),
            ("resultado", "cierre_guion_04_transparente.png"),
            ("cierre", "cierre_guion_08_busqueda_investigacion_transparente.png"),
        )
    elif "08" in nombre_base or "busqueda" in nombre_base or "investigacion" in nombre_base:
        return _set(
            T,
            ("cold_open", "cold_open_guion_08_busqueda_investigacion_transparente.png"),
            ("hook", "hook_guion_08_busqueda_investigacion_transparente.png"),
            ("problema", "problema_guion_08_busqueda_investigacion_transparente.png"),
            ("punto_1", "punto_1_guion_08_busqueda_investigacion_transparente.png"),
            ("punto_2", "punto_2_guion_08_busqueda_investigacion_transparente.png"),
            ("resultado", "resultado_guion_08_busqueda_investigacion_transparente.png"),
            ("cierre", "cierre_guion_08_busqueda_investigacion_transparente.png"),
        )
    elif "07" in nombre_base or "excel" in nombre_base:
        return _set(
            T,
            ("cold_open", "byte_cortocircuito_transparente.png"),
            ("hook", "hook_guion_07_transparente.png"),
            ("problema", "problema_guion_07_transparente.png"),
            ("punto_1", "punto_1_guion_07_transparente.png"),
            ("punto_2", "punto_2_guion_07_transparente.png"),
            ("resultado", "resultado_guion_07_transparente.png"),
            ("cierre", "cierre_guion_07_transparente.png"),
        )
    elif (
        mockup_sugerido == "gestor_tareas"
        or "04" in nombre_base or "correo" in nombre_base
        or "05" in nombre_base or "presentaciones" in nombre_base
        or "06" in nombre_base or "atencion" in nombre_base
    ):
        return _set(
            I,
            ("escena_problema", "byte_estresado.png"),
            ("punto_1", "byte_ojos_estrella.png"),
            ("punto_2", "Byte_enojado_computadora.png"),
            ("resultado", "byte_pacifico_rodeados_archivos.png"),
            ("cierre", "byte_saltando_feliz.png"),
        )
    elif mockup_sugerido == "reunion_transcripcion":
        return _set(
            I,
            ("hook", "byte_estresado.png"),
            ("punto1", "byte_ojos_estrella.png"),
            ("punto2", "byte_pacifico_rodeados_archivos.png"),
            ("cierre", "byte_saltando_feliz.png"),
        )
    return _set(
        I,
        ("hook", "Byte_enojado_computadora.png"),
        ("punto1", "byte_ojos_estrella.png"),
        ("punto2", "byte_pacifico_rodeados_archivos.png"),
        ("cierre", "byte_señalando_serio.png"),
    )


def _viejo_overlay(nombre_base) -> bool:
    return (
        "06" in nombre_base or "atencion" in nombre_base
        or "07" in nombre_base or "excel" in nombre_base
        or "08" in nombre_base or "busqueda" in nombre_base
        or "investigacion" in nombre_base
        or "09" in nombre_base or "diseno" in nombre_base
        or "flyers" in nombre_base
        or "10" in nombre_base or "cotizacion" in nombre_base
        or "11" in nombre_base or "cincuenta" in nombre_base
        or "archivos" in nombre_base
        or "12" in nombre_base or "ciberseguridad" in nombre_base
        or "google_ads" in nombre_base
        or "13" in nombre_base or "noticias" in nombre_base
        or "14" in nombre_base or "agua" in nombre_base
        or "15" in nombre_base or "celular" in nombre_base
    )


def _viejo_generador(nombre_base, mockup_sugerido):
    if ("15" in nombre_base or "celular" in nombre_base
            or mockup_sugerido in ["celular_ia", "celular"]):
        return "generar_video_interactivo_celular_ia"
    if ("14" in nombre_base or "agua" in nombre_base
            or mockup_sugerido in ["agua_ia", "agua"]):
        return "generar_video_interactivo_agua_ia"
    if mockup_sugerido == "gestor_tareas" or ("03" in nombre_base and "04" not in nombre_base):
        return "generar_video_interactivo_tareas"
    if "04" in nombre_base or "correo" in nombre_base or mockup_sugerido == "asistente_correo":
        return "generar_video_interactivo_correo"
    if mockup_sugerido == "reunion_transcripcion":
        return "generar_video_interactivo_reunion"
    if "05" in nombre_base or "presentaciones" in nombre_base or mockup_sugerido == "presentaciones":
        return "generar_video_interactivo_presentaciones"
    if "06" in nombre_base or "atencion" in nombre_base or mockup_sugerido == "atencion_clientes":
        return "generar_video_interactivo_atencion_clientes"
    if "07" in nombre_base or "excel" in nombre_base or mockup_sugerido in ["excel_reportes", "dinamico_con_memes"]:
        return "generar_video_interactivo_excel_reportes"
    if ("08" in nombre_base or "busqueda" in nombre_base or "investigacion" in nombre_base
            or mockup_sugerido == "busqueda_investigacion"):
        return "generar_video_interactivo_busqueda_investigacion"
    if ("09" in nombre_base or "diseno" in nombre_base or "flyers" in nombre_base
            or mockup_sugerido in ["diseno_flyers", "flyers"]):
        return "generar_video_interactivo_diseno_flyers"
    if ("10" in nombre_base or "cotizacion" in nombre_base
            or mockup_sugerido in ["cotizacion_automatica", "cotizacion"]):
        return "generar_video_interactivo_cotizacion_automatica"
    if ("11" in nombre_base or "cincuenta" in nombre_base or "archivos" in nombre_base
            or mockup_sugerido in ["cincuenta_archivos", "archivos"]):
        return "generar_video_interactivo_cincuenta_archivos"
    if ("12" in nombre_base or "ciberseguridad" in nombre_base or "google_ads" in nombre_base
            or mockup_sugerido in ["ciberseguridad_google_ads", "ciberseguridad"]):
        return "generar_video_interactivo_ciberseguridad_google_ads"
    if ("13" in nombre_base or "noticias" in nombre_base
            or mockup_sugerido in ["noticias_ia_realidad", "noticias"]):
        return "generar_video_interactivo_noticias_ia_realidad"
    return None


# ---------------------------------------------------------------------------
# Matrices de entrada
# ---------------------------------------------------------------------------

MOCKUPS = [
    "gestor_tareas", "reunion_transcripcion", "asistente_correo", "presentaciones",
    "atencion_clientes", "excel_reportes", "dinamico_con_memes", "busqueda_investigacion",
    "diseno_flyers", "flyers", "cotizacion_automatica", "cotizacion",
    "cincuenta_archivos", "archivos", "ciberseguridad_google_ads", "ciberseguridad",
    "noticias_ia_realidad", "noticias", "agua_ia", "agua", "celular_ia", "celular",
    "bandeja_correo", None,
]


def _stems_de_prueba():
    stems = sorted(p.stem for p in DIR_GUIONES.glob("guion_*.json"))
    stems += [
        "guion_01_bandeja_correo", "guion_12_ciberseguridad_google_ads",
        "guion_13_noticias_ia_realidad", "guion_99_desconocido", "prueba_real",
    ]
    return stems


def _nombre_bases_de_prueba():
    nombres = sorted({resolver_carpeta(s)[0] for s in _stems_de_prueba()})
    nombres += [
        "guion_06", "guion_07", "guion_08", "guion_04_correo_extra",
        "video_guion_13_noticias_ia_realidad", "desconocido_total",
    ]
    # sin duplicados, preservando orden
    vistos, salida = set(), []
    for n in nombres:
        if n not in vistos:
            vistos.add(n)
            salida.append(n)
    return salida


class TestEquivalenciaRegistro(unittest.TestCase):

    def test_carpeta_por_stem(self):
        for stem in _stems_de_prueba():
            self.assertEqual(
                resolver_carpeta(stem), _vieja_carpeta(stem),
                f"resolver_carpeta difiere para stem '{stem}'",
            )

    def test_sprites(self):
        for nombre in _nombre_bases_de_prueba():
            for mockup in MOCKUPS:
                self.assertEqual(
                    sprites_para(nombre, mockup), _viejos_sprites(nombre, mockup),
                    f"sprites difieren para nombre_base='{nombre}' mockup='{mockup}'",
                )

    def test_overlay_vacio(self):
        for nombre in _nombre_bases_de_prueba():
            self.assertEqual(
                overlay_vacio(nombre), _viejo_overlay(nombre),
                f"overlay difiere para nombre_base='{nombre}'",
            )

    def test_generador_de_fondos(self):
        for nombre in _nombre_bases_de_prueba():
            for mockup in MOCKUPS:
                cfg = config_de_fondos(nombre, mockup)
                nuevo = cfg.generador_fondos if cfg else None
                self.assertEqual(
                    nuevo, _viejo_generador(nombre, mockup),
                    f"generador difiere para nombre_base='{nombre}' mockup='{mockup}'",
                )

    def test_todos_los_generadores_resuelven(self):
        for cfg in CONFIGS:
            if cfg.generador_fondos:
                fn = obtener_generador(cfg.generador_fondos)
                self.assertTrue(callable(fn), f"{cfg.generador_fondos} no es callable")

    def test_catalogo_cubre_los_guiones(self):
        """Cada guion del catálogo cae en una carpeta esperada de videos/."""
        esperado = {
            "guion_02_reuniones": "video_02_reuniones",
            "guion_03_tareas": "video_03_tareas",
            "guion_04_correo": "video_04_correo",
            "guion_05_presentaciones": "video_05_presentaciones",
            "guion_06_atencion_clientes": "video_06_atencion_clientes",
            "guion_07_excel_reportes": "video_07_excel_reportes",
            "guion_08_busqueda_investigacion": "video_08_busqueda_investigacion",
            "guion_09_diseno_flyers": "video_09_diseno_flyers",
            "guion_10_cotizacion_automatica": "video_10_cotizacion_automatica",
            "guion_11_cincuenta_archivos": "video_11_cincuenta_archivos",
            "guion_12_ciberseguridad_google_ads": "video_12_ciberseguridad_google_ads",
            "guion_13_noticias_ia_realidad": "video_13_noticias_ia_realidad",
            "guion_14_agua_ia": "video_14_agua_ia",
            "guion_15_ia_celular": "video_15_ia_celular",
        }
        for p in sorted(DIR_GUIONES.glob("guion_*.json")):
            self.assertIn(p.stem, esperado, f"guion sin predecir: {p.name}")
            _, carpeta = resolver_carpeta(p.stem)
            self.assertEqual(carpeta, esperado[p.stem], f"carpeta mal para {p.name}")


if __name__ == "__main__":
    unittest.main(verbosity=2)
