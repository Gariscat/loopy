from loopy.utils import hhmmss2sec, parse_sig, DEFAULT_SR, pos2index, add_y, piano_key2midi_id, midi_id2piano_key, PIANO_KEYS
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
from matplotlib.collections import LineCollection
import librosa
from librosa import display
from PIL import Image, ImageOps

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
        
    def render(self, gain: int = 7.5):
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

    def save_json(self, save_dir):
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
        
    def get_mel(self, st_bar: int, ed_bar: int, save_dir: str, part: str):
        st_idx = st_bar * self._beats_per_bar * 60 * self._sr // self._bpm
        ed_idx = ed_bar * self._beats_per_bar * 60 * self._sr // self._bpm
        y = np.transpose(self.render()[st_idx:ed_idx])
        sr = self._sr
        if part == 'lead':
            import pedalboard
            high_pass = pedalboard.HighpassFilter(cutoff_frequency_hz=1000)
            y = high_pass.process(input_array=y, sample_rate=sr)
        ### print(y.shape)
        
        for i, part in enumerate(('left', 'right')):
            """mel_spec = librosa.feature.melspectrogram(y=y[i], sr=sr)
            mel_spec = librosa.power_to_db(mel_spec, ref=np.max)"""
            S = np.abs(librosa.stft(y[i], n_fft=4096))**2
            fig, ax = plt.subplots(nrows=1, sharex=True)
            img = librosa.display.specshow(librosa.amplitude_to_db(S, ref=np.max),
                               y_axis='log', x_axis='time', ax=ax)
            plt.axis('off')
            plt.savefig('tmp.jpg', dpi=600, bbox_inches='tight', pad_inches=0)
            ### plt.show()
            plt.close()
            
            tmp_img = Image.open('tmp.jpg')
            img = tmp_img.resize((512, 512))
            # img = ImageOps.flip(img)
            img.save(os.path.join(save_dir, self._name+f'_{part}.jpg'))
    
    def print_melody(self):
        notes = self._patterns[0]._core._notes
        # segments = [((st_pos, j), (ed_pos, j)) for j, (note_value, st_pos, ed_pos) in enumerate(self._place_holders)]
        segments = []
        for note in notes:
            if note._generator._name != 'main':
                continue
            st = note._pos_in_pattern
            ed = note._pos_in_pattern + note._note_value / self._beat_value
            h = piano_key2midi_id(note._key_name)
            segments += [((st, h), (ed, h))]
        fig, ax = plt.subplots()
        ax.add_collection(LineCollection(segments))
        ax.autoscale()
        m = ax.get_yticks().tolist()
        ax.set_yticks(m)
        m = [midi_id2piano_key(int(x)) for x in m]
        ax.set_yticklabels(m)
        plt.savefig(f'../data/{self._name}-melody.jpg')
        # plt.show()
        plt.close()