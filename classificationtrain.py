from pathlib import Path
from fastai.vision.data import DataBlock, ImageBlock, CategoryBlock, MultiCategoryBlock
from fastai.vision.augment import RandomResizedCrop, aug_transforms
from fastai.vision.data import get_image_files, RandomSplitter, parent_label
import pandas as pd
from fastai.vision.learner import *
from fastai.vision.models import resnet18
from fastai.metrics import partial, accuracy_multi, error_rate
from fastai.callback import fp16
from fastai.callback.schedule import fine_tune
from fastai.learner import export

def trainAndExport(datasetPath, modelOutputName):
    clothes = DataBlock(
        blocks=(ImageBlock, CategoryBlock), 
        get_items=get_image_files, 
        splitter=RandomSplitter(valid_pct=0.2, seed=42),
        get_y=parent_label,
        item_tfms=RandomResizedCrop(460, min_scale=0.5),
        batch_tfms=aug_transforms(size=224, min_scale=0.7))
    
    dls = clothes.dataloaders(datasetPath)
    learn = cnn_learner(dls, resnet18, metrics=error_rate).to_fp16()
    learn.fine_tune(20)
    learner_name = "single_label_model_subset.pkl"
    learn.export(learner_name)
    return learn

# Turning it into a multilabel data block
def train():
    #from fastbook import *
    datasetPath = Path('apparel-dataset')
    modelOutputName = "multi_label_model_subset_10.pkl"
    learn = trainAndExport(datasetPath, modelOutputName)
    return learn