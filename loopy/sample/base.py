import librosa
import soundfile as sf
from playsound import playsound
import os

class LoopySample():
    def __init__(self,
        source_path: str,
        target_sr: int = None,
        name: str = None,
    ) -> None:
        y, orig_sr = librosa.load(source_path)
        # print('original sample rate:', orig_sr)
        if target_sr is None:
            target_sr = orig_sr
        self._y = librosa.resample(y, orig_sr=orig_sr, target_sr=target_sr)
        self._sr = target_sr
        
        if name is None:
            name = source_path

    def preview(self):
        tmp_addr = './tmp.wav'
        sf.write(tmp_addr, self._y, self._sr)
        playsound(tmp_addr)
        os.remove(tmp_addr)