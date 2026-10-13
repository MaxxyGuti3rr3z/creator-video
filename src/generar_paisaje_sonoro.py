"""
Módulo para la síntesis procedural de efectos de sonido (SFX) y música ambiental tech (BGM)
para la Fase 3 del generador de Shorts.

Genera archivos WAV limpios, sin compresión previa y 100% libres de derechos
para ser mezclados por FFmpeg con precisión de milisegundos.
"""

from pathlib import Path
from typing import Union, Optional, List, Dict, Any, Tuple
import numpy as np
import scipy.io.wavfile as wavfile


def generar_sfx_whoosh(ruta_wav: Path, sample_rate: int = 44100):
    """Whoosh suave y cinematográfico para transiciones entre escenas (~0.35s)."""
    dur = 0.35
    t = np.linspace(0, dur, int(sample_rate * dur), endpoint=False)
    # Ruido blanco filtrado con barrido de frecuencia
    noise = np.random.uniform(-1, 1, len(t))
    # Curva de envolvente senoidal suave
    env = np.sin(np.pi * (t / dur)) ** 2
    # Modulación de frecuencia (sweep)
    freq = np.linspace(150, 900, len(t))
    phase = 2 * np.pi * np.cumsum(freq) / sample_rate
    carrier = np.sin(phase)
    signal = (0.6 * carrier + 0.4 * noise) * env
    signal = signal / np.max(np.abs(signal) + 1e-6) * 0.75
    wavfile.write(str(ruta_wav), sample_rate, (signal * 32767).astype(np.int16))


def generar_sfx_click(ruta_wav: Path, sample_rate: int = 44100):
    """Clic de mouse táctil y nítido para la acción en el mockup (~0.08s)."""
    dur = 0.08
    t = np.linspace(0, dur, int(sample_rate * dur), endpoint=False)
    # Transiente agudo inicial
    snap = np.sin(2 * np.pi * 3200 * t) * np.exp(-t / 0.005)
    # Resonancia mecánica del botón
    body = np.sin(2 * np.pi * 1400 * t) * np.exp(-t / 0.025)
    signal = 0.65 * snap + 0.35 * body
    signal = signal / np.max(np.abs(signal) + 1e-6) * 0.8
    wavfile.write(str(ruta_wav), sample_rate, (signal * 32767).astype(np.int16))


def generar_sfx_slide(ruta_wav: Path, sample_rate: int = 44100):
    """Sonido 'swish' suave simulando el archivo de correos en carpetas (~0.45s)."""
    dur = 0.45
    t = np.linspace(0, dur, int(sample_rate * dur), endpoint=False)
    noise = np.random.uniform(-1, 1, len(t))
    env = np.sin(np.pi * (t / dur)) ** 1.5
    frec = np.linspace(800, 300, len(t))
    phase = 2 * np.pi * np.cumsum(frec) / sample_rate
    signal = (0.5 * np.sin(phase) + 0.5 * noise) * env
    signal = signal / np.max(np.abs(signal) + 1e-6) * 0.6
    wavfile.write(str(ruta_wav), sample_rate, (signal * 32767).astype(np.int16))


def generar_sfx_chime(ruta_wav: Path, sample_rate: int = 44100):
    """Campana armónica brillante y gratificante para Inbox Zero (~1.2s)."""
    dur = 1.2
    t = np.linspace(0, dur, int(sample_rate * dur), endpoint=False)
    # Acorde mayor brillante: C6 (1046.5Hz), E6 (1318.5Hz), G6 (1568Hz), C7 (2093Hz)
    ch1 = np.sin(2 * np.pi * 1046.5 * t) * np.exp(-t / 0.5)
    ch2 = np.sin(2 * np.pi * 1318.5 * t) * np.exp(-t / 0.6)
    ch3 = np.sin(2 * np.pi * 1568.0 * t) * np.exp(-t / 0.7)
    ch4 = np.sin(2 * np.pi * 2093.0 * t) * np.exp(-t / 0.4)
    # Brillo shimmer
    shimmer = np.sin(2 * np.pi * 3136.0 * t) * np.exp(-t / 0.25) * 0.3
    signal = 0.35 * ch1 + 0.3 * ch2 + 0.25 * ch3 + 0.2 * ch4 + shimmer
    signal = signal / np.max(np.abs(signal) + 1e-6) * 0.75
    wavfile.write(str(ruta_wav), sample_rate, (signal * 32767).astype(np.int16))


def generar_sfx_bounce(ruta_wav: Path, sample_rate: int = 44100):
    """Pop/bounce amigable y futurista para las entradas elásticas de Byte (~0.22s)."""
    dur = 0.22
    t = np.linspace(0, dur, int(sample_rate * dur), endpoint=False)
    # Barrido de tono elástico: sube y baja ligeramente
    freq = 280 + 260 * np.sin(np.pi * (t / dur))
    phase = 2 * np.pi * np.cumsum(freq) / sample_rate
    env = np.exp(-t / 0.08)
    signal = np.sin(phase) * env
    signal = signal / np.max(np.abs(signal) + 1e-6) * 0.65
    wavfile.write(str(ruta_wav), sample_rate, (signal * 32767).astype(np.int16))


def generar_sfx_riser(ruta_wav: Path, sample_rate: int = 44100):
    """Riser de anticipación (~0.85s): barrido ascendente + ruido que sube,
    para colocar justo ANTES del segmento payoff (resultado/cierre)."""
    dur = 0.85
    t = np.linspace(0, dur, int(sample_rate * dur), endpoint=False)
    # Tono: ~2 octavas ascendentes (220 -> 880 Hz) con envolvente creciente
    freq = 220.0 * (2.0 ** (2.0 * (t / dur)))
    phase = 2 * np.pi * np.cumsum(freq) / sample_rate
    tono = np.sin(phase)
    # Ruido filtrado en paso (aproximación: ruido con amplitud creciente)
    ruido = np.random.uniform(-1, 1, len(t))
    env = (t / dur) ** 2.2
    signal = (0.55 * tono + 0.45 * ruido) * env
    # Pequeño remate final para enganchar al impacto
    signal[-int(0.03 * sample_rate):] *= np.linspace(1.0, 0.6, int(0.03 * sample_rate))
    signal = signal / np.max(np.abs(signal) + 1e-6) * 0.7
    wavfile.write(str(ruta_wav), sample_rate, (signal * 32767).astype(np.int16))


def generar_sfx_impact(ruta_wav: Path, sample_rate: int = 44100):
    """Impacto suave de payoff (~0.5s): sub-gravedad que cae + golpe de ruido
    corto, para capas con el chime en el momento resultado."""
    dur = 0.5
    t = np.linspace(0, dur, int(sample_rate * dur), endpoint=False)
    # Sub: barrido descendente 110 -> 48 Hz
    freq = 110.0 * np.exp(-t / 0.18) + 48.0
    phase = 2 * np.pi * np.cumsum(freq) / sample_rate
    sub = np.sin(phase) * np.exp(-t / 0.16)
    # Golpe de ruido corto (transiente)
    n = int(0.06 * sample_rate)
    golpe = np.zeros_like(t)
    golpe[:n] = np.random.uniform(-1, 1, n) * np.exp(-t[:n] / 0.015)
    signal = 0.8 * sub + 0.35 * golpe
    signal = signal / np.max(np.abs(signal) + 1e-6) * 0.75
    wavfile.write(str(ruta_wav), sample_rate, (signal * 32767).astype(np.int16))


def generar_musica_fondo_tech(ruta_wav: Path, duracion_total: float = 35.0, sample_rate: int = 44100):
    """
    Genera una pista de fondo Synthwave / Cyberpunk Lo-Fi moderna y de alta calidad (100% royalty-free):
    - Tempo: 112 BPM (ritmo activo y moderno).
    - Progresión armónica: Cm9 -> Abmaj7 -> Fm7 -> Bbadd9.
    - Instrumentos:
      1. Batería analógica: Bombo punchy con sweep de sub-graves, caja/clap nítida con reverb y hi-hats 16th con paneo estéreo.
      2. Bajo synthwave: Línea de bajo rodante en corcheas con saturación analógica.
      3. Pads analógicos: Acordes exuberantes con coro/detune estéreo sedoso.
      4. Arpegio tech: Plucks cristalinos en semicorcheas con eco estéreo que aportan vida tecnológica.
    - Mezclado en 2 canales estéreo (L/R) a 44.1 kHz.
    """
    import math

    total_samples = int(sample_rate * duracion_total)
    bpm = 112.0
    beat_dur = 60.0 / bpm
    bar_dur = beat_dur * 4.0
    step_16th = beat_dur / 4.0

    left = np.zeros(total_samples, dtype=np.float32)
    right = np.zeros(total_samples, dtype=np.float32)

    # Progresión armónica en C Menor
    prog = [
        {"root": 65.41, "pad": [130.81, 155.56, 196.00, 233.08], "arp": [261.63, 311.13, 392.00, 466.16, 523.25]},  # Cm9
        {"root": 51.91, "pad": [103.83, 130.81, 155.56, 196.00], "arp": [207.65, 261.63, 311.13, 392.00, 415.30]},  # Abmaj7
        {"root": 43.65, "pad": [87.31, 103.83, 130.81, 174.61],  "arp": [174.61, 207.65, 261.63, 349.23, 392.00]},  # Fm7
        {"root": 58.27, "pad": [116.54, 146.83, 174.61, 233.08], "arp": [233.08, 293.66, 349.23, 466.16, 523.25]}   # Bbadd9
    ]

    num_bars = int(np.ceil(duracion_total / bar_dur)) + 1

    for b_idx in range(num_bars):
        t_bar = b_idx * bar_dur
        if t_bar >= duracion_total:
            break
        ch = prog[b_idx % len(prog)]

        # 1. Pads exuberantes con detuning estéreo
        s_idx0 = int(t_bar * sample_rate)
        s_idx1 = min(total_samples, int((t_bar + bar_dur) * sample_rate))
        n_s = s_idx1 - s_idx0
        if n_s > 0:
            t_p = np.linspace(0, n_s / sample_rate, n_s, endpoint=False)
            env_pad = np.sin(np.pi * (t_p / (n_s / sample_rate))) ** 1.3

            pad_l = np.zeros(n_s, dtype=np.float32)
            pad_r = np.zeros(n_s, dtype=np.float32)
            for freq in ch["pad"]:
                w1 = np.sin(2 * np.pi * freq * t_p)
                w2 = np.sin(2 * np.pi * (freq * 1.003) * t_p)
                w3 = np.sin(2 * np.pi * (freq * 0.997) * t_p)
                pad_l += (w1 + 0.6 * w2)
                pad_r += (w1 + 0.6 * w3)
            pad_l = pad_l / len(ch["pad"]) * env_pad * 0.16
            pad_r = pad_r / len(ch["pad"]) * env_pad * 0.16
            left[s_idx0:s_idx1] += pad_l
            right[s_idx0:s_idx1] += pad_r

        # 2. Línea de bajo synthwave (corcheas pulsantes)
        for step in range(8):
            t_bass = t_bar + step * (beat_dur / 2.0)
            b0 = int(t_bass * sample_rate)
            b1 = min(total_samples, b0 + int(0.22 * sample_rate))
            if b1 > b0:
                tb = np.linspace(0, (b1 - b0) / sample_rate, b1 - b0, endpoint=False)
                env_b = np.exp(-tb / 0.08)
                f_b = ch["root"] * 2.0
                bass_tone = (
                    np.sin(2 * np.pi * f_b * tb) +
                    0.5 * np.sin(4 * np.pi * f_b * tb) +
                    0.25 * np.sin(6 * np.pi * f_b * tb)
                ) * env_b * 0.20
                left[b0:b1] += bass_tone
                right[b0:b1] += bass_tone

        # 3. Batería analógica (Kick, Snare/Clap, 16th Hi-hats)
        for beat in range(4):
            t_bt = t_bar + beat * beat_dur

            # Bombo en beats 0 y 2
            if beat in [0, 2]:
                k0 = int(t_bt * sample_rate)
                k1 = min(total_samples, k0 + int(0.18 * sample_rate))
                if k1 > k0:
                    tk = np.linspace(0, (k1 - k0) / sample_rate, k1 - k0, endpoint=False)
                    fk = 45 + 95 * np.exp(-tk / 0.035)
                    phk = 2 * np.pi * np.cumsum(fk) / sample_rate
                    kick = np.sin(phk) * np.exp(-tk / 0.065) * 0.38
                    left[k0:k1] += kick
                    right[k0:k1] += kick

            # Caja/Clap en beats 1 y 3
            if beat in [1, 3]:
                sn0 = int(t_bt * sample_rate)
                sn1 = min(total_samples, sn0 + int(0.20 * sample_rate))
                if sn1 > sn0:
                    tsn = np.linspace(0, (sn1 - sn0) / sample_rate, sn1 - sn0, endpoint=False)
                    body = np.sin(2 * np.pi * 185 * tsn) * np.exp(-tsn / 0.045)
                    noise = np.random.uniform(-1, 1, len(tsn)) * np.exp(-tsn / 0.08)
                    snare = (0.5 * body + 0.5 * noise) * 0.25
                    left[sn0:sn1] += snare
                    right[sn0:sn1] += snare

            # Hi-hats en semicorcheas con balanceo estéreo
            for h in range(4):
                th = t_bt + h * step_16th
                h0 = int(th * sample_rate)
                h1 = min(total_samples, h0 + int(0.045 * sample_rate))
                if h1 > h0:
                    th_v = np.linspace(0, (h1 - h0) / sample_rate, h1 - h0, endpoint=False)
                    h_noise = np.random.uniform(-1, 1, len(th_v)) * np.exp(-th_v / 0.018)
                    vol_h = 0.11 if h % 2 == 0 else 0.06
                    pan = 0.28 * math.sin(h * 1.5)
                    left[h0:h1] += h_noise * vol_h * (0.5 - pan)
                    right[h0:h1] += h_noise * vol_h * (0.5 + pan)

        # 4. Arpegio tech en semicorcheas
        arp_notes = ch["arp"]
        for s16 in range(16):
            t_arp = t_bar + s16 * step_16th
            a0 = int(t_arp * sample_rate)
            a1 = min(total_samples, a0 + int(0.12 * sample_rate))
            if a1 > a0:
                ta = np.linspace(0, (a1 - a0) / sample_rate, a1 - a0, endpoint=False)
                f_arp = arp_notes[s16 % len(arp_notes)]
                env_arp = np.exp(-ta / 0.04)
                arp_tone = (
                    np.sin(2 * np.pi * f_arp * ta) +
                    0.3 * np.sin(4 * np.pi * f_arp * ta)
                ) * env_arp * 0.08
                pan_arp = 0.32 * math.sin(s16 * 0.9)
                left[a0:a1] += arp_tone * (0.5 - pan_arp)
                right[a0:a1] += arp_tone * (0.5 + pan_arp)

    # Master estéreo de la música
    stereo = np.column_stack((left, right))
    peak = np.max(np.abs(stereo)) + 1e-6
    stereo = stereo / peak * 0.85

    # Fade in inicial (0.4s) y fade out final (1.2s)
    fade_in_samples = int(0.4 * sample_rate)
    fade_out_samples = int(1.2 * sample_rate)
    stereo[:fade_in_samples] *= np.linspace(0, 1, fade_in_samples)[:, np.newaxis]
    stereo[-fade_out_samples:] *= np.linspace(1, 0, fade_out_samples)[:, np.newaxis]

    wavfile.write(str(ruta_wav), sample_rate, (stereo * 32767).astype(np.int16))
    print(f"Música de fondo Synthwave estéreo generada en: {ruta_wav} ({duracion_total:.2f}s)")


def generar_todos_los_sfx(dir_sfx: Path) -> dict:
    """Genera toda la biblioteca de efectos de sonido requerida para el video."""
    dir_sfx = Path(dir_sfx)
    dir_sfx.mkdir(parents=True, exist_ok=True)
    rutas = {
        "whoosh": dir_sfx / "sfx_whoosh.wav",
        "click": dir_sfx / "sfx_click.wav",
        "slide": dir_sfx / "sfx_slide.wav",
        "chime": dir_sfx / "sfx_chime.wav",
        "bounce": dir_sfx / "sfx_bounce.wav",
        "riser": dir_sfx / "sfx_riser.wav",
        "impact": dir_sfx / "sfx_impact.wav",
        "musica": dir_sfx / "musica_fondo.wav",
    }

    if not rutas["whoosh"].exists():
        generar_sfx_whoosh(rutas["whoosh"])
    if not rutas["click"].exists():
        generar_sfx_click(rutas["click"])
    if not rutas["slide"].exists():
        generar_sfx_slide(rutas["slide"])
    if not rutas["chime"].exists():
        generar_sfx_chime(rutas["chime"])
    if not rutas["bounce"].exists():
        generar_sfx_bounce(rutas["bounce"])
    if not rutas["riser"].exists():
        generar_sfx_riser(rutas["riser"])
    if not rutas["impact"].exists():
        generar_sfx_impact(rutas["impact"])
    # Siempre regenerar música para aplicar el nuevo motor synthwave
    generar_musica_fondo_tech(rutas["musica"], duracion_total=35.0)

    return rutas


def _planificar_sfx(segmentos: List[Dict[str, Any]]) -> List[Tuple[str, float, float]]:
    """
    Planifica los SFX a partir de los segmentos reales del video (con 'tipo' e 'inicio'):
      - escena 0:        whoosh de apertura + bounce de entrada
      - cada transición: whoosh antes del corte + bounce en la entrada de la nueva escena
      - payoff:          riser de anticipación 0.85s antes de 'resultado' (o 'cierre'),
                         e impacto + chime en el inicio del payoff
      - 'punto_1/2':     click + slide de interacción a mitad del primer segundo de demo
    Devuelve tuplas (nombre_sfx, t_segundo, volumen).
    """
    plan: List[Tuple[str, float, float]] = []
    if not segmentos:
        plan.append(("whoosh", 0.0, 0.35))
        return plan

    ordenados = sorted(segmentos, key=lambda s: float(s.get("inicio", 0.0)))
    for i, seg in enumerate(ordenados):
        t0 = float(seg.get("inicio", 0.0))
        tipo = str(seg.get("tipo", ""))
        if i == 0:
            plan.append(("whoosh", 0.0, 0.35))
            plan.append(("bounce", 0.08, 0.30))
        else:
            plan.append(("whoosh", max(0.0, t0 - 0.15), 0.38))
            plan.append(("bounce", t0 + 0.08, 0.30))
        if tipo == "resultado":
            plan.append(("chime", t0 + 0.22, 0.65))
        elif tipo in ("punto_1", "punto_2", "demostracion_1", "demostracion_2"):
            plan.append(("click", t0 + 1.2, 0.70))
            plan.append(("slide", t0 + 1.7, 0.45))

    # Payoff: riser de anticipación + impacto (si no hay 'resultado', el
    # 'cierre' actúa como payoff final)
    payoff = next((s for s in ordenados if str(s.get("tipo", "")) == "resultado"), None)
    if payoff is None:
        payoff = next((s for s in ordenados if str(s.get("tipo", "")) == "cierre"), None)
    if payoff is not None:
        t0p = float(payoff.get("inicio", 0.0))
        plan.append(("riser", max(0.0, t0p - 0.85), 0.50))
        plan.append(("impact", t0p + 0.22, 0.55))
    return plan


def mezclar_paisaje_sonoro_completo(
    ruta_voz: Union[str, Path],
    ruta_salida_wav: Union[str, Path],
    duracion_total: float,
    segmentos: Optional[List[dict]] = None,
    dir_audio: Optional[Union[str, Path]] = None,
    sample_rate: int = 44100
) -> Path:
    """
    Mezclador multitrack procedural estéreo:
    1. Locución principal de ElevenLabs nítida y al frente (centrada).
    2. Música de fondo Synthwave estéreo con sidechain ducking adaptativo:
       - Baja a -22dB cuando Byte habla para que no tape ninguna palabra.
       - Sube a -14dB con energía en las pausas y cambios de escena.
    3. SFX de alta fidelidad sincronizados con la animación de Byte y los mockups.
    """
    import subprocess
    import tempfile

    ruta_voz = Path(ruta_voz).resolve()
    ruta_salida_wav = Path(ruta_salida_wav).resolve()
    ruta_salida_wav.parent.mkdir(parents=True, exist_ok=True)

    if dir_audio is None:
        dir_audio = ruta_salida_wav.parent
    else:
        dir_audio = Path(dir_audio).resolve()

    sfx_dict = generar_todos_los_sfx(dir_audio)

    # 1. Cargar y decodificar voz
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_voz:
        tmp_voz_path = Path(tmp_voz.name)

    try:
        cmd_decode = [
            "ffmpeg", "-y",
            "-i", str(ruta_voz),
            "-ar", str(sample_rate),
            "-ac", "1",
            "-f", "wav",
            str(tmp_voz_path)
        ]
        subprocess.run(cmd_decode, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        _, voz_raw = wavfile.read(str(tmp_voz_path))
    finally:
        if tmp_voz_path.exists():
            tmp_voz_path.unlink()

    voz = voz_raw.astype(np.float32) / 32768.0
    pico_voz = np.max(np.abs(voz)) + 1e-6
    voz = voz / pico_voz * 0.90

    total_samples = max(len(voz), int(duracion_total * sample_rate))
    master = np.zeros((total_samples, 2), dtype=np.float32)

    # Voz centrada en ambos canales
    master[:len(voz), 0] += voz
    master[:len(voz), 1] += voz

    # 2. Mezclar Música de Fondo Synthwave con Sidechain Ducking
    _, bgm_raw = wavfile.read(str(sfx_dict["musica"]))
    if bgm_raw.ndim == 1:
        bgm = np.column_stack((bgm_raw, bgm_raw)).astype(np.float32) / 32768.0
    else:
        bgm = bgm_raw.astype(np.float32) / 32768.0

    if len(bgm) < total_samples:
        repeats = int(np.ceil(total_samples / len(bgm)))
        bgm = np.tile(bgm, (repeats, 1))[:total_samples]
    else:
        bgm = bgm[:total_samples]

    # Calcular envolvente vocal para sidechain ducking
    voz_padded = np.zeros(total_samples, dtype=np.float32)
    voz_padded[:len(voz)] = np.abs(voz)
    win_len = int(0.20 * sample_rate)
    window = np.ones(win_len, dtype=np.float32) / win_len
    env_voz = np.convolve(voz_padded, window, mode="same")

    # Ganancia adaptativa suave:
    # Activa con voz: 0.085 (~ -21dB)
    # Silencios / pausas: 0.22 (~ -13dB)
    gain_bgm = np.where(env_voz > 0.025, 0.085, 0.22)
    gain_bgm = np.convolve(gain_bgm, window, mode="same")[:, np.newaxis]

    master += bgm * gain_bgm

    # 3. Inyectar SFX
    def inyectar_sfx(p_sfx: Path, t_seg: float, vol: float):
        if not p_sfx.exists() or t_seg < 0:
            return
        _, s_raw = wavfile.read(str(p_sfx))
        if s_raw.ndim == 1:
            s_float = (s_raw.astype(np.float32) / 32768.0) * vol
            s_stereo = np.column_stack((s_float, s_float))
        else:
            s_stereo = (s_raw.astype(np.float32) / 32768.0) * vol

        idx_ini = int(t_seg * sample_rate)
        idx_fin = min(total_samples, idx_ini + len(s_stereo))
        len_inject = idx_fin - idx_ini
        if len_inject > 0:
            master[idx_ini:idx_fin] += s_stereo[:len_inject]

    # 4. Efectos sincronizados con las escenas (planificados por tipo de segmento)
    for nombre_sfx, t_seg, vol in _planificar_sfx(segmentos or []):
        inyectar_sfx(sfx_dict[nombre_sfx], t_seg, vol)

    # 5. Master Limiter
    pico_master = np.max(np.abs(master))
    if pico_master > 0.95:
        master = np.tanh(master / pico_master * 1.05) * 0.95

    # 6. Guardar WAV estéreo 16-bit
    audio_int16 = (master * 32767.0).astype(np.int16)
    wavfile.write(str(ruta_salida_wav), sample_rate, audio_int16)
    print(f"Paisaje sonoro Synthwave estéreo masterizado en: {ruta_salida_wav} ({duracion_total:.2f}s)")
    return ruta_salida_wav


if __name__ == "__main__":
    try:
        from src.rutas import DIR_AUDIO
        carpeta_audio = DIR_AUDIO
    except ImportError:
        from rutas import DIR_AUDIO
        carpeta_audio = DIR_AUDIO
    generar_todos_los_sfx(carpeta_audio)

