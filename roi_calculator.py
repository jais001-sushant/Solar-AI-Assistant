from data.india_data import (
    PANEL_TYPES, MONTHLY_FACTORS,
    LABOR_COST_PER_PANEL, MAINTENANCE_RATE, DEGRADATION_RATE
)
from utils import calculate_co2_savings, calculate_subsidy, get_system_size_kw

def calculate_solar_estimates(area_m2, city_data, panel_type_name, electricity_rate):

    panel = PANEL_TYPES[panel_type_name]
    sun_hours_per_day = city_data["sun_hours"]
    sun_hours_per_year = sun_hours_per_day * 365

    # Panel Count
    usable_area = area_m2 * 0.75
    num_panels = int(usable_area // panel["area_m2"])

    if num_panels == 0:
        return None

    # System Size
    system_kw = get_system_size_kw(num_panels, panel["watt"])

    # Energy Output
    energy_kwh_year = num_panels * (panel["watt"] / 1000) * sun_hours_per_year
    energy_kwh_year = round(energy_kwh_year, 2)

    # Monthly Energy Breakdown
    monthly_energy = {
        month: round(energy_kwh_year * factor / 12, 2)
        for month, factor in MONTHLY_FACTORS.items()
    }

    # Costs
    panel_cost = num_panels * panel["cost"]
    labor_cost = num_panels * LABOR_COST_PER_PANEL
    install_cost = panel_cost + labor_cost

    # Subsidy
    subsidy = calculate_subsidy(system_kw)
    net_cost = install_cost - subsidy

    # Yearly Financials
    yearly_savings = round(energy_kwh_year * electricity_rate, 2)
    yearly_maintenance = round(net_cost * MAINTENANCE_RATE, 2)
    net_yearly_savings = round(yearly_savings - yearly_maintenance, 2)

    # Payback Period
    payback_years = round(net_cost / net_yearly_savings, 1) if net_yearly_savings > 0 else 0

    # ROI
    roi_percent = round((net_yearly_savings / net_cost) * 100, 2) if net_cost > 0 else 0

    # 25 Year Projection
    yearly_projection = []
    cumulative = -net_cost
    for year in range(1, panel["lifespan"] + 1):
        degradation = (1 - DEGRADATION_RATE) ** year
        adjusted_savings = net_yearly_savings * degradation
        cumulative = round(cumulative + adjusted_savings, 2)
        yearly_projection.append({
            "year": year,
            "cumulative": cumulative,
            "savings": round(adjusted_savings, 2)
        })

    # CO2 & Carbon Credits
    co2_kg, co2_tonnes, carbon_credit_value = calculate_co2_savings(energy_kwh_year)

    # Total Lifetime Savings
    total_lifetime_savings = yearly_projection[-1]["cumulative"]

    return {
        "num_panels":             num_panels,
        "system_kw":              system_kw,
        "panel_type":             panel_type_name,
        "energy_kwh_year":        energy_kwh_year,
        "monthly_energy":         monthly_energy,
        "panel_cost":             round(panel_cost, 2),
        "labor_cost":             round(labor_cost, 2),
        "install_cost":           round(install_cost, 2),
        "subsidy":                round(subsidy, 2),
        "net_cost":               round(net_cost, 2),
        "yearly_savings":         yearly_savings,
        "yearly_maintenance":     yearly_maintenance,
        "net_yearly_savings":     net_yearly_savings,
        "payback_years":          payback_years,
        "roi_percent":            roi_percent,
        "yearly_projection":      yearly_projection,
        "co2_kg":                 co2_kg,
        "co2_tonnes":             co2_tonnes,
        "carbon_credit_value":    carbon_credit_value,
        "total_lifetime_savings": total_lifetime_savings,
        "sun_hours":              sun_hours_per_day,
        "electricity_rate":       electricity_rate,
    }
