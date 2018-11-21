#!/bin/bash
ffmpeg -f video4linux2 -i /dev/video0 \
-vcodec libx264 -s 640x480 -r 30 \
-biv 150k -bufsize -an \
http://localhost:8090/feed1.ffm
-crf 23
-preset ultrafast
-tune zerolatency

# CRF Example
ffmpeg -i input.avi -c:v libx264 -preset slow -crf 22 -c:a copy output.mkv

# Two-Pass
ffmpeg -y -i input -c:v libx264 -b:v 2600k -pass 1 -an -f mp4 /dev/null && \
ffmpeg -i input -c:v libx264 -b:v 2600k -pass 2 -c:a aac -b:a 128k output.mp4

# Overwriting default preset settings
ffmpeg -i input -c:v libx264 -preset slow -crf 22 -x264-params keyint=123:min-keyint=20 -c:a copy output.mkv 

Warning: Do not use the option x264opts, 
as it will eventually be removed. 
Use x264-params instead. 

# Low Latency
x264 offers a -tune zerolatency option 
for low latency streaming. 

# CBR (Constant Bit Rate)
ffmpeg -i input.mp4 -c:v libx264 -x264-params "nal-hrd=cbr" -b:v 1M -minrate 1M -maxrate 1M -bufsize 2M output.ts

# Contrained encoding (VBV / maximum bit rate)
to Constrain the maximum bitrate used, or keep the stream''s birtrate
within certatin bounds.
This is particularly useful for online streaming, where the client expects a
certatin average bitrate, but you still want the encoder to adjust the 
bitrate per-frame.

You can use -crf or -b:v with a maximum bit rate by specifying 
both -maxrate and -bufsize:

## VBV, One-pass approach
ffmpeg -i input -c:v libx264 -crf23 -maxrate 1M -bufsize 2M output.mp4

## VBV, Two-pass approach
ffmpeg -i input -c:v libx264 -b:v 1M -maxrate 1M -bufsize 2M -pass 1 -f mp4 /dev/null
ffmpeg -i input -c:v libx264 -b:v 1M -maxrate 1M -bufszie 2M -pass 2 output.mp4

# how to Pix_format setting?
-pix_fmt yuv420p

# `faststart` for web video
You can add `-movflags +faststart` as an ouput option if your vides are goint to
be viewed in a browser. This will move some information to the 
beggining of your file and allow the video to begin playing before it is completetly
downloaded by the viewer.
It it not required if you are going to use a video services such as YouTube.