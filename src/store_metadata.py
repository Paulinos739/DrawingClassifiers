"""June 2021 for FID BAUdigital, ULB Darmstadt"""

'@author: Paul Steggemann'
'This program predicts architectural categories in floor plan images through DNN models '
'and stores the labels (Metadata) in a json string'

""

# Keras Preprocessing and other Libraries
from keras.models import load_model
from keras.preprocessing import image

from typing import List, Iterable
import numpy as np
import os
import json

# List to put in the label predictions, 2D Numpy array with 0 and 1 int!
label_list_Numpy_2D = []

# img data directory
folder_path = 'path to image folder'

# put all images into a list
images = []
for img in os.listdir(folder_path):
        img = os.path.join(folder_path, img)
        img = image.load_img(img, target_size=(64, 64, 3))
        img = image.img_to_array(img)
        img = np.expand_dims(img, axis=0)
        images.append(img)

# Stack up images to pass for predction
images = np.vstack(images)

# join img-names with its np.arrays. Not finished yet!
filenames_list = os.listdir(folder_path)
print(filenames_list)


model_map = {
    "Rechteck": 'trained_classifiers_weights\\Recheck_100_trained_CNN.h5',
    "L": 'trained_classifiers_weights\\L_100_trained_CNN.h5',
    "linear": 'trained_classifiers_weights\\linear_100_trained_CNN.h5',
    "Kreis": 'trained_classifiers_weights\\Circle_100_trained_CNN.h5',
    "Polygon": 'trained_classifiers_weights\\Polygon_200_trained_CNN.h5',
    "organisch": 'trained_classifiers_weights\\organisch_100_trained_CNN.h5',
    "Hof": 'trained_classifiers_weights\\Hof_200_trained_CNN.h5',
}


# make predictions with all models on the image data
def classify_by_model(model_path: str, image_array_list: List[np.array]):
    model = load_model(model_path, compile=True)
    result = model.predict(image_array_list)
    label_list_Numpy_2D.append(result)

    return result


VECTOR_LABEL_LIST = ["Rechteck", "Komposit", "Longitudinal", "Kreis", "Polygonal", "Organisch", "Atrium",
                     "Stuetzenraster", "Treppe"]


def convert_to_semantic(feature_vector: Iterable[int]) -> List[str]:
    # List to parse the predictions from the classifiers
    labels_to_add = []
    for i, val in enumerate(feature_vector):
        if val:
            labels_to_add.append(VECTOR_LABEL_LIST[i])
    return labels_to_add


# Then set up the main program to predict and save to json
def Metadata_Generator():
    with open('labels_floor_plans.json', 'w') as outfile:
        # Call the predictions
        for model_name, model_path in model_map.items():
            r = classify_by_model(model_path, images)
            print(r)

        # Convert a 2D Numpy Array to a Python list to be able parse it
        label_list = np.array(label_list_Numpy_2D).tolist()

        # Convert the binary values to its semantic meaning
        labels_to_add = convert_to_semantic(label_list)
        result = labels_to_add

        # Save the predicted features to json str (date: 17.06.21)
        json.dump(result, outfile, ensure_ascii=False)


if __name__ == '__main__':
    Metadata_Generator()
