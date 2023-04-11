from typing import Any
import numpy as np
from loopy.utils import DEFAULT_SR, beat2index
from pedalboard import HighpassFilter, LowpassFilter, Reverb, Gain, Limiter, Compressor, Distortion
from math import ceil
import matplotlib.pylab as plt
from typing import Dict


class LoopyEffect():
    def __init__(self) -> None:
        self._params = {}
    
    def add_param(self, k: str, v: Any):
        self._params[k] = v

    def __call__(self, y: np.ndarray, *args: Any, **kwds: Any) -> np.ndarray:
        return self.forward(y, *args, **kwds)

    def __str__(self) -> str:
        return self._params

    def __dict__(self):
        return self.__str__()

    def reset(self):
        pass


class LoopyHighpass(LoopyEffect):
    def __init__(self, freq: int) -> None:
        super().__init__()
        self.add_param('name', 'highpass')
        self.add_param('cutoff', freq)
        self.filter = HighpassFilter(freq)

    def forward(self, y: np.ndarray):
        y_filted = self.filter.process(y, sample_rate=DEFAULT_SR, reset=True)
        return y_filted

    def reset(self):
        self.filter.reset()

class LoopyLowpass(LoopyEffect):
    def __init__(self, freq: int) -> None:
        super().__init__()
        self.add_param('name', 'lowpass')
        self.add_param('cutoff', freq)
        self.filter = LowpassFilter(freq)

    def forward(self, y: np.ndarray):
        y_filted = self.filter.process(y, sample_rate=DEFAULT_SR, reset=True)
        return y_filted

    def reset(self):
        self.filter.reset()

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
        self.add_param('name', 'reverb')
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

    def reset(self):
        self.reverb.reset()

class LoopySidechain(LoopyEffect):
    def __init__(self,
        length: float = 1.0,  # unit is beat
        attain: float = 0.125,  # unit is beat
        interp_order: float = 1,
        mag: float = 1,
    ) -> None:
        super().__init__()
        self.add_param('name', 'sidechain')
        self.add_param('length', length)
        self.add_param('attain', attain)
        self.add_param('interp_order', interp_order)
        self.add_param('mag', mag)

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
            plt.plot(y[:, 0], c='mediumblue', label='inst_mono')
            plt.legend()
            plt.show()
            plt.close()

            plt.plot(envelope, c='slateblue', label='envelope')
            plt.legend()
            plt.show()
            plt.close()
        
        return ret * self._params['mag'] + y * (1 - self._params['mag'])


class LoopyBalance(LoopyEffect):
    def __init__(self,
        db: float = 1.0  # unit is dB
    ) -> None:
        super().__init__()
        self.add_param('name', 'balance')
        self.add_param('db', db)
    
        self.gain = Gain(gain_db=self._params['db'])
    
    def forward(self, y: np.ndarray):
        return self.gain.process(y, sample_rate=DEFAULT_SR, reset=True)

    def reset(self):
        self.gain.reset()


class LoopyLimiter(LoopyEffect):
    def __init__(self,
        thres: float = 0.0  # unit is dB
    ) -> None:
        super().__init__()
        self.add_param('name', 'limiter')
        self.add_param('thres', thres)
    
        self.limiter = Limiter(threshold_db=self._params['thres'])
    
    def forward(self, y: np.ndarray):
        return self.limiter.process(y, sample_rate=DEFAULT_SR, reset=True)

    def reset(self):
        self.limiter.reset()


class LoopyCompressor(LoopyEffect):
    def __init__(self,
        thres: float = 0.0,  # unit is dB,
        ratio: float = 1.0,
        attack_ms: float = 1.0,
        release_ms: float = 100,
    ) -> None:
        super().__init__()
        self.add_param('name', 'limiter')
        self.add_param('thres', thres)
        self.add_param('ratio', ratio)
        self.add_param('attack', attack_ms)
        self.add_param('release', release_ms)
    
        self.compressor = Compressor(
            threshold_db=self._params['thres'],
            ratio=self._params['ratio'],
            attack_ms=self._params['attack'],
            release_ms=self._params['release']
        )
    
    def forward(self, y: np.ndarray):
        return self.compressor.process(y, sample_rate=DEFAULT_SR, reset=True)

    def reset(self):
        self.compressor.reset()


class LoopyDist(LoopyEffect):
    def __init__(self,
        drive: float = 25  # unit is dB
    ) -> None:
        super().__init__()
        self.add_param('name', 'distortion')
        self.add_param('drive', drive)
    
        self.dist = Distortion(drive_db=self._params['drive'])
    
    def forward(self, y: np.ndarray):
        return self.dist.process(y, sample_rate=DEFAULT_SR, reset=True)

    def reset(self):
        self.dist.reset()


def dict2fx(info: Dict) -> LoopyEffect:
    if info['type'] == 'highpass':
        return LoopyHighpass(info['freq'])
    elif info['type'] == 'lowpass':
        return LoopyLowpass(info['freq'])
    elif info['type'] == 'reverb':
        return LoopyReverb(
            room_size=info['room_size'] if info.get('room_size') else 0.5,
            damping=info['damping'] if info.get('damping') else 0.5,
            wet_level=info['wet_level'] if info.get('wet_level') else 0.33,
            dry_level=info['dry_level'] if info.get('dry_level') else 0.4,
            width=info['width'] if info.get('width') else 1.0,
        )
    elif info['type'] == 'sidechain':
        return LoopySidechain(
            length=info['length'] if info.get('length') else 1.0,  # unit is beat
            attain=info['attain'] if info.get('attain') else 0.125,  # unit is beat
            interp_order=info['interp_order'] if info.get('interp_order') else 1,
            mag=info['mag'] if info.get('mag') else 1,
        )
    elif info['type'] == 'balance':
        return LoopyBalance(info['gain'])
    elif info['type'] == 'limiter':
        return LoopyBalance(info['thres'])
    elif info['type'] == 'compressor':
        return LoopyCompressor(
            thres=info['thres'] if info.get('thres') else 0,  # unit is beat
            ratio=info['ratio'] if info.get('ratio') else 1,  # unit is beat
            attack_ms=info['attack'] if info.get('attack') else 1.0,
            release_ms=info['release'] if info.get('release') else 100,
        )
    elif info['type'] == 'distortion':
        return LoopyBalance(info['drive'])
    else:
        raise NotImplementedError("This effect is not implemented yet")
    