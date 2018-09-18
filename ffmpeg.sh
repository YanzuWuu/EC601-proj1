#!/bin/bash
ffmpeg -r 1 -i %02d.jpg -vcodec mpeg4 -y movie.mp4
