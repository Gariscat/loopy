from loopy.utils import hhmmss2sec, parse_sig, DEFAULT_SR, pos2index, add_y
from loopy.channel import LoopyChannel
from loopy.pattern import LoopyPatternCore, LoopyPattern
from loopy.sample import LoopySampleCore, LoopySample
import numpy as np
from math import ceil

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
        self._sig = sig
        self._beats_per_bar, self._beat_value = parse_sig(sig)
        self._tot_samples = int(ceil(hhmmss2sec(length) * sr))
        
        self._pattern_types = set()  # set of LoopyPatternCore
        self._sample_types = set()  # set of LoopySampleCore
        self._patterns = []  # list of LoopyPattern
        self._samples = []  # list of LoopySample
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

    def fit_sample(self, sample_type: LoopySampleCore):
        """
        Checks whether this sample fits a track.
        Args:
            sample_type (LoopySampleCore): the target sample type
        Returns: bool
        """
        ret = True
        ret &= (self._sr == sample_type._sr)
        return ret

    def add_pattern(self, pattern_type: LoopyPatternCore, global_pos: int, local_pos: float, channel: LoopyChannel = None):
        if not self.fit_pattern(pattern_type):
            raise TypeError('could not add this pattern...')
        self._pattern_types.add(pattern_type)
        
        pattern = LoopyPattern(
            global_pos=global_pos,
            core=pattern_type,
            channel=channel,
            local_pos=local_pos
        )

        self._patterns.append(pattern)
    
    def add_sample(self, sample_type: LoopySampleCore, global_pos: int, local_pos: float, channel: LoopyChannel = None):
        if not self.fit_sample(sample_type):
            raise TypeError('could not add this sample...')

        self._sample_types.add(sample_type)

        sample = LoopySample(
            global_pos=global_pos,
            core=sample_type,
            channel=channel,
            local_pos=local_pos
        )

        self._samples.append(sample)
        
    def render(self):
        self._y = np.zeros((self._tot_samples, 2))
        
        for pattern in self._patterns:
            st_index = pos2index(
                global_pos=pattern._global_pos,
                local_pos=pattern._local_pos,
                sr=self._sr,
                sig=self._sig,
                bpm=self._bpm
            )
            add_y(
                target_y=self._y,
                source_y=pattern.render(),
                st_index=st_index
            )

        for sample in self._samples:
            st_index = pos2index(
                global_pos=sample._global_pos,
                local_pos=sample._local_pos,
                sr=self._sr,
                sig=self._sig,
                bpm=self._bpm,
            )
            add_y(
                target_y=self._y,
                source_y=sample.render(),
                st_index=st_index
            )
        
        return self._y

    def add_channel(self, channel: LoopyChannel):
        self._channels.append(channel)