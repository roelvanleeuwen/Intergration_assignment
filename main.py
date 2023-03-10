import numpy as np
import matplotlib.pyplot as plt

import devices
import stabilization
import supply
import demand
import application_rules
import constants
import revenue

batto1 = devices.Battolyser(1.5, 100, 10000000000000, 0.8, 0.85 * (1 - 0.18))
# batto1 = devices.Battolyser(1, 50, 1.5, 0.8, 0.85 * (1 - 0.18))
fuelcell1 = devices.Fuel_cell(1, 0.6)



start = 0
period = 365
data = supply.supply(start, period)
time = np.array(data["Time (UTC)"])
supply = np.array(data["P [MW]"].div(70).round(5))
price_list = np.array(data["Price [€/MWh]"])

demand = demand.demand_scaled(period)

delta_list = np.array(supply - demand)

print("GENERAL DATA")
print("Start of period in days since 01-01-2030= " + str(start))
print("Duration of period in days= " + str(period))
print("Battolyser power in MW= " + str(batto1.power))
print("Hydrogen storage capacity = " + str(batto1.h2_capacity))
print("")


'''
This block of code is to provide data on purely hydrogen storage in the tank and hydrogen usage in the fuel cell
'''
bat_charge = np.array([0])
h2_charge = np.array([0])

delta_after = np.array([0])
delta_res = np.array([0])
delta_after, bat_charge, h2_charge_with_tank, act_fuel_cell = application_rules.application_seq(delta_list, delta_after, delta_res,
                                                                                 bat_charge,
                                                                                 h2_charge, batto1.bat_capacity,
                                                                                 batto1.h2_capacity,
                                                                                 batto1.eff_bat,
                                                                                 batto1.eff_electrolysis,
                                                                                 fuelcell1.eff, batto1.power, fuelcell1.power)
print("Fuel cell energy conversion =" + str(act_fuel_cell))


'''
This block of code is to provide data on the unlimited hydrogen production 
'''
bat_charge_2 = np.array([0])
h2_charge_2 = np.array([0])

delta_after_2 = np.array([0])
delta_res_2 = np.array([0])
h2_export_without_tank = application_rules.application_seq(delta_list, delta_after_2, delta_res_2, bat_charge_2,
                                                           h2_charge_2, batto1.bat_capacity,
                                                           batto1.h2_export_capacity,
                                                           batto1.eff_bat, batto1.eff_electrolysis,
                                                           fuelcell1.eff, batto1.power, fuelcell1.power)[2]

'''
This block of code is to provide data on revenues of the system. First the hydrogen revenue. Second the 
electricity revenue. 
'''

h2_export_revenue, h2_sold, h2_diff = revenue.h2_export(h2_export_without_tank, h2_charge_with_tank, batto1.h2_capacity)
elec_revenue, elec_sold = revenue.elec_export(price_list, supply, bat_charge, h2_charge_with_tank)
print("REVENUE DATA")
print("h2 export revenue = " + str(h2_export_revenue))
print("electricity export revenue = " + str(elec_revenue))
print("total revenue = " + str(elec_revenue+h2_export_revenue*constants.additional_losses))
print("")


'''
This block of code is to provide data on the amount of stabilization that is obtained with the current system.
First the actual stabilization is obtained, then an analysis plot is made for different combinations of battolyser
power and hydrogen storage capacity.  
'''
stabilization_sys = (np.average(abs(delta_after[3:-1])) - np.average(abs(delta_list[2:-2]))) / np.average(
    abs(delta_list[2:-2])) * 100
power_list = np.arange(1, 5, 0.5)
h2_capacity_list = np.arange(1, 502, 25)
# stabilization.stabilization_plot_analyis(power_list, h2_capacity_list, delta_list, batto1, fuelcell1)
print("STABILIZATION DATA")
print("Stabilization of the system in % = " + str(stabilization_sys))

print(max(delta_list))

'''
This block of code shows different revenues for different battolyser, fuelcell combinations
'''
# batto_list = []
# fuelcell_list = []
# batto_power_list = np.arange(0.5, 7.5, 1)
# batto_h2_capacity_list = np.arange(1, 1001, 100)
# fuelcell_power_list = np.arange(0, 5, 1)
#
#
# for x in range(len(batto_h2_capacity_list)):
#     elec_revenue_list = np.array([])
#     h2_export_revenue_list = np.array([])
#     total_revenue_list = np.array([])
#     stabilization_sys_list = np.array([])
#     batto = devices.Battolyser(2, batto_h2_capacity_list[x], 10000000000000, 0.8, 0.85 * (1 - 0.18))
#     for y in range(len(fuelcell_power_list)):
#         fuelcell = devices.Fuel_cell(fuelcell_power_list[y], 0.6)
#
#         bat_charge = np.array([0])
#         h2_charge = np.array([0])
#
#         delta_after = np.array([0])
#         delta_res = np.array([0])
#         delta_after, bat_charge, h2_charge_with_tank, act_fuel_cell = application_rules.application_seq(delta_list,
#                                                                                                         delta_after,
#                                                                                                         delta_res,
#                                                                                                         bat_charge,
#                                                                                                         h2_charge,
#                                                                                                         batto.bat_capacity,
#                                                                                                         batto.h2_capacity,
#                                                                                                         batto.eff_bat,
#                                                                                                         batto.eff_electrolysis,
#                                                                                                         fuelcell.eff,
#                                                                                                         batto.power,
#                                                                                                         fuelcell.power)
#
#         bat_charge_2 = np.array([0])
#         h2_charge_2 = np.array([0])
#
#         delta_after_2 = np.array([0])
#         delta_res_2 = np.array([0])
#         h2_export_without_tank = application_rules.application_seq(delta_list, delta_after_2, delta_res_2, bat_charge_2,
#                                                                    h2_charge_2, batto.bat_capacity,
#                                                                    batto.h2_export_capacity,
#                                                                    batto.eff_bat, batto.eff_electrolysis,
#                                                                    fuelcell.eff, batto.power, fuelcell.power)[2]
#
#         h2_export_revenue, h2_sold, h2_diff = revenue.h2_export(h2_export_without_tank, h2_charge_with_tank,
#                                                                 batto1.h2_capacity)
#         elec_revenue, elec_sold = revenue.elec_export(price_list, supply, bat_charge, h2_charge_with_tank)
#
#         h2_export_revenue_list = np.append(h2_export_revenue_list, h2_export_revenue)
#         elec_revenue_list = np.append(elec_revenue_list, elec_revenue)
#         total_revenue_list = np.append(total_revenue_list, h2_export_revenue+elec_revenue)
#         stabilization_sys = (np.average(abs(delta_after[3:-1])) - np.average(abs(delta_list[2:-2]))) / np.average(
#             abs(delta_list[2:-2])) * 100
#         stabilization_sys_list = np.append(stabilization_sys_list, stabilization_sys)
#
#     # plt.plot(fuelcell_power_list, h2_export_revenue_list, label="h2_rev: Batto power= " + str(batto_power_list[x]))
#     # plt.plot(fuelcell_power_list, elec_revenue_list, label="elec_rev: Batto power= " + str(batto_power_list[x]))
#     # plt.plot(fuelcell_power_list, total_revenue_list, label="total rev: Batto power= " + str(batto_power_list[x]))
#
#     plt.plot(fuelcell_power_list, total_revenue_list, label="total rev: Batto power= " + str(batto_h2_capacity_list[x]))
#     plt.xlabel("fuelcell_power [MW]")
#     plt.ylabel("revenu [EUR]")
#
#     # plt.plot(fuelcell_power_list, stabilization_sys_list, label="total rev: Batto power= " + str(batto_power_list[x]))
#     # plt.xlabel("fuelcell_power [MW]")
#     # plt.ylabel("stailization [%]")
#
# plt.legend()
# plt.show()

'''
This block prints all the time variables that are useful
'''
# plt.plot(time[2:-2], supply[2:-2], label="supply", linestyle='--')
# plt.plot(time[2:-2], demand[2:-2], label="demand", linestyle='-')
# plt.plot(time[2:-2], delta_list[2:-2], label="destabilization", linestyle='-.')
# plt.plot(time[2:-2], delta_after[3:-1], label="stabilized", linestyle='-.')
# plt.plot(time[2:-2], bat_charge[2:-2], label="battery charge", linestyle='solid')
# plt.plot(time[2:-2], h2_charge_with_tank[2:-2], label="hydrogen charge of tank", linestyle=':')
# plt.plot(time[2:-2], h2_export_without_tank[2:-2], label="hydrogen pure export", linestyle='--')
# plt.plot(time[2:-2], h2_sold, label="hydrogen export", linestyle='--')

# plt.plot(time[2:-2], h2_charge_with_tank[2:-2], label="hydrogen charge of tank", linestyle='solid')
# plt.plot(time[2:-2], h2_export_without_tank[2:-2], label="hydrogen export instances", linestyle='--')
# plt.plot(time[2:-2], h2_diff[2:-2], label="hydrogen export - hydrogen charge", linestyle=':')
# plt.plot(time[2:-2], h2_sold, label="sold hydrogen", linestyle='-.')

# plt.grid()
# plt.legend()
# plt.show()
