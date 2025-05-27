import numpy as np
import cv2

def convert_pixels_to_m2(mask, pixel_scale=0.05):
    """
    Converts the number of white pixels in the mask to square meters.
    pixel_scale: meters per pixel (default = 0.3 m/pixel)
    """
    white_pixel_count = np.sum(mask == 255)
    area_m2 = white_pixel_count * (pixel_scale ** 2)
    return round(area_m2, 2)

def resize_image(image, max_size=1024):
    """
    Resizes an image to a max width or height while maintaining aspect ratio.
    """
    h, w = image.shape[:2]
    scale = min(max_size / h, max_size / w)
    if scale < 1.0:
        new_size = (int(w * scale), int(h * scale))
        return cv2.resize(image, new_size)
    return image

def format_currency(value):
    """
    Formats a float as USD currency (e.g., $12,345.67)
    """
    return "${:,.2f}".format(value)
