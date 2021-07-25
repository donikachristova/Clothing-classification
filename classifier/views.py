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

                # Save the uplaoded image file 
                myfile = request.FILES['myfile']
                fs = FileSystemStorage()
                filename = fs.save(myfile.name, myfile)
                print('FILENAME: ',filename)
                uploaded_file_url = fs.url(filename)
                file_path = "media/" +filename

                # Call classify ML function 
                classify_output = classify(file_path, "multi_label_model_subset.pkl")[0]
                print(classify_output)

                # Pass output to context
                category_output = classify_output["category"].split('_')
                context['colour'] =category_output[0]
                context['type'] = category_output[1]
                context['image_url'] = uploaded_file_url
                context['confidence'] = classify_output["loss"]
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



def classify(image, modelPath):
    path = Path(os.getcwd())
    this_learner = learner.load_learner(path/modelPath)
    output = this_learner.predict(path/image)
    # return correct output
    categories = output[0]
    loss_values = output[2][output[1]]
    category_loss_dict = [{"category": categories[i], "loss": loss_values[i].item()} for i in range(len(categories))]
    return category_loss_dict



# def classify(image):
#     path = Path(pathlib.Path.cwd())
#     print(path)
#     this_learner = learner.load_learner(path/'export.pkl')
#     output = this_learner.predict(path/image)
#     print(output[0])
#     return {"classification": output[0]}