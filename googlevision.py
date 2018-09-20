#!/usr/bin/env python
import os
import io
from google.cloud import vision


    
def detect_label():

    client = vision.ImageAnnotatorClient()
    dir=path
    num=0
    for root,dirname,filenames in os.walk(dir):
        for filename in filenames:
            if os.path.splitext(filename)[1]=='.jpg':
                num = num +1

    i=0
    while (i<num):
        file_name = os.path.join(os.path.dirname(__file__),path+'/'+str(i)+'.jpg')
        with io.open(file_name, 'rb') as image_file:
            content = image_file.read()
        

        image = types.Image(content=content)
        response = client.label_detection(image=image)
        labels = response.label_annotations
        print('Labels:')
        for label in labels:
            print(label.description)
        i += 1
if __name__ == '__main__':

    path=os.getcwd()
    detect_label()


