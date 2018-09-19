#!/usr/bin/env python
import os
import io
from google.cloud import vision


    
def detect_labels(path):
    """Detects labels in the file."""
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.types.Image(content=content)

    response = client.label_detection(image=image)
    labels = response.label_annotations
    print('Labels:')

    for label in labels:
        print(label.description)


if __name__ == '__main__':

    PATH=os.getcwd()
    detect_labels(PATH+"/01.jpg")
