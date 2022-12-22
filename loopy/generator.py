import librosa
import soundfile as sf
from playsound import playsound
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

class LoopyPreset():
    def __init__(self,
        source_path: str,
        target_sr: int = 44100,
        name: str = None,
        load_bpm: int = 64,
    ) -> None:
        y, _ = librosa.load(source_path, sr=target_sr, mono=False)
        self._y = np.transpose(y, axes=(1, 0))
        self._sr = target_sr
        
        self._name = source_path if name is None else name
        self._load_bpm = load_bpm

        self.parse()

    def parse(self):
        for i in range(88):
            st = int(i*60*self._sr/self._load_bpm)
            ed = int((i+1)*60*self._sr/self._load_bpm)
            print(st, ed)
            # sf.write(f'{i+1}.wav', y[st:ed], sr)