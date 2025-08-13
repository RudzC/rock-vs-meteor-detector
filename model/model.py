from flask import request, jsonify, send_file
import io
import logging
from pathlib import Path

import numpy as np
import torch
from PIL import Image
from ultralytics import YOLO

logging.basicConfig(level=logging.DEBUG)

def get_device():
    if torch.cuda.is_available():
        return torch.device("cuda")
    if torch.backends.mps.is_available():
        return torch.device("mps")
    return torch.device("cpu")


def handle_uploaded_image(file):
    if file:
        image_bytes = file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        resized_image = image.resize(size=(640, 640))
        image_np = np.array(resized_image)
        return image_np
    return None


class YOLOModel:
    def __init__(self):
        logging.debug("Loading YOLO model initialized")

        repo_root = Path(__file__).resolve().parents[1]
        weights_path = repo_root / "model" / "YOLO_BBoxMeteorRockDetector_Final_20_jul" / "detect" / "meteor_rock_detector" / "weights" / "best.pt"

        if not weights_path.exists():
            raise FileNotFoundError(f"Weights not found at: {weights_path}")

        self.device = get_device()
        logging.debug(f"Selected device: {self.device}")

        try:
            self.model = YOLO(str(weights_path))
            self.model.to(self.device.type)
            self.model.eval()
            logging.info("YOLO model loaded successfully.")
        except Exception as e:
            logging.exception("Failed to load YOLO model.")
            raise


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