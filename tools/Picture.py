import cv2
cap=cv2.VideoCapture(0)
i=1

while True:
    ret,frame=cap.read()
    cv2.imshow("a",frame)
    key = cv2.waitKey(1)
    if key == ord("a"):
        i+=1
        cv2.imwrite("images/rs"+str(i)+".jpg",frame)
    if key == 27:
        break