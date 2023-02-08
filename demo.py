import matplotlib.pyplot as plt
import numpy as np
from loopy import LoopyTrack, LoopyPreset, LoopyPatternCore, PRESET_DIR, DEFAULT_SR, preview_notes, LoopySidechain, LoopyBalance
from loopy.utils import *
import os
import librosa
from loopy.template import *
from tqdm import tqdm
"""
lead = LoopyPreset(find_preset('Ultrasonic-LD-Stars.wav'))
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
"""
from loopy import LoopySidechain
sides = LoopySidechain(attain=0.5, interp_order=2)
balance = LoopyBalance(-6)
inst = sides.forward(preview_notes(key_name_list=get_chord_notes(chord_id=1), play_now=True, as_chord=True), debug=True)
inst = balance(inst)

track = LoopyTrack('plot', length='00:1.875')
add_kick(track, num_bars=1)
kick = track.render()
plt.plot(kick[:, 0], c='mediumorchid', label='kick_drum')
plt.legend()
plt.show()
plt.close()

y = kick + inst
plt.plot(y[:, 0], c='darkorchid', label='mix')
plt.legend()
plt.show()
plt.close()
exit()
"""


"""melody_line = '84 84 84 84 00 00 86 86 86 86 00 00 00 00 86 00 86 86 84 00 84 84 81 81 81 81 00 00 00 00 89 00 89 89 88 00 88 88 86 86 86 86 00 00 00 00 86 00 86 86 84 84 86 86 81 81 81 81 00 00 00 00 00 00'
melody_line = [int(x)-11 if int(x) else 0 for x in melody_line.split()] * 2
chord_line = []

chord_line += [6] * 16
chord_line += [4] * 8
chord_line += [1] * 8
chord_line += [5] * 8
chord_line += [6] * 8
chord_line += [4] * 8
chord_line += [5] * 8

chord_line += [6] * 16
chord_line += [4] * 8
chord_line += [1] * 8
chord_line += [5] * 8
chord_line += [6] * 8
chord_line += [4] * 8
chord_line += [5] * 8"""

with open('raw_80.txt', 'r') as f:
    lines = f.readlines()
    melody_line, chord_line = None, None
    for i, line in tqdm(enumerate(lines), total=len(lines)):
        if i % 4 == 1:
            melody_line = [int(x) for x in line.strip().split()]
        elif i % 4 == 2:
            chord_line = [int(x) for x in line.strip().split()]

        if melody_line and chord_line:
            prog_track = prog_house(melody_line, chord_line, chord_sync=True, preview=False, style='Tobu', name='exp')
            prog_track.save_audio(target_dir='D:\\Project 2023\\renders')
            melody_line, chord_line = None, None

            
            prog_track.save()

