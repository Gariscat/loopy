import numpy as np
from loopy.generator import LoopyPreset, LoopyNote
from loopy.utils import parse_sig, beat2index, add_y

class LoopyPatternCore():
    def __init__(self,
        num_bars: int,
        bpm: int = 128,
        name: str = None,
        sr: int = 44100,
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

    def render(self):
        self._y = np.zeros((self._tot_samples, 2))
        for note in self._notes:
            st_index = beat2index(note._pos_in_pattern, bpm=self._bpm, sr=self._sr)
            note_y = note.render(bpm=self._bpm, sig=self._sig)
            add_y(self._y, note_y, st_index)
        # TODO
        return self._y
    
    
class LoopyPattern():
    def __init__(self,
        global_pos: int,
        channel_id: int,
        core: LoopyPatternCore,
    ) -> None:
        """
        Defines a specific pattern in the track.
        Args:
            global_pos (int): position in the track (measure id).
            channel_id (int): channel id that takes in the pattern.
            core (LoopyPatternCore): the skeleton of this pattern.
        """
        self._global_pos = global_pos
        self._channel_id = channel_id
        self._core = core
        
    def render(self):
        return self._core.render()
        