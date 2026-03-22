import cv2
import numpy as np
from utils import convert_pixels_to_m2, resize_image

def analyse_rooftop(pil_img):
    img = np.array(pil_img)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    img = resize_image(img)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)

    thresh1 = cv2.adaptiveThreshold(
        blurred, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY_INV, 21, 10
    )
    _, thresh2 = cv2.threshold(
        blurred, 0, 255,
        cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU
    )

    combined = cv2.bitwise_or(thresh1, thresh2)

    kernel = np.ones((7, 7), np.uint8)
    closed = cv2.morphologyEx(combined, cv2.MORPH_CLOSE, kernel)
    opened = cv2.morphologyEx(closed, cv2.MORPH_OPEN, kernel)

    contours, _ = cv2.findContours(opened, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        return np.zeros_like(gray), 0, None

    min_area = img.shape[0] * img.shape[1] * 0.05
    valid_contours = [c for c in contours if cv2.contourArea(c) > min_area]

    if not valid_contours:
        return np.zeros_like(gray), 0, None

    largest = max(valid_contours, key=cv2.contourArea)

    mask = np.zeros_like(gray)
    cv2.drawContours(mask, [largest], -1, 255, thickness=cv2.FILLED)

    area_m2 = convert_pixels_to_m2(mask)

    overlay = create_overlay(img, mask)

    return mask, area_m2, overlay


def create_overlay(img, mask):
    overlay = img.copy()
    colored_mask = np.zeros_like(img)
    colored_mask[mask == 255] = [0, 255, 100]
    blended = cv2.addWeighted(overlay, 0.7, colored_mask, 0.3, 0)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(blended, contours, -1, (0, 200, 80), 2)
    result = cv2.cvtColor(blended, cv2.COLOR_BGR2RGB)
    return result
