

#
Capture and stream a webcam To capture using the iSight camera on a Mac, or infact any other webcam connected to the Mac, we can use FFmpeg. First get a list of the devices installed.
```
ffmpeg -f avfoundation -list_devices true -i ""
```
This will list the aviable video and audio devices.

The below will capture at 30fps and the set video size to a file.
```
fmpeg -f avfoundation -framerate 30 -video_size 640x480 -i "0:none" out.avi
```
The -i 0:none will select the 0 indexed video source and no audio.

We can stream this to the network with
```
ffmpeg -f avfoundation -framerate 30 -video_size 640x480 -i "0:none" -vcodec libx264 -preset ultrafast -tune zerolatency -pix_fmt yuv422p -f mpegts udp://localhost:12345
```
This can be viewed using VLC or OpenCV, although there maybe a significant lactancy in the stream

```
ffmpeg -f avfoundation -framerate 30 -i "0:none" -video_size 640x480 -vcodec libx264 output.mp4
```