import base64
import os
import tempfile

import cv2
import numpy as np
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from PIL import Image
from google.cloud import vision

# ───────────────────────────────────────────────────────────────
# Configuration
# ───────────────────────────────────────────────────────────────
CONVERSION_RATE = 1.95583
MAX_IMAGE_DIM = 1080

app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), '..', 'templates'),
    static_folder=os.path.join(os.path.dirname(__file__), '..', 'static')
)
CORS(app)

vision_client = vision.ImageAnnotatorClient()

# ───────────────────────────────────────────────────────────────
# Utility Functions
# ───────────────────────────────────────────────────────────────

def resize_image(image: np.ndarray, max_dim: int = MAX_IMAGE_DIM) -> np.ndarray:
    h, w = image.shape[:2]
    scale = min(max_dim / max(h, w), 1.0)
    return cv2.resize(image, (int(w * scale), int(h * scale))) if scale < 1.0 else image

def annotate_image(image: np.ndarray, annotations) -> np.ndarray:
    for annotation in annotations:
        if not any(char.isdigit() for char in annotation.description):
            continue
        vertices = [(v.x, v.y) for v in annotation.bounding_poly.vertices]
        if len(vertices) == 4:
            cv2.rectangle(image, vertices[0], vertices[2], (0, 255, 0), 2)
            cv2.putText(image, annotation.description, vertices[0], cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
    return image

def extract_numeric_data(annotations) -> list:
    def compute_area(annotation):
        vertices = annotation.bounding_poly.vertices
        if len(vertices) == 4:
            width = abs(vertices[1].x - vertices[0].x)
            height = abs(vertices[2].y - vertices[1].y)
            return width * height
        return 0

    sorted_annotations = sorted(annotations, key=compute_area, reverse=True)

    numbers = []
    for annotation in sorted_annotations:
        text = annotation.description.lstrip("0").strip()
        cleaned = text.replace(",", ".")
        if cleaned.replace(".", "", 1).isdigit():
            try:
                value = float(cleaned)
                numbers.append({
                    "original": text,
                    "converted_bgn": round(value * CONVERSION_RATE, 2)
                })
            except ValueError:
                continue

    return merge_split_numbers(numbers)

def merge_split_numbers(words: list) -> list:
    merged, skip = [], False
    for i, word in enumerate(words):
        if skip:
            skip = False
            continue
        if i + 1 < len(words) and word['original'].isdigit() and words[i + 1]['original'].isdigit():
            merged_num = f"{word['original']}.{words[i + 1]['original']}"
            merged.append({
                "original": merged_num,
                "converted_bgn": round(float(merged_num) * CONVERSION_RATE, 2)
            })
            skip = True
        else:
            merged.append(word)
    return merged

def encode_image_to_base64(image: np.ndarray) -> str:
    _, buffer = cv2.imencode('.jpg', image)
    return base64.b64encode(buffer).decode('utf-8')

# ───────────────────────────────────────────────────────────────
# Routes
# ───────────────────────────────────────────────────────────────

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_images():
    results, annotated_images = [], []

    for image_file in request.files.getlist("images"):
        with tempfile.NamedTemporaryFile(delete=True, suffix='.png') as tmp:
            image_file.save(tmp.name)
            image = np.array(Image.open(tmp.name).convert("RGB"))
            image = resize_image(image)

            with open(tmp.name, 'rb') as f:
                content = f.read()

            response = vision_client.text_detection(image=vision.Image(content=content))
            annotations = response.text_annotations[1:]  # Skip full block

            annotated = annotate_image(image.copy(), annotations)
            extracted = extract_numeric_data(annotations)

            results.append(extracted)
            annotated_images.append(encode_image_to_base64(annotated))

    return jsonify({
        "results": results,
        "annotated_images": annotated_images
    })

# ───────────────────────────────────────────────────────────────

if __name__ == '__main__':
    app.run(debug=False)
