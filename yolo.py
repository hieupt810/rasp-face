import cv2
import cvzone
import RPi.GPIO as GPIO
from ultralytics import YOLO


def change_led_status(pin, mode: str):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    if mode.lower() == "on":
        GPIO.output(pin, GPIO.HIGH)
    elif mode.lower() == "off":
        GPIO.output(pin, GPIO.LOW)


if __name__ == "__main__":
    video = cv2.VideoCapture(0)
    face_model = YOLO("yolov8n-face.pt")
    leds = [7, 12, 16, 20, 21]

    while True:
        rt, frame = video.read()
        frame = cv2.resize(frame, (frame.shape[1] // 2, frame.shape[0] // 2))

        face_result = face_model.predict(frame, conf=0.25)
        for i in range(0, 5):
            change_led_status(leds[i], "off")

        for info in face_result:
            parameters = info.boxes

            for idx, box in enumerate(parameters):
                change_led_status(leds[idx if idx < 5 else 4], "on")

                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                h, w = y2 - y1, x2 - x1
                frame = cvzone.cornerRect(frame, (x1, y1, w, h), l=9, rt=3)

        cv2.imshow("Camera", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    video.release()
    cv2.destroyAllWindows()
