import os
from threading import Thread
from time import sleep

import cv2
import requests
import RPi.GPIO as GPIO


def change_led_status(pin, mode: str):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)

    if mode.lower() == "on":
        GPIO.output(pin, GPIO.HIGH)
    elif mode.lower() == "off":
        GPIO.output(pin, GPIO.LOW)


def send_request():
    leds = [7, 12, 16, 20, 21]
    while True:
        try:
            resp = requests.post(
                API_URL,
                files={
                    "image": (
                        os.path.join(os.getcwd() + "frame.jpg"),
                        open("frame.jpg", "rb"),
                        "multipart/form-data",
                        {"Expires": "0"},
                    )
                },
            )
            result = resp.json()["result"]
            print(result)
            if result > 5:
                result = 5
            for i in range(result):
                change_led_status(leds[i], "on")
            for i in range(result, 5 - result):
                change_led_status(leds[i], "off")
            sleep(0.7)
        except Exception as e:
            print(e)
            print("Failed to send image")


if __name__ == "__main__":
    API_URL = "https://z7c8xmfw-8080.asse.devtunnels.ms/"
    cap = cv2.VideoCapture(0)
    thread = Thread(target=send_request)
    thread.start()
    while True:
        ret, frame = cap.read()
        frame = cv2.resize(frame, (frame.shape[1] // 2, frame.shape[0] // 2))
        # cv2.imshow("frame", frame)
        cv2.imwrite("frame.jpg", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()
