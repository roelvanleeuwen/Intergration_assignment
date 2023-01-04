import numpy as np
import constants


def h2_export(h2_export_without_tank, h2_charge_with_tank, h2_tank_capacity):
    h2_sold = np.array([])
    h2_diff = h2_export_without_tank - h2_charge_with_tank
    for n in range(2, len(h2_charge_with_tank) - 2):
        if h2_diff[n] - h2_diff[n - 1] > 0:
            h2_sold = np.append(h2_sold, h2_diff[n] - h2_diff[n - 1])
        else:
            h2_sold = np.append(h2_sold, 0)
    revenue = sum(h2_sold) / constants.h2_mass_energy_density * constants.h2_price_2030
    return revenue, h2_sold, h2_diff


def elec_export(elec_price, supply, bat_charge, h2_charge):
    elec_sold = np.array([])
    elec_revenue = 0

    for n in range(len(supply)):
        bat_diff = bat_charge[n] - bat_charge[n - 1]
        h2_diff = h2_charge[n] - h2_charge[n - 1]

        if bat_diff < 0:
            elec_sold = np.append(elec_sold, supply[n] - bat_diff)

        elif h2_diff < 0:
            elec_sold = np.append(elec_sold, supply[n] - h2_diff)

        else:
            elec_sold = np.append(elec_sold, supply[n])

        elec_revenue += elec_sold[n] * elec_price[n]
    return elec_revenue, elec_sold

