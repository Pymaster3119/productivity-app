import cv2
import numpy as np
import urllib.request
import os

def download_yolo_model():
    model_files = {
        'yolov4.weights': 'https://github.com/AlexeyAB/darknet/releases/download/darknet_yolo_v3_optimal/yolov4.weights',
        'yolov4.cfg': 'https://raw.githubusercontent.com/AlexeyAB/darknet/master/cfg/yolov4.cfg',
        'coco.names': 'https://raw.githubusercontent.com/AlexeyAB/darknet/master/data/coco.names'
    }
    
    for filename, url in model_files.items():
        if not os.path.exists(filename):
            print(f"Downloading {filename}")
            urllib.request.urlretrieve(url, filename)
    return True

def load_yolo_model():
    if not download_yolo_model():
        return None, None
        
    # Load YOLO
    net = cv2.dnn.readNet('yolov4.weights', 'yolov4.cfg')
    
    # Load classes
    with open('coco.names', 'r') as f:
        classes = [line.strip() for line in f.readlines()]
        
    return net, classes

def ai_detect_objects(frame, net, classes):
    if net is None:
        return None

    # Input preprocessing
    height, width = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(frame, 1/255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    
    # Get outputs
    layer_names = net.getLayerNames()
    unconnected = net.getUnconnectedOutLayers()
    
    output_layers = [layer_names[i - 1] for i in unconnected]
    outputs = net.forward(output_layers)
    
    # Process outputs
    boxes = []
    confidences = []
    class_ids = []
    
    for output in outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            
            if confidence > 0.75:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)
    
    # Apply non-max suppression
    if len(boxes) > 0:
        indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        if len(indices) == 0:
            indices = []
    else:
        indices = []
    
    return boxes, confidences, class_ids, indices, classes

def grab_frame():
    cap = cv2.VideoCapture(0)
    print("Here")
    if not cap.isOpened():
        print("Error: Cannot open camera")
        return None

    ret, frame = cap.read()
    cap.release()
    print("Here")

    if not ret:
        return None

    return frame

cap = cv2.VideoCapture(0)

# Load YOLO model
yolo_net, class_names = load_yolo_model()


while True:
    ret, frame = cap.read()
    if frame is not None:
        # Detect objects using YOLO
        detection_result = ai_detect_objects(frame, yolo_net, class_names)
        if detection_result is not None:
            boxes, confidences, class_ids, indices, classes = detection_result
            segmented_frame = frame.copy()
            
            print(f"Detected {len(indices) if len(indices) > 0 else 0} objects")
            for index in range(len(indices)):
                print(f"Object {index}: Class ID = {class_ids[indices[index]]}, Class Name = {classes[class_ids[indices[index]]]}, Confidence = {confidences[indices[index]]:.2f}")
            print("-"*30)