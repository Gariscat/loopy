import matplotlib.pyplot as plt
import numpy as np
from loopy import LoopyPreset
from loopy import LoopyPatternCore, PRESET_DIR
from loopy.utils import preview_wave
import os
import librosa

lead = LoopyPreset(os.path.join(PRESET_DIR, 'Ultrasonic-LD-Follow.wav'))
# preset.preview('A5')

pattern_type = LoopyPatternCore(num_bars=4)
pattern_type.add_note('G5', 1/4, 0, lead)
pattern_type.add_note('G5', 1/4, 1, lead)
pattern_type.add_note('A5', 1/4, 2, lead)
pattern_type.add_note('B5', 1/8, 3, lead)
pattern_type.add_note('D6', 1/4, 3.5, lead)
pattern_type.add_note('D6', 1/4, 4.5, lead)
pattern_type.add_note('B5', 1/8, 5.5, lead)
pattern_type.add_note('D6', 1/4, 6, lead)
pattern_type.add_note('E6', 1/4, 7, lead)

y = pattern_type.render()
# y, sr = librosa.load('./dry.wav', sr=44100, mono=False)
# y = np.transpose(y)
# Design filter

from loopy.effect import LoopyLowpass, LoopyReverb

lp = LoopyLowpass(freq=200)
y_filted = lp(y)
# print(y_filted.shape)

rv = LoopyReverb(wet_level=0.25)
y_reverb = rv(y)
# print(y_reverb.shape)

preview_wave(y)
preview_wave(y_reverb)

