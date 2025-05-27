import cv2
import numpy as np
from utils import convert_pixels_to_m2, resize_image

def analyse_rooftop(pil_img):
    """
    Takes a PIL image of a rooftop, processes it to detect the rooftop area,
    and returns a binary mask + calculated usable area in square meters.
    """
    # Convert PIL to OpenCV (numpy array)
    img = np.array(pil_img)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    # Resize to optimize performance
    img = resize_image(img)

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Adaptive thresholding for better rooftop segmentation
    thresh = cv2.adaptiveThreshold(
        blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY_INV, 21, 10
    )

    # Morphological closing to fill holes
    kernel = np.ones((5, 5), np.uint8)
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    # Find largest contour (assumed rooftop)
    contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return np.zeros_like(gray), 0

    largest = max(contours, key=cv2.contourArea)

    # Create a mask of the rooftop
    mask = np.zeros_like(gray)
    cv2.drawContours(mask, [largest], -1, 255, thickness=cv2.FILLED)

    # Calculate area
    area_m2 = convert_pixels_to_m2(mask)

    return mask, area_m2
