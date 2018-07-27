import numpy as np
import subprocess as sp
import cv2

cap = cv2.VideoCapture("toystory.mp4")
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
fps = cap.get(cv2.CAP_PROP_FPS)
print(width, height, fps)

#url = 'rtmp://localhost:1935/dash/live'
#command = 'ffmpeg -i - -vcodec libx264 -f flv {}'.format(url)
#print(command)
#proc = sp.Popen(command, stdin=sp.PIPE, shell=True, bufsize=10**8)

command = ['ffmpeg',
        '-y', # (optional) overwrite output file if it exists
        '-f', 'rawvideo',
        '-vcodec','rawvideo',
        '-s', '640x360', # size of one frame
        '-pix_fmt', 'rgb24',
        '-r', '29.97',  # frames per second
        '-i', '-',  # The imput comes from a pipe
        '-an',  # Tells FFMPEG not to expect any audio
        '-vcodec', 'libx264',
        'my_output_videofile.mp4' ]

stream_command = ['ffmpeg',
        '-y', # (optional) overwrite output file if it exists
        '-f', 'rawvideo',
        '-vcodec','rawvideo',
        '-s', '640x360', # size of one frame
        '-pix_fmt', 'rgb24',
        '-r', '29.97',  # frames per second
        '-i', '-',  # The imput comes from a pipe
        '-an',  # Tells FFMPEG not to expect any audio
        '-vcodec', 'libx264',
        '-f', 'flv',
        'rtmp://localhost:1935/dash/live' ]

pipe = sp.Popen(command, stdin=sp.PIPE, stderr=sp.PIPE)
stream = sp.Popen(stream_command, stdin=sp.PIPE, stderr=sp.PIPE)
while cap.isOpened():
    # Capture frame-by-frame
    ret, frame = cap.read()  # frame size: 640x360x3(=691200)
    if ret:
        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        print(gray.size) # (= 230400)
        # Display the resulting frame
        cv2.imshow('frame', gray)
        print(frame.size)  # 640x360x3(=691200)
        pipe.stdin.write(gray.tostring())
        stream.stdin.write(frame.tostring())
    else:
        break
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
