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

PRESET_DIR = '../presets'
LOAD_BPM = 64

def modify_preset_dir(target_dir: int):
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

    def preview(self, note_name: str = None):
        tmp_addr = 'tmp.wav'
        y = self._raw_notes[note_name] if note_name in self._raw_notes.keys() else self._y
        sf.write(tmp_addr, y, self._sr)
        try:
            playsound(tmp_addr)
        except:
            print('Could not play with PyThon... Please preview it in the folder.')
        # os.remove(tmp_addr)

    def render(self):
        pass

preset = LoopyPreset(os.path.join(PRESET_DIR, 'Ultrasonic-LD-Supersaw.wav'))
preset.preview('A5')