#!/bin/bash
ffmpeg -f video4linux2 -i /dev/video0 \
-vcodec libx264 -s 640x480 -r 30 \
-biv 150k -bufsize -an \
http://localhost:8090/feed1.ffm