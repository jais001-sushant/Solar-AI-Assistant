import numpy as np
import cv2
from data.india_data import CARBON_CREDIT_RATE, CO2_PER_KWH

def convert_pixels_to_m2(mask, pixel_scale=0.05):
    white_pixels = np.sum(mask == 255)
    area_m2 = white_pixels * (pixel_scale ** 2)
    return round(area_m2, 2)

def resize_image(image, max_size=1024):
    h, w = image.shape[:2]
    scale = min(max_size / h, max_size / w)
    if scale < 1.0:
        new_size = (int(w * scale), int(h * scale))
        return cv2.resize(image, new_size)
    return image

def _format_indian_number(value):
    value = int(round(value))
    s = str(value)
    if len(s) <= 3:
        return s
    last3 = s[-3:]
    rest = s[:-3]
    groups = []
    while len(rest) > 2:
        groups.append(rest[-2:])
        rest = rest[:-2]
    if rest:
        groups.append(rest)
    groups.reverse()
    return f"{','.join(groups)},{last3}"

def format_inr(value):
    return f"₹{_format_indian_number(value)}"

def format_inr_pdf(value):
    return f"Rs.{_format_indian_number(value)}"

def calculate_co2_savings(energy_kwh):
    co2_kg = energy_kwh * CO2_PER_KWH
    co2_tonnes = co2_kg / 1000
    carbon_credit_value = co2_tonnes * CARBON_CREDIT_RATE
    return round(co2_kg, 2), round(co2_tonnes, 4), round(carbon_credit_value, 2)

def calculate_subsidy(total_kw):
    from data.india_data import SUBSIDY_SLABS
    if total_kw <= 3:
        subsidy = total_kw * 1000 * SUBSIDY_SLABS[0]["rate"]
        return min(subsidy, SUBSIDY_SLABS[0]["max_amount"])
    elif total_kw <= 10:
        base = 3 * 1000 * SUBSIDY_SLABS[0]["rate"]
        extra = (total_kw - 3) * 1000 * SUBSIDY_SLABS[1]["rate"]
        return min(base, SUBSIDY_SLABS[0]["max_amount"]) + extra
    else:
        base = 3 * 1000 * SUBSIDY_SLABS[0]["rate"]
        extra = 7 * 1000 * SUBSIDY_SLABS[1]["rate"]
        return min(base, SUBSIDY_SLABS[0]["max_amount"]) + extra

def get_system_size_kw(num_panels, panel_watt):
    return round((num_panels * panel_watt) / 1000, 2)