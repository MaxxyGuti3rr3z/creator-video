import subprocess
from pathlib import Path

# Dialogue starts at 0.0s.
# Word 1: '¿BANDEJA' starts at 0.0s, ends at 0.5s -> pop from 0 to 100ms, then back to 200ms
# Word 2: 'DE' starts at 0.59s -> pop from 590ms to 680ms
# Word 3: 'ENTRADA' starts at 0.68s -> pop from 680ms to 780ms to 880ms

ass_content = """[Script Info]
Title: Test Subtitles with Dynamic Pop
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: KaraokeByte,Arial,84,&H00FFE500,&H00FFFFFF,&H00000000,&H90000000,-1,0,0,0,100,100,1,0,1,8,4,2,80,80,680,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.00,0:00:02.50,KaraokeByte,,0,0,0,,{\\1c&H00FFE500&\\t(0,100,\\fscx120\\fscy120)\\t(100,200,\\fscx100\\fscy100)\\k50}¿BANDEJA {\\1c&H00FFE500&\\t(500,580,\\fscx115\\fscy115)\\t(580,680,\\fscx100\\fscy100)\\k18}DE {\\1c&H000AD6FF&\\t(680,780,\\fscx122\\fscy122)\\t(780,900,\\fscx100\\fscy100)\\k40}ENTRADA {\\1c&H003A45FF&\\k70}LLENA?
"""

Path("test_sub.ass").write_text(ass_content, encoding="utf-8")

# Render at 0.75s (when ENTRADA is peaking in size)
cmd = [
    "ffmpeg", "-y",
    "-f", "lavfi", "-i", "color=c=0x111827:s=1080x1920:d=2.5:r=30",
    "-vf", "subtitles=test_sub.ass",
    "-frames:v", "1", "-ss", "0.76",
    "-update", "1",
    "test_sub_pop_render.png"
]
subprocess.run(cmd, check=True, capture_output=True)
print("Subtítulo con pop renderizado en test_sub_pop_render.png")
