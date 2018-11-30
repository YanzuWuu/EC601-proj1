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
        consumer_key = 'P0ZYeebu0IiZ2yXDkJYMKa4QN'
        consumer_secret = '1o8drgPRXHxks3FhGLeNJbMXjPf8p3GbE0ywbdlRS1kpGEU5LO'
        access_token = '1037401110389174272-6iC08TC3wyhtB3QE5lzaipeM18KYe7'
        access_secret = 'TkxumYnCOj8zepySPctzFeKvDS9SFx82gKVjS6evfOjMe'
        #authorize twitter, initialize tweepy
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_secret)
        api = tweepy.API(auth)
        
        #initialize a list to hold all the tweepy Tweets
        alltweets = []

        #make initial request for most recent tweets (200 is the maximum allowed count)
        new_tweets = api.user_timeline(screen_name = screen_name,count=20)

        #save most recent tweets
        alltweets.extend(new_tweets)

        #save the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        #keep grabbing tweets until there are no tweets left to grab
        while len(new_tweets) > 0:

            #all subsiquent requests use the max_id param to prevent duplicates
            new_tweets = api.user_timeline(screen_name = screen_name,count=100,max_id=oldest)
            #save most recent tweets
            alltweets.extend(new_tweets)

            #update the id of the oldest tweet less one
            oldest = alltweets[-1].id - 1
            if(len(alltweets) > 10):
                break
            print ("...%s tweets downloaded so far" % (len(alltweets)))

        #write tweet objects to JSON
        file = open('tweet.json', 'w')
        print ("Writing tweet objects to JSON please wait...")
        media_files=set()
        for status in alltweets:
            media = status.entities.get('media',[])
            if (len(media)>0):
                media_files.add(media[0]['media_url'])

        for media_file in media_files:
            wget.download(media_file)
        file.close()
    


def rename(PATH):
    filelist = os.listdir(PATH)
    total_num = len(filelist)
    m = 0
    for item in filelist:

        if item.endswith('.jpg'):

            src = os.path.join(os.path.abspath(PATH), item)
            if m<10:
                dst = os.path.join(os.path.abspath(PATH), '0'+str(m) + '.jpg')
            else:
                dst = os.path.join(os.path.abspath(PATH), str(m) + '.jpg')
            m=m+1
            try:
                os.rename(src, dst)
                print('converting %s to %s ...' % (src, dst))
            except:

                continue
    print ('total %d to rename & converted %d jpgs' % (total_num, m))
    return m

def conv_image():
     print('Converting the images to video....Processing')
     subprocess.call(['ffmpeg', '-r', '1', '-i', '%02d.jpg', '-vcodec', 'mpeg4','-y','movie.mp4'])

client = vision.ImageAnnotatorClient()

def get_describe(m):
    print('Label the Images...Processing')
    #filelist = os.listdir(PATH)


    for i in range(m):
        #if file.endswith(".jpg"):
            #file_name = os.path.join(os.path.dirname(__file__),'%02d.jpg'%(i))
            file_name = os.path.basename(__file__)
            with io.open(file_name, 'rb') as image_file:
                content = image_file.read()

                image = vision.types.Image(content=content)

                response = client.label_detection(image=image)
                labels = response.label_annotations
            j = 0
            for label in labels:
                # print(label.description)
                raw_image = Image.open(file_name)
                draw = ImageDraw.Draw(raw_image)  # 修改图片
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
    get_describe(m)
    conv_image()

