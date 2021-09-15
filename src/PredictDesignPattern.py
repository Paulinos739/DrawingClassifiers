"""July 2021 for FID BAUdigital, ULB Darmstadt"""

'@author: Paul Steggemann (github @paulinos739)'
'Code originates from Forschungsmodul "DeepPattern" SoSe 20 at DDU, TU Darmstadt'
""

# Import Libraries
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import os
import re
import numpy as np
import pandas as pd

model_dir = 'TrainedModels/DesignPatternModels/'

def PatternPrediction(directory: str, filetype='json'):
    # Lists to store incoming data
    filenames = []
    labels = []
    columns = []
    predictions = []

    for filename in os.listdir(directory):
        filenames.append(filename)

    # Load each trained model in model_dir and call the predictions
    for classifier_file in os.listdir(model_dir):
        match = re.search('^classifier_(.+)_(\d+)_(.+)\.h5', classifier_file)
        if match:
            classifier_name = match.group(1)
            classifier_image_size = int(match.group(2))
            classifier_color_mode = match.group(3)
            classifier_input = []
            for filename in filenames:
                # stack up images to pass them for prediction
                img = image.load_img(os.path.join(directory, filename), target_size=(classifier_image_size, classifier_image_size, 1), color_mode=classifier_color_mode)
                img = image.img_to_array(img)
                img = np.expand_dims(img, axis=0)
                classifier_input.append(img)
            classifier_input = np.vstack(classifier_input)

            classifier = load_model(os.path.join(model_dir, classifier_file), compile=True)            
            result = classifier.predict(classifier_input)
            columns.append(classifier_name)
            predictions.append(result)

    # Concatenate the predictions and join filenames
    if len(predictions) > 0:
        labels = np.concatenate(predictions, axis=1)

    # Call DataFrame constructor with columns specified
    df = pd.DataFrame(labels, index=filenames, columns=columns)
    # Add row index name
    df.rename_axis('File', inplace=True)

    # Export to files
    if not filetype in ['csv', 'json']:
        print('unknown filetype requested:', filetype, '. resetting to json', flush=True)
        filetype = 'json'

    if filetype == 'csv':
        return df.to_csv(index=True)
    elif filetype == 'json':
        return df.to_json(orient='index')
