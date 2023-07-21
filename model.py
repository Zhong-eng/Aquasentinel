import yolov5
import cv2
import matplotlib.pyplot as plt

####################################### DEFINE MODEL PARAMETERS ##############################################

model = yolov5.load('Batman1702/Aquasentinel')
model.conf = 0.25  # NMS confidence threshold
model.iou = 0.45  # NMS IoU threshold
model.agnostic = False  # NMS class-agnostic
model.multi_label = False  # NMS multiple labels per box
model.max_det = 1000  # maximum number of detections per image


##############################################################################################################

def run_model(img):
    results = model(img)

    for box in results.xyxy[0]:
        if box[4] >= 0.15:
            if box[5] == 0:
                xB = int(box[2])
                xA = int(box[0])
                yB = int(box[3])
                yA = int(box[1])
                cv2.rectangle(img, (xA, yA), (xB, yB), (255, 255, 255), 2)
                cv2.putText(img, 'Active Drowning', (xA, yA - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (36, 255, 12),
                            2)
            elif box[5] == 1:
                xB = int(box[2])
                xA = int(box[0])
                yB = int(box[3])
                yA = int(box[1])
                cv2.rectangle(img, (xA, yA), (xB, yB), (0, 0, 255), 2)
                cv2.putText(img, 'Possible Passive Drowner', (xA, yA - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            (36, 255, 12),
                            2)
            elif box[5] == 2:
                xB = int(box[2])
                xA = int(box[0])
                yB = int(box[3])
                yA = int(box[1])
                cv2.rectangle(img, (xA, yA), (xB, yB), (0, 0, 0), 2)
                cv2.putText(img, 'Running', (xA, yA - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
            # elif box[5] == 3:
            #     xB = int(box[2])
            #     xA = int(box[0])
            #     yB = int(box[3])
            #     yA = int(box[1])
            #     cv2.rectangle(img, (xA, yA), (xB, yB), (155, 95, 255), 2)
            #     cv2.putText(img, 'Safe', (xA, yA - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (36, 255, 12), 2)

    plt.axis("off")
    # plt.legend()
    plt.imshow(img)
    plt.savefig("static/assets/results/frame.png")
    return img


def current_situation(img):
    results = model(img)
    for box in results.xyxy[0]:
        if box[4] >= 0.15:
            if box[5] == 0:
                return 0
            elif box[5] == 1:
                return 1
            elif box[5] == 2:
                return 2


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


class Model:
    def __init__(self, model):
        self.model = model
        self.active_drowning = False
        self.passive_drowning = False
        self.running = False

    def run_model(self, img):
        self.active_drowning = False
        self.passive_drowning = False
        self.running = False
        results = model(img)

        for box in results.xyxy[0]:
            if box[4] >= 0.15:
                if box[5] == 0:
                    xB = int(box[2])
                    xA = int(box[0])
                    yB = int(box[3])
                    yA = int(box[1])
                    cv2.rectangle(img, (xA, yA), (xB, yB), (255, 255, 255), 2)
                    cv2.putText(img, 'Active Drowning', (xA, yA - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (36, 255, 12),
                                2)
                    self.active_drowning = True
                elif box[5] == 1:
                    xB = int(box[2])
                    xA = int(box[0])
                    yB = int(box[3])
                    yA = int(box[1])
                    cv2.rectangle(img, (xA, yA), (xB, yB), (0, 0, 255), 2)
                    cv2.putText(img, 'Possible Passive Drowner', (xA, yA - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                                (36, 255, 12),
                                2)
                    self.passive_drowning = True
                elif box[5] == 2:
                    xB = int(box[2])
                    xA = int(box[0])
                    yB = int(box[3])
                    yA = int(box[1])
                    cv2.rectangle(img, (xA, yA), (xB, yB), (0, 0, 0), 2)
                    cv2.putText(img, 'Running', (xA, yA - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
                    self.running = True
        plt.axis("off")
        # plt.legend()
        plt.imshow(img)
        plt.savefig("static/assets/results/frame.png")
        return img


SmarterModel = Model(model)
