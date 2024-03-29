import librosa
import soundfile as sf
from playsound import playsound
import os
import numpy as np
from loopy.utils import sec2hhmmss, DEFAULT_SR, parse_sig, find_preset
from loopy.channel import LoopyChannel
from loopy.effect import LoopyBalance


SAMPLE_DIR = 'C:\\Program Files\\Image-Line\\FL Studio 21\\Data\\Patches\\Packs\\Old Packs'

"""def modify_sample_dir(target_dir: str):
    print(f'Cautious: the sample folder path has been changed from {SAMPLE_DIR} to {target_dir}')
    SAMPLE_DIR = target_dir"""

class LoopySampleCore():
    def __init__(self,
        source_path: str,
        bpm: int = 128,
        sr: int = DEFAULT_SR,
        sig: str = '4/4',
        name: str = None,
        truncate: int = None,
        balance_db: float = 0,
    ) -> None:
        """
        Defines the skeleton of a sample.
        Args:
            source_path (str): path to the file.
            bpm (int, optional): beats per minutes. Defaults to 128.
            sr (int, optional): sapmle rate. Defaults to 44100.
            sig (str, optional): signature. Defaults to '4/4'.
            name (str, optional): name of the sample. Defaults to None.
            truncate (int, optinal): use first n beats only. Defaults is None.
        """
        self._bpm = bpm
        self._sig = sig
        self._beats_per_bar, self._beat_value = parse_sig(sig)
        self._source_path = find_preset(source_path, SAMPLE_DIR)
        self._truncate = truncate
        self._balance_db = balance_db
        self._balance = LoopyBalance(balance_db)

        y, _ = librosa.load(self._source_path, sr=sr, mono=False)
        self._y = np.transpose(y, axes=(1, 0))

        if truncate is not None:
            lim = int(60 * sr * truncate / bpm)
            self._y = self._y[:lim, :]

        self._sr = sr
        self._length = sec2hhmmss(self._y.shape[0]/self._sr)
        
        self._name = source_path if name is None else name

    def render(self):
        return self._balance(self._y)
        # return self._y

    def __dict__(self):
        return {
            'bpm': self._bpm,
            'sr': self._sr,
            'sig': self._sig,
            'source_path': self._source_path,
            'name': self._name,
            'truncate': self._truncate,
        }

class LoopySample():
    def __init__(self,
        global_pos: int,
        core: LoopySampleCore,
        channel: LoopyChannel = None,
        local_pos: float = 0,
    ) -> None:
        """
        Defines a specific sample in the track.
        Args:
            global_pos (int): position in the track (measure id).
            core (LoopyPatternCore): the skeleton of this sample.
            channel (LoopyChannel, optional): mixer channel takes in the pattern. Defaults to None.
            local_pos (float, optional): in-measure position (unit: beat). Defaults to 0.
        """
        self._global_pos = global_pos
        self._channel = channel
        self._core = core
        self._local_pos = local_pos
        
    def render(self):
        if self._channel is None:
            return self._core.render()
        else:
            return self._channel(self._core.render())

    def __dict__(self):
        return {
            'global_pos': self._global_pos,
            'channel': self._channel.__dict__(),
            'core': self._core.__dict__(),
            'local_pos': self._local_pos,
        }