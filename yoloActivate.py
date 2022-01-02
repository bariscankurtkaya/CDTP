import torch
import cv2

# Model
model = torch.hub.load('ultralytics/yolov5', 'yolov5x6', pretrained=True)
#model.classes = [0, 1, 2, 3, 4, 5, 7, 11, 15, 16, 17, 18, 19, 36, 37]
# From camera
vid = cv2.VideoCapture(0)
vid2 = cv2.VideoCapture(1)


# Images
imgs = ['https://ultralytics.com/images/zidane.jpg']  # batch of images

while True:
    ret, frame = vid.read()
    ret2, frame2 = vid2.read()
    
    # Inference
    results = model(frame)
    results2 = model(frame2)

    # Results
    #results.print()
    results.save() 

    #results2.print()
    results2.save() 
    cv2.imshow("res",frame)
    cv2.imshow("res2",frame2)

    #print("results1", results.pandas().xyxy[0])
    #print("results2", results2.pandas().xyxy[0])


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# After the loop release the cap object
vid.release()
vid2.release()

# Destroy all the windows
cv2.destroyAllWindows()
