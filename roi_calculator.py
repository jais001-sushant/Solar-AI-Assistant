# roi_calculator.py

def calculate_solar_estimates(area_m2):
    # Constants (feel free to adjust)
    PANEL_AREA = 1.5  # m² per panel
    PANEL_WATT = 200  # watts per panel
    SUN_HOURS_PER_YEAR = 2856  # average sun hours/year
    INSTALLATION_COST_PER_PANEL = 8000  # ₹ per panel (includes panel + labor)
    ELECTRICITY_RATE = 3  # ₹ per kWh
    MAINTENANCE_RATE = 0.04  # 4% yearly maintenance
    CO2_SAVED_PER_KWH = 0.7  # kg CO2 saved

    # Basic calculations
    num_panels = int(area_m2 // PANEL_AREA)
    energy_output_kwh = num_panels * PANEL_WATT * (SUN_HOURS_PER_YEAR / 1000)
    install_cost = num_panels * INSTALLATION_COST_PER_PANEL
    yearly_maintenance = install_cost * MAINTENANCE_RATE
    yearly_savings = energy_output_kwh * ELECTRICITY_RATE

    payback_years = round(install_cost / yearly_savings, 2) if yearly_savings else 0
    co2_savings = energy_output_kwh * CO2_SAVED_PER_KWH

    roi_percent = ((yearly_savings - yearly_maintenance) / install_cost) * 100

    return {
        "area_m2": area_m2,
        "num_panels": num_panels,
        "energy_output_kwh": energy_output_kwh,
        "install_cost": install_cost,
        "yearly_maintenance": yearly_maintenance,
        "yearly_savings": yearly_savings,
        "payback_years": payback_years,
        "roi_percent": roi_percent,
        "co2_savings": co2_savings,
    }
