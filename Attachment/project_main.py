import cv2
from sort import *
import math
import numpy as np
from ultralytics import YOLO
import cvzone
import easyocr
from formatting import check, formatted, read

reader = easyocr.Reader(['en'], gpu=False)
cap = cv2.VideoCapture('./video/IMG_3709.MOV')
model = YOLO('yolov8n.pt')
license_plate_detector = YOLO('license_plate_detector.pt')

classnames  = []
with open('classes.txt','r') as f:
    classnames = f.read().splitlines()

tracker = Sort(max_age=20)
line = [1060,630,1350,630]
counter = []
with open('./fee.csv', 'a') as f:
    f.write('{},{},{}\n'.format('Car_id', 'License Plate', 'Score'))
    while 1:
        ret,frame = cap.read()
        if not ret:
            cap = cv2.VideoCapture('./video/IMG_3709.MOV')
            continue
        detections = np.empty((0,5))
        result = model(frame,stream=1)
        for info in result:
            boxes = info.boxes
            for box in boxes:
                x1,y1,x2,y2 = box.xyxy[0]
                conf = box.conf[0]
                classindex = box.cls[0]
                conf = math.ceil(conf * 100)
                classindex = int(classindex)
                objectdetect = classnames[classindex]

                if objectdetect == 'car' or objectdetect == 'bus' or objectdetect =='truck' and conf >60:
                    x1,y1,x2,y2 = int(x1),int(y1),int(x2),int(y2)
                    new_detections = np.array([x1,y1,x2,y2,conf])
                    detections = np.vstack((detections,new_detections))

        track_result = tracker.update(detections)
    
        cv2.line(frame,(line[0],line[1]),(line[2],line[3]),(0,255,255),2)

        for results in track_result:
            cx1,cy1,cx2,cy2,id = results
            x1, y1, x2, y2, id = int(cx1), int(cy1), int(cx2), int(cy2),int(id)
            cx,cy = x2, y2-90
            if line[0] < cx <line[2] and line[1] -30 <cy <line[1]+150:
                cv2.circle(frame,(cx,cy),6,(0,0,255),-1)
                cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),3)
                cvzone.putTextRect(frame,f'{id}', [x1+8,y1-12],thickness=2,scale=1.5, colorR=(255, 0, 0))

            
                cv2.line(frame, (line[0], line[1]), (line[2], line[3]), (0, 0, 255), 4)
                if counter.count(id) == 0:
                    counter.append(id)
            
                license_plates = license_plate_detector(frame)[0]
            
                for license_plate in license_plates.boxes.data.tolist():
                    lx1, ly1, lx2, ly2, score, class_id = license_plate
            
                    if lx1 > cx1 and ly1 > cy1 and lx2 < cx2 and ly2 < cy2:
            
            # crop license plate
                        license_plate_crop = frame[int(ly1):int(ly2), int(lx1): int(lx2), :]
                      
            # process license plate
                        license_plate_crop_gray = cv2.cvtColor(license_plate_crop, cv2.COLOR_BGR2GRAY)
                        _, license_plate_crop_thresh = cv2.threshold(license_plate_crop_gray, 64, 255, cv2.THRESH_BINARY_INV)
                
                        cv2.rectangle(frame,(int(lx1),int(ly1)),(int(lx2),int(ly2)),(0,0,255),3)
            
            # read license plate
                        detections = reader.readtext(license_plate_crop)

                        for detection in detections:
                            _, text, score = detection

                            text = text.upper().replace(' ', '')
                        
                            cvzone.putTextRect(frame,f'License Plate ={read(text)}',[0,200],thickness=2,scale=1.5,border=1,colorR=(255, 0, 0))
        
                            f.write('{},{},{}\n'.format(id, read(text), score))
            
            # resize license plate
                        license_plate_crop=cv2.resize(license_plate_crop, (0,0), fx=4, fy=4)
                        license_plate_crop_thresh=cv2.resize(license_plate_crop_thresh, (0,0), fx=4, fy=4)
                        #cv2.imshow("PLAKA",license_plate_crop)
                        #cv2.imshow("threshold",license_plate_crop_thresh)

        cvzone.putTextRect(frame,f'Total Nr.of Fee ={len(counter)}',[500,34],thickness=4,scale=2.3,border=2,colorR=(255, 0, 0))

        cv2.imshow('frame',frame)
        cv2.waitKey(1)
    f.close()