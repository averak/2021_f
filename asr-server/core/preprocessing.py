import numpy as np
from scipy import signal
import sklearn
import rwave

from core import config


# convert wave to MFCC
def extract_feature(file_name: str) -> np.ndarray:
    result: np.array = rwave.to_mfcc(
        file_name,
        config.WAVE_RATE,
        config.MFCC_DIM,
    )
    result = np.reshape(result, (*result.shape, 1))
    return result


# normalize to 0~1
def normalize(feature: np.ndarray) -> np.ndarray:
    result: np.ndarray = feature.flatten()
    result_shape: tuple = feature.shape

    result = sklearn.preprocessing.minmax_scale(result)
    result = np.reshape(result, result_shape)

    return result


# band-pass filter
def filtering(feature: np.ndarray) -> np.ndarray:
    # edge freq [Hz]
    low_edge = 100
    high_edge = 8000

    n_sample: int = len(feature)
    delte = (config.WAVE_RATE / 2) / n_sample
    bpf: np.ndarray = np.zeros(n_sample)

    for i in range(n_sample):
        freq: float = i * delte
        if freq > low_edge and freq < high_edge:
            bpf[i] = 1

    return feature * bpf


# resample feature
def resample(feature: np.ndarray) -> np.ndarray:
    result: np.ndarray = signal.resample(
        feature.T,
        config.MFCC_SAMPLES,
        axis=1,
    )
    result = result.T
    return result
