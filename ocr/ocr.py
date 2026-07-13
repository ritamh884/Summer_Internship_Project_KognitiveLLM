import cv2
import fitz
import pytesseract
import numpy as np
from PIL import Image

# Tesseract Path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def pdf_to_image(pdf_path):

    doc = fitz.open(pdf_path)

    images = []

    for page_num in range(len(doc)):

        page = doc.load_page(page_num)

        pix = page.get_pixmap(matrix=fitz.Matrix(4, 4))

        img = Image.frombytes(
            "RGB",
            [pix.width, pix.height],
            pix.samples
        )

        img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

        images.append(img)

    return images


def preprocess(image):

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Noise removal
    gray = cv2.bilateralFilter(gray, 11, 17, 17)

    # Sharpen image
    kernel = np.array([[0,-1,0],
                       [-1,5,-1],
                       [0,-1,0]])

    gray = cv2.filter2D(gray, -1, kernel)

    # Adaptive Threshold
    thresh = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,
        2
    )

    return thresh


def extract_text(file_path):

    full_text = ""

    if file_path.lower().endswith(".pdf"):

        pages = pdf_to_image(file_path)

        for i, image in enumerate(pages):

            processed = preprocess(image)

            cv2.imwrite(f"processed_page_{i+1}.png", processed)

            config = r'--oem 3 --psm 6'

            text = pytesseract.image_to_string(
                processed,
                config=config,
                lang="eng"
            )

            full_text += "\n" + text

    else:

        image = cv2.imread(file_path)

        processed = preprocess(image)

        cv2.imwrite("processed_image.png", processed)

        config = r'--oem 3 --psm 6'

        full_text = pytesseract.image_to_string(
            processed,
            config=config,
            lang="eng"
        )

    return full_text