import yolov5
import cv2
# import mediapipe as mp
# from skimage import io
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, Response, redirect
from utils import get_base_url
import flask

####################################### DEFINE MODEL PARAMETERS ##############################################

model = yolov5.load('Batman1702/AI-Lifeguard')
model.conf = 0.25  # NMS confidence threshold
model.iou = 0.45  # NMS IoU threshold
model.agnostic = False  # NMS class-agnostic
model.multi_label = False  # NMS multiple labels per box
model.max_det = 1000  # maximum number of detections per image


##############################################################################################################

def run_model(img):
    print(type(img))
    results = model(img)

    for box in results.xyxy[0]:
        if box[5] == 0:
            print(box)
            xB = int(box[2])
            xA = int(box[0])
            yB = int(box[3])
            yA = int(box[1])
            cv2.rectangle(img, (xA, yA), (xB, yB), (255, 255, 255), 2)
            cv2.putText(img, 'Active Drowning', (xA, yA - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (36, 255, 12),
                        2)
        elif box[5] == 1:
            print(box)
            xB = int(box[2])
            xA = int(box[0])
            yB = int(box[3])
            yA = int(box[1])
            cv2.rectangle(img, (xA, yA), (xB, yB), (0, 0, 255), 2)
            cv2.putText(img, 'Possible Passive Drowner', (xA, yA - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (36, 255, 12),
                        2)
        if box[5] == 2:
            print(box)
            xB = int(box[2])
            xA = int(box[0])
            yB = int(box[3])
            yA = int(box[1])
            cv2.rectangle(img, (xA, yA), (xB, yB), (0, 0, 0), 2)
            cv2.putText(img, 'Running', (xA, yA - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        elif box[5] == 3:
            print(box)
            xB = int(box[2])
            xA = int(box[0])
            yB = int(box[3])
            yA = int(box[1])
            cv2.rectangle(img, (xA, yA), (xB, yB), (155, 95, 255), 2)
            cv2.putText(img, 'Safe', (xA, yA - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (36, 255, 12), 2)

    plt.axis("off")
    # plt.legend()
    plt.imshow(img)
    plt.savefig("static/assets/results/frame.png")
    return img

def run_live():
    camera = cv2.VideoCapture(0)  # Set camera
    # mpDraw = mp.solutions.drawing_utils  # Set draw function
    while True:
        success, img = camera.read()
        img = run_model(img)
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        cv2.imshow("Image", img)
        cv2.waitKey(1)

        # else:
        #     break
        # print("Camera issues")

