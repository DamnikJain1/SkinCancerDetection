from django.shortcuts import render
from keras.models import Sequential
from keras.layers import Dense
from keras.models import model_from_json
import numpy as np
from PIL import Image

import os
# Create your views here.
from django.http import HttpResponse
from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView


def index(request):


    
    abs_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resnet50.json')
    h5_abs_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resnet50.h5')
    img_abs_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'benign1.jpg')

    json_file = open(abs_path, 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights(h5_abs_path)
    print("Loaded model from disk")
    read = lambda imname: np.asarray(Image.open(imname).convert("RGB"))
    ims_benign = [read(img_abs_path)]

    X_benign = np.array(ims_benign, dtype='uint8')
    X_benign=X_benign/255
 

    #print(X_benign)
    #print(loaded_model.predict_classes(X_benign))
    #print(loaded_model.predict_classes(X_malignant))
    print(loaded_model.predict(X_benign))
    return HttpResponse(loaded_model.predict(X_benign))
