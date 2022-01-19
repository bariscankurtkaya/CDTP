import torch
import cv2
import numpy as np
import bluetooth
import time
import serial

# configure the serial connections (the parameters differs on the device you are connecting to)

arduino = serial.Serial(port='COM5', baudrate=115200, timeout=.1)
def write_read(x):
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.05)
    data = arduino.readline()
    return data

# Model
model = torch.hub.load('ultralytics/yolov5', 'yolov5x6', pretrained=True)
model.classes = [2, 7, 15, 16, 17, 18, 19, 64]
model.conf = 0.70
# From camera
vid = cv2.VideoCapture(0)
vid2 = cv2.VideoCapture(1)

sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect(("00:19:10:09:0F:33", 1))



value = write_read("0")

while True:
    ret, frame = vid.read()
    ret2, frame2 = vid2.read()
    
    # Inference

    # Results
    
    
    """
    [359.062744140625 197.2888946533203 639.4095458984375 477.38427734375 0.9300717711448669 17       'horse']
    0  xmin           1  ymin           2 xmax            3 ymax          4 prob.            5 class -1   6 name

    classes: https://gist.github.com/AruniRC/7b3dadd004da04c80198557db5da4bda


    1. name stop sign varsa dikkat kaza var ya da yavaşlayın
    2. name insan yolda insan var yavaşlayın
    3. name horse, dog, cat, cow, sheep ise yolda hayvan var yavaşla
    4. name tır ise ve sağdaysa tır sol şeritten sağa geçin
    5. name mouse opsiyonel taş
    """


    results = model(frame)
    results2 = model(frame2)

    npResults = results.pandas().xyxy[0].to_numpy()
    npResults2 = results2.pandas().xyxy[0].to_numpy()
    isTwoImportant = True
    print("Girdi")
    if(len(npResults2) != 0):
        for i in range(len(npResults2)):
            #We define the class number into the classNumber variable and class name to className
            classNumber = npResults2[i][5]
            className = npResults2[i][6]
            xmin = npResults2[i][0]
            xmax = npResults2[i][2]

            #First Case
            if(classNumber == 11): #Stop sign
                print("There is a stop sign", className)
                value = write_read("1")

            #Second Case
            elif(classNumber == 0):
                """
                print("There is a person in the road", className)
                value = write_read("2")
                sock.send("W")
                time.sleep(1)
                sock.send("S")
                time.sleep(2)
                """

            #Third Case
            elif classNumber in [15,16,17,18,19]:
                print("AT at AT")
                value = write_read("3")
                sock.send("W")
                time.sleep(2)
                sock.send("S")
                time.sleep(3)


            #Fourth Case
            elif(classNumber == 7 and (xmin + xmax) > 640 ):
                value = write_read("4")
                sock.send("W")
                print("w")
                time.sleep(3)
                print("s")
                sock.send("S")
                time.sleep(3)
                print("Tır sağa geç", className)

            #Fifth class
            elif(classNumber == 64):
                value = write_read("5")
                print("Taş var dikkat ettt", "Rock")
                sock.send("W")
                time.sleep(1.5)
                sock.send("S")
                time.sleep(3)


            

        if( isTwoImportant ):
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
                        value = write_read("6")

                    #Second Case
                    elif(classNumber == 0):
                        print("There is a person in the road", className)
                        value = write_read("7")
                        sock.send("W")
                        time.sleep(0.5)
                        sock.send("S")
                        time.sleep(0.5)

                    #Third Case
                    elif classNumber in [15,16,17,18,19]:
                        print("There is a animal in the road", className)
                        value = write_read("8")
                        sock.send("W")
                        time.sleep(4)
                        sock.send("S")
                        time.sleep(5)


                    #Fourth Case
                    elif(classNumber == 7 and (xmin + xmax) > 640 ):
                        value = write_read("9")
                        print("Tır sağa geç", className)

                    #Fifth class
                    elif(classNumber == 64):
                        value = write_read("10")
                        print("Taş var dikkat ettt", "Rock")
                        sock.send("W")
                        time.sleep(4.5)
                        sock.send("S")
                        time.sleep(3)

    results.save()
    results2.save() 
    cv2.imshow("res1",frame)
    cv2.imshow("res2",frame2)

    #results2.print()
    #results2.save() 

    #cv2.imshow("res2",frame2)

    #print("results1", results.pandas().xyxy[0])
    #print("results2", results2.pandas().xyxy[0])

    #if ()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# After the loop release the cap object
sock.send("S")
sock.send("K")
vid.release()
#vid2.release()

# Destroy all the windows
cv2.destroyAllWindows()
sock.close()