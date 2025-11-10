import cv2
import numpy as np

def enhance_image(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return thresh

def resize_image(image, width):
    aspect_ratio = image.shape[1] / image.shape[0]
    height = int(width / aspect_ratio)
    resized_image = cv2.resize(image, (width, height))
    return resized_image

def save_processed_image(image, output_path):
    cv2.imwrite(output_path, image)

def process_image(image_path, output_path, width=800):
    enhanced_image = enhance_image(image_path)
    resized_image = resize_image(enhanced_image, width)
    save_processed_image(resized_image, output_path)