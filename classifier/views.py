#Django Imports
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse 
from django.views.decorators.csrf import csrf_exempt

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
    if request.method == 'POST' and request.FILES['myfile']:
        print("File")
        print(request.FILES)
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
        context['image'] = uploaded_file_url
        context['confidence'] = '95'
        return render(request, 'results.html', context)

    else:
        context['error'] = 'No file uploaded'
        return render(request, 'upload.html', context)
    # return render(request, 'upload.html')




@csrf_exempt
def result(request):
    return render(request, 'results.html')
    # file = request.POST
    # if file != '':
    #     print(file)
    #     context["output"] = 'black'
    #     context['image'] = request.POST
    #     # classify_output = classify(file)
    #     # context["output"] = classify["classification"]
    # else:
    #     context["output"]= "Something went wrong"
    # return render(request, 'results.html', context)
    # HttpResponse(json.dumps(context), content_type ="application/json")



def classify(image):
    path = Path(pathlib.Path.cwd()).resolve()
    print(path)
    this_learner = learner.load_learner(path/'export.pkl')
    output = this_learner.predict(image)
    print(output[0])
    return {"classification": output[0]}



