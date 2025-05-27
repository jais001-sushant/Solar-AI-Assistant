import random

def simulate_ai_rooftop_analysis():
    """
    Simulates an AI vision model analyzing a rooftop image.
    Returns structured output like roof type, shading, and confidence.
    """
    roof_types = ["flat", "gabled", "hipped", "sloped"]
    shading_levels = ["none", "low", "medium", "high"]

    return {
        "roof_type": random.choice(roof_types),
        "shading": random.choice(shading_levels),
        "confidence": round(random.uniform(0.75, 0.98), 2)
    }

