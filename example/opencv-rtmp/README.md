# OpenCV-rtmp

## Test
```
ffmpeg -f avfoundation -r 30 -i "0:0" -deinterlace -vcodec libx264 -pix_fmt yuv420p -preset medium -g 60 -b:v 2500k -acodec libmp3lame -ar 44100 -threads 6 -qscale 3 -b:a 712000 -bufsize 512k -f flv rtmp://localhost:1935/target_address
```
