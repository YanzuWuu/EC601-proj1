# EC601-proj1
This contains the files of the MINI project1, please ignore other repository, they'er just for test.

The main program is temp.py, which includes the twitter API tweepy, and have the function of downloading the pictures from twitter account.

The ffmpeg.sh is a simple shell command, which use ffmpeg API to convert the images(.jpg) to a video(.mp4). And the .mp4 file will also in 
the local file under my project1.

The googlevision.py uses Google Vision API to do some research and give the features of pictures. It maybe kind of weird when I import the 
"google.cloud" module, some erro comes out like "No module named google.cloud", we need to make sure it has been installed in the right file
with "pip" or "pip3".
As for the google vision API, some resources may be helpful:
https://cloud.google.com/vision/docs/quickstart

Finally, the json file is used for the data transformation during the pictures download process. I just left it here.
