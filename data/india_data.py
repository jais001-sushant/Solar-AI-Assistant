CITY_SOLAR_DATA = {
    "Mumbai":      {"state": "Maharashtra", "sun_hours": 5.5, "lat": 19.07, "lon": 72.87},
    "Delhi":       {"state": "Delhi",       "sun_hours": 5.8, "lat": 28.61, "lon": 77.20},
    "Bangalore":   {"state": "Karnataka",   "sun_hours": 5.4, "lat": 12.97, "lon": 77.59},
    "Chennai":     {"state": "Tamil Nadu",  "sun_hours": 5.6, "lat": 13.08, "lon": 80.27},
    "Jaipur":      {"state": "Rajasthan",   "sun_hours": 6.2, "lat": 26.91, "lon": 75.78},
    "Hyderabad":   {"state": "Telangana",   "sun_hours": 5.5, "lat": 17.38, "lon": 78.48},
    "Kolkata":     {"state": "West Bengal", "sun_hours": 4.8, "lat": 22.57, "lon": 88.36},
    "Pune":        {"state": "Maharashtra", "sun_hours": 5.4, "lat": 18.52, "lon": 73.85},
    "Ahmedabad":   {"state": "Gujarat",     "sun_hours": 6.0, "lat": 23.02, "lon": 72.57},
    "Lucknow":     {"state": "Uttar Pradesh","sun_hours": 5.3, "lat": 26.84, "lon": 80.94},
    "Bhopal":      {"state": "Madhya Pradesh","sun_hours": 5.6, "lat": 23.25, "lon": 77.40},
    "Chandigarh":  {"state": "Punjab",      "sun_hours": 5.1, "lat": 30.73, "lon": 76.78},
    "Kochi":       {"state": "Kerala",      "sun_hours": 4.9, "lat": 9.93,  "lon": 76.26},
    "Nagpur":      {"state": "Maharashtra", "sun_hours": 5.7, "lat": 21.14, "lon": 79.08},
    "Surat":       {"state": "Gujarat",     "sun_hours": 5.9, "lat": 21.17, "lon": 72.83},
    "Jodhpur":     {"state": "Rajasthan",   "sun_hours": 6.5, "lat": 26.29, "lon": 73.01},
    "Patna":       {"state": "Bihar",       "sun_hours": 5.0, "lat": 25.59, "lon": 85.13},
    "Visakhapatnam":{"state": "Andhra Pradesh","sun_hours": 5.4,"lat": 17.68,"lon": 83.21},
    "Indore":      {"state": "Madhya Pradesh","sun_hours": 5.5, "lat": 22.71, "lon": 75.85},
    "Coimbatore":  {"state": "Tamil Nadu",  "sun_hours": 5.5, "lat": 11.01, "lon": 76.96},
}


STATE_ELECTRICITY_RATES = {
    "Maharashtra":      9.5,
    "Delhi":            8.0,
    "Karnataka":        7.5,
    "Tamil Nadu":       7.0,
    "Rajasthan":        6.5,
    "Telangana":        8.5,
    "West Bengal":      7.2,
    "Gujarat":          5.5,
    "Uttar Pradesh":    6.0,
    "Madhya Pradesh":   6.8,
    "Punjab":           7.0,
    "Kerala":           4.5,
    "Andhra Pradesh":   7.5,
    "Bihar":            6.5,
}


PANEL_TYPES = {
    "Polycrystalline": {
        "watt":        270,
        "cost":        6000,
        "efficiency":  0.15,
        "area_m2":     1.6,
        "lifespan":    25,
        "description": "Budget-friendly, good for large rooftops"
    },
    "Monocrystalline": {
        "watt":        350,
        "cost":        8000,
        "efficiency":  0.20,
        "area_m2":     1.7,
        "lifespan":    25,
        "description": "Most popular, best efficiency for homes"
    },
    "Bifacial": {
        "watt":        420,
        "cost":        12000,
        "efficiency":  0.23,
        "area_m2":     1.8,
        "lifespan":    30,
        "description": "Premium panels, captures light from both sides"
    }
}


SUBSIDY_SLABS = [
    {"max_kw": 3,    "rate": 0.40, "max_amount": 78000},
    {"max_kw": 10,   "rate": 0.20, "max_amount": None},
    {"max_kw": float("inf"), "rate": 0.0, "max_amount": 0},
]


MONTHLY_FACTORS = {
    "Jan": 0.85, "Feb": 0.90, "Mar": 1.00,
    "Apr": 1.05, "May": 1.10, "Jun": 0.95,
    "Jul": 0.80, "Aug": 0.82, "Sep": 0.90,
    "Oct": 0.95, "Nov": 0.88, "Dec": 0.83,
}


CO2_PER_KWH        = 0.716
CARBON_CREDIT_RATE = 1200


LABOR_COST_PER_PANEL    = 1500
MAINTENANCE_RATE        = 0.01
DEGRADATION_RATE        = 0.005
USABLE_ROOF_FACTOR      = 0.75