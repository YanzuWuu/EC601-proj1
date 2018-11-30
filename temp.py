#!/usr/bin/env python
# encoding: utf-8
import tweepy
import os
import wget
import subprocess
import io
from google.cloud import vision
from PIL import ImageDraw, Image, ImageFont
from PIL import Image

from all import client

def get_all_tweets(screen_name):
        
        #Twitter only allows access to a users most recent 3240 tweets with this method
        consumer_key = ''
        consumer_secret = ''
        access_token = ''
        access_secret = ''
        #authorize twitter, initialize tweepy
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_secret)
        api = tweepy.API(auth)
        
        #initialize a list to hold all the tweepy Tweets

        #make initial request for most recent tweets (200 is the maximum allowed count)
        Twitter_Page = api.user_timeline(screen_name, count=100)
        Twitter_with_image=set()
        print('Downloading the Image from '+ screen_name)
        print('Processing.....')
        for status in Twitter_Page:
            media = status.entities.get('media', [])
            if (len(media) > 0):
                Twitter_with_image.add(media[0]['media_url'])
        i=0
        for url in Twitter_with_image:
            image=wget.download(url)
            os.rename(image, str(i) + '.jpg')
            i += 1
    


def rename(PATH):
    filelist = os.listdir(PATH)
    total_num = len(filelist)
    m = 0
    for item in filelist:

        if item.endswith('.jpg'):
            m=m+1
    print ('total %d to rename & converted %d jpgs' % (total_num, m))
    return m

def conv_image():
     print('Converting the images to video....Processing')
     subprocess.call(['ffmpeg', '-r', '1', '-i', '%01d.jpg', '-vcodec', 'mpeg4','-y','movie.mp4'])
client = vision.ImageAnnotatorClient()


def get_label(m):
    print('giving the labels')
    for i in range(m):
        file_name = os.path.join(os.path.dirname(__file__), '%s.jpg'%(i))
        with io.open(file_name, 'rb') as image_file:
            content = image_file.read()

            image = vision.types.Image(content=content)

            response = client.label_detection(image=image)
            labels = response.label_annotations
        j = 0
        for label in labels:
                # print(label.description)
                raw_image = Image.open(file_name)
                draw = ImageDraw.Draw(raw_image)
                font = ImageFont.truetype('/Library/Fonts/Times New Roman.ttf', 36)
                draw.text((50, 40 + j), label.description, fill=(0,0,0), font=font)
                j += 30
                raw_image.save(file_name)



if __name__ == '__main__':
    #pass in the username of the account you want to download
    get_all_tweets("hulu")
#    __init__(self)
    PATH=os.getcwd()
#    self.path = '/home/ece-student/601Task1/newtask1/'
    rename(PATH)
    m=rename(PATH)
    get_label(m)
    conv_image()
