import soundcard as sc
import numpy as np
from scipy.io.wavfile import write


class Recorder:
    def __init__(self, sampling, quantization):
        self.sampling = sampling
        self.quantization = quantization
        self.audio = sc.default_microphone()
        self.rec_audio = None

    def clear_recorded_audio(self):
        self.rec_audio = None

    def record(self, seconds: int):
        self.rec_audio = self.audio.record(int(seconds * self.sampling), self.sampling)

    def save(self, filename: str) -> str:
        data = self.rec_audio
        try:
            if self.quantization == 8:
                data = np.int8(data / np.max(abs(data)) * np.iinfo("int8").max)
            elif self.quantization == 16:
                data = np.int16(data / np.max(abs(data)) * np.iinfo("int16").max)
            else:
                data = np.int32(data / np.max(abs(data)) * np.iinfo("int32").max)
            write(filename, self.sampling, data)
            return "Recording has been saved successfully."
        except TypeError:
            return "There is no recorded audio to save."
