# ---------------------------------This project is made ------------------------------------------------
# ----------------------------------By MD SUKUN UL QALB ---------------------------------------------
#------------------------------------------------------------------------------------------------------



# All the imports go here
import numpy as np
import cv2
import datetime

# Initializing the face and eye cascade classifiers from xml files
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye_tree_eyeglasses.xml')

# Variable store execution state
first_read = True

# Starting the video capture
cap = cv2.VideoCapture(0)
ret, img = cap.read()

t=0
t2=0
i=0
avg=0
Sum = 0


while (ret):
    ret, img = cap.read()
    # Coverting the recorded image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Applying filter to remove impurities
    gray = cv2.bilateralFilter(gray, 5, 1, 1)

    # Detecting the face for region of image to be fed to eye classifier
    faces = face_cascade.detectMultiScale(gray, 1.3, 5, minSize=(200, 200))
    if (len(faces) > 0):
        for (x, y, w, h) in faces:
            img = cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

            # roi_face is face which is input to eye classifier
            roi_face = gray[y:y + h, x:x + w]
            roi_face_clr = img[y:y + h, x:x + w]
            eyes = eye_cascade.detectMultiScale(roi_face, 1.3, 5, minSize=(50, 50))

            # Examining the length of eyes object for eyes
            if (len(eyes) >= 2):
                # Check if program is running for detection
                if (first_read):
                    cv2.putText(img,"Eye detected press s to begin",(70, 70),cv2.FONT_HERSHEY_PLAIN, 3,(0, 255, 0), 2)
                    t = datetime.datetime.now()

            else:
                if (first_read):
                    # To ensure if the eyes are present before starting
                    cv2.putText(img,"No eyes detected", (70, 70),cv2.FONT_HERSHEY_PLAIN, 3,(0, 0, 255), 2)
                else:
                    # This will print on console and restart the algorithm
                    cv2.putText(img, "Game Over !! , Check Your Score !!", (70,70), cv2.FONT_HERSHEY_PLAIN, 3,(0,0,255), 3)
                    i=i+1
                    print("Blink Detected : ",i)
                    t2 = datetime.datetime.now()
                    if(t2.second<=t.second):
                        Sum = Sum + ((t2.second - t.second + 60))
                        avg = Sum/i
                        if ((t2.second - t.second) > 40):
                            print(t2.second - t.second+ 60, " seconds,  Well Played")
                            print("Average after ", i, " blinks : ", avg)
                        elif ((t2.second - t.second) > 20):
                            print(t2.second - t.second + 60, " seconds , You Can Do Better !!")
                        else:
                            print(t2.second - t.second + 60, " Seconds, Below Average")
                        print("Average after ", i, " blinks : ", avg)
                    else :
                        Sum = Sum + ((t2.second - t.second))
                        avg = Sum/i
                        if ((t2.second-t.second)>40 ):
                            print(t2.second-t.second," seconds,  Well Played")

                        elif ((t2.second-t.second)>20):
                            print(t2.second-t.second," seconds , You Can Do Better !!")
                        else :
                            print(t2.second-t.second," Seconds, Below Average")
                        print("Average after ", i, " blinks : ", avg)
                    first_read = True
                    break

    else:
        cv2.putText(img,"No face detected", (100, 100),cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 2)

        # Controlling the algorithm with key
    
    cv2.imshow('img', img)

    a = cv2.waitKey(1)
    if (a == ord('q')):
        break
    elif (a == ord('s') and first_read):
        # This will start the detection
        first_read = False


cap.release()
cv2.destroyAllWindows()