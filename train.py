from pathlib import Path
from fastai.vision.data import DataBlock, ImageBlock, MultiCategoryBlock
from fastai.vision.augment import RandomResizedCrop, aug_transforms
import pandas as pd
from fastai.vision.learner import *
from fastai.vision.models import resnet18
from fastai.metrics import partial, accuracy_multi

def get_x(r): return Path('.')/r['filename']

def get_y(r): return r['label'].split(' ')

def trainAndExport(filename, modelOutputName):
    multilables = pd.read_csv(filename)
    dblock = DataBlock(blocks=(ImageBlock, MultiCategoryBlock), 
                   get_x = get_x, 
                   get_y = get_y, 
                  item_tfms=RandomResizedCrop(460, min_scale=0.5),
                   batch_tfms=aug_transforms(size=224, min_scale=0.7))
    dls = dblock.dataloaders(multilables)
    learn = cnn_learner(dls, resnet18, metrics=partial(accuracy_multi, thresh=0.2)).to_fp16()
    learn.fine_tune(20)
    learner_name = "multi_label_model_subset.pkl"
    learn.export(learner_name)

# Turning it into a multilabel data block
def train():
    #from fastbook import *
    filename = 'labels_subset_10.csv'
    modelOutputName = "multi_label_model_subset_10.pkl"
    trainAndExport(filename, modelOutputName)
