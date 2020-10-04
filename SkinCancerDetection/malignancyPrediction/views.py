from django.shortcuts import render
from keras.models import Sequential
from keras.layers import Dense
from keras.models import model_from_json
import numpy as np
from PIL import Image
from .models import Doctor
import os
# Create your views here.
from django.http import HttpResponse
from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage

# def index(request):
#     abs_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resnet50.json')
#     h5_abs_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resnet50.h5')
#     img_abs_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static/'+request.GET.get('fn'))

#     json_file = open(abs_path, 'r')
#     loaded_model_json = json_file.read()
#     json_file.close()
#     loaded_model = model_from_json(loaded_model_json)
#     # load weights into new model
#     loaded_model.load_weights(h5_abs_path)
#     print("Loaded model from disk")
#     read = lambda imname: np.asarray(Image.open(imname).convert("RGB"))
#     ims_benign = [read(img_abs_path)]

#     X_benign = np.array(ims_benign, dtype='uint8')
#     X_benign=X_benign/255

#     #print(X_benign)
#     #print(loaded_model.predict_classes(X_benign))
#     #print(loaded_model.predict_classes(X_malignant))
#     print(loaded_model.predict(X_benign))
#     res = loaded_model.predict(X_benign)
#     res = res[0]
#     http_response = {}
#     http_response['benign'] = float(str(format(float(res[0]), "f"))[:5])
#     http_response['malignant'] = float(str(format(float(res[1]), "f"))[:5])
#     print(http_response)
#     return JsonResponse(http_response)

from django.views.decorators.csrf import csrf_exempt
import numpy as np
import argparse
import cv2

def verify_skin(img_abs_path):
    image = cv2.imread(img_abs_path)

    lower = np.array([0, 30, 60], dtype="uint8")
    upper = np.array([20, 150, 255], dtype="uint8")
    converted = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    skinMask = cv2.inRange(converted, lower, upper)
    no_skin = cv2.countNonZero(skinMask)
    if no_skin > 5000:
        # print("Image no: ", k+1)
        #print("Skin pixel count ", no_skin)
        #print("Skin present\n\n")
        return True

    else:
        #print("Skin absent\n")
        return False




@csrf_exempt
def simple_upload(request):
    if request.method == 'POST' and request.FILES['myfile']:
        
        #File uploading
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save("malignancyPrediction/static/"+myfile.name, myfile)
        uploaded_file_url = "/static/"+myfile.name
        request.session['file_name'] = myfile.name

        #Prediction
        abs_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resnet50.json')
        h5_abs_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resnet50.h5')
        img_abs_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static/'+request.session['file_name'])
        ans = verify_skin(img_abs_path)
        request.session['verify_skin'] = ans
        print("Verify Skin: "+str(ans))
        if(ans==False):
            file1 = open("myfile.txt","w")
            file1.write("0,0,"+str(ans))
            return JsonResponse({"res":"Not a skin image"})
        else:
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
            res = loaded_model.predict(X_benign)
            res = res[0]
            b_val = str(format(float(res[0]), "f"))[:5]
            m_val = str(format(float(res[1]), "f"))[:5]
            http_response = {}
            http_response['benign'] = float(b_val)
            http_response['malignant'] = float(m_val)
            print(http_response)
            request.session['b_val'] = b_val
            request.session['m_val'] = m_val
            file1 = open("myfile.txt","w")
            file1.write(b_val+","+m_val+","+str(ans))
            file1.close()
            return JsonResponse(http_response)
            # return render(request, 'simple_upload.html', {
            #     'uploaded_file_url': uploaded_file_url,
            #     'result_url': '/detection/predict'
            # })
    return render(request, 'simple_upload.html')

@csrf_exempt
def get_result(request):
    if request.method=="GET":
        file1 = open("myfile.txt","r+")  
        con_val = file1.read().split(",")
        file1.close();
        b_val = float(con_val[0])
        m_val = float(con_val[1])
        ans = con_val[2]
        http_response = {}
        http_response['benign'] = float(b_val)
        http_response['malignant'] = float(m_val)
        http_response['verify_skin'] = ans;
        print('Get Result Response:')
        print(http_response)
        return JsonResponse(http_response)


@csrf_exempt
def just_upload(request):
    print('Request received')
    print('Method: '+request.method)
    if request.method == 'POST' and request.FILES['myfile']:
        
        #File uploading
        myfile = request.FILES['myfile']
        print(myfile)
        fs = FileSystemStorage()
        filename = fs.save("malignancyPrediction/static/"+myfile.name, myfile)
        uploaded_file_url = "/static/"+myfile.name
        request.session['file_name'] = myfile.name
        return render(request, 'simple_upload.html', {
            'uploaded_file_url': uploaded_file_url,
            'result_url': '/detection/predict'
        })

    return render(request, 'simple_upload.html')

@csrf_exempt
def locate_dermats(request):
    print('Request received')
    print('Method: '+request.method)
    if request.method == 'POST' and request.data['pincode']:
        user_pin = request.data['pincode']
        print(user_pin)
        doctors = Doctor.objects.filter(pincode=user_pin)
        http_response = {}
        http_response['doctors'] = doctors
        print('Get Result Response:')
        print(http_response)
        return JsonResponse(http_response)





