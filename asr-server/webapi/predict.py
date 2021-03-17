from flask import Blueprint, request, jsonify, current_app
import copy
import numpy as np
import rwave

from core import config
from core import nnet
from core import preprocessing

bp: Blueprint = Blueprint('infer', __name__)

nnet_: nnet.NNet = nnet.NNet()


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower(
           ) in current_app.config['ALLOWED_EXTENSIONS']


@bp.route('/', methods=['GET', 'POST'])
def predict():
    result: dict = copy.copy(config.API_RESPONSE)
    status: int = 200

    wav_file_key: str = 'wavfile'
    # received wav file
    if wav_file_key in request.files:
        file = request.files[wav_file_key]
        file.save(config.UPLOAD_WAV_PATH)

    # not received wav file
    else:
        result['status'] = config.API_ERROR_STATUS
        result['message'] = 'wav file not sent'
        status = 400
        return jsonify(result), status

    # predict
    mfcc = rwave.to_mfcc(config.UPLOAD_WAV_PATH,
                         config.WAVE_RATE, config.MFCC_DIM)
    mfcc = preprocessing.resample(mfcc, config.MFCC_FRAMES)
    mfcc = np.reshape(mfcc, (*mfcc.shape, 1))
    pred_class = nnet_.predict(mfcc)
    result['class'] = config.CLASSES[pred_class]

    return jsonify(result), status
