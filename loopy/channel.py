from loopy.effect import LoopyEffect
import numpy as np
from typing import List

class LoopyChannel():
    def __init__(self,
        # sr: int = 44100,
        name: str,
        effects: List[LoopyEffect] = None,
    ) -> None:
        # self._sr = sr
        self._name = name
        self._effects = effects if effects else list()  # list of LoopyEffect
        
    def add_effect(self, fx: LoopyEffect):
        self._effects.append(fx)

    def __call__(self, y: np.ndarray):
        for fx in self._effects:
            y = fx(y)
            fx.reset()
        return y
    
    def __len__(self):
        return len(self._effects)

    def __dict__(self):
        return {
            'name': self._name,
            'effects': [effect.__dict__() for effect in self._effects]
        }
    
    """def __str__(self):
        return str(self.__dict__())"""


def merge_channels(name: str, channels: List[LoopyChannel]):
    ret = LoopyChannel(name)
    for channel in channels:
        for fx in channel._effects:
            ret.add_effect(fx)
    return ret