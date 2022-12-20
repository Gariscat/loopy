import librosa
from ..utils import hhmmss2sec


class LoopyTrack():
    def __init__(self,
        bpm: int = 128,
        sr: int = 22050,
        sig: str = '4/4',
        length: str = '00:00',
    ) -> None:
        self._bpm = bpm
        self._sr = sr
        self._length = length
        self._beats_per_bar, n = [int(x) for x in sig.split('/')]
        self._beat = 1 / n  # 4/4 means 1 quarter note receives 1 beat
        self._tot_samples = hhmmss2sec(length) * sr
        
    