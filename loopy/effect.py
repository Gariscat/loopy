from typing import Any
import numpy as np
from loopy.utils import DEFAULT_SR
from pedalboard import HighpassFilter, LowpassFilter, Reverb

class LoopyEffect():
    def __init__(self) -> None:
        self._params = {}
    
    def add_param(self, k: str, v: Any):
        self._params[k] = v

    def __call__(self, y: np.ndarray, *args: Any, **kwds: Any) -> np.ndarray:
        return self.forward(y)

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