import numpy as np
from loopy.generator import LoopyPreset, LoopyNote, PRESET_DIR
from loopy.utils import parse_sig, beat2index, add_y, DEFAULT_SR, preview_wave
from loopy.channel import LoopyChannel
import os
from typing import List, Tuple
from math import ceil

class LoopyPatternCore():
    def __init__(self,
        num_bars: int,
        bpm: int = 128,
        name: str = None,
        sr: int = DEFAULT_SR,
        sig: str = '4/4',
        resolution: float = 1/16,
    ) -> None:
        """
        Defines the skeleton of a pattern.
        Args:
            num_bars (int): number of bars.
            bpm (int, optional): beats per minutes. Defaults to 128.
            name (str, optional): name (label). Defaults to None.
            sr (int, optional): sapmle rate. Defaults to 44100.
            sig (str, optional): signature. Defaults to '4/4'.
            resolution (float, optional): length of the shortest note. Defaults to 1/16.
        """
        self._bpm = bpm
        self._name = name
        self._sr = sr
        self._sig = sig
        self._beats_per_bar, self._beat_value = parse_sig(sig)
        self._generators = set()
        self._notes = []
        self._tot_samples = int(num_bars * self._beats_per_bar * 60 * sr / bpm)
        self._resolution = resolution

    def add_note(self,
        key_name: str,
        note_value: float,
        pos_in_pattern: float,  # unit is beat
        generator: LoopyPreset,
        attack: int = 0,  # unit is ms
        decay: int = 0,  # unit is ms
        sustain: float = 1.0,  # between 0 and 1
        release: int = 0,  # unit is ms
    ):
        note = LoopyNote(
            key_name=key_name,
            note_value=note_value,
            pos_in_pattern=pos_in_pattern,
            generator=generator,
            attack=attack,
            decay=decay,
            sustain=sustain,
            release=release,
        )
        self._notes.append(note)
        self._generators.add(generator)

    def add_notes(self,
        notes: List[Tuple[str, float, float]],
        generator: LoopyPreset,
        attack: int = 0,  # unit is ms
        decay: int = 0,  # unit is ms
        sustain: float = 1.0,  # between 0 and 1
        release: int = 0,  # unit is ms
    ):
        for key_name, note_value, pos_in_pattern in notes:
            self.add_note(
                key_name=key_name,
                note_value=note_value,
                pos_in_pattern=pos_in_pattern,
                generator=generator,
                attack=attack,
                decay=decay,
                sustain=sustain,
                release=release,
            )

    def render(self):
        self._y = np.zeros((self._tot_samples, 2))
        for note in self._notes:
            st_index = beat2index(note._pos_in_pattern, bpm=self._bpm, sr=self._sr)
            note_y = note.render(bpm=self._bpm, sig=self._sig)
            ### print(st_index, note_y.shape)
            add_y(self._y, note_y, st_index)

        return self._y
    
    
class LoopyPattern():
    def __init__(self,
        global_pos: int,
        core: LoopyPatternCore,
        channel: LoopyChannel = None,
        local_pos: float = 0,
    ) -> None:
        """
        Defines a specific pattern in the track.
        Args:
            global_pos (int): position in the track (measure id).
            core (LoopyPatternCore): the skeleton of this pattern.
            channel (LoopyChannel, optional): mixer channel takes in the pattern. Defaults to None.
            local_pos (float, optional): in-measure position (unit: beat). Defaults to 0.
        """
        self._global_pos = global_pos
        self._channel = channel
        self._core = core
        self._local_pos = local_pos
        
    def render(self):
        if self._channel is None:
            return self._core.render()
        else:
            return self._channel(self._core.render())


def preview_notes(
    key_name_list: List[str],
    preset_name: str = 'Ultrasonic-PD-Heart.wav',
    play_now: bool = True,
    as_chord: bool = False,
):
    ch = LoopyPreset(os.path.join(PRESET_DIR, preset_name))
    if as_chord:
        pattern_type = LoopyPatternCore(num_bars=1)
        for key_name in key_name_list:
            pattern_type.add_note(key_name, note_value=1/4, pos_in_pattern=0, generator=ch)
    else:
        pattern_type = LoopyPatternCore(bpm=100, num_bars=ceil(len(key_name_list)/2))
        for (i, key_name) in enumerate(key_name_list):
            pattern_type.add_note(key_name, note_value=1/2, pos_in_pattern=i/2, generator=ch)
    y = pattern_type.render()
    if play_now:
        preview_wave(y)
    return y