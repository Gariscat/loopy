from loopy.utils import parse_sig, find_preset, preview_wave
from loopy.template import add_kick
from loopy import LoopyPatternCore, LoopyPreset, LoopyTrack
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import numpy as np
import os
import json
from typing import List

class LoopyRhythm():
    def __init__(self,
        name: str = '',
        num_bars: int = 4,
        sig: str = '4/4',
        resolution: float = 1/16,
    ) -> None:
        self._name = name
        self._num_bars = num_bars
        self._sig = sig
        self._beats_per_bar, self._beat_value = parse_sig(sig)
        self._resolution = resolution
    
        self._place_holders = []
        ### should contain pairs of (note_value, start_pos, end_pos)

    def preview(self, default_note='C5', default_preset='Ultrasonic-LD-Forever.wav'):
        temp_core = LoopyPatternCore(
            num_bars=self._num_bars,
            sig=self._sig,
            resolution=self._resolution
        )
        temp_gen = LoopyPreset(
            source_path=find_preset(default_preset),
            name='',
        )
        for place_holder in self._place_holders:
            temp_core.add_note(
                key_name=default_note,
                note_value=place_holder[0],
                pos_in_pattern=place_holder[1],
                generator=temp_gen,
            )

        temp_track = LoopyTrack(name='', length='00:7.5')
        temp_track.add_pattern(temp_core, 0, 0)
        add_kick(temp_track, num_bars=self._num_bars)
        preview_wave(temp_track.render())

    def __dict__(self):
        return {
            'name': self._name,
            'sig': self._sig,
            'num_bars': self._num_bars,
            'resolution': self._resolution,
            'place_holders': self._place_holders
        }

    def save(self, save_dir):
        with open(os.path.join(save_dir, f'rhythm-{self._name}.json'), 'w') as f:
            json.dump(self.__dict__(), f)

    def generate(self,
        seed: int = 0,
        note_values: List[int] = [i/16 for i in (2,3,4)],
        note_values_weight: List[int] = None,
        mode: str = 'poisson',
        param: dict = {'lambda': 1.0},
        debug: bool = False
    ):
        if mode != 'poisson':
            raise NotImplementedError('Distributions beside Poisson not implemented')
        
        np.random.seed(seed)

        st_pos, ed_pos = 0.0, 0.0
        total_beats = self._num_bars * self._beats_per_bar

        while ed_pos < total_beats:
            st_pos = ed_pos + np.random.poisson(param['lambda']) * self._resolution / self._beat_value
            note_value = np.random.choice(note_values, p=note_values_weight)
            ed_pos = st_pos + note_value / self._beat_value
            
            if ed_pos > total_beats:
                break
            
            self._place_holders.append((note_value, st_pos, ed_pos))

        if debug:
            print(self._place_holders)
            segments = [((st_pos, j), (ed_pos, j)) for j, (note_value, st_pos, ed_pos) in enumerate(self._place_holders)]
            fig, ax = plt.subplots()
            ax.add_collection(LineCollection(segments))
            ax.autoscale()

            for i in range(total_beats):
                plt.axvline(x=i, color='red', label='beat (kick)', ls=':')
            plt.savefig('./tmp.jpg')
            plt.show()
            plt.close()

            