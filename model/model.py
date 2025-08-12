from flask import request, jsonify, send_file
from ultralytics import YOLO
import numpy as np
from PIL import Image
import io


def handle_uploaded_image(file):
    if file:
        image_bytes = file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        resized_image = image.resize(size=(610, 610))
        image_np = np.array(resized_image)
        return image_np
    return None


class YOLOModel:
    def __init__(self):
        folder_path = 'model/YOLO_BBoxMeteorRockDetector_Final_20_jul/detect/meteor_rock_detector'
        try:
            self.model = YOLO(f'{folder_path}/args.yaml', task='rock-vs-meteor-detection')
            self.model.load(f'{folder_path}/weights/best.pt')
        except Exception:
            self.model = YOLO(f'{folder_path}/weights/best.pt', task='rock-vs-meteor-detection')

    def predict(self):
        if 'file' not in request.files:
            return jsonify({'error': 'No file part in the request'}), 400

        file = request.files['file']

        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400

        try:
            image_np = handle_uploaded_image(file)

            if image_np is None:
                return jsonify({'error': 'Invalid image file'}), 400

            results = self.model(image_np)

            for idx, result in enumerate(results):
                annotated_bgr = result.plot()
                annotated_rgb = annotated_bgr[..., ::-1]

                buf = io.BytesIO()
                Image.fromarray(annotated_rgb).save(buf, format="JPEG", quality=90)
                buf.seek(0)

                return send_file(
                    buf,
                    mimetype="image/jpeg",
                    as_attachment=False,
                    download_name="prediction.jpg"
                )

            return jsonify({'error': 'Oops! Something went wrong! No Results!'}), 500

        except Exception as e:
            return jsonify({'error': str(e)}), 500