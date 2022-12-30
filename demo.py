from loopy import LoopyPreset
from loopy.generator import PRESET_DIR
import os

preset = LoopyPreset(os.path.join(PRESET_DIR, 'Ultrasonic-LD-Forever.wav'))
# preset.preview('A5')

preset.render(
    key_name='C#6',
    attack=300,
    decay=50,
    sustain=0.8,
    release=50,
    note_value=1/2,
    bpm=128,
    sig='4/4',
    preview=False,
    debug=False,
)