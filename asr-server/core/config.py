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

# wave config
WAVE_RATE: int = 16000
WAVE_BIT: int = 16

# training params
EPOCHS: int = 50
BATCH_SIZE: int = 32
VALIDATION_SPLIT: float = 0.1
OPTIMIZER: str = 'adam'
LOSS: str = 'sparse_categorical_crossentropy'
METRICS: list = ['accuracy']

# classes
CLASSES = ('1', '2', '3', '4', '5', '6', '7', '8', '9')
