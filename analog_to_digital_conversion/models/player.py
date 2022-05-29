import numpy as np
import soundcard as sc
from scipy.io.wavfile import read


class Player:
    def __init__(self, sampling):
        self.sampling = sampling
        self.audio = sc.default_speaker()

    def play_recorded(self, data: np.ndarray) -> str:
        try:
            self.audio.play(data, self.sampling)
            return "Playing recorded audio."
        except TypeError:
            return "There is no recorded audio to play."

    def play_saved(self, filename: str) -> str:
        try:
            data = read(filename)
            sampling = data[0]
            data = np.float64(data[1] / np.max(abs(data[1])))
            channels = []
            for i in range(len(data[0])):
                channels.append(i)
            self.audio.play(data, sampling, channels)
            return "Playing saved audio."
        except FileNotFoundError:
            return "File with audio content does not exist."
