"""July 2021 for FID BAUdigital at TU Darmstadt"""

'@author: Paul Steggemann (github@ Paulinos739)'

'This program tests a pretrained Classification CNN model on architectural drawing types. '
'The trained classifier (hdf5) is located in a respective folder.'
""

# Import Libraries
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
import os
import pandas as pd


# load trained classifier
def DrawingCategoryClassifier():
    return load_model('TrainedModels/DrawingCategoryModels/classifier_multiclass_drawing_category.hdf5', compile=True)


def CategoryPrediction(directory: str, filetype='json'):
    # Lists to store incoming data
    images = []
    filenames = []

    # stack up images to pass them for prediction
    for filename in os.listdir(directory):
        img = image.load_img(os.path.join(directory, filename), target_size=(64, 64))
        img = image.img_to_array(img)
        img = np.expand_dims(img, axis=0)
        images.append(img)
        filenames.append(filename)

    images = np.vstack(images)

    # Then run inference
    predictions = DrawingCategoryClassifier().predict(images)

    # Create Pandas DataFrame with shape (10,5)
    df = pd.DataFrame(data=predictions, columns=['elevation', 'floor-plan', 'section'])
    df.insert(0, 'file', filenames)

    # Export to files
    if not filetype in ['csv', 'json']:
        print('unknown filetype requested:', filetype,'. resetting to json', flush=True)
        filetype = 'json'

    if filetype == 'csv':
        return df.to_csv(index=False)
    elif filetype == 'json':
        return df.to_json(orient='records')