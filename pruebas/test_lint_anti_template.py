"""
Test unitario del linter anti-template (pruebas/lint_anti_template.py).

Usa guiones y catálogos sintéticos en tmp; no depende del catálogo real
salvo dos tests de propiedad (estructura y byte_agotado en cero sobre
guiones/ + registro, que son datos rastreados por git).

Ejecutar: python pruebas/test_lint_anti_template.py
"""
import json
import sys
import tempfile
import unittest
from pathlib import Path

DIR_RAIZ = Path(__file__).resolve().parent.parent
if str(DIR_RAIZ) not in sys.path:
    sys.path.insert(0, str(DIR_RAIZ))

from pruebas.lint_anti_template import (
    FORMATOS_ROTACION,
    VideoCatalogo,
    cargar_catalogo,
    checar_videos,
    clasificar_cierre,
    main,
)


def video(numero, estructura=None, cierre="",
          sprites=(("hook", "a.png"), ("cierre", "b.png"))):
    return VideoCatalogo(
        numero=numero, nombre=f"guion_{numero:02d}_x",
        estructura=estructura if estructura is not None else f"gen_{numero}",
        cierre=cierre, sprites=tuple(sprites),
    )


def escribir_guion(tmp: Path, numero: int, cierre="Contame en comentarios",
                   tipo_mockup=None, mockup_sugerido=None) -> Path:
    data = {"cierre": cierre}
    if tipo_mockup is not None:
        data["tipo_mockup"] = tipo_mockup
    if mockup_sugerido is not None:
        data["mockup_sugerido"] = mockup_sugerido
    p = tmp / f"guion_{numero:02d}_x.json"
    p.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
    return p


class TestClasificarCierre(unittest.TestCase):
    def test_encuesta_abc(self):
        self.assertEqual(
            clasificar_cierre("¿Sos Team Canva o Team Photoshop a mano? Contame abajo"),
            "encuesta_abc",
        )

    def test_battle_vs(self):
        self.assertEqual(clasificar_cierre("¿Canva vs Photoshop?"), "battle_vs")

    def test_medidor_dolor(self):
        self.assertEqual(
            clasificar_cierre("¿Cuántos archivos tenés acumulados en tu compu?"),
            "medidor_dolor",
        )

    def test_compartir(self):
        self.assertEqual(
            clasificar_cierre("Compartile este video con datos reales y contame si te lo creíste"),
            "compartir",
        )

    def test_pregunta_debate(self):
        self.assertEqual(
            clasificar_cierre("Contame en comentarios cómo tomás notas"),
            "pregunta_debate",
        )

    def test_otro(self):
        self.assertEqual(clasificar_cierre("Para mí, esto sí es ahorrar tiempo"), "otro")

    def test_vacio_es_otro(self):
        self.assertEqual(clasificar_cierre(""), "otro")
        self.assertEqual(clasificar_cierre(None), "otro")

    def test_todos_los_formatos_son_validos(self):
        for f in ("encuesta_abc", "battle_vs", "pregunta_debate", "medidor_dolor"):
            self.assertIn(f, FORMATOS_ROTACION)


class TestChecarVideos(unittest.TestCase):
    def test_videos_sanos_sin_problemas(self):
        vids = [
            video(1, estructura="gen_a", cierre="Contame en comentarios"),
            video(2, estructura="gen_b", cierre="¿Cuántos archivos tenés?"),
        ]
        self.assertEqual(checar_videos(vids), [])

    def test_misma_estructura_consecutiva_falla(self):
        vids = [video(1, estructura="gen_a"), video(2, estructura="gen_a")]
        probs = checar_videos(vids)
        self.assertEqual([p.check for p in probs], ["estructura"])

    def test_estructuras_distintas_pasan(self):
        vids = [video(1, estructura="gen_a"), video(2, estructura="gen_b")]
        self.assertEqual(checar_videos(vids), [])

    def test_estructura_desconocido_no_compara(self):
        vids = [video(1, estructura="desconocido"), video(2, estructura="desconocido")]
        self.assertEqual(checar_videos(vids), [])

    def test_byte_agotado_consecutivo_falla(self):
        sprites_agotado = (("cold_open", "byte_agotado_transparente.png"), ("cierre", "x.png"))
        vids = [
            video(1, sprites=sprites_agotado),
            video(2, sprites=sprites_agotado),
        ]
        probs = checar_videos(vids)
        self.assertEqual([p.check for p in probs], ["byte_agotado"])

    def test_byte_agotado_aislado_pasa(self):
        vids = [
            video(1, sprites=(("cold_open", "byte_agotado_transparente.png"),)),
            video(2, sprites=(("cold_open", "feliz.png"),)),
        ]
        self.assertEqual(checar_videos(vids), [])

    def test_sprite_repetido_escenas_consecutivas_falla(self):
        v = video(1, sprites=(("punto_1", "m.png"), ("punto_2", "m.png")))
        probs = checar_videos([v])
        self.assertEqual([p.check for p in probs], ["sprite_escenas"])

    def test_sprite_repetido_no_consecutivo_pasa(self):
        v = video(1, sprites=(("a", "x.png"), ("b", "y.png"), ("c", "x.png")))
        self.assertEqual(checar_videos([v]), [])

    def test_cierre_debate_repetido_falla(self):
        vids = [
            video(1, cierre="Contame en comentarios"),
            video(2, cierre="Dejame tu historia abajo"),
        ]
        probs = checar_videos(vids)
        self.assertEqual([p.check for p in probs], ["cierre"])

    def test_cierre_otro_repetido_no_falla(self):
        cierre = "Para mí, esto sí es ahorrar tiempo"
        vids = [video(1, cierre=cierre), video(2, cierre=cierre)]
        self.assertEqual(checar_videos(vids), [])

    def test_numeros_no_adyacentes_no_se_comparan(self):
        vids = [
            video(13, cierre="Contame en comentarios"),
            video(15, cierre="Contame en comentarios"),
        ]
        self.assertEqual(checar_videos(vids), [])

    def test_video_unico_solo_chequeo_interno(self):
        v = video(7, sprites=(("a", "m.png"), ("b", "m.png")))
        probs = checar_videos([v])
        self.assertEqual([p.check for p in probs], ["sprite_escenas"])
        self.assertEqual(probs[0].numeros, (7,))


class TestCargarCatalogo(unittest.TestCase):
    def test_usa_generador_del_registro_para_videos_reales(self):
        with tempfile.TemporaryDirectory() as tmp:
            ruta = escribir_guion(Path(tmp), 13, tipo_mockup="x")
            vids = cargar_catalogo([ruta])
        self.assertEqual(len(vids), 1)
        self.assertEqual(
            vids[0].estructura, "generar_video_interactivo_noticias_ia_realidad"
        )
        self.assertTrue(vids[0].sprites)  # sprites resueltos desde registro

    def test_videos_desconocidos_usan_campo_del_guion(self):
        with tempfile.TemporaryDirectory() as tmp:
            ruta = escribir_guion(Path(tmp), 90, tipo_mockup="mock_a")
            vids = cargar_catalogo([ruta])
        self.assertEqual(vids[0].estructura, "mock_a")
        self.assertEqual(vids[0].sprites, ())

    def test_mockup_sugerido_tiene_prioridad(self):
        with tempfile.TemporaryDirectory() as tmp:
            ruta = escribir_guion(
                Path(tmp), 91, tipo_mockup="t", mockup_sugerido="s"
            )
            vids = cargar_catalogo([ruta])
        self.assertEqual(vids[0].estructura, "s")

    def test_orden_por_numero(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            r12 = escribir_guion(tmp, 12)
            r2 = escribir_guion(tmp, 2)
            vids = cargar_catalogo([r12, r2])
        self.assertEqual([v.numero for v in vids], [2, 12])

    def test_mismo_numero_gana_la_ultima_ruta(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            r_vieja = escribir_guion(tmp, 90, tipo_mockup="vieja")
            r_nueva = escribir_guion(tmp, 90, tipo_mockup="nueva")
            vids = cargar_catalogo([r_vieja, r_nueva])
        self.assertEqual(vids[0].estructura, "nueva")


class TestCLI(unittest.TestCase):
    def test_catalogo_sano_exit_0(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            escribir_guion(tmp, 90, tipo_mockup="mock_a",
                           cierre="Contame en comentarios")
            escribir_guion(tmp, 91, tipo_mockup="mock_b",
                           cierre="¿Cuántos archivos tenés?")
            rc = main(["--dir", str(tmp)])
        self.assertEqual(rc, 0)

    def test_catalogo_con_violacion_exit_1(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            escribir_guion(tmp, 90, tipo_mockup="mock_a",
                           cierre="Contame en comentarios")
            escribir_guion(tmp, 91, tipo_mockup="mock_a",
                           cierre="Dejame tu historia abajo")
            rc = main(["--dir", str(tmp)])
        self.assertEqual(rc, 1)

    def test_foco_video_limpio_ignora_vecino_sucio(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            # 90 y 91 repiten cierre (violación del par), pero el foco es 92
            escribir_guion(tmp, 90, tipo_mockup="a",
                           cierre="Contame en comentarios")
            escribir_guion(tmp, 91, tipo_mockup="b",
                           cierre="Dejame tu historia abajo")
            escribir_guion(tmp, 92, tipo_mockup="c",
                           cierre="¿Cuántos archivos tenés?")
            rc = main(["--dir", str(tmp), str(tmp / "guion_92_x.json")])
        self.assertEqual(rc, 0)

    def test_foco_video_sucio_exit_1(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp)
            escribir_guion(tmp, 90, tipo_mockup="a",
                           cierre="Contame en comentarios")
            escribir_guion(tmp, 91, tipo_mockup="b",
                           cierre="Dejame tu historia abajo")
            rc = main(["--dir", str(tmp), str(tmp / "guion_91_x.json")])
        self.assertEqual(rc, 1)

    def test_dir_vacio_exit_0(self):
        with tempfile.TemporaryDirectory() as tmp:
            rc = main(["--dir", tmp])
        self.assertEqual(rc, 0)


class TestPropiedadCatalogoReal(unittest.TestCase):
    """Propiedades que deben mantenerse sobre guiones/ + registro (git-tracked)."""

    def test_estructura_unica_entre_consecutivos(self):
        guiones = sorted((DIR_RAIZ / "guiones").glob("guion_*.json"))
        vids = cargar_catalogo(guiones)
        probs = [p for p in checar_videos(vids) if p.check == "estructura"]
        self.assertEqual(probs, [], "dos videos consecutivos comparten estructura")

    def test_byte_agotado_nunca_consecutivo(self):
        guiones = sorted((DIR_RAIZ / "guiones").glob("guion_*.json"))
        vids = cargar_catalogo(guiones)
        probs = [p for p in checar_videos(vids) if p.check == "byte_agotado"]
        self.assertEqual(probs, [], "byte_agotado aparece en videos consecutivos")


if __name__ == "__main__":
    unittest.main(verbosity=2)
