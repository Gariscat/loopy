import numpy as np

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
        self._beats_per_bar, n = [int(x) for x in sig.split('/')]
        self._beat = 1 / n  # 4/4 means 1 quarter note receives 1 beat
        self._notes = []
        self._tot_samples = int(num_bars * self._beats_per_bar * 60 * sr / bpm)
        self._resolution = resolution
    
    def render(self):
        self._y = np.zeros((self._tot_samples, 2))
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
        