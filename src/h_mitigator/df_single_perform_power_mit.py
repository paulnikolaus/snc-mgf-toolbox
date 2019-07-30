"""Compute performance standard_bound and write into csv file"""

from typing import List

import pandas as pd

from bound_evaluation.data_frame_to_csv import data_frame_to_csv
from h_mitigator.optimize_mitigator import OptimizeMitigator
from h_mitigator.single_server_mit_perform import SingleServerMitPerform
from nc_arrivals.arrival_distribution import ArrivalDistribution
from nc_arrivals.markov_modulated import MMOOFluid
from nc_arrivals.qt import DM1, MD1
from nc_operations.perform_enum import PerformEnum
from nc_server.constant_rate_server import ConstantRateServer
from optimization.opt_method import OptMethod
from optimization.optimize import Optimize
from utils.perform_param_list import PerformParamList

# import sys
# import os
# Necessary to make it executable in terminal
# sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)),
#                              os.pardir))


def single_server_df(arr_list: List[ArrivalDistribution],
                     ser_list: List[ConstantRateServer], opt_method: OptMethod,
                     perform_param_list: PerformParamList) -> pd.DataFrame:
    """
    Compute output standard_bound for T in T_list and write into dataframe
    Args:
        arr_list: Arrival object list
        ser_list: Service object list
        opt_method: method name as string, GS or PS
        perform_param_list: list of performance parameter values

    Returns:
        dataframe
    """

    standard_bound = [0.0] * len(perform_param_list)
    new_bound = [0.0] * len(perform_param_list)

    for _i in range(len(perform_param_list)):
        setting = SingleServerMitPerform(
            arr=arr_list[0],
            const_rate=ser_list[0],
            perform_param=perform_param_list.get_parameter_at_i(_i))

        if opt_method == OptMethod.GRID_SEARCH:
            standard_bound[_i] = Optimize(setting=setting).grid_search(
                bound_list=[(0.1, 4.0)], delta=0.1)
            new_bound[_i] = OptimizeMitigator(
                setting_h_mit=setting).grid_search(bound_list=[(0.1, 4.0),
                                                               (0.9, 8.0)],
                                                   delta=0.05)

        elif opt_method == OptMethod.PATTERN_SEARCH:
            standard_bound[_i] = Optimize(setting=setting).pattern_search(
                start_list=[0.5], delta=3.0, delta_min=0.01)
            new_bound[_i] = OptimizeMitigator(
                setting_h_mit=setting).pattern_search(start_list=[0.5, 2.0],
                                                      delta=3.0,
                                                      delta_min=0.01)
        else:
            raise NameError(
                f"Optimization parameter {opt_method} is infeasible")

    delay_bounds_df = pd.DataFrame(
        {
            "standard_bound": standard_bound,
            "h_mit_bound": new_bound
        },
        index=perform_param_list.values_list)
    delay_bounds_df = delay_bounds_df[["standard_bound", "h_mit_bound"]]

    return delay_bounds_df


if __name__ == '__main__':
    OUTPUT_LIST = PerformParamList(perform_metric=PerformEnum.OUTPUT,
                                   values_list=range(4, 15))

    print(
        data_frame_to_csv(prefix="single_",
                          data_frame_creator=single_server_df,
                          arr_list=[DM1(lamb=3.8, n=1)],
                          ser_list=[ConstantRateServer(rate=3.0)],
                          perform_param_list=OUTPUT_LIST,
                          opt_method=OptMethod.GRID_SEARCH))

    print(
        data_frame_to_csv(
            prefix="single_",
            data_frame_creator=single_server_df,
            arr_list=[MMOOFluid(mu=8.0, lamb=12.0, burst=3.0, n=1)],
            ser_list=[ConstantRateServer(rate=1.5)],
            perform_param_list=OUTPUT_LIST,
            opt_method=OptMethod.GRID_SEARCH))

    RATE_1 = ConstantRateServer(rate=1.0)

    print(
        data_frame_to_csv(prefix="single_",
                          data_frame_creator=single_server_df,
                          arr_list=[MD1(lamb=0.5, mu=1.0)],
                          ser_list=[RATE_1],
                          perform_param_list=OUTPUT_LIST,
                          opt_method=OptMethod.GRID_SEARCH))
