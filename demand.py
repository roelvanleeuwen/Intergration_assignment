import numpy as np



def get_demand(days: int = 1):
    demand = np.array(
        [10645.875, 10333.3125, 10138.25, 10120.875, 10201, 10534.6875, 11548.375, 13037.25, 14265.5625, 14261.3125,
         13750.75, 13403.4375, 13185.625, 13597.875, 13946.125, 14373.8125, 14967.1875, 15439.5, 14828.91667,
         14234.875, 13736.75, 13191.625, 12558.25, 11935.8125])

    supply = 4714716.3  # yearly farm supply in MWh

    daily_demand = np.sum(demand)
    yearly_demand = daily_demand * 365

    fcsf = supply / yearly_demand  # farm capacity scaling factor

    demand_change = 2_500_000  # MWh

    dsf = 1 + (demand_change / yearly_demand)  # demand scaling factor for change of demand until 2030

    return np.tile(demand * fcsf * dsf, days)


def demand_scaled(days: int = 1):
    n_turbine = 70
    demand_ned_hour = np.array(
        [10645.875, 10333.3125, 10138.25, 10120.875, 10201, 10534.6875, 11548.375, 13037.25, 14265.5625, 14261.3125,
         13750.75, 13403.4375, 13185.625, 13597.875, 13946.125, 14373.8125, 14967.1875, 15439.5, 14828.91667,
         14234.875, 13736.75, 13191.625, 12558.25, 11935.8125])

    demand_day = np.sum(demand_ned_hour)
    demand_year = 365 * demand_day

    demand_change_2030 = 25_000_000  # MWh
    demand_change_factor_year_2030 = (demand_year+demand_change_2030)/demand_year

    power_rated_farm = 1000 # MW
    supply_year = 4714716.3 # MWh
    factor_supply_demand_year = supply_year/demand_year

    demand_farm_hour = factor_supply_demand_year * demand_ned_hour * demand_change_factor_year_2030
    demand_one_turbine = demand_farm_hour/n_turbine
    demand_period = np.tile(demand_one_turbine, days)
    return demand_period

