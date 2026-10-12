"""
src.mockups.planos.wrappers
---------------------------------------------------------------------------
CONFIGS por video y wrappers generar_video_interactivo_* (videos 06-13).
"""

from typing import Dict, Any, Optional, Tuple, List, Union
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

from src.mockups.planos.router import generar_video_cinematico_escena
from src.rutas import DIR_BYTE_TRANSPARENTES, DIR_BYTE_ILUSTRACIONES


# ---------------------------------------------------------------------------
# Mapeo y Wrapper para Video 06: Atención al Cliente con IA
# ---------------------------------------------------------------------------
CONFIGS_ATENCION_CLIENTES = {
    "escena_problema": ("PLANO_HERO_CAOS", {
        "badge": "MENSAJES REPETITIVOS A MANO",
        "elementos": [
            {"x": 60, "y": 240, "w": 330, "h": 160, "rot": -10, "tit": "¿Cuánto sale el envío?", "sub": "Pregunta #1 • Sin responder", "col": (225, 29, 72)},
            {"x": 660, "y": 230, "w": 330, "h": 170, "rot": 12, "tit": "¿Tienen stock disponible?", "sub": "Pregunta #2 • Esperando 2h", "col": (225, 29, 72)},
            {"x": 40, "y": 870, "w": 320, "h": 150, "rot": 8, "tit": "¿Cuáles son los horarios?", "sub": "Pregunta #3 • Clientes impacientes", "col": (245, 158, 11)},
            {"x": 690, "y": 910, "w": 330, "h": 160, "rot": -8, "tit": "¿Cómo hago para pagar?", "sub": "Pregunta #4 • Misma duda diaria", "col": (225, 29, 72)},
        ]
    }),
    "punto_1": ("PLANO_SHOWCASE_PANORAMICO", {
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
    "punto_2": ("PLANO_SPLIT_BEFORE_AFTER", {
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
    "resultado": ("PLANO_DECK_3D", {
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
    "cierre": ("PLANO_HOST_COMMUNITY", {
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
}

def generar_video_interactivo_atencion_clientes(
    tipo_escena: str,
    duracion_segundos: float,
    ruta_salida: Union[str, Path],
    fps: int = 30,
    ancho: int = 1080,
    alto: int = 1920
) -> Path:
    """Wrapper para generar videos de fondo interactivos de Video 06 (Atención al cliente con IA)."""
    mapa = {
        "escena_problema": "escena_problema",
        "hook": "escena_problema",
        "problema": "escena_problema",
        "punto_1": "punto_1",
        "demostracion_1": "punto_1",
        "fin": "punto_1",
        "intercom": "punto_1",
        "punto_2": "punto_2",
        "demostracion_2": "punto_2",
        "lyro": "punto_2",
        "tidio": "punto_2",
        "resultado": "resultado",
        "cierre": "cierre",
    }
    clave = mapa.get(tipo_escena, "escena_problema")
    arquetipo, cfg = CONFIGS_ATENCION_CLIENTES.get(clave, ("PLANO_HERO_CAOS", {}))
    return generar_video_cinematico_escena(
        arquetipo=arquetipo,
        duracion_segundos=duracion_segundos,
        ruta_salida=ruta_salida,
        config=cfg,
        fps=fps,
        ancho=ancho,
        alto=alto
    )


# ---------------------------------------------------------------------------
# Mapeo y Wrapper para Video 07: Salir del Excel (Julius AI + Gamma)
# ---------------------------------------------------------------------------
CONFIGS_EXCEL_REPORTES = {
    "cold_open": ("PLANO_PANICO_RELOJ", {
        "estilo_fondo": "ciudad_cyberpunk",
        "badge": "VIERNES • 17:59 HS",
        "hora": "17:59",
        "sub_reloj": "TIEMPO LÍMITE: 1 MINUTO PARA EL CIERRE",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "byte_cortocircuito_transparente.png",
        "elementos": [
            {"x": 40, "y": 410, "w": 340, "h": 140, "rot": -10, "tit": "POV: Viernes 17:59", "sub": "El jefe pide el reporte", "col": (225, 29, 72)},
            {"x": 690, "y": 400, "w": 340, "h": 140, "rot": 12, "tit": "¡SIN REPORTE!", "sub": "Y con ganas de irte a casa", "col": (239, 68, 68)},
        ]
    }),
    "hook": ("PLANO_HERO_CAOS", {
        "estilo_fondo": "ciudad_cyberpunk",
        "badge": "ESTO TE SACA DEL EXCEL",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "hook_guion_07_transparente.png",
        "elementos": [
            {"x": 60, "y": 240, "w": 340, "h": 150, "rot": -9, "tit": "Error #¡REF!", "sub": "Fórmula rota en fila 420", "col": (225, 29, 72)},
            {"x": 660, "y": 230, "w": 340, "h": 150, "rot": 11, "tit": "4.280 filas", "sub": "Sin ordenar ni limpiar", "col": (225, 29, 72)},
            {"x": 50, "y": 1200, "w": 340, "h": 150, "rot": 7, "tit": "#¡VALOR!", "sub": "Faltan datos de ventas", "col": (245, 158, 11)},
            {"x": 670, "y": 1220, "w": 340, "h": 150, "rot": -7, "tit": "Cálculo infinito...", "sub": "Ventilador al máximo", "col": (225, 29, 72)},
        ]
    }),
    "problema": ("PLANO_HERO_CAOS", {
        "estilo_fondo": "ciudad_cyberpunk",
        "badge": "EL INFORME TE COME LA TARDE",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "problema_guion_07_transparente.png",
        "elementos": [
            {"x": 60, "y": 250, "w": 330, "h": 150, "rot": -8, "tit": "Copiar y pegar", "sub": "Celdas que no coinciden", "col": (225, 29, 72)},
            {"x": 670, "y": 240, "w": 330, "h": 150, "rot": 10, "tit": "Acomodar gráficos", "sub": "Tablas desalineadas", "col": (225, 29, 72)},
            {"x": 50, "y": 1200, "w": 340, "h": 150, "rot": 7, "tit": "Horas perdidas", "sub": "Un viernes a la tarde", "col": (245, 158, 11)},
            {"x": 680, "y": 1220, "w": 340, "h": 150, "rot": -8, "tit": "Borrador sin fin", "sub": "Todo por hacer a mano", "col": (225, 29, 72)},
        ]
    }),
    "punto_1": ("PLANO_JULIUS_DASHBOARD", {
        "estilo_fondo": "ciudad_cyberpunk",
        "header": "JULIUS AI • Analista de Datos Inteligente",
        "badge": "Gráficos en 1 Frase",
        "titulo": "Analizá las ventas de la semana y armá gráficos",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "punto_1_guion_07_transparente.png"
    }),
    "punto_2": ("PLANO_GAMMA_SLIDES", {
        "estilo_fondo": "ciudad_cyberpunk",
        "header": "GAMMA • Diapositivas Generadas con IA",
        "badge": "De Idea a Slides",
        "titulo": "Presentación Prolija en Minutos",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "punto_2_guion_07_transparente.png"
    }),
    "resultado": ("PLANO_LAPTOP_CERRADA", {
        "estilo_fondo": "ciudad_cyberpunk",
        "badge": "VIERNES 18:00 • INFORME ENVIADO",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "resultado_guion_07_transparente.png"
    }),
    "cierre": ("PLANO_HOST_COMMUNITY", {
        "estilo_fondo": "ciudad_cyberpunk",
        "pregunta_tit": "PREGUNTA A LA COMUNIDAD:",
        "pregunta_l1": "¿Vos cómo armás tus reportes",
        "pregunta_l2": "hoy en el trabajo?",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "cierre_guion_07_transparente.png",
        "opciones": [
            ("A", "Excel a mano y sufriendo hasta tarde", (225, 29, 72), (255, 241, 242)),
            ("B", "Copio y pego fórmulas rezando que anden", (124, 58, 237), (245, 243, 255)),
            ("C", "Ya uso IA y salgo a las 18:00 en punto", (16, 185, 129), (236, 253, 245)),
        ],
        "callout": "Contame abajo"
    }),
}

def generar_video_interactivo_excel_reportes(
    tipo_escena: str,
    duracion_segundos: float,
    ruta_salida: Union[str, Path],
    fps: int = 30,
    ancho: int = 1080,
    alto: int = 1920
) -> Path:
    """Wrapper para generar videos de fondo interactivos de Video 07 (Salir del Excel con Julius y Gamma)."""
    mapa = {
        "cold_open": "cold_open",
        "panico": "cold_open",
        "reloj": "cold_open",
        "hook": "hook",
        "problema": "problema",
        "escena_problema": "problema",
        "punto_1": "punto_1",
        "demostracion_1": "punto_1",
        "julius": "punto_1",
        "punto_2": "punto_2",
        "demostracion_2": "punto_2",
        "gamma": "punto_2",
        "resultado": "resultado",
        "cierre": "cierre",
    }
    clave = mapa.get(tipo_escena, "cold_open")
    arquetipo, cfg = CONFIGS_EXCEL_REPORTES.get(clave, ("PLANO_HERO_CAOS", {}))
    return generar_video_cinematico_escena(
        arquetipo=arquetipo,
        duracion_segundos=duracion_segundos,
        ruta_salida=ruta_salida,
        config=cfg,
        fps=fps,
        ancho=ancho,
        alto=alto
    )


# ---------------------------------------------------------------------------
# Configuración de Escenas para Video 08 (Búsqueda e Investigación: Perplexity y NotebookLM)
# ---------------------------------------------------------------------------
CONFIGS_BUSQUEDA_INVESTIGACION = {
    "cold_open": ("PLANO_BROWSER_TABS_CAOS", {
        "estilo_fondo": "viaje_espacial",
        "badge": "POV: 10 PESTAÑAS ABIERTAS",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "cold_open_guion_08_busqueda_investigacion_transparente.png",
    }),
    "hook": ("PLANO_BROWSER_TABS_CAOS", {
        "estilo_fondo": "viaje_espacial",
        "badge": "DEJÁ DE BUSCAR A CIEGAS",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "hook_guion_08_busqueda_investigacion_transparente.png",
    }),
    "problema": ("PLANO_BROWSER_TABS_CAOS", {
        "estilo_fondo": "viaje_espacial",
        "badge": "NINGUNA DA LA RESPUESTA",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "problema_guion_08_busqueda_investigacion_transparente.png",
    }),
    "punto_1": ("PLANO_PERPLEXITY_SEARCH", {
        "estilo_fondo": "viaje_espacial",
        "header": "PERPLEXITY AI • Motor de Respuestas en Tiempo Real",
        "badge": "⚡ En Vivo",
        "titulo": "Buscá datos verificados de mercado y citá fuentes",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "punto_1_guion_08_busqueda_investigacion_transparente.png"
    }),
    "punto_2": ("PLANO_NOTEBOOKLM_DOCS", {
        "estilo_fondo": "viaje_espacial",
        "header": "GOOGLE NOTEBOOKLM • Asistente de tus Propios Archivos",
        "badge": "✓ Tus Datos",
        "titulo": "Resumí las obligaciones del contrato y los plazos",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "punto_2_guion_08_busqueda_investigacion_transparente.png"
    }),
    "resultado": ("PLANO_SINGLE_TAB_ZEN", {
        "estilo_fondo": "viaje_espacial",
        "badge": "RESPUESTA CORRECTA AL TOQUE",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "resultado_guion_08_busqueda_investigacion_transparente.png"
    }),
    "cierre": ("PLANO_BATTLE_VS", {
        "estilo_fondo": "viaje_espacial",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "cierre_guion_08_busqueda_investigacion_transparente.png",
    }),
}

def generar_video_interactivo_busqueda_investigacion(
    tipo_escena: str,
    duracion_segundos: float,
    ruta_salida: Union[str, Path],
    fps: int = 30,
    ancho: int = 1080,
    alto: int = 1920
) -> Path:
    """Wrapper para generar videos de fondo interactivos de Video 08 (Búsqueda e Investigación con Perplexity y NotebookLM)."""
    mapa = {
        "cold_open": "cold_open",
        "panico": "cold_open",
        "hook": "hook",
        "problema": "problema",
        "escena_problema": "problema",
        "punto_1": "punto_1",
        "demostracion_1": "punto_1",
        "perplexity": "punto_1",
        "punto_2": "punto_2",
        "demostracion_2": "punto_2",
        "notebooklm": "punto_2",
        "resultado": "resultado",
        "cierre": "cierre",
    }
    clave = mapa.get(tipo_escena, "cold_open")
    arquetipo, cfg = CONFIGS_BUSQUEDA_INVESTIGACION.get(clave, ("PLANO_HERO_CAOS", {}))
    return generar_video_cinematico_escena(
        arquetipo=arquetipo,
        duracion_segundos=duracion_segundos,
        ruta_salida=ruta_salida,
        config=cfg,
        fps=fps,
        ancho=ancho,
        alto=alto
    )


# ---------------------------------------------------------------------------
# Configuración de Escenas para Video 09 (Diseño de Flyers: Canva y Remove.bg)
# ---------------------------------------------------------------------------
CONFIGS_DISENO_FLYERS = {
    "cold_open": ("PLANO_CHAT_FLYER_URGENTE", {
        "estilo_fondo": "estudio_creativo",
        "badge": "POV: NECESITÁS UN FLYER URGENTE",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "byte_agotado_transparente.png",
    }),
    "hook": ("PLANO_PHOTOSHOP_FREEZE", {
        "estilo_fondo": "estudio_creativo",
        "badge": "DEJÁ DE PELEAR CON EL DISEÑO",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "punto_2_guion_04_transparente.png",
    }),
    "problema": ("PLANO_LIENZO_BLANCO_BLOQUEO", {
        "estilo_fondo": "estudio_creativo",
        "badge": "ABRÍS Y NO SABÉS QUÉ HACER",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "byte_cortocircuito_transparente.png",
    }),
    "punto_1": ("PLANO_CANVA_MAGIC_DESIGN", {
        "estilo_fondo": "estudio_creativo",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "punto_1_guion_04_transparente.png",
    }),
    "punto_2": ("PLANO_REMOVE_BG_LASER", {
        "estilo_fondo": "estudio_creativo",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "cierre_transparente.png",
    }),
    "resultado": ("PLANO_SMARTPHONE_INSTAGRAM_FEED", {
        "estilo_fondo": "estudio_creativo",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "cierre_guion_04_transparente.png",
    }),
    "cierre": ("PLANO_BATTLE_VS", {
        "estilo_fondo": "estudio_creativo",
        "header_debate": "DEBATE A LA COMUNIDAD:",
        "pregunta_debate": "¿Sos Team Canva o Team Photoshop?",
        "titulo_izq": "TEAM PHOTOSHOP",
        "titulo_der": "TEAM CANVA + IA",
        "items_izq": [
            "• Recortando a pluma",
            "• 50 capas sin nombrar",
            "• Programa pesado y caro",
            "• Tarde entera perdida"
        ],
        "items_der": [
            "• Magic Design en 1 clic",
            "• Remove.bg automático",
            "• Layouts pro al instante",
            "• Publicado en 3 minutos"
        ],
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "cierre_guion_08_busqueda_investigacion_transparente.png",
    }),
}

def generar_video_interactivo_diseno_flyers(
    tipo_escena: str,
    duracion_segundos: float,
    ruta_salida: Union[str, Path],
    fps: int = 30,
    ancho: int = 1080,
    alto: int = 1920
) -> Path:
    """Wrapper para generar videos de fondo interactivos de Video 09 (Diseño de Flyers: Canva y Remove.bg)."""
    mapa = {
        "cold_open": "cold_open",
        "hook": "hook",
        "problema": "problema",
        "escena_problema": "problema",
        "punto_1": "punto_1",
        "demostracion_1": "punto_1",
        "canva": "punto_1",
        "punto_2": "punto_2",
        "demostracion_2": "punto_2",
        "remove_bg": "punto_2",
        "removebg": "punto_2",
        "resultado": "resultado",
        "cierre": "cierre",
    }
    clave = mapa.get(tipo_escena, "cold_open")
    arquetipo, cfg = CONFIGS_DISENO_FLYERS.get(clave, ("PLANO_FLYER_PAINT_CAOS", {}))
    return generar_video_cinematico_escena(
        arquetipo=arquetipo,
        duracion_segundos=duracion_segundos,
        ruta_salida=ruta_salida,
        config=cfg,
        fps=fps,
        ancho=ancho,
        alto=alto
    )


# ---------------------------------------------------------------------------
# Configuración de Escenas para Video 10 (Cotización Automática de Pedidos)
# ---------------------------------------------------------------------------
CONFIGS_COTIZACION_AUTOMATICA = {
    "cold_open": ("PLANO_WHATSAPP_PEDIDO_REMERAS", {
        "estilo_fondo": "estudio_creativo",
        "badge": "PEDIDO ENTRANTE DE UN CLIENTE",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "cierre_transparente.png",
    }),
    "hook": ("PLANO_WHATSAPP_PEDIDO_REMERAS", {
        "estilo_fondo": "estudio_creativo",
        "badge": "NO PIENSO CALCULAR ESTO A MANO",
        "alerta_calculo": True,
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "punto_2_guion_04_transparente.png",
    }),
    "problema": ("PLANO_BYTE_PASE_IA", {
        "estilo_fondo": "estudio_creativo",
        "badge": "LE PASO EL TEXTO DIRECTO A LA IA",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "byte_computadora_feliz_transparente.png",
    }),
    "punto_1": ("PLANO_TABLA_PRESUPUESTO_EXTRACCION", {
        "estilo_fondo": "estudio_creativo",
        "badge": "EXTRAE CANTIDADES Y DETALLES EN SEGUNDOS",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "punto_1_guion_04_transparente.png",
    }),
    "punto_2": ("PLANO_TABLA_COTIZAR_ORDENADA", {
        "estilo_fondo": "estudio_creativo",
        "badge": "TODO ORDENADO Y LISTO PARA COTIZAR",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "punto_2_guion_08_busqueda_investigacion_transparente.png",
    }),
    "resultado": ("PLANO_COTIZACION_FORMAL_PDF", {
        "estilo_fondo": "estudio_creativo",
        "badge": "REVISO LOS PRECIOS Y SE LA MANDO AL CLIENTE",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "cierre_guion_04_transparente.png",
    }),
    "cierre": ("PLANO_CIERRE_PREGUNTA_AUTOMATIZAR", {
        "estilo_fondo": "estudio_creativo",
        "badge": "¿QUÉ TAREA AUTOMATIZARÍAS PRIMERO?",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "cierre_saltando_transparente.png",
    }),
}


def generar_video_interactivo_cotizacion_automatica(
    tipo_escena: str,
    duracion_segundos: float,
    ruta_salida: Union[str, Path],
    fps: int = 30,
    ancho: int = 1080,
    alto: int = 1920
) -> Path:
    """Wrapper para generar videos de fondo interactivos de Video 10 (Cotización Automática de Pedidos)."""
    mapa = {
        "cold_open": "cold_open",
        "hook": "hook",
        "problema": "problema",
        "escena_problema": "problema",
        "punto_1": "punto_1",
        "demostracion_1": "punto_1",
        "extraccion": "punto_1",
        "punto_2": "punto_2",
        "demostracion_2": "punto_2",
        "presupuesto": "punto_2",
        "resultado": "resultado",
        "cierre": "cierre",
    }
    clave = mapa.get(tipo_escena, "cold_open")
    arquetipo, cfg = CONFIGS_COTIZACION_AUTOMATICA.get(clave, ("PLANO_WHATSAPP_PEDIDO_REMERAS", {}))
    return generar_video_cinematico_escena(
        arquetipo=arquetipo,
        duracion_segundos=duracion_segundos,
        ruta_salida=ruta_salida,
        config=cfg,
        fps=fps,
        ancho=ancho,
        alto=alto
    )


# ---------------------------------------------------------------------------
# Configuración de Escenas para Video 11 (50 Archivos - Análisis Documental IA)
# ---------------------------------------------------------------------------
CONFIGS_CINCUENTA_ARCHIVOS = {
    "cold_open": ("PLANO_CINCUENTA_ARCHIVOS_CAOS", {
        "estilo_fondo": "estudio_tech",
        "badge": "CARPETA: FACTURAS_PROVEEDORES/ (50 PDFs)",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "escena_problema_guion_03_transparente.png",
    }),
    "hook": ("PLANO_BYTE_RECHAZO_MANUAL", {
        "estilo_fondo": "estudio_tech",
        "badge": "NO PIENSO ABRIR UNA POR UNA",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "punto_2_guion_10_cotizacion_automatica_transparente.png",
    }),
    "problema": ("PLANO_BYTE_RECHAZO_MANUAL", {
        "estilo_fondo": "estudio_tech",
        "badge": "SI REVISO 1 POR 1 SE ME VA TODA LA TARDE",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "byte_cortocircuito_transparente.png",
    }),
    "punto_1": ("PLANO_DRAG_DROP_IA_ANALISIS", {
        "estilo_fondo": "estudio_tech",
        "badge": "CARGA MASIVA Y ANÁLISIS EN SEGUNDOS",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "byte_computadora_feliz_transparente.png",
    }),
    "punto_2": ("PLANO_RAG_RESULTADO_CITAS", {
        "estilo_fondo": "estudio_tech",
        "badge": "TOTAL EXTRAÍDO + DOCUMENTOS DE ORIGEN",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "resultado_guion_08_busqueda_investigacion_transparente.png",
    }),
    "resultado": ("PLANO_HUMOR_SUFRIR_GRATIS", {
        "estilo_fondo": "estudio_tech",
        "badge": "QUÉ MANERA DE COMPLICARME SOLO",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "cierre_guion_07_transparente.png",
    }),
    "cierre": ("PLANO_CIERRE_ARCHIVOS_ACUMULADOS", {
        "estilo_fondo": "estudio_tech",
        "badge": "¿CUÁNTOS ARCHIVOS TENÉS ACUMULADOS?",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "cierre_saltando_transparente.png",
    }),
}


def generar_video_interactivo_cincuenta_archivos(
    tipo_escena: str,
    duracion_segundos: float,
    ruta_salida: Union[str, Path],
    fps: int = 30,
    ancho: int = 1080,
    alto: int = 1920
) -> Path:
    """Wrapper para generar videos de fondo interactivos de Video 11 (50 Archivos - Análisis Documental IA)."""
    mapa = {
        "cold_open": "cold_open",
        "hook": "hook",
        "problema": "problema",
        "escena_problema": "problema",
        "punto_1": "punto_1",
        "demostracion_1": "punto_1",
        "extraccion": "punto_1",
        "punto_2": "punto_2",
        "demostracion_2": "punto_2",
        "citas": "punto_2",
        "resultado": "resultado",
        "cierre": "cierre",
    }
    clave = mapa.get(tipo_escena, "cold_open")
    arquetipo, cfg = CONFIGS_CINCUENTA_ARCHIVOS.get(clave, ("PLANO_CINCUENTA_ARCHIVOS_CAOS", {}))
    return generar_video_cinematico_escena(
        arquetipo=arquetipo,
        duracion_segundos=duracion_segundos,
        ruta_salida=ruta_salida,
        config=cfg,
        fps=fps,
        ancho=ancho,
        alto=alto
    )

# ---------------------------------------------------------------------------
# Configuración de Escenas para Video 12 (Ciberseguridad y Google Ads Maliciosos)
# ---------------------------------------------------------------------------
CONFIGS_CIBERSEGURIDAD_GOOGLE_ADS = {
    "cold_open": ("PLANO_GOOGLE_ADS_BUSQUEDA_TRAMPA", {
        "estilo_fondo": "ciudad_cyberpunk",
        "badge": "GOOGLE SEARCH • BANCO RÍO",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "punto_1_guion_08_busqueda_investigacion_transparente.png",
    }),
    "hook": ("PLANO_ALERTA_SITIO_CLONADO", {
        "estilo_fondo": "ciudad_cyberpunk",
        "badge": "ALERTA: SITIO CLONADO (PHISHING)",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "hook_estresado_transparente.png",
    }),
    "problema": ("PLANO_MECANICA_ANUNCIO_PAGADO", {
        "estilo_fondo": "ciudad_cyberpunk",
        "badge": "LOS ESTAFADORES PAGAN ANUNCIOS",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "byte_cortocircuito_transparente.png",
    }),
    "punto_1": ("PLANO_INSPECCION_URL_LUPA", {
        "estilo_fondo": "ciudad_cyberpunk",
        "badge": "SI DICE PATROCINADO, MIRÁ LA URL",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "punto_1_guion_08_busqueda_investigacion_transparente.png",
    }),
    "punto_2": ("PLANO_SPLIT_ANUNCIO_VS_ORGANICO", {
        "estilo_fondo": "ciudad_cyberpunk",
        "badge": "RESULTADO ORGÁNICO OFICIAL",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "punto_2_guion_08_busqueda_investigacion_transparente.png",
    }),
    "resultado": ("PLANO_ESCUDO_CIBERSEGURIDAD", {
        "estilo_fondo": "ciudad_cyberpunk",
        "badge": "ESCUDO DE NAVEGACIÓN ACTIVO",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "resultado_guion_10_cotizacion_automatica_transparente.png",
    }),
    "cierre": ("PLANO_CIERRE_DEBATE_ESTAFAS", {
        "estilo_fondo": "ciudad_cyberpunk",
        "badge": "¿CASI CAÉS EN UN LINK TRAMPA?",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "cierre_saltando_transparente.png",
    }),
}


def generar_video_interactivo_ciberseguridad_google_ads(
    tipo_escena: str,
    duracion_segundos: float,
    ruta_salida: Union[str, Path],
    fps: int = 30,
    ancho: int = 1080,
    alto: int = 1920
) -> Path:
    """Wrapper para generar videos de fondo interactivos de Video 12 (Ciberseguridad y Google Ads Maliciosos)."""
    mapa = {
        "cold_open": "cold_open",
        "hook": "hook",
        "problema": "problema",
        "escena_problema": "problema",
        "punto_1": "punto_1",
        "demostracion_1": "punto_1",
        "inspeccion": "punto_1",
        "punto_2": "punto_2",
        "demostracion_2": "punto_2",
        "organico": "punto_2",
        "resultado": "resultado",
        "cierre": "cierre",
    }
    clave = mapa.get(tipo_escena, "cold_open")
    arquetipo, cfg = CONFIGS_CIBERSEGURIDAD_GOOGLE_ADS.get(clave, ("PLANO_GOOGLE_ADS_BUSQUEDA_TRAMPA", {}))
    return generar_video_cinematico_escena(
        arquetipo=arquetipo,
        duracion_segundos=duracion_segundos,
        ruta_salida=ruta_salida,
        config=cfg,
        fps=fps,
        ancho=ancho,
        alto=alto
    )

# ---------------------------------------------------------------------------
# Configuración de Escenas para Video 13 (Portal de Noticias de IA - Qué Hace Realmente la IA)
# ---------------------------------------------------------------------------
CONFIGS_NOTICIAS_IA_REALIDAD = {
    "cold_open": ("PLANO_NOTICIAS_MITO_CHAT", {
        "estilo_fondo": "estudio_tech",
        "badge": "BYTE TECH NEWS • FLASH ESPECIAL",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "cierre_transparente.png",
    }),
    "hook": ("PLANO_NOTICIAS_BREAKING_IMPACTO", {
        "estilo_fondo": "estudio_tech",
        "badge": "BREAKING NEWS • IMPACTO REAL",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "punto1_feliz_transparente.png",
    }),
    "problema": ("PLANO_NOTICIAS_TRANSFORMACION_SILENCIOSA", {
        "estilo_fondo": "estudio_tech",
        "badge": "TRANSFORMACIÓN EN SILENCIO",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "punto_1_guion_08_busqueda_investigacion_transparente.png",
    }),
    "punto_1": ("PLANO_NOTICIAS_MEDICINA_DIAGNOSTICO", {
        "estilo_fondo": "estudio_tech",
        "badge": "NOTICIA 01 • MEDICINA",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "punto_2_guion_08_busqueda_investigacion_transparente.png",
    }),
    "punto_2": ("PLANO_NOTICIAS_CIENCIA_CLIMA_MATERIALES", {
        "estilo_fondo": "estudio_tech",
        "badge": "NOTICIA 02 • CIENCIA Y MATERIALES",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "punto_2_guion_08_busqueda_investigacion_transparente.png",
    }),
    "resultado": ("PLANO_NOTICIAS_ACELERACION_EDITORIAL", {
        "estilo_fondo": "estudio_tech",
        "badge": "EDITORIAL FINAL • BYTE TECH NEWS",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "resultado_guion_10_cotizacion_automatica_transparente.png",
    }),
    "cierre": ("PLANO_NOTICIAS_CIERRE_ENCUESTA_FUTURO", {
        "estilo_fondo": "estudio_tech",
        "badge": "¿EN QUÉ ÁREA IMPACTARÁ MÁS?",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "cierre_saltando_transparente.png",
    }),
}


def generar_video_interactivo_noticias_ia_realidad(
    tipo_escena: str,
    duracion_segundos: float,
    ruta_salida: Union[str, Path],
    fps: int = 30,
    ancho: int = 1080,
    alto: int = 1920
) -> Path:
    """Wrapper para generar videos de fondo interactivos de Video 13 (Portal de Noticias de IA)."""
    mapa = {
        "cold_open": "cold_open",
        "hook": "hook",
        "problema": "problema",
        "escena_problema": "problema",
        "punto_1": "punto_1",
        "demostracion_1": "punto_1",
        "medicina": "punto_1",
        "punto_2": "punto_2",
        "demostracion_2": "punto_2",
        "ciencia": "punto_2",
        "resultado": "resultado",
        "cierre": "cierre",
    }
    clave = mapa.get(tipo_escena, "cold_open")
    arquetipo, cfg = CONFIGS_NOTICIAS_IA_REALIDAD.get(clave, ("PLANO_NOTICIAS_MITO_CHAT", {}))
    return generar_video_cinematico_escena(
        arquetipo=arquetipo,
        duracion_segundos=duracion_segundos,
        ruta_salida=ruta_salida,
        config=cfg,
        fps=fps,
        ancho=ancho,
        alto=alto
    )


# ---------------------------------------------------------------------------
# Configuración de Escenas para Video 14 (Agua e IA: Desmintiendo el Pánico)
# ---------------------------------------------------------------------------
CONFIGS_AGUA_IA = {
    "cold_open": ("PLANO_HERO_CAOS", {
        "estilo_fondo": "ciudad_cyberpunk",
        "badge": "EL MITO QUE CORRE EN TODOS LADOS",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "hook_estresado_transparente.png",
        "elementos": [
            {"x": 100, "y": 330, "w": 340, "h": 150, "rot": -9, "tit": "Botella por pregunta", "sub": "Titular viral de hoy", "col": (225, 29, 72)},
            {"x": 640, "y": 330, "w": 340, "h": 150, "rot": 11, "tit": "¿La IA seca ríos?", "sub": "Videos con pánico", "col": (225, 29, 72)},
            {"x": 100, "y": 600, "w": 340, "h": 150, "rot": 7, "tit": "700 mil litros", "sub": "Dato sin contexto", "col": (245, 158, 11)},
            {"x": 640, "y": 600, "w": 340, "h": 150, "rot": -7, "tit": "¡No preguntes!", "sub": "Comentarios asustados", "col": (225, 29, 72)},
        ]
    }),
    "hook": ("PLANO_HERO_CAOS", {
        "estilo_fondo": "ciudad_cyberpunk",
        "badge": "¿UNA BOTELLA DE AGUA POR PREGUNTA?",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "byte_cortocircuito_transparente.png",
        "elementos": [
            {"x": 100, "y": 330, "w": 340, "h": 150, "rot": -8, "tit": "¿Es verdad?", "sub": "La pregunta de todos", "col": (245, 158, 11)},
            {"x": 640, "y": 330, "w": 340, "h": 150, "rot": 10, "tit": "Todos lo comparten", "sub": "Sin mirar la fuente", "col": (225, 29, 72)},
            {"x": 100, "y": 600, "w": 340, "h": 150, "rot": 7, "tit": "500 ml", "sub": "Cada 10 respuestas", "col": (225, 29, 72)},
            {"x": 640, "y": 600, "w": 340, "h": 150, "rot": -7, "tit": "Vamos a los datos", "sub": "Sin pánico y sin negar", "col": (14, 165, 233)},
        ]
    }),
    "problema": ("PLANO_HERO_CAOS", {
        "estilo_fondo": "ciudad_cyberpunk",
        "badge": "EL DATO QUE NADIE CONTEXTO",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "punto_1_guion_13_noticias_ia_realidad_transparente.png",
        "elementos": [
            {"x": 100, "y": 330, "w": 340, "h": 150, "rot": -9, "tit": "Estudio de 2023", "sub": "Making AI Less Thirsty", "col": (245, 158, 11)},
            {"x": 640, "y": 330, "w": 340, "h": 150, "rot": 11, "tit": "Modelo GPT-3", "sub": "De 2020, ya superado", "col": (245, 158, 11)},
            {"x": 100, "y": 600, "w": 340, "h": 150, "rot": 7, "tit": "700 mil litros", "sub": "Solo del entrenamiento", "col": (225, 29, 72)},
            {"x": 640, "y": 600, "w": 340, "h": 150, "rot": -7, "tit": "Centros en EE UU", "sub": "Depende del clima local", "col": (14, 165, 233)},
        ]
    }),
    "punto_1": ("PLANO_SPLIT_BEFORE_AFTER", {
        "estilo_fondo": "ciudad_cyberpunk",
        "antes_tag": "EL PÁNICO",
        "antes_tit": "Lo que dice el viral",
        "antes_items": [
            "• Una botella de 500 ml cada 10 respuestas",
            "• Dato de 2023 sobre el modelo GPT-3",
            "• Estimado en centros de datos de EE UU"
        ],
        "separador": "LO MEDIDO EN 2025",
        "despues_tag": "LA MEDICIÓN",
        "despues_tit": "Gemini de Google, texto típico",
        "pills_despues": [
            ("0,26 mL", "Cinco gotas de agua", (14, 165, 233), (240, 249, 255)),
            ("0,24 Wh", "Menos que 9 s de tele", (16, 185, 129), (236, 253, 245)),
            ("33× menos", "Energía en 12 meses", (16, 185, 129), (236, 253, 245))
        ],
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "punto1_feliz_transparente.png",
    }),
    "punto_2": ("PLANO_SHOWCASE_PANORAMICO", {
        "estilo_fondo": "ciudad_cyberpunk",
        "header": "EL MATIZ • NI PÁNICO NI NEGACIÓN",
        "badge": "Cifras oficiales",
        "titulo": "Lo que sí es real",
        "subtitulo": "El costo existe, pero se mide, se publica y se baja",
        "items": [
            ("Entrenamiento", "GPT-3 evaporó 700 mil litros", (225, 29, 72), (255, 241, 242)),
            ("Imágenes y video", "Pesan mucho más que el texto", (245, 158, 11), (255, 251, 235)),
            ("Agua local", "46% de Microsoft en zonas con estrés", (37, 99, 235), (239, 246, 255))
        ],
        "footer": "Fuente: Google 2025 y reportes de Microsoft",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "punto_2_guion_13_noticias_ia_realidad_transparente.png",
    }),
    "resultado": ("PLANO_DECK_3D", {
        "estilo_fondo": "ciudad_cyberpunk",
        "titulo": "La industria ya responde",
        "subtitulo": "Diseños que ahorran millones de litros por planta",
        "cards": [
            {"x_off": -180, "y": 500, "tit": "Microsoft", "desc": "Cero agua de enfriamiento", "rot": -7, "col": (37, 99, 235)},
            {"x_off": 180, "y": 500, "tit": "Circuito cerrado", "desc": "Enfriamiento a nivel de chip", "rot": 7, "col": (124, 58, 237)},
            {"x_off": 0, "y": 480, "tit": "125 millones", "desc": "de litros ahorrados al año", "rot": 0, "col": (16, 185, 129)}
        ],
        "pills": [
            ("Diseño nuevo", (16, 185, 129)),
            ("Menos litros", (14, 165, 233)),
            ("Datos abiertos", (124, 58, 237))
        ],
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "byte_computadora_feliz_transparente.png",
    }),
    "cierre": ("PLANO_BATTLE_VS", {
        "estilo_fondo": "ciudad_cyberpunk",
        "atenuacion_oscura": 0.45,
        "header_debate": "DEBATE: EL PÁNICO VS LOS DATOS",
        "pregunta_debate": "¿Te lo creíste o ya sabías que era mentira?",
        "titulo_izq": "EL PÁNICO VIRAL",
        "items_izq": [
            "• 500 ml cada 10 preguntas",
            "• Dato de 2023 sin contexto",
            "• Se comparte sin mirar",
            "• Música de miedo incluida",
        ],
        "titulo_der": "LOS DATOS REALES",
        "items_der": [
            "• 0,26 mL = 5 gotas",
            "• 0,24 Wh por consulta",
            "• Medido en 2025",
            "• Google y Microsoft lo publican",
        ],
        "callout": "Contame: ¿te lo creíste?",
        "sprite_byte": DIR_BYTE_TRANSPARENTES / "cierre_guion_13_noticias_ia_realidad_transparente.png",
    }),
}


def generar_video_interactivo_agua_ia(
    tipo_escena: str,
    duracion_segundos: float,
    ruta_salida: Union[str, Path],
    fps: int = 30,
    ancho: int = 1080,
    alto: int = 1920
) -> Path:
    """Wrapper para generar videos de fondo interactivos de Video 14 (Agua e IA: desmintiendo el pánico)."""
    mapa = {
        "cold_open": "cold_open",
        "hook": "hook",
        "problema": "problema",
        "escena_problema": "problema",
        "punto_1": "punto_1",
        "demostracion_1": "punto_1",
        "gemini": "punto_1",
        "punto_2": "punto_2",
        "demostracion_2": "punto_2",
        "gpt3": "punto_2",
        "resultado": "resultado",
        "cierre": "cierre",
    }
    clave = mapa.get(tipo_escena, "cold_open")
    arquetipo, cfg = CONFIGS_AGUA_IA.get(clave, ("PLANO_HERO_CAOS", {}))
    return generar_video_cinematico_escena(
        arquetipo=arquetipo,
        duracion_segundos=duracion_segundos,
        ruta_salida=ruta_salida,
        config=cfg,
        fps=fps,
        ancho=ancho,
        alto=alto
    )
