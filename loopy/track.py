from loopy.utils import hhmmss2sec, parse_sig, DEFAULT_SR, pos2index, add_y
from loopy.channel import LoopyChannel
from loopy.pattern import LoopyPatternCore, LoopyPattern
from loopy.sample import LoopySampleCore, LoopySample
from loopy.effect import LoopyBalance
import numpy as np
from math import ceil
import os
import soundfile as sf
import json
from typing import Dict
import matplotlib.pyplot as plt

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
            sr (int, optional): sample rate. Defaults to 44100.
            sig (str, optional): signature. Defaults to '4/4'.
            length (str, optional): length in MM:SS. Defaults to "00:00".
        """
        self._name = name
        self._bpm = bpm
        self._sr = sr
        self._length = length
        self._sig = sig
        self._beats_per_bar, self._beat_value = parse_sig(sig)
        self._tot_samples = int(hhmmss2sec(length) * sr)
        
        self._pattern_types = set()  # set of LoopyPatternCore
        self._sample_types = set()  # set of LoopySampleCore
        self._patterns = []  # list of LoopyPattern
        self._samples = []  # list of LoopySample
        self._channels = set()  # set of LoopyChannel
        self._generators = set()

        self._recipe = dict()
    
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
        ret &= (self._beat_value == pattern_type._beat_value)
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
        self._channels.add(channel)
        self._generators.update(pattern_type._generators)
    
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
        self._channels.add(channel)
        
    def render(self, gain: int = 6.0):
        y = np.zeros((self._tot_samples, 2))
        
        for pattern in self._patterns:
            st_index = pos2index(
                global_pos=pattern._global_pos,
                local_pos=pattern._local_pos,
                sr=self._sr,
                sig=self._sig,
                bpm=self._bpm
            )
            add_y(
                target_y=y,
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
                target_y=y,
                source_y=sample.render(),
                st_index=st_index
            )

        self._master_channel = LoopyChannel(
            name='master',
            effects=[LoopyBalance(gain)]
        )
        return self._master_channel(y)

    def add_channel(self, channel: LoopyChannel):
        self._channels.append(channel)

    def save_audio(self, save_name: str = None, target_dir: str = os.getcwd(), gain: int = 6.):
        target_path = os.path.join(target_dir, save_name+'.wav' if save_name else self._name+'.wav')
        sf.write(target_path, self.render(gain), self._sr)

    def save(self, save_dir):
        info = {
            'name': self._name,
            'bpm': self._bpm,
            'sr': self._sr,
            'length': self._length,
            'sig': self._sig,
            'generators': [generator.__dict__() for generator in self._generators],
            'patterns': [pattern.__dict__() for pattern in self._patterns],
            'samples': [sample.__dict__() for sample in self._samples],
            'channels': [channel.__dict__() for channel in self._channels],
            # 'recipe': self._recipe
        }
        # print(self._patterns[1].__dict__())
        with open(os.path.join(save_dir, f'track-{self._name}.json'), 'w') as f:
            json.dump(info, f)
    
    def save_recipe(self, sound_sheet: Dict, inst_channel_sheet: Dict):
        self._recipe['sound'] = sound_sheet
        self._recipe['channel'] = inst_channel_sheet