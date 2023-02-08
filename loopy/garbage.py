from scipy import signal
import audio_dspy as adsp
from typing import Any
import numpy as np
from loopy.utils import DEFAULT_SR

ORDER = 2

class LoopyEffect():
    def __init__(self) -> None:
        self._params = {}
    
    def add_param(self, k: str, v: Any):
        self._params[k] = v

    def __call__(self, y: np.ndarray, *args: Any, **kwds: Any) -> np.ndarray:
        return self.forward(y)

class LoopyPassFilter(LoopyEffect):
    # https://audio-dspy.readthedocs.io/en/latest/tutorials/eq_tutorial.html#basic-filter-design
    def __init__(self, type: str, freq: int) -> None:
        super().__init__()
        assert type in ('low', 'high')
        self.add_param('type', type)
        self.add_param('cutoff', freq)
        self.filter = adsp.Filter(ORDER, DEFAULT_SR)
        design_cls = adsp.design_HPF2 if type == 'high' else adsp.design_LPF2
        self.b, self.a = design_cls(freq, 0.7071, DEFAULT_SR)
        self.filter.set_coefs(self.b, self.a)

    def forward(self, y: np.ndarray):
        assert y.shape == (y.shape[0], 2)
        self.filter.reset()
        y_filted = np.zeros_like(y)
        y_filted[:, 0] = self.filter.process_block(y[:, 0])
        y_filted[:, 1] = self.filter.process_block(y[:, 1])
        return y_filted


