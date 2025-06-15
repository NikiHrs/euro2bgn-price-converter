# Price Scanner (EUR → BGN OCR)

A web application for scanning prices from images using the Google Cloud Vision API. It detects numeric values (e.g., prices) and converts them from **EUR to BGN** using a fixed conversion rate (**1 EUR = 1.95583 BGN**).

The app is optimized for mobile and supports camera input and multi-image uploads. Images are annotated with OCR results and presented with the extracted numbers and their BGN equivalents.

<img width="322" alt="Screenshot 2025-06-15 at 22 33 40" src="https://github.com/user-attachments/assets/53743522-da31-4a05-9694-ff4f57b5fb01" />

---

## Features

- Capture images via camera
- Automatically detects numbers using Google Cloud Vision OCR
- Converts EUR values to BGN using a fixed exchange rate (1.95583)
- Annotates and returns the processed image
- Mobile-friendly frontend

---

## Tech Stack

| Component     | Technology                             |
|---------------|----------------------------------------|
| Frontend      | HTML, JavaScript                       |
| Backend       | Python (Flask)                         |
| OCR Service   | Google Cloud Vision API                |
| Image Handling| OpenCV                                 |

---

## Requirements

- Python 3.8+
- A valid Google Cloud Platform (GCP) service account with Vision API access
- `GOOGLE_APPLICATION_CREDENTIALS` environment variable pointing to your service account key file

---

## Installation

1. **Clone the repository:**

```bash
git clone https://github.com/your-org/price-scanner.git
cd price-scanner
```

2. **Create and activate a virtual environment:**

```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

4. **Set up Google Cloud credentials:**

Make sure you have a service account key file with `Vision API` access.

```bash
export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"
```

On Windows:

```cmd
set GOOGLE_APPLICATION_CREDENTIALS="C:\path\to\your\keyfile.json"
```

---

## How to Run

1. Navigate to the server directory:

```bash
cd server
```

2. Start the Flask development server:

```bash
python app.py
```

3. Open your browser and go to:

```
http://127.0.0.1:5000
```


---

## Google Cloud Vision Integration

- Images are uploaded via the frontend and stored temporarily
- The backend sends the image content to the Cloud Vision API
- Text detection is performed using `image_annotator_client.document_text_detection()`
- Detected numbers are extracted using regex and converted to BGN
- The results are annotated on the image and returned as base64-encoded strings

---

## Deployment

This app can be deployed using any Python-compatible hosting environment that supports:

- Google Cloud credentials
- External HTTP requests to the Cloud Vision API

Options include:

- Google Cloud Run
- Render

Make sure to set the environment variable for credentials securely.

---

## License

This project is licensed under the MIT License.

---

## Credits

This project was extensively built and iterated using VibeCode.
