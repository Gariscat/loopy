import librosa
import soundfile as sf
from playsound import playsound
import os
import numpy as np
from loopy.utils import sec2hhmmss, DEFAULT_SR
from loopy.channel import LoopyChannel


SAMPLE_DIR = 'C:\\Program Files\\Image-Line\\FL Studio 20\\Data\\Patches\\Packs'

"""def modify_sample_dir(target_dir: str):
    print(f'Cautious: the sample folder path has been changed from {SAMPLE_DIR} to {target_dir}')
    SAMPLE_DIR = target_dir"""

class LoopySampleCore():
    def __init__(self,
        source_path: str,
        sr: int = DEFAULT_SR,
        name: str = None,
    ) -> None:
        """
        Defines the skeleton of a sample.
        Args:
            source_path (str): path to the file.
            sr (int, optional): sapmle rate. Defaults to 44100.
            name (str, optional): name of the sample. Defaults to None.
        """
        y, _ = librosa.load(source_path, sr=sr, mono=False)
        self._y = np.transpose(y, axes=(1, 0))
        self._sr = sr
        self._length = sec2hhmmss(self._y.shape[0]/self._sr)
        
        self._name = source_path if name is None else name

    def render(self):
        return self._y

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

