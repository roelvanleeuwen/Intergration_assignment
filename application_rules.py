import numpy as np


def charge_bat(delta: float, delta_after: np.ndarray, delta_res: np.ndarray, bat_charge: np.ndarray, max_power: float,
               bat_capacity: float, eff_bat: float):
    delta_bat = 0
    if delta < max_power:  # check if the battolyser can handle delta
        delta_bat = delta
    elif delta > max_power:
        delta_bat = max_power

    if bat_charge[-1] + eff_bat * delta < bat_capacity:  # first fill the battery independent of hydrogen storage
        delta_after = np.append(delta_after, delta - delta_bat)  # delta when energy is stored
        charge_diff = delta_bat * eff_bat
        bat_charge = np.append(bat_charge, bat_charge[-1] + charge_diff)
        delta_res = np.append(delta_res, 0)  # there is no charge left for hydrogen

    elif bat_charge[
        -1] + eff_bat * delta >= bat_capacity:  # if too much delta is present there is a residual for hydrogen
        delta_bat = bat_capacity - bat_charge[-1]  # this is the input energy to the battery
        delta_after = np.append(delta_after, delta - delta_bat)
        charge_diff = delta_bat * eff_bat
        bat_charge = np.append(bat_charge, bat_capacity)
        delta_res = np.append(delta_res, delta - delta_bat)  # there is charge left to go to hydrogen

    # else:
    #     delta_after = np.append(delta_after, 30)
    return bat_charge, delta_after, delta_res


def charge_h2(delta_res: np.ndarray, delta_after: np.ndarray, h2_charge: np.ndarray, max_power: float,
              h2_capacity: float,
              eff_electrolysis: float):
    delta_h2 = 0
    delta = delta_res[-1]
    if delta < max_power:  # check if the battolyser can handle delta
        delta_h2 = delta
    elif delta > max_power:
        delta_h2 = max_power

    if h2_charge[-1] + eff_electrolysis * delta < h2_capacity:
        delta_after[-1] = 0
        charge_diff = delta_h2 * eff_electrolysis
        h2_charge = np.append(h2_charge, h2_charge[-1] + charge_diff)
        delta_res[-1] = 0  # there is no charge left

    elif h2_charge[
        -1] + eff_electrolysis * delta >= h2_capacity:  # if too much delta is present there is a residual for hydrogen
        delta_h2 = h2_capacity - h2_charge[-1]  # this is the input energy to the hydrogen
        delta_after[-1] = delta_res[-1] - delta_h2
        charge_diff = delta_h2 * eff_electrolysis
        h2_charge = np.append(h2_charge, h2_capacity)
        delta_res[-1] = delta_res[-1] - delta_h2

    # else:
    #     delta_after = np.append(delta_after, 60)

    return h2_charge, delta_after, delta_res


def deploy_bat(delta: np.ndarray, delta_after: np.ndarray, delta_res: np.ndarray, bat_charge: np.ndarray,
               max_power: float):
    delta_bat = 0
    delta = delta
    if abs(delta) < max_power:  # check if the battolyser can handle delta
        delta_bat = delta
    elif abs(delta) > max_power:
        delta_bat = -max_power

    if bat_charge[-1] + delta > 0:
        delta_bat = delta_bat
        delta_after = np.append(delta_after, 0)
        charge_diff = delta_bat
        bat_charge = np.append(bat_charge, bat_charge[-1] + charge_diff)
        delta_res = np.append(delta_res, 0)

    elif bat_charge[-1] + delta <= 0:
        delta_bat = -bat_charge[-1]
        delta_after = np.append(delta_after, delta + delta_bat)
        charge_diff = delta_bat
        bat_charge = np.append(bat_charge, 0)
        delta_res = np.append(delta_res, delta-delta_bat)
    # else:
    #     delta_after = np.append(delta_after, -30)
    return bat_charge, delta_after, delta_res


def deploy_h2(delta_res: np.ndarray, delta_after: np.ndarray, h2_charge: np.ndarray, eff_fuel_cell: float,
              max_power: float):
    delta_h2 = 0
    delta = delta_res[-1]
    if abs(delta) < max_power:  # check if the battolyser can handle delta
        delta_h2 = delta
    elif abs(delta) > max_power:
        delta_h2 = -max_power

    if h2_charge[-1] + delta / eff_fuel_cell > 0:  # enough hydrogen to only use hydrogen ; delta is negative
        # delta_h2 = delta # this is the output energy to the fuelcell
        delta_after[-1] = 0
        charge_diff = delta_h2 / eff_fuel_cell
        h2_charge = np.append(h2_charge, h2_charge[-1] + charge_diff)  # + charge_diff since delta is negative
        delta_res[-1] = 0

    elif h2_charge[-1] + delta / eff_fuel_cell <= 0:  # not enough hydrogen, delta_after is non-zero ; delta is negative
        delta_h2 = -h2_charge[-1]  # this is the output energy to the fuelcell
        delta_after[-1] = delta_after[-1] - delta_h2  # delta going to the battery
        charge_diff = delta_h2 / eff_fuel_cell
        h2_charge = np.append(h2_charge, 0)  # + charge_diff since delta is negative
        delta_res[-1] = 0

    # else:
    #     delta_after = np.append(delta_after, -60)

    return h2_charge, delta_after, delta_res


def idle(delta_after: np.ndarray, delta_res: np.ndarray, h2_charge: np.ndarray, bat_charge: np.ndarray):
    delta_after = np.append(delta_after, 0)
    delta_res = np.append(delta_res, 0)
    h2_charge = np.append(h2_charge, h2_charge[-1])
    bat_charge = np.append(bat_charge, bat_charge[-1])
    return h2_charge, bat_charge, delta_after, delta_res


def application_seq(delta_list: np.ndarray, delta_after: np.ndarray, delta_res: np.ndarray, bat_charge: np.ndarray,
                    h2_charge: np.ndarray,
                    bat_capacity: float, h2_capacity: float, eff_bat: float, eff_electrolysis: float,
                    eff_fuel_cell: float, max_power: float):
    for i in range(0, len(delta_list)-1):
        # print("i: " + str(i))
        delta = delta_list[i]
        # print("delta = " + str(delta))
        # print("h2 = " + str(h2_charge[i]))
        # print("bat =" + str(bat_charge[i]))
        if delta > 0:
            # print("option 1")
            # print("")
            # Charge battery
            bat_charge, delta_after, delta_res = charge_bat(delta, delta_after, delta_res, bat_charge, max_power,
                                                            bat_capacity, eff_bat)
            h2_charge, delta_after, delta_res = charge_h2(delta_res, delta_after, h2_charge, max_power, h2_capacity,
                                                          eff_electrolysis)
        elif delta < 0:
            # print("option 2")
            # print("")
            # Deploy battery
            bat_charge, delta_after, delta_res = deploy_bat(delta, delta_after, delta_res, bat_charge, max_power)
            h2_charge, delta_after, delta_res = deploy_h2(delta_res, delta_after, h2_charge, eff_fuel_cell, max_power)

        elif delta == 0:
            # print("option 3")
            # print("")
            # Idle
            h2_charge, bat_charge, delta_after, delta_res = idle(delta_after, delta_res, h2_charge, bat_charge)

    return delta_after, bat_charge, h2_charge


# delta_list = np.array([0, 100, 200, 300, 200, 100, -200, -500])
# delta_after = np.array([0])
# delta_res = np.array([0])
# bat_charge = np.array([0])
# h2_charge = np.array([0])
# bat_capacity = 1000
# h2_capacity = 1000
# eff_bat = 0.8
# eff_electrolysis = 0.8
# eff_fuel_cell = 0.65
# max_power = 1000
#
# delta_after, bat_charge, h2_charge = application_seq(delta_list, delta_after, delta_res, bat_charge, h2_charge,
#                                                      bat_capacity, h2_capacity,
#                                                      eff_bat, eff_electrolysis, eff_fuel_cell, max_power)
#
# print(delta_after)
