import numpy as np

from core import config


# band-pass filter
def filtering(feature: np.ndarray) -> np.ndarray:
    n_sample: int = len(feature)
    delte = (config.WAVE_RATE / 2) / n_sample
    bpf: np.ndarray = np.zeros(n_sample)

    for i in range(n_sample):
        freq: float = i * delte
        if freq > config.BPF_LOW_FREQ and freq < config.BPF_HIGH_FREQ:
            bpf[i] = 1

    return feature * bpf
