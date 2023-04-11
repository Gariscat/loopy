from loopy.utils import parse_sig, find_preset, preview_wave
from loopy.utils import piano_id2piano_key, piano_key2piano_id
from loopy.utils import get_chord_notes, octave_shift
from loopy.template import add_kick
from loopy import LoopyPatternCore, LoopyPreset, LoopyTrack
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
import numpy as np
import os
import json
from typing import List, Dict

class LoopyRhythm():
    def __init__(self,
        seed: int = 0,
        name: str = None,
        rep_bars: int = 1,
        sig: str = '4/4',
        resolution: float = 1/16,
    ) -> None:
        """A sequence of place holders as rhythm of an repetitive structures in patterns

        Args:
            seed (int, optional): random seed. Defaults to 0.
            name (str, optional): name of the rhythm. Defaults to None.
            rep_bars (int, optional): the longest number of bars during which the rhythm is repetitive. Defaults to 1.
            sig (str, optional): signature. Defaults to '4/4'.
            resolution (float, optional): length of the shortest note. Defaults to 1/16.
        """
        self._seed = seed
        self._name = name if name else str(seed)
        self._rep_bars = rep_bars
        self._sig = sig
        self._beats_per_bar, self._beat_value = parse_sig(sig)
        self._resolution = resolution
    
        self._place_holders = []
        ### should contain pairs of (note_value, start_pos, end_pos)

    def preview(self, default_preset='Ultrasonic-LD-Forever.wav', tot_bars: int = 8, place_holders: List = None):
        if place_holders is None:
            place_holders = self._place_holders
        if len(place_holders) == 0:
            raise FileExistsError("Please determine the rhythm by the place holders first")
        temp_track = LoopyTrack(name='', length=f'00:{1.875*tot_bars}')
        temp_gen = LoopyPreset(
            source_path=find_preset(default_preset),
            name='',
        )
        temp_core = LoopyPatternCore(
            num_bars=tot_bars,
            sig=self._sig,
            resolution=self._resolution
        )
        notes = self.trivial_melody_from_rhythm(place_holders)
        temp_core.add_notes(notes=notes, generator=temp_gen)
        temp_track.add_pattern(temp_core, 0, 0)

        add_kick(temp_track, num_bars=tot_bars)
        preview_wave(temp_track.render())

    def __dict__(self):
        return {
            'name': self._name,
            'sig': self._sig,
            'rep_bars': self._rep_bars,
            'resolution': self._resolution,
            'place_holders': self._place_holders
        }

    def save(self, save_dir):
        with open(os.path.join(save_dir, f'rhythm-{self._name}.json'), 'w') as f:
            json.dump(self.__dict__(), f)

    def generate_rhythm(self,
        note_values: List[int] = [i/16 for i in (2,3,4)],
        note_values_weight: List[int] = None,
        mode: str = 'poisson',
        param: dict = {'lambda': 1.0},
        debug: bool = False
    ):
        if mode != 'poisson':
            raise NotImplementedError('Distributions beside Poisson not implemented')
        
        np.random.seed(self._seed)

        st_pos, ed_pos = 0.0, 0.0
        rep_beats = self._rep_bars * self._beats_per_bar

        while ed_pos < rep_beats:
            st_pos = ed_pos + np.random.poisson(param['lambda']) * self._resolution / self._beat_value
            note_value = np.random.choice(note_values, p=note_values_weight)
            ed_pos = st_pos + note_value / self._beat_value
            
            if ed_pos > rep_beats:
                break
            
            self._place_holders.append((note_value, st_pos, ed_pos))

        if debug:
            print(self._place_holders)
            segments = [((st_pos, j), (ed_pos, j)) for j, (note_value, st_pos, ed_pos) in enumerate(self._place_holders)]
            fig, ax = plt.subplots()
            ax.add_collection(LineCollection(segments))
            ax.autoscale()

            for i in range(rep_beats):
                plt.axvline(x=i, color='red', label='beat (kick)', ls=':')
            plt.savefig('./tmp.jpg')
            plt.show()
            plt.close()

    def repeat(self, tot_bars: int):
        """repeat the generated rhythm


        Args:
            tot_bars (int): total number of bars that contain this repetitive rhythm
        Returns:
            List: place holders
        """
        place_holders = []
        for i in range(tot_bars//self._rep_bars):
            delta = i * self._rep_bars * self._beats_per_bar
            for note_value, st_pos, ed_pos in self._place_holders:
                place_holders.append((note_value, st_pos+delta, ed_pos+delta))
        return place_holders
                
            
    def trivial_melody_from_rhythm(self,
        place_holders: List = None,
        seed: int = None,
        scale_root: str = 'C',
        scale_type: str = 'maj',
        root_area: str = '5',
    ):
        root_id = piano_key2piano_id(scale_root+root_area)
        if scale_type == 'maj':
            note_ids = [root_id+i for i in (0, 2, 4, 5, 7, 9, 11)]
        else:
            note_ids = [root_id+i for i in (0, 2, 3, 5, 7, 8, 10)]

        note_keys = [piano_id2piano_key(x) for x in note_ids]
        
        if seed is not None:
            np.random.seed(seed)
        if place_holders is None:
            place_holders = self._place_holders

        return [(np.random.choice(note_keys), place_holder[0], place_holder[1]) for place_holder in place_holders]
    

def trivial_accomp(
    sig: str = '4/4',
    place_holders: List = [],
    chord_prog: List[List] = None,
    scale_root: str = 'C',
    scale_type: str = 'maj',
    root_area: str = '4',  # C3, D3, E3......
    del_second: bool = False,
    decr_octave: bool = True,
    incr_octave: bool = False,
    decor_map: Dict[int, List[int]] = dict(),
    # [chord_id, start_global_pos, end_global_pos] 
):
    # return 3 lists of notes, for chord, bass and subbass
    beats_per_bar, beat_value = parse_sig(sig)
    if place_holders == []: # uniform-rhythm chords
        tot_bars = max(int(_[2]) for _ in chord_prog)
        for i in np.arange(0, tot_bars * beats_per_bar, 1/4):
            place_holders += [(1/4, i, i+1/4)]

    score, roots, sub_roots = [], [], []
    i, j = 0, 0
    while i < len(place_holders):
        note_value, st_pos, ed_pos = place_holders[i]
        while chord_prog[j][2] * beats_per_bar < ed_pos and j < len(chord_prog):
            j += 1
        chord_id = chord_prog[j][0]
        decor_notes = decor_map[chord_id] if chord_id in decor_map.keys() else []
        key_names = get_chord_notes(
            chord_id=chord_id,
            scale_root=scale_root,
            scale_type=scale_type,
            root_area=root_area,
            del_second=del_second,
            decr_octave=decr_octave,
            incr_octave=incr_octave,
            decor_notes=decor_notes,
        )
        for key_name in key_names:
            score += [(key_name, note_value, st_pos)]
        roots += [(key_names[0], note_value, st_pos)]
        sub_roots += [(key_names[0], note_value, st_pos)]

        i += 1

    return score, roots, sub_roots