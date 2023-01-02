from loopy import LoopyPreset
from loopy import LoopyPatternCore, PRESET_DIR
from loopy.utils import preview_wave
import os

preset = LoopyPreset(os.path.join(PRESET_DIR, 'Ultrasonic-LD-Forever.wav'))
# preset.preview('A5')

pattern_type = LoopyPatternCore(num_bars=4)
pattern_type.add_note('C5', 1/4, 0, preset)
pattern_type.add_note('C5', 1/4, 1, preset)
pattern_type.add_note('D5', 1/4, 2, preset)
pattern_type.add_note('E5', 1/8, 3, preset)
pattern_type.add_note('G5', 1/8, 3.5, preset)

preview_wave(pattern_type.render())