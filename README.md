# EC601-proj1
This contains the files of the MINI project1, please ignore other repository, they'er just for test.

The main program is temp.py, which quote the twitter API tweepy, and have the function of downloading the pictures from specific twitter account gave at the end of code. I used "while" "for" & "if" loop to read the media fiels' url and download the ones endwith ".jpg". The "wget.download" & "item.endwith" function is of vital importance here. Besides, the reason why i add a "0" before the new name of images under ten is to make sure they can be renamed with the same style, so that they can be downloaded correctly. 

The ffmpeg.sh is a simple shell command, which use ffmpeg API to convert the images(.jpg) to a video(.mp4). And the .mp4 file will also in the local file under my project1.

The googlevision.py uses Google Vision API to do some research and give the features of pictures. For each image, the code gives some labels and print them on the screen. It maybe kind of weird when I import the "google.cloud" module, some erro comes out like "No module named google.cloud", we need to make sure it has been installed in the right file with "pip" or "pip3". 
As for the google vision API, some resources may be helpful:
https://cloud.google.com/vision/docs/quickstart

Finally, the json file is used for the data transformation during the pictures download process. I just left it here.
##############################################. update line  #############################################
I combine the ffmpeg.sh command and googlevision.py into the main code: temp.py, and right now it can download images and have label on them, and create video at one time.
