# data path
DATA_ROOT_PATH: str = './data'
TEACHER_ROOT_PATH: str = DATA_ROOT_PATH + '/teacher'
TEACHER_X_PATH: str = TEACHER_ROOT_PATH + '/x.npy'
TEACHER_Y_PATH: str = TEACHER_ROOT_PATH + '/y.npy'
RECORD_ROOT_PATH: str = DATA_ROOT_PATH + '/record'
SPEECH_ROOT_PATH: str = RECORD_ROOT_PATH + '/speech'
NOISE_ROOT_PATH: str = RECORD_ROOT_PATH + '/noise'
MODEL_ROOT_PATH: str = './ckpt'
MODEL_PATH: str = MODEL_ROOT_PATH + '/final.h5'
RECORD_WAV_PATH: str = DATA_ROOT_PATH + '/record.wav'
UPLOAD_WAV_PATH: str = DATA_ROOT_PATH + '/upload.wav'

# wave config
WAVE_RATE: int = 16000
WAVE_BIT: int = 16
WAVE_CHANNELS: int = 1
WAVE_CHUNK: int = 1024
WAVE_DEFECT_SEC: float = 0.4
WAVE_AMP_SAMPLES: int = 6
MFCC_DIM: int = 12
MFCC_SAMPLES: int = 64
FFT_LENGTH: int = 512
MIN_SILENCE_LENGTH: int = 100
SILENCE_THRESH: int = -20
KEEP_SILENCE: int = 100
INPUT_SHAPE: tuple = (MFCC_DIM, MFCC_SAMPLES, 1)

# training params
EPOCHS: int = 20
BATCH_SIZE: int = 32
VALIDATION_SPLIT: float = 0.1
DROPOUT_RATE: float = 0.5
OPTIMIZER: str = 'adam'
LOSS: str = 'sparse_categorical_crossentropy'
METRICS: list = ['accuracy']

# classes
CLASSES: tuple = ('1', '2', '3', '4', '5', '6', '7', '8', '9')
N_CLASSES: int = len(CLASSES)

# api
API_SUCCESS_STATUS = 'OK'
API_ERROR_STATUS = 'NG'
API_SUCCESS_MSG = 'success'
API_RESPONSE: dict = {'status': API_SUCCESS_STATUS, 'message': API_SUCCESS_MSG}
API_PORT: int = 3033
