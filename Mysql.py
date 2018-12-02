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
from time import time,localtime,asctime
import numpy as np
import pymongo
from collections import Counter

from bson.objectid import ObjectId


os.environ['GOOGLE_APPLICATION_CREDENTIALS']= "mini-project-3-224202-35e30ab59ec6.json"

def input_ID():
    screen_name = input("Type the new Twitter ID:")
    return screen_name



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

        #screen_name = input_ID()

        #make initial request for most recent tweets (200 is the maximum allowed count)
        Twitter_Page = api.user_timeline(screen_name, count=20)
        Twitter_with_image=set()
        print('Downloading the Image from '+ screen_name + '.....')
        for status in Twitter_Page:
            media = status.entities.get('media', [])
            if (len(media) > 0):
                Twitter_with_image.add(media[0]['media_url'])
        i=0
        for url in Twitter_with_image:
            image=wget.download(url)
            os.rename(image, str(i) + '.jpg')
            i += 1

        print ('total 20 twitters & renamed %d jpgs' % (i))

        return i

# def rename(PATH):
#     filelist = os.listdir(PATH)
#     # total_num = len(filelist)
#     m = 0
#     for item in filelist:
#
#         if item.endswith('.jpg'):
#             m=m+1
#     print ('total 20 twitters & renamed %d jpgs' % (m))
#     return m

def conv_image():
     print('Converting the images to video....Processing')
     subprocess.call(['ffmpeg', '-r', '1', '-i', '%01d.jpg', '-vcodec', 'mpeg4','-y','video.mp4'])

client = vision.ImageAnnotatorClient()

def get_label(twitterID,m):

    clientt = pymongo.MongoClient('127.0.0.1',27017)
    db = clientt.MyDbs
    my_set = db.images

    print('giving the labels')
    print('It will take some seconds...')

    for i in range(m):
        file_name = os.path.join(os.path.dirname(__file__), '%s.jpg'%(i))
        with io.open(file_name, 'rb') as image_file:
            content = image_file.read()

            image = vision.types.Image(content=content)

            response = client.label_detection(image=image)

            labels = response.label_annotations
        j = 0
        string=''
        for label in labels:
            string= string + label.description + ','

            #print(label.description)
            raw_image = Image.open(file_name)
            draw = ImageDraw.Draw(raw_image)
            font = ImageFont.truetype('/Library/Fonts/Times New Roman.ttf', 36)
            draw.text((50, 40 + j), label.description, fill=(0,0,0), font=font)
            j += 30
            raw_image.save(file_name)
        my_set.insert({"Twitter ID":twitterID,"Total image":m,"#":i,"Labels":string,"Time":asctime(localtime(time()))})


    #return labels


def user_interface():

    while(True):
        print("\n#############  Menu:  ############\n#     1.Show the database        #\n#     2.Add new TwitterID        #\n#     3.Delete a user            #\n#     4.Search keyword           #\n"
      "#     5.The most popular labels  #\n#     6.Delete the database      #\n#     7.Exit                     #\n##################################")
        x = 0
        while x is 0:
            try:
                x = int(input("Select an number: "))
                if 0 < x < 8:
                    continue
                else:
                    print("The number is out of range. Try again")
                    x = 0
            except ValueError:
                print("Please input number. Try again ")

        if ( x == 1):
            all_data()

        elif ( x == 2):
            twitterID=input_ID()
            #PATH=os.getcwd()
            m=get_all_tweets(twitterID)
            get_label(twitterID,m)

        elif ( x == 3):
            delete_user()

        elif ( x == 4):
            search_keyword()

        elif ( x == 5):
            popular()

        elif ( x == 6):
            delete_database()

        elif ( x== 7):
            return

def all_data():
    clientt = pymongo.MongoClient('127.0.0.1',27017)
    db = clientt.MyDbs
    #print(db.images.find().pretty())
    cur=db.images.find()
    for doc in cur:
        print(doc)

def delete_user():

    clientt = pymongo.MongoClient('127.0.0.1',27017)
    db = clientt.MyDbs
    my_set = db.images

    delete_name = input("Delete the Twitter ID:")
    my_set.delete_many({ "Twitter ID" : delete_name })

def delete_database():

    clientt = pymongo.MongoClient('127.0.0.1',27017)
    db = clientt.MyDbs
    db.command("dropDatabase")

def search_keyword():

    clientt = pymongo.MongoClient('127.0.0.1',27017)
    db = clientt.MyDbs
    my_set = db.images
    twitterIDs=[]
    word=input("Type the keyword u want to search: ")
    for twitterID in my_set.find():
        labels = twitterID.get('Labels')
        label = labels.split(',')
        if word in label:
            x = twitterID.get('Twitter ID')
            twitterIDs.append(x)


    if twitterIDs == []:
        print("There is no TitterID has the label (",word,") in their images.")
    else:
        print("These TitterID has the label (",word,") in their images:")
        # ignore the same users
        l = []
        for i in twitterIDs:
            if not i in l:
                l.append(i)
        print(l)

def popular():

    clientt = pymongo.MongoClient('127.0.0.1',27017)
    db = clientt.MyDbs
    my_set = db.images
    label = []
    for twitterID in my_set.find():
        labels = twitterID.get('Labels')
        x = labels.split(',')
        label = np.append(x, label)

    #print(label)
    label_counts = Counter(label)
    top_three = label_counts.most_common(4)
    print("The top three popular labels are:\n",top_three[1:])


if __name__ == '__main__':
    #twitterID="hulu"
    #get_all_tweets()
    # PATH=os.getcwd()
    # rename(PATH)
    # m=rename(PATH)
    # get_label(twitterID,m)
    # conv_image()
    user_interface()




