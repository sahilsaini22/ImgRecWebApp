from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from tensorflow import keras
import numpy as np
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


# Create your views here.


# from .forms import *
from .forms import ImageForm


def home_view(request):
    context = {}
    context['form'] = ImageForm()
    return render(request, "home.html", context)


def predict(request):
 #   template: "interact/upload.html"

    # if request.method == 'GET':
    #    return render(request, "predict/predict.html")

    if request.method == 'POST':

        image = request.FILES['file']
        print(image.name)

        if image.name.endswith('.jpg') or image.name.endswith('.jpeg') or image.name.endswith('.png'):

            print('hello1')

            context = {}
            context['file'] = ['file']

            f = request.FILES['file']
            file_name = "pic.jpeg"
            file_name_2 = default_storage.save(file_name, f)

            model = keras.models.load_model(
                'predict/Fruit_Rec.pickle')
            test_image = keras.preprocessing.image.load_img(
                file_name_2, target_size=(64, 64))
            test_image = keras.preprocessing.image.img_to_array(test_image)
            test_image = np.expand_dims(test_image, axis=0)
            result = model.predict(test_image)
            prediction = 'none'
            if result[0][0] == 1:
                prediction = 'apple'
            if result[0][1] == 1:
                prediction = 'broccoli'
            if result[0][2] == 1:
                prediction = 'grape'
            if result[0][3] == 1:
                prediction = 'lemon'
            if result[0][4] == 1:
                prediction = 'mango'
            if result[0][5] == 1:
                prediction = 'orange'
            if result[0][6] == 1:
                prediction = 'strawberry'
            print(prediction)
            context['name'] = prediction

            default_storage.delete(file_name_2)

        else:
            messages.error(request, 'Incorrect file format')

        return render(request, "predict/predict.html", context)
    else:
        return render(request, 'predict/predict.html')
