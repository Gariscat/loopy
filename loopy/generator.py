import librosa
import soundfile as sf
from loopy.utils import preview_wave
import os
import numpy as np


PIANO_KEYS = ['A1', 'A#1', 'B1', 'C2']
for i in range(2, 9):
    PIANO_KEYS += [
        f'C#{i}', f'D{i}', f'D#{i}', f'E{i}',
        f'F{i}', f'F#{i}', f'G{i}', f'G#{i}',
        f'A{i}', f'A#{i}', f'B{i}', f'C{i+1}'
    ]
assert(len(PIANO_KEYS) == 88)

PRESET_DIR = 'D:\\Project 2023\\loopy\\presets'
LOAD_BPM = 64

def modify_preset_dir(target_dir: str):
    print(f'Cautious: the preset folder path has been changed from {PRESET_DIR} to {target_dir}')
    PRESET_DIR = target_dir

def modify_load_bpm(target_bpm: int):
    print(f'Cautious: the BPM for preset loading has been changed from {LOAD_BPM} to {target_bpm}')
    LOAD_BPM = target_bpm

class LoopyPreset():
    def __init__(self,
        source_path: str,
        target_sr: int = 44100,
        name: str = None,
        load_bpm: int = LOAD_BPM,
    ) -> None:
        y, _ = librosa.load(source_path, sr=target_sr, mono=False)
        self._y = np.transpose(y, axes=(1, 0))
        self._sr = target_sr
        
        self._name = source_path if name is None else name
        self._load_bpm = load_bpm

        self.parse()

    def parse(self):
        self._raw_notes = {}
        for i in range(88):
            st = int(i*60*self._sr/self._load_bpm)
            ed = int((i+1)*60*self._sr/self._load_bpm)
            self._raw_notes[PIANO_KEYS[i]] = self._y[st:ed]
            # print(st, ed)
            # sf.write(f'{i+1}.wav', y[st:ed], sr)

    def envelope(self,
        attack: int,  # unit is ms
        decay: int,  # unit is ms
        sustain: float,  # between 0 and 1
        release: int,  # unit is ms
        note_value: float,  # e.g. 1/4, 1/8, 1/16, etc.
        bpm: int,
        sig: str = '4/4',
    ):
        # https://en.wikipedia.org/wiki/Envelope_(music)
        beat_value = 1 / float(sig[-1])  # 4/4 means 1 quarter note receives 1 beat
        sec_per_beat = 60 / bpm
        num_sec_key = min(sec_per_beat * note_value / beat_value, 60 / LOAD_BPM - release / 1000)

        num_sec_a = attack / 1000
        num_sec_d = decay / 1000
        num_sec_s = num_sec_key - num_sec_a - num_sec_d
        num_sec_r = release / 1000

        num_sec_tot = num_sec_key + num_sec_r  # (a+d+s)+r

        if min(num_sec_a, num_sec_d, num_sec_s, num_sec_r) < 0:
            raise KeyError("Length of part of ADSR is negative")

        p1_idx = int(num_sec_a*self._sr)
        p2_idx = int((num_sec_a+num_sec_d)*self._sr)
        p3_idx = int((num_sec_a+num_sec_d+num_sec_s)*self._sr)
        p4_idx = int(num_sec_tot*self._sr)

        e = np.zeros(p4_idx)
        # attack
        for i in range(0, p1_idx):
            e[i] = i / p1_idx
        # decay
        for i in range(p1_idx, p2_idx):
            e[i] = 1 - (1-sustain) * (i-p1_idx) / (p2_idx-p1_idx)
        # sustain
        for i in range(p2_idx, p3_idx):
            e[i] = sustain
        # release
        for i in range(p3_idx, p4_idx):
            e[i] = sustain - sustain * (i-p3_idx) / (p4_idx-p3_idx)

        return e, p4_idx

    def render(self,
        key_name: str,  # C5, A#6, etc.
        attack: int,  # unit is ms
        decay: int,  # unit is ms
        sustain: float,  # between 0 and 1
        release: int,  # unit is ms
        note_value: float,  # e.g. 1/4, 1/8, 1/16, etc.
        bpm: int,
        sig: str = '4/4',
        preview: bool = False,
        debug: bool = False,
    ):
        e, num_samples = self.envelope(attack, decay, sustain, release, note_value, bpm, sig)
        y = self._raw_notes[key_name][:num_samples, :]
        # then apply the envelope to the original waveform
        ret = y * np.expand_dims(e, -1)
        if preview:
            preview_wave(ret, self._sr)
        if debug:
            import matplotlib.pyplot as plt
            fig, axs = plt.subplots(3)
            fig.suptitle('preview (envelope/raw/wrapped)')
            axs[0].plot(e)
            axs[1].plot(y)
            axs[2].plot(ret)
            plt.show()
            plt.close()
        return ret


class LoopyNote():
    def __init__(self,
        key_name: str,
        note_value: float,
        pos_in_pattern: float,
        generator: LoopyPreset,
        attack: int,  # unit is ms
        decay: int,  # unit is ms
        sustain: float,  # between 0 and 1
        release: int,  # unit is ms
    ) -> None:
        self._key_name = key_name
        self._note_value = note_value
        self._pos_in_pattern = pos_in_pattern
        self._generator = generator

        self._attack = attack
        self._decay = decay
        self._sustain = sustain
        self._release = release
    
    def render(self,
        bpm: int,
        sig: str = '4/4',
    ):
        return self._generator.render(
            key_name=self._key_name,
            attack=self._attack,
            decay=self._decay,
            sustain=self._sustain,
            release=self._release,
            note_value=self._note_value,
            bpm=bpm, sig=sig,
        )
