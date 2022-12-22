import librosa
import soundfile as sf
from playsound import playsound
import os
import numpy as np

class LoopySampleCore():
    def __init__(self,
        source_path: str,
        target_sr: int = 44100,
        name: str = None,
    ) -> None:
        y, _ = librosa.load(source_path, sr=target_sr, mono=False)
        self._y = np.transpose(y, axes=(1, 0))
        self._sr = target_sr
        
        self._name = source_path if name is None else name

    def preview(self):
        tmp_addr = './tmp.wav'
        sf.write(tmp_addr, self._y, self._sr)
        playsound(tmp_addr)
        os.remove(tmp_addr)