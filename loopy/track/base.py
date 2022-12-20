import librosa
from ..utils import hhmmss2sec

class LoopyTrack():
    def __init__(self,
        bpm: int = 128,
        sr: int = 22050,
        length: str = '00:00',
    ) -> None:
        self._bpm = bpm
        self._sr = sr
        self._length = length
        self._tot_samples = hhmmss2sec(length) * sr