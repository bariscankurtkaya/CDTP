import torch
import cv2
import numpy as np

# Model
model = torch.hub.load('ultralytics/yolov5', 'yolov5x6', pretrained=True)
model.classes = [0, 2, 7, 15, 16, 17, 18, 19, 64]
# From camera
vid = cv2.VideoCapture(0)
#vid2 = cv2.VideoCapture(1)


# Images
imgs = ['https://ultralytics.com/images/zidane.jpg']  # batch of images

while True:
    ret, frame = vid.read()
    #ret2, frame2 = vid2.read()
    
    # Inference
    #results2 = model(frame2)

    # Results
    
    
    """
    [359.062744140625 197.2888946533203 639.4095458984375 477.38427734375 0.9300717711448669 17       'horse']
    0  xmin           1  ymin           2 xmax            3 ymax          4 prob.            5 class -1   6 name

    classes: https://gist.github.com/AruniRC/7b3dadd004da04c80198557db5da4bda


    1. name stop sign varsa dikkat kaza var ya da yavaşlayın
    2. name insan yolda insan var yavaşlayın
    3. name horse, dog, cat, cow, sheep ise yolda hayvan var yavaşla
    4. name tır ise ve sağdaysa tır bey sol şeritten sağa geçin
    5. name mouse opsiyonel taş
    """


    results = model(frame)
    npResults = results.pandas().xyxy[0].to_numpy()

    if(len(npResults) != 0):
        for i in range(len(npResults)):
            #We define the class number into the classNumber variable and class name to className
            classNumber = npResults[i][5]
            className = npResults[i][6]
            xmin = npResults[i][0]
            xmax = npResults[i][2]

            #First Case
            if(classNumber == 11): #Stop sign
                print("There is a stop sign", className) 

            #Second Case
            elif(classNumber == 0):
                print("There is a person in the road", className)

            #Third Case
            elif classNumber in [15,16,17,18,19]:
                print("There is a animal in the road", className)

            #Fourth Case
            elif(classNumber == 7 and (xmin + xmax) > 640 ):
                print("Tır sağa geç", className)

            #Fifth class
            elif(classNumber == 64):
                print("Taş var dikkat ettt", "Rock")

    results.save() 
    cv2.imshow("res",frame)

    #results2.print()
    #results2.save() 

    #cv2.imshow("res2",frame2)

    #print("results1", results.pandas().xyxy[0])
    #print("results2", results2.pandas().xyxy[0])

    #if ()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# After the loop release the cap object
vid.release()
#vid2.release()

# Destroy all the windows
cv2.destroyAllWindows()
