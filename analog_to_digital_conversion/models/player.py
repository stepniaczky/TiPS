import numpy as np
import soundcard as sc
from scipy.io.wavfile import read


class Player:
    def __init__(self, sampling):
        self.sampling = sampling
        self.audio = sc.default_speaker()
        self.channels = None

    def play_recorded(self, data: np.ndarray):
        self.audio.play(data, self.sampling, self.channels)

    def play_saved(self, filename: str):
        data = read(filename)
        sampling = data[0]
        data = np.float64(data[1] / np.max(abs(data[1])))
        channels = []
        for i in range(len(data[0])):
            channels.append(i)
        self.audio.play(data, sampling, channels)
