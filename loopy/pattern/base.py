from ..track import LoopyTrack


class LoopyPattern():
    def __init__(self,
        bpm: int = 128,
        name: str = None,
        sr: int = 22050,
        sig: str = '4/4',
        resolution: float = 1/16
    ) -> None:
        self._bpm = bpm
        self._name = name
        self._sr = sr
        self._beats_per_bar, n = [int(x) for x in sig.split('/')]
        self._beat = 1 / n  # 4/4 means 1 quarter note receives 1 beat
        
    def fit_track(self, track: LoopyTrack):
        ret = True
        ret &= (self._sr == track._sr)
        ret &= (self._beats_per_bar == track._beats_per_bar)
        ret &= (self._beat == track._beat)
        return ret