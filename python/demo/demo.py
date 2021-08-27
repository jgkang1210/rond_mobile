import cv2
import numpy as np
import serial
import time

serial_port = serial.Serial(
    port="/dev/ttyACM0",
    baudrate=115200,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
)

def send_packet(center_x, center_y, width, height):
    # start byte : !
    # second byte : 0xff
    # third byte : 0xff
    # fourth byte : 
    # end byte : 

    # if the object is too close stop the motor
    if width > 160 || height > 120:


    serial_port.write(bytes(bytearray([0x21])))

# 웹캠 신호 받기, 숫자는 컴퓨터에 연결된 영상장비 번호
# frame size 640 * 480 by setting v4l2 API
VideoSignal = cv2.VideoCapture(0, cv2.CAP_V4L2)
VideoSignal.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M','J','P','G'))

# 미리 학습된 YOLO weights 파일과 CFG 파일 로드
YOLO_net = cv2.dnn.readNet("yolov3-tiny.weights","yolov3-tiny.cfg")

# YOLO NETWORK 재구성
classes = []
with open("yolo.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = YOLO_net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in YOLO_net.getUnconnectedOutLayers()]

while True:
    # 웹캠 프레임
    ret, frame = VideoSignal.read()
    h, w, c = frame.shape

    # YOLO 입력
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0),True, crop=False)
    YOLO_net.setInput(blob)
    outs = YOLO_net.forward(output_layers)

    class_ids = []
    confidences = []
    boxes = []

    for out in outs:

        for detection in out:

            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > 0.5:
                # Object detected
                center_x = int(detection[0] * w)
                center_y = int(detection[1] * h)
                dw = int(detection[2] * w)
                dh = int(detection[3] * h)

                # Rectangle coordinate
                x = int(center_x - dw / 2)
                y = int(center_y - dh / 2)
                boxes.append([x, y, dw, dh])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.45, 0.4)


    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]
            label = str(classes[class_ids[i]])
            score = confidences[i]

            # if human ?
            if class_ids[i] == 0:
                # 경계상자와 클래스 정보 이미지에 입력
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 5)
                cv2.putText(frame, label, (x, y - 20), cv2.FONT_ITALIC, 0.5, (255, 255, 255), 1)
                cv2.arrowedLine(frame, (320,240), (center_x, 240), (255,0,0), 3)
                if center_x > 280 and center_x < 360:
                    cv2.putText(frame, "Aligned", (320, 400), cv2.FONT_ITALIC, 1,(0,0,0),1)
                elif center_x < 280:
                    cv2.putText(frame, "Left", (320, 400), cv2.FONT_ITALIC, 1, (0,0,0),1)
                else:
                    cv2.putText(frame, "Right", (320, 400), cv2.FONT_ITALIC, 1, (0,0,0),1)

                

    cv2.imshow("YOLOv3", frame)

    if cv2.waitKey(100) > 0:
        break

VideoSignal.release()
cv2.destroyAllWindows()
