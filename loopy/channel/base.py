from ..track import LoopyTrack


class LoopyChannel():
    def __init__(self,
        channel_id,
        sr: int = 44100,
        name: str = None,
    ) -> None:
        self._channel_id = channel_id
        self._sr = sr
        self._name = name
        self._fx = []  # list of LoopyEffect
        
    