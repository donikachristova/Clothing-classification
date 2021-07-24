#Django Imports
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse 
from django.views.decorators.csrf import csrf_exempt
from django.utils.datastructures import MultiValueDictKeyError

#Fast AI imports
import logging
import azure.functions as func
# import image
from PIL import Image
import io
import json
import pathlib
from pathlib import Path
import os
from fastai.vision import learner




def home(request):
    return render(request, 'home.html')


@csrf_exempt
def upload(request):
    context = {}
    context['error'] = ''
    if request.method == 'POST':
        try:
            if request.FILES['myfile']:
                print("File")
                myfile = request.FILES['myfile']
                print('RequestFile: ',myfile)
                fs = FileSystemStorage()
                print('FS: ',fs)
                filename = fs.save(myfile.name, myfile)
                print('FILENAME: ',filename)
                uploaded_file_url = fs.url(filename)
                print(uploaded_file_url)
                classify_output = classify(filename)
                print(classify_output)
                context['colour'] = classify_output["classification"]
                context['image_url'] = uploaded_file_url
                context['confidence'] = '95'
                return render(request, 'results.html', context)
            else:
                raise
        except MultiValueDictKeyError:
            context['error'] = 'No file uploaded'
            return render(request, 'upload.html', context)
        # except:
        #     context['error'] = 'Opps, something happened! Please try again.'
        #     return render(request, 'upload.html', context)
    else:
        return render(request, 'upload.html')



@csrf_exempt
def result(request):
    return render(request, 'results.html')



def classify(image):
    path = Path(pathlib.Path.cwd())
    print(path)
    this_learner = learner.load_learner(path/'export.pkl')
    output = this_learner.predict(path/media/image)
    print(output[0])
    return {"classification": output[0]}



