import matplotlib.pyplot as plt
import numpy as np
from loopy import LoopyTrack, LoopyPreset, LoopyPatternCore, PRESET_DIR, DEFAULT_SR, preview_notes, LoopySidechain, LoopyBalance
from loopy.utils import *
import os
import librosa
from loopy.template import *
"""
lead = LoopyPreset(os.path.join(PRESET_DIR, 'Ultrasonic-LD-Stars.wav'))
# preset.preview('A5')

pattern_type = LoopyPatternCore(num_bars=4)
pattern_type.add_note('G4', 1/4, 0, lead)
pattern_type.add_note('G4', 1/4, 1, lead)
pattern_type.add_note('A4', 1/4, 2, lead)
pattern_type.add_note('B4', 1/8, 3, lead)
pattern_type.add_note('D5', 1/4, 3.5, lead)
pattern_type.add_note('D5', 1/4, 4.5, lead)
pattern_type.add_note('B4', 1/8, 5.5, lead)
pattern_type.add_note('D5', 1/4, 6, lead)
pattern_type.add_note('E5', 1/4, 7, lead)

y = pattern_type.render()
# y, sr = librosa.load('./dry.wav', sr=44100, mono=False)
# y = np.transpose(y)
# Design filter

from loopy.effect import LoopyLowpass, LoopyHighpass, LoopyReverb

lp = LoopyHighpass(freq=500)
y = lp(y)
# print(y_filted.shape)

rv = LoopyReverb(wet_level=0.25)
y_reverb = rv(y)
# print(y_reverb.shape)

preview_wave(y)
preview_wave(y_reverb)

from loopy import LoopySidechain
sides = LoopySidechain(interp_order=2)
sides.forward(np.random.rand(DEFAULT_SR*15, 2))

seq = [84, 84, 84, 0, 76, 76, 76, 0, 76, 76, 76, 0, 74, 74, 72, 72, 79, 79, 72, 72, 72, 0, 74, 74, 74, 0, 74, 0, 74, 0, 72, 72, 76, 76, 76, 0, 84, 84, 84, 0, 84, 0, 84, 0, 81, 0, 79, 0, 81, 0, 79, 79, 79, 0, 79, 79, 79, 0, 79, 0, 79, 0, 76, 0, 81, 81, 81, 0, 81, 81, 81, 0, 81, 0, 81, 0, 79, 0, 76, 0, 79, 0, 79, 79, 79, 0, 76, 76, 76, 0, 76, 0, 74, 0, 72, 0, 74, 74, 74, 0, 81, 81, 81, 0, 81, 0, 81, 81, 81, 0, 79, 79, 79, 0, 0, 0, 0, 0, 0, 0, 0, 0, 76, 0, 74, 0, 72, 0]
notes = seq_note_parser(seq)
print(notes)
"""
"""key_name_list = ('A2', 'A3', 'C4', 'E4', 'G4')
y = preview_chord(key_name_list, play_now=False)

sd = LoopySidechain(attain=0.3, interp_order=2)

y = sd(y)
preview_wave(y)"""


"""
y_s = []
for del_second in (False,):
    for decr_octave in (False,):
        for incr_octave in (False,):
            
            for chord_id in [6, 4, 1, 5]:
                notes = get_chord_notes(
                    chord_id=chord_id,
                    scale_root='C',
                    scale_type='maj',
                    root_area='3',
                    del_second=del_second,
                    decr_octave=decr_octave,
                    incr_octave=incr_octave,
                    decor_notes=[2]
                )
                y = preview_notes(notes, play_now=False, as_chord=True, preset_name='Ultrasonic-PD-MG.wav')
                y_s.append(y)


preview_wave(np.concatenate(y_s, axis=0))
"""
"""

track = LoopyTrack('test', length='00:15')
add_kick(track, num_bars=8)
add_clap(track, num_bars=8)
add_hat(track, num_bars=8)

y = track.render()
preview_wave(y)


"""

melody_line = [79, 79, 0, 79, 79, 0, 79, 79, 0, 79, 79, 0, 72, 72, 67, 67, 77, 77, 0, 77, 77, 0, 76, 76, 0, 76, 76, 0, 74, 74, 72, 72, 79, 79, 0, 79, 79, 0, 79, 79, 0, 79, 79, 0, 72, 72, 84, 84, 83, 83, 0, 83, 83, 0, 79, 79, 0, 79, 79, 0, 74, 74, 76, 76, 79, 79, 0, 79, 79, 0, 79, 79, 0, 79, 79, 0, 72, 72, 67, 67, 77, 77, 77, 77, 77, 77, 76, 76, 76, 76, 76, 76, 74, 74, 72, 72, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 79, 72, 72, 84, 84, 83, 83, 83, 83, 83, 83, 79, 
79, 79, 79, 79, 79, 71, 71, 72, 72]

chord_line = [6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 
5, 5, 5, 5, 5, 5, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 6, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]

assert len(melody_line) == len(chord_line)

melody_notes = note_seq_parser(melody_line)
print(melody_notes)
chord_notes = chord_seq_parser(chord_line, melody_line)
print(chord_notes)

lead = LoopyPreset(os.path.join(PRESET_DIR, 'Ultrasonic-LD-Forever.wav'))
chord = LoopyPreset(os.path.join(PRESET_DIR, 'Ultrasonic-PD-FarAway.wav'))

pattern_core = LoopyPatternCore(num_bars=8)
pattern_core.add_notes(melody_notes, lead)
pattern_core.add_notes(chord_notes, chord)

preview_wave(pattern_core.render())