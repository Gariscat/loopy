import librosa
import soundfile as sf
from playsound import playsound
import os
import numpy as np
from loopy.utils import sec2hhmmss

class LoopySampleCore():
    def __init__(self,
        source_path: str,
        sr: int = 44100,
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
        self._length = sec2hhmmss(self._y/self._sr)
        
        self._name = source_path if name is None else name

    def preview(self):
        tmp_addr = 'tmp.wav'
        sf.write(tmp_addr, self._y, self._sr)
        try:
            playsound(tmp_addr)
        except:
            print('Could not play with PyThon... Please preview it in the folder.')
        # os.remove(tmp_addr)

    def render(self):
        return self._y

class LoopySample():
    def __init__(self,
        global_pos: int,
        channel_id: int,
        core: LoopySampleCore,
    ) -> None:
        """
        Defines a specific sample in the track.
        Args:
            global_pos (int): position in the track (measure id).
            channel_id (int): channel id that takes in the sample.
            core (LoopySampleCore): the skeleton of this sample.
        """
        self._global_pos = global_pos
        self._channel_id = channel_id
        self._core = core
        
    def render(self):
        return self._core.render()


