import numpy as np
import time
import cv2


INPUT_FILE='/Dataset/1.jpg'
OUTPUT_FILE='./predicted.jpg'
LABELS_FILE='../darknet/data/coco.names'
CONFIG_FILE='../darknet/cfg/yolov3.cfg'
WEIGHTS_FILE='../darknet/yolov3.weights'
CONFIDENCE_THRESHOLD=0.3

LABELS = open(LABELS_FILE).read().strip().split("\n")

np.random.seed(4)
COLORS = np.random.randint(0, 255, size=(len(LABELS), 3),
	dtype="uint8")


net = cv2.dnn.readNetFromDarknet(CONFIG_FILE, WEIGHTS_FILE)

image = cv2.imread(INPUT_FILE)
(H, W) = image.shape[:2]

# determine only the *output* layer names that we need from YOLO
ln = net.getLayerNames()
ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]


blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416),
	swapRB=True, crop=False)
net.setInput(blob)
start = time.time()
layerOutputs = net.forward(ln)
end = time.time()


print("[INFO] YOLO took {:.6f} seconds".format(end - start))


# initialize our lists of detected bounding boxes, confidences, and
# class IDs, respectively
boxes = []
confidences = []
classIDs = []

# loop over each of the layer outputs
for output in layerOutputs:
	# loop over each of the detections
	for detection in output:
		# extract the class ID and confidence (i.e., probability) of
		# the current object detection
		scores = detection[5:]
		classID = np.argmax(scores)
		confidence = scores[classID]

		# filter out weak predictions by ensuring the detected
		# probability is greater than the minimum probability
		if confidence > CONFIDENCE_THRESHOLD:
			# scale the bounding box coordinates back relative to the
			# size of the image, keeping in mind that YOLO actually
			# returns the center (x, y)-coordinates of the bounding
			# box followed by the boxes' width and height
			box = detection[0:4] * np.array([W, H, W, H])
			(centerX, centerY, width, height) = box.astype("int")

			# use the center (x, y)-coordinates to derive the top and
			# and left corner of the bounding box
			x = int(centerX - (width / 2))
			y = int(centerY - (height / 2))

			# update our list of bounding box coordinates, confidences,
			# and class IDs
			boxes.append([x, y, int(width), int(height)])
			confidences.append(float(confidence))
			classIDs.append(classID)

# apply non-maxima suppression to suppress weak, overlapping bounding
# boxes
idxs = cv2.dnn.NMSBoxes(boxes, confidences, CONFIDENCE_THRESHOLD,
	CONFIDENCE_THRESHOLD)

# ensure at least one detection exists
if len(idxs) > 0:
	# loop over the indexes we are keeping
	for i in idxs.flatten():
		# extract the bounding box coordinates
		(x, y) = (boxes[i][0], boxes[i][1])
		(w, h) = (boxes[i][2], boxes[i][3])

		color = [int(c) for c in COLORS[classIDs[i]]]

		cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
		text = "{}: {:.4f}".format(LABELS[classIDs[i]], confidences[i])
		cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,
			0.5, color, 2)

# show the output image
cv2.imwrite("example.png", image)















































"""
import sys
sys.path.append('/home/baris/Github/darknet/python/')

from darknet import performDetect as scan #calling 'performDetect' function from darknet.py
"""

from darknetpy.detector import Detector


######################### FUNCTIONS  ###########################
"""
def detect(picPath):
    ''' this script if you want only want get the coord '''
    cfg='../darknet/cfg/yolov3.cfg' #change this if you want use different config
    coco='../darknet/cfg/coco.data' #you can change this too
    data='../darknet/yolov3.weights' #and this, can be change by you
    test = scan(imagePath=picPath, thresh=0.25, configPath=cfg, weightPath=data, metaPath=coco, showImage=True, makeImageOnly=False, initOnly=False) #default format, i prefer only call the result not to produce image to get more performance

    #until here you will get some data in default mode from alexeyAB, as explain in module.
    #try to: help(scan), explain about the result format of process is: [(item_name, convidence_rate (x_center_image, y_center_image, width_size_box, height_size_of_box))], 
    #to change it with generally used form, like PIL/opencv, do like this below (still in detect function that we create):

    newdata = []
    if len(test) >=2:
        for x in test:
            item, confidence_rate, imagedata = x
            x1, y1, w_size, h_size = imagedata
            x_start = round(x1 - (w_size/2))
            y_start = round(y1 - (h_size/2))
            x_end = round(x_start + w_size)
            y_end = round(y_start + h_size)
            data = (item, confidence_rate, (x_start, y_start, x_end, y_end), w_size, h_size)
            newdata.append(data)

    elif len(test) == 1:
        item, confidence_rate, imagedata = test[0]
        x1, y1, w_size, h_size = imagedata
        x_start = round(x1 - (w_size/2))
        y_start = round(y1 - (h_size/2))
        x_end = round(x_start + w_size)
        y_end = round(y_start + h_size)
        data = (item, confidence_rate, (x_start, y_start, x_end, y_end), w_size, h_size)
        newdata.append(data)

    else:
        newdata = False

    return newdata

"""

def detectWithDarknetpy(imgPath):
    cfg='../darknet/cfg/yolov3.cfg' #change this if you want use different config
    coco='../darknet/cfg/coco.data' #you can change this too
    data='../darknet/yolov3.weights' #and this, can be change by you
    
    detector = Detector(coco,cfg,data)

    results = detector.detect(imgPath)
    
    print(results)


######################### ALGORITHM  ###########################

table = './Dataset/1.jpg'

detectWithDarknetpy(table)

"""
checking = detect(table)

for x in checking:
    item = x[0]
    x1, y1, x2, y2 = x[2]
    print(item)
    print(x1, y1, x2, y2)
"""