import numpy as np
import matplotlib.pyplot as plt

import application_rules


def stabilization_plot_analyis(power, h2_capacity, delta_list, batto, fuel_cell):
    for i in range(len(power)):
        stabilization_list = np.array([])
        for j in range(len(h2_capacity)):
            bat_charge = np.array([0])
            h2_charge = np.array([0])

            delta_after = np.array([0])
            delta_res = np.array([0])

            delta_after, bat_charge, h2_charge = application_rules.application_seq(delta_list, delta_after, delta_res,
                                                                                   bat_charge,
                                                                                   h2_charge, power[i],
                                                                                   h2_capacity[j],
                                                                                   batto.eff_bat,
                                                                                   batto.eff_electrolysis,
                                                                                   fuel_cell.eff, power[i])

            stabilization = (np.average(abs(delta_after[3:-1])) - np.average(abs(delta_list[2:-2]))) / np.average(
                abs(delta_list[2:-2])) * 100
            stabilization_list = np.append(stabilization_list, stabilization)
        plt.plot(h2_capacity, stabilization_list, label="Battolyser power= " + str(power[i]))
    plt.xlabel("H2 capacity [MW]")
    plt.ylabel("stabilization [%]")
    plt.legend()
    plt.show()
