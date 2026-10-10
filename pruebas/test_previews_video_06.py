"""
test_previews_video_06.py
-------------------------
Genera previews en PNG de los 5 arquetipos cinematográficos para el Guion 06 (Atención al cliente con IA).
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
from src.rutas import DIR_VIDEOS
from src.mockups.director_escena import renderizar_escena_por_arquetipo

DIR_OUT = DIR_VIDEOS / "video_06_atencion_clientes" / "intermedios" / "previews_director"
DIR_OUT.mkdir(parents=True, exist_ok=True)

ARQUETIPOS_V06 = [
    ("01_hero_caos", "PLANO_HERO_CAOS", 2.0, 5.0, {
        "badge": "MENSAJES REPETITIVOS A MANO",
        "elementos": [
            {"x": 60, "y": 240, "w": 330, "h": 160, "rot": -10, "tit": "¿Cuánto sale el envío?", "sub": "Pregunta #1 • Sin responder", "col": (225, 29, 72)},
            {"x": 660, "y": 230, "w": 330, "h": 170, "rot": 12, "tit": "¿Tienen stock disponible?", "sub": "Pregunta #2 • Esperando 2h", "col": (225, 29, 72)},
            {"x": 40, "y": 870, "w": 320, "h": 150, "rot": 8, "tit": "¿Cuáles son los horarios?", "sub": "Pregunta #3 • Clientes impacientes", "col": (245, 158, 11)},
            {"x": 690, "y": 910, "w": 330, "h": 160, "rot": -8, "tit": "¿Cómo hago para pagar?", "sub": "Pregunta #4 • Misma duda diaria", "col": (225, 29, 72)},
        ]
    }),
    ("02_showcase_fin", "PLANO_SHOWCASE_PANORAMICO", 2.5, 6.0, {
        "header": "Intercom Fin • Agente de IA Activo 24/7",
        "badge": "⚡ Soporte Autónomo",
        "titulo": "Consulta de Cliente: Envíos al Interior",
        "subtitulo": "Fin lee tu centro de ayuda y responde con precisión en 2 segundos",
        "items": [
            ("01 • Duda Cliente", "¿Hacen envíos al interior del país?", (37, 99, 235), (239, 246, 255)),
            ("02 • RAG en Docs", "Consultando base de conocimiento...", (124, 58, 237), (245, 243, 255)),
            ("03 • Respuesta Fin", "Sí, entregas en 24 a 48 hs hábiles", (5, 150, 105), (236, 253, 245))
        ],
        "footer": "Ticket resuelto al instante sin tocar el teclado"
    }),
    ("03_split_lyro", "PLANO_SPLIT_BEFORE_AFTER", 2.0, 5.5, {
        "antes_tag": "ANTES",
        "antes_tit": "Soporte manual lento y con demoras",
        "antes_items": [
            "• Cliente esperando 4 horas fuera de horario",
            "• Mensajes repetidos colapsando la bandeja",
            "• Equipo saturado respondiendo siempre lo mismo"
        ],
        "separador": "TIDIO LYRO AI",
        "despues_tag": "DESPUÉS",
        "despues_tit": "Resolución automática las 24 horas",
        "pills_despues": [
            ("Cero Espera", "Respuestas en 3 segundos a las 03:00 AM", (124, 58, 237), (245, 243, 255)),
            ("Entrenado con FAQs", "Cita artículos oficiales sin alucinar", (14, 165, 233), (240, 249, 255)),
            ("Equipo Liberado", "Foco 100% en dudas complejas y ventas", (16, 185, 129), (236, 253, 245))
        ]
    }),
    ("04_deck_3d", "PLANO_DECK_3D", 2.0, 5.0, {
        "titulo": "¡Bandeja de Soporte en Cero!",
        "subtitulo": "Lo repetitivo resuelto, foco en lo que necesita atención humana",
        "cards": [
            {"x_off": -180, "y": 380, "tit": "Ticket #182 • Envíos", "desc": "Resuelto por IA al instante", "rot": -7, "col": (37, 99, 235)},
            {"x_off": 180, "y": 380, "tit": "Ticket #184 • Precios", "desc": "Resuelto por IA al instante", "rot": 7, "col": (124, 58, 237)},
            {"x_off": 0, "y": 360, "tit": "Ticket #183 • Caso VIP", "desc": "Derivado a atención humana", "rot": 0, "col": (16, 185, 129)}
        ],
        "pills": [
            ("Menos Caos", (16, 185, 129)),
            ("Más Liviano", (14, 165, 233)),
            ("Foco Humano", (124, 58, 237))
        ]
    }),
    ("05_host_community", "PLANO_HOST_COMMUNITY", 1.5, 4.0, {
        "pregunta_tit": "PREGUNTA A LA COMUNIDAD:",
        "pregunta_l1": "¿Cuántas horas al día perdés",
        "pregunta_l2": "respondiendo mensajes?",
        "opciones": [
            ("A", "1 a 2 horas respondiendo lo mismo", (37, 99, 235), (239, 246, 255)),
            ("B", "Medio día atado a contestar mensajes", (124, 58, 237), (245, 243, 255)),
            ("C", "Vivo contestando dudas todo el día", (16, 185, 129), (236, 253, 245)),
        ],
        "callout": "Contame abajo"
    }),
]

def main():
    print("[DIRECTOR DE ESCENA - VIDEO 06] Generando previews de los 5 arquetipos...")
    generados = []
    for prefijo, arq, t_sec, dur, cfg in ARQUETIPOS_V06:
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
