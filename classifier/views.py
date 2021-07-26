#Django Imports
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse 
from django.views.decorators.csrf import csrf_exempt
from django.utils.datastructures import MultiValueDictKeyError
from decimal import *

#Fast AI imports
import logging
import azure.functions as func
# import image
from PIL import Image
import io
import json
import pathlib
from pathlib import Path
import os, shutil
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

                # Clean Image Directory
                path = os.path.join(Path(pathlib.Path.cwd()),'media')
                for root, dirs, files in os.walk(path):
                    for f in files:
                        os.unlink(os.path.join(root, f))
                    for d in dirs:
                        shutil.rmtree(os.path.join(root, d))

                # Save the uplaoded image file 
                myfile = request.FILES['myfile']
                fs = FileSystemStorage()
                filename = fs.save(myfile.name, myfile)
                print('FILENAME: ',filename)
                uploaded_file_url = fs.url(filename)
                file_path = "media/" +filename

                # Call classify ML function 
                classify_output = classify(file_path)
                print(classify_output)

                # Pass output to context
                context['colour'] = classify_output["classification"].replace("_", " ")
                context['confidence'] = round(Decimal(classify_output["loss"].item() * 100), 1)
                context['image_url'] = uploaded_file_url

                return render(request, 'results.html', context)
            else:
                raise

        except MultiValueDictKeyError:
            context['error'] = 'No file uploaded'
            return render(request, 'upload.html', context)

        except:
            context['error'] = 'Opps, something happened! Please try again.'
            return render(request, 'upload.html', context)

    else:
        return render(request, 'upload.html')



@csrf_exempt
def result(request):
    return render(request, 'results.html')



def classify(image):
    path = Path(pathlib.Path.cwd())
    print(path)
    this_learner = learner.load_learner(path/'single_label_model_subset.pkl')
    output = this_learner.predict(path/image)
    print(output[0])
    print(output[2][output[1]])
    return {"classification": output[0], "loss":output[2][output[1]]}



