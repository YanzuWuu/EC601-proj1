#!/usr/bin/env python
# encoding: utf-8
#Author - Prateek Mehta


import tweepy #https://github.com/tweepy/tweepy
#import json
#import urllib.request
import os
import wget
#import subprocesss
#import ffmpy
#Twitter API credentials



def get_all_tweets(screen_name):
        
        #Twitter only allows access to a users most recent 3240 tweets with this method
        
        #authorize twitter, initialize tweepy
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_secret)
        api = tweepy.API(auth)
        
        #initialize a list to hold all the tweepy Tweets
        alltweets = []    
        
        #make initial request for most recent tweets (200 is the maximum allowed count)
        new_tweets = api.user_timeline(screen_name = screen_name,count=10)
        
        #save most recent tweets
        alltweets.extend(new_tweets)
        
        #save the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1
        
        #keep grabbing tweets until there are no tweets left to grab
        while len(new_tweets) > 0:
            
            #all subsiquent requests use the max_id param to prevent duplicates
            new_tweets = api.user_timeline(screen_name = screen_name,count=10,max_id=oldest)
            
            #save most recent tweets
            alltweets.extend(new_tweets)
            
            #update the id of the oldest tweet less one
            oldest = alltweets[-1].id - 1
            if(len(alltweets) > 15):
                break
            print ("...%s tweets downloaded so far" % (len(alltweets)))
           
        #write tweet objects to JSON
        file = open('tweet.json', 'w') 
    
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
    
'''    
    def save_img(media_url,file_name,file_path='pic'):
        #save in pic
        try:
            if not os.path.exists(file_path):
                print ('folder',file_path,'donot exist, create again')
                #os.mkdir(file_path)
                os.makedirs(file_path)
            #attain the last word of pics
    
           
    
            file_suffix = os.path.splitext(media_url)[1]
            #full file name
            filename = '{}{}{}{}'.format(file_path,os.sep,file_name,file_suffix)
            #save pics in file
            wget.download(media_url,file_path)
        except IOError as e:
            print ('process fault',e)
        except Exception as e:
            print ('erro：',e)
'''
#close the file

#def __init__(PATH):
#    PATH = '/home/ece-student/601Task1/newtask1/'

def rename(PATH):
    filelist = os.listdir(PATH)
    total_num = len(filelist)
    i = 0
    for item in filelist:

        if item.endswith('.jpg'):
                
        
            src = os.path.join(os.path.abspath(PATH), item)
            if i<10:
                dst = os.path.join(os.path.abspath(PATH), '0'+str(i) + '.jpg')
            else:
                dst = os.path.join(os.path.abspath(PATH), str(i) + '.jpg')
            i=i+1
            try:
                os.rename(src, dst)
                print('converting %s to %s ...' % (src, dst))
            except:

                continue
           

    print ('total %d to rename & converted %d jpgs' % (total_num, i))



if __name__ == '__main__':
    #pass in the username of the account you want to download
    get_all_tweets("@Ibra_official")
#    __init__(self)
    PATH=os.getcwd()
#    self.path = '/home/ece-student/601Task1/newtask1/'
    rename(PATH)
    os.chdir(PATH)
