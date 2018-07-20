import cv2

cap = cv2.VideoCapture("rtsp://localhost:5454/live.rtsp")

while cap.isOpened():

    _, frame = cap.read()

    cv2.imshow("rtsp", frame)

    if cv2.waitKey(1) & 0xff == ord('q'):
        break

cap.Release()
cv2.destoryAllWindows()
