from PIL import Image
import pytesseract
import cv2
import numpy as np

def preprocess_image(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return thresh

def extract_text(image_path):
    processed_image = preprocess_image(image_path)
    text = pytesseract.image_to_string(processed_image)
    return text

def extract_text_from_image(image):
    text = pytesseract.image_to_string(image)
    return text

def get_text_from_image_file(image_path):
    image = Image.open(image_path)
    text = extract_text(image_path)
    return text.strip()