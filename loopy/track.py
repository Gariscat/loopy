import librosa


from utils import hhmmss2sec
from channel import LoopyChannel
from pattern import LoopyPatternCore, LoopyPattern

class LoopyTrack():
    def __init__(self,
        bpm: int = 128,
        sr: int = 44100,
        sig: str = '4/4',
        length: str = '00:00',
    ) -> None:
        self._bpm = bpm
        self._sr = sr
        self._length = length
        self._beats_per_bar, n = [int(x) for x in sig.split('/')]
        self._beat = 1 / n  # 4/4 means 1 quarter note receives 1 beat
        self._tot_samples = hhmmss2sec(length) * sr
        
        self._pattern_types = []  # list of LoopyPatternCore
        self._patterns = []  # list of LoopyPattern
        self._channels = []  # list of LoopyChannel
    
    def fit_pattern(self, pattern_type: LoopyPatternCore):
        """
        Checks whether this pattern fits a track.
        Args:
            track (LoopyTrack): the target track
        Returns: bool
        """
        ret = True
        ret &= (self._sr == pattern_type._sr)
        ret &= (self._beats_per_bar == pattern_type._beats_per_bar)
        ret &= (self._beat == pattern_type._beat)
        return ret