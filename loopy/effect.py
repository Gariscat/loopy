from typing import Any
import numpy as np
from loopy.utils import DEFAULT_SR, beat2index
from pedalboard import HighpassFilter, LowpassFilter, Reverb, Gain
from math import ceil
import matplotlib.pylab as plt


class LoopyEffect():
    def __init__(self) -> None:
        self._params = {}
    
    def add_param(self, k: str, v: Any):
        self._params[k] = v

    def __call__(self, y: np.ndarray, *args: Any, **kwds: Any) -> np.ndarray:
        return self.forward(y, *args, **kwds)

    def __str__(self) -> str:
        return self._params


class LoopyHighpass(LoopyEffect):
    def __init__(self, freq: int) -> None:
        super().__init__()
        self.add_param('cutoff', freq)
        self.filter = HighpassFilter(freq)

    def forward(self, y: np.ndarray):
        y_filted = self.filter.process(y, sample_rate=DEFAULT_SR, reset=True)
        return y_filted

class LoopyLowpass(LoopyEffect):
    def __init__(self, freq: int) -> None:
        super().__init__()
        self.add_param('cutoff', freq)
        self.filter = LowpassFilter(freq)

    def forward(self, y: np.ndarray):
        y_filted = self.filter.process(y, sample_rate=DEFAULT_SR, reset=True)
        return y_filted

class LoopyReverb(LoopyEffect):
    def __init__(self,
        room_size: float = 0.5,
        damping: float = 0.5,
        wet_level: float = 0.33,
        dry_level: float = 0.4,
        width: float = 1.0,
        freeze_mode: float = 0.0,
    ) -> None:
        super().__init__()
        self.add_param('room_size', room_size)
        self.add_param('damping', damping)
        self.add_param('wet_level', wet_level)
        self.add_param('dry_level', dry_level)
        self.add_param('width', width)
        self.add_param('freeze_mode', freeze_mode)

        self.reverb = Reverb(
            room_size=room_size,
            damping=damping,
            wet_level=wet_level,
            dry_level=dry_level,
            width=width,
            freeze_mode=freeze_mode,
        )

    def forward(self, y: np.ndarray):
        return self.reverb.process(y, sample_rate=DEFAULT_SR, reset=True)

class LoopySidechain(LoopyEffect):
    def __init__(self,
        length: float = 1.0,  # unit is beat
        attain: float = 0.125,  # unit is beat
        interp_order: float = 1,
    ) -> None:
        super().__init__()
        self.add_param('length', length)
        self.add_param('attain', attain)
        self.add_param('interp_order', interp_order)

    def forward(self,
        y: np.ndarray,
        bpm: int = 128,
        sr: int = DEFAULT_SR,
        debug: bool = False,
    ):
        # construct envelope (unit) for one cycle
        envelope_unit = np.ones(beat2index(self._params['length'], bpm, sr), dtype=float)
        attain_idx = beat2index(self._params['attain'], bpm, sr)
        for i in range(attain_idx):
            envelope_unit[i] = np.power(i/attain_idx, self._params['interp_order'])
        # repeat the envelope (unit) for the complete envelope
        num_repeat = ceil(y.shape[0]/envelope_unit.shape[0])
        envelope = np.concatenate([envelope_unit]*num_repeat)[:y.shape[0]]
        envelope = np.expand_dims(envelope, axis=-1)  # for element-wise product broadcast
        # apply the envelope
        ret = y * envelope

        if debug:
            plt.plot(y)
            plt.show()
            plt.close()

            plt.plot(envelope)
            plt.plot(ret)
            plt.show()
            plt.close()
        
        return ret


class LoopyBalance(LoopyEffect):
    def __init__(self,
        db: float = 1.0  # unit is dB
    ) -> None:
        super().__init__()
        self.add_param('db', db)
    
        self.gain = Gain(gain_db=self._params['db'])
    
    def forward(self, y: np.ndarray):
        return self.gain.process(y, sample_rate=DEFAULT_SR, reset=True)