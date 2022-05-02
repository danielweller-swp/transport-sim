# Compute CO2 emissions using the COPERT4 model
# and coefficients taken from https://link.springer.com/article/10.1007/s12159-016-0148-5

def get_co2_emissions_kg_per_100km(speed_kmh: float):
    a = -465.38
    b = 155.18
    c = 5.93
    d = 1888.82
    e = 1
    f = -0.22
    g = 0.05
    v = speed_kmh

    fuel_consumption_kg = (a + b*v + c*v*v + d/v)/(e + f*v + g*v*v)
    emission_factor=3.1643
    emission = fuel_consumption_kg * emission_factor
    return emission/10.0