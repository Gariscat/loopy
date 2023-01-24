from loopy.effect import LoopyEffect
import numpy as np

class LoopyChannel():
    def __init__(self,
        channel_id,
        sr: int = 44100,
        name: str = None,
    ) -> None:
        self._channel_id = channel_id
        self._sr = sr
        self._name = name
        self._effects = []  # list of LoopyEffect
        
    def add_effect(self, fx: LoopyEffect):
        self._effects.append(fx)

    def __call__(self, y: np.ndarray):
        for fx in self._effects:
            y = fx(y)
        return y
