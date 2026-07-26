# StrokeFlow
https://strokeflow.onrender.com/
Digitize handwritten signatures into clean, transparent PNG and scalable SVG files in seconds.

StrokeFlow is an OpenCV-powered web application that automatically removes paper backgrounds, isolates the signature, enhances the strokes, and exports professional digital signatures ready for documents, forms, presentations, or design software.

---

- Transparent PNG
- Editable SVG
- Smart automatic cropping
- Enhanced signature strokes
- Ready-to-use digital signature

---

## Features

- Automatic background removal
- Smart signature detection and cropping
- Noise reduction using OpenCV
- Stroke enhancement
- Transparent PNG export
- SVG vector conversion
- Responsive modern interface
- No registration required
- Works completely locally

---

## Built With

### Backend

- Python
- Flask
- OpenCV
- NumPy

### Frontend

- HTML5
- Tailwind CSS
- JavaScript

---

## How It Works

1. Upload a signature image.
2. Convert the image to grayscale.
3. Reduce image noise using bilateral filtering.
4. Apply Otsu thresholding to separate the signature.
5. Detect contours.
6. Automatically crop around the signature.
7. Clean the mask using morphological operations.
8. Sharpen signature strokes.
9. Generate:
   - Transparent PNG
   - SVG Vector

---

## Project Structure

```
StrokeFlow/
│
├── static/
│   ├── uploads/
│   └── favicon.svg
│
├── templates/
│   ├── index.html
│   ├── upload.html
│   └── result.html
│
├── image_processing.py
├── app.py
└── README.md
```

---

## Installation

Clone the repository

```bash
git clone https://github.com/HasimChaudhary/StrokeFlow.git
```

Move into the project

```bash
cd StrokeFlow
```

Run the application

```bash
python app.py
```

Open your browser

```
http://127.0.0.1:5000
```

---

## Supported Formats

### Input

- PNG
- JPG
- JPEG

### Output

- Transparent PNG
- SVG

---

## Future Improvements

- Signature color customization
- Batch processing
- AI-powered background detection
- Signature verification module
- PDF signature extraction
- Drag & Drop upload
- API support

---

## Why I Built This

Many online tools either require subscriptions, upload files to external servers, or provide inconsistent results. I wanted to build a lightweight application that performs the entire signature digitization process locally using computer vision techniques.

The focus of this project wasn't just creating another upload tool—it was understanding the image processing pipeline behind background removal, contour detection, morphological operations, and vector generation.

---


## Author

**Hasim Chaudhary**

B.Sc. Data Science

Interested in Computer Vision, AI, Machine Learning, and building practical software that solves real-world problems.

GitHub:
https://github.com/HasimChaudhary
