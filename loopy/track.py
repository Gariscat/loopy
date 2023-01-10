from loopy.utils import hhmmss2sec, parse_sig, DEFAULT_SR
from loopy.channel import LoopyChannel
from loopy.pattern import LoopyPatternCore, LoopyPattern

class LoopyTrack():
    def __init__(self,
        name: str,
        bpm: int = 128,
        sr: int = DEFAULT_SR,
        sig: str = '4/4',
        length: str = '00:00',
    ) -> None:
        """
        Defines a track.
        Args:
            name (str): name of the track.
            bpm (int, optional): beats per minutes. Defaults to 128.
            sr (int, optional): sapmle rate. Defaults to 44100.
            sig (str, optional): signature. Defaults to '4/4'.
            length (str, optional): length in MM:SS. Defaults to "00:00".
        """
        self._name = name
        self._bpm = bpm
        self._sr = sr
        self._length = length
        self._beats_per_bar, self._beat_value = parse_sig(sig)
        self._tot_samples = hhmmss2sec(length) * sr
        
        self._pattern_types = []  # list of LoopyPatternCore
        self._patterns = []  # list of LoopyPattern
        self._channels = []  # list of LoopyChannel
    
    def fit_pattern(self, pattern_type: LoopyPatternCore):
        """
        Checks whether this pattern fits a track.
        Args:
            pattern_type (LoopyPatternCore): the target pattern type
        Returns: bool
        """
        ret = True
        ret &= (self._sr == pattern_type._sr)
        ret &= (self._beats_per_bar == pattern_type._beats_per_bar)
        ret &= (self._beat == pattern_type._beat)
        return ret