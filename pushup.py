import cv2
import numpy as np
import time
from Posemoduleforpushup import PoseDetector
debug = False
def main():
    cap = cv2.VideoCapture('/home/cyclops/Desktop/datahon/pushuptest.mp4')
    #cap = cv2.VideoCapture(2)
    
    detector = PoseDetector()
    count = 0
    direction = 0
    form = 0
    feedback = "GOOFY Form"
    recordedCount = 0
    start_time = 0
    end_time = 0
    rep_time = 0

    while cap.isOpened():
        ret, img = cap.read() 
        width  = cap.get(3)  # float width
        height = cap.get(4)  # float height
        if debug:
            print(width, height)
        
        img = detector.findPose(img, False)
        lmList = detector.findPosition(img, False)
        if debug:
            print(lmList)
        if len(lmList) != 0:
            elbow = detector.findAngle(img, 11, 13, 15)
            shoulder = detector.findAngle(img, 13, 11, 23)
            hip = detector.findAngle(img, 11, 23,25)
            
            per = np.interp(elbow, (90, 160), (0, 100))
            
            bar = np.interp(elbow, (90, 160), (380, 50))

            if elbow > 160 and shoulder > 40 and hip > 160:
                form = 1
        
            if form == 1:
                if per == 0:
                    if elbow <= 90 and hip > 160:
                        feedback = "GO UP NOW"
                        if direction == 0:
                            count += 0.5
                            direction = 1
                            end_time = time.time()
                            rep_time = end_time - start_time
                            print("Time taken for rep:", rep_time)
                            if count == 6:
                                exit(0)
                    else:
                        feedback = "goofy form"
                        
                if per == 100:
                    if elbow > 160 and shoulder > 40 and hip > 160:
                        feedback = "G0 DOWN NOW"
                        if direction == 1:
                            count += 0.5
                            direction = 0
                            start_time = time.time()
                    else:
                        feedback = "goofy Form"
                        
            #if count != recordedCount:
                #print(count)
            
            recordedCount = count

            
            if form == 1:
                cv2.rectangle(img, (580, 50), (600, 380), (0, 255, 0), 3)
                cv2.rectangle(img, (580, int(bar)), (600, 380), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, f'{int(per)}%', (565, 430), cv2.FONT_HERSHEY_PLAIN, 2,(255, 0, 0), 2)

            cv2.putText(img, str(int(count)), (25, 455), cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 0), 5)
            cv2.putText(img, feedback, (500, 40 ), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)

            
        cv2.imshow('meow', img)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()