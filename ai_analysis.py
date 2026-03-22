import anthropic
import base64
import json
import io

def encode_image_to_base64(pil_img):
    buffer = io.BytesIO()
    pil_img.save(buffer, format="JPEG")
    return base64.standard_b64encode(buffer.getvalue()).decode("utf-8")

def analyse_rooftop_with_ai(pil_img, api_key):
    client = anthropic.Anthropic(api_key=api_key)
    image_data = encode_image_to_base64(pil_img)

    prompt = """You are a solar energy expert analysing a rooftop image for solar panel installation.
Analyse this rooftop image and respond ONLY with a valid JSON object in exactly this format:

{
  "roof_type": "flat" | "gabled" | "hipped" | "sloped" | "mixed" | "unknown",
  "shading_level": "none" | "low" | "medium" | "high",
  "roof_condition": "excellent" | "good" | "fair" | "poor",
  "orientation": "south" | "north" | "east" | "west" | "mixed" | "unknown",
  "obstacles": ["list any visible obstacles like chimneys, vents, AC units"],
  "solar_suitability": "excellent" | "good" | "moderate" | "poor",
  "recommended_placement": "brief recommendation on where to place panels",
  "confidence": a number between 0.70 and 0.99,
  "notes": "any additional observations about the rooftop"
}

Be accurate and realistic. If the image is not clearly a rooftop, set solar_suitability to poor and confidence to 0.70."""

    try:
        response = client.messages.create(
            model="claude-opus-4-5",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/jpeg",
                                "data": image_data,
                            },
                        },
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ],
                }
            ],
        )

        raw = response.content[0].text.strip()

        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        raw = raw.strip()

        result = json.loads(raw)
        return result, None

    except json.JSONDecodeError:
        return None, "AI response was not valid JSON. Please try again."
    except anthropic.APIError as e:
        return None, f"API Error: {str(e)}"
    except Exception as e:
        return None, f"Unexpected error: {str(e)}"


def get_suitability_color(suitability):
    colors = {
        "excellent": "🟢",
        "good":      "🟡",
        "moderate":  "🟠",
        "poor":      "🔴"
    }
    return colors.get(suitability.lower(), "⚪")


def get_shading_adjustment(shading_level):
    adjustments = {
        "none":   1.00,
        "low":    0.95,
        "medium": 0.85,
        "high":   0.70
    }
    return adjustments.get(shading_level.lower(), 1.00)