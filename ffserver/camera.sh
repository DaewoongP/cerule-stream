#!/bin/bash
ffmpeg -r 30 -s 640x480 -f video4linux2 -i /dev/video0 http://localhost:8090/feed1.ffm
