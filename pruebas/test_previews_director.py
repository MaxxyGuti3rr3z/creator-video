"""
test_previews_director.py
-------------------------
Genera previews en PNG de los 5 arquetipos cinematográficos para el Guion 05 (Presentaciones e Informes).
Permite verificar la composición visual antes de renderizar el video completo.
"""

import sys
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass
from pathlib import Path
DIR_RAIZ = Path(__file__).resolve().parent.parent
if str(DIR_RAIZ) not in sys.path:
    sys.path.insert(0, str(DIR_RAIZ))

from PIL import Image
from src.rutas import DIR_VIDEOS, DIR_BYTE_TRANSPARENTES
from src.mockups.director_escena import (
    renderizar_plano_hero_caos,
    renderizar_plano_showcase_panoramico,
    renderizar_plano_split_before_after,
    renderizar_plano_deck_3d,
    renderizar_plano_host_community,
    renderizar_escena_por_arquetipo
)

DIR_OUT = DIR_VIDEOS / "video_05_presentaciones" / "intermedios" / "previews_director"
DIR_OUT.mkdir(parents=True, exist_ok=True)

ARQUETIPOS = [
    ("01_hero_caos", "PLANO_HERO_CAOS", 2.0, 5.0, {
        "badge": "HORAS PERDIDAS",
        "tit": "Informes interminables",
        "sub": "Buscando datos y acomodando diapositivas a mano"
    }),
    ("02_showcase_gamma", "PLANO_SHOWCASE_PANORAMICO", 2.5, 6.0, {
        "app_nombre": "Gamma App",
        "app_url": "gamma.app/new-deck",
        "prompt": "Generar presentación ejecutiva de 8 diapositivas...",
        "badge_herramienta": "HERRAMIENTA 1 • GAMMA",
        "titulo_accion": "De una idea a presentación completa en segundos"
    }),
    ("03_split_canva", "PLANO_SPLIT_BEFORE_AFTER", 2.0, 5.5, {
        "badge_herramienta": "HERRAMIENTA 2 • CANVA IA",
        "titulo_accion": "Pulido visual y estilización automática",
        "antes_tit": "Informe crudo y plano",
        "despues_tit": "Diseño profesional y dinámico"
    }),
    ("04_deck_3d", "PLANO_DECK_3D", 2.0, 5.0, {
        "badge_resultado": "RESULTADO FINAL",
        "titulo_resultado": "Material listo y profesional",
        "subtitulo_resultado": "Sin convertir cada informe en un proyecto eterno"
    }),
    ("05_host_community", "PLANO_HOST_COMMUNITY", 1.5, 4.0, {
        "pregunta": "¿Cuál parte de tus informes automatizarías primero?",
        "opciones": [
            ("A", "La búsqueda y resumen de datos", True),
            ("B", "El diseño de las diapositivas", False),
            ("C", "La redacción de conclusiones", False),
        ]
    }),
]

def main():
    print("[DIRECTOR DE ESCENA] Generando previews de los 5 arquetipos...")
    generados = []
    for prefijo, arq, t_sec, dur, cfg in ARQUETIPOS:
        salida = DIR_OUT / f"preview_{prefijo}.png"
        img = renderizar_escena_por_arquetipo(
            arquetipo=arq,
            ancho=1080,
            alto=1920,
            t_sec=t_sec,
            duracion=dur,
            config=cfg
        )
        img.save(salida, "PNG")
        generados.append(salida)
        print(f"  [OK] {prefijo} ({arq}) -> {salida.resolve()}")

    print(f"\n[OK] Se generaron {len(generados)} previews en: {DIR_OUT.resolve()}")

if __name__ == "__main__":
    main()
