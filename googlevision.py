import os
from google.cloud import vision

def detect_labels_uri(PATH):
    """Detects labels in the file located in Google Cloud Storage or on the
    Web."""
    client = vision.ImageAnnotatorClient()
    image = vision.types.Image()

    image.source.image_uri = PATH

    response = client.label_detection(image=image)
    labels = response.label_annotations
    print('Labels:')

    for label in labels:
        print(label.description)
    
if __name__ == '__main__':

    PATH=os.getcwd()
    detect_labels_uri(PATH)
