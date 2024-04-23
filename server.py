import os

from deepface import DeepFace
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


def face_detection(img):
    result = DeepFace.extract_faces(
        img_path=img, detector_backend="yolov8", enforce_detection=False
    )
    return len(result)


def face_recognition(img):
    result = DeepFace.verify(
        img1_path=img,
        img2_path=os.path.join(os.getcwd() + "/db/frame.jpg"),
        model_name="Facenet512",
        enforce_detection=False,
    )
    return 1 if result["verified"] else 0


@app.route("/", methods=["POST"])
def image_request():
    image = request.files.get("image")
    if image:
        image.save("receive.jpg")
        return jsonify({"result": face_detection("receive.jpg")}), 200
    else:
        return jsonify({"result": 0}), 200


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True, threaded=True)
