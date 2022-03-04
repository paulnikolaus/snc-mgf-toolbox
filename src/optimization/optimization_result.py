from typing import List, Set


class OptimizationResult(object):
    def __init__(self, opt_x: List[float], obj_value: float, heuristic=""):
        self.opt_x = opt_x
        self.obj_value = obj_value
        self.heuristic = heuristic

    def __lt__(self, other):
        return self.obj_value < other.obj_value

    def __str__(self) -> str:
        return f"{self.heuristic}: obj_value = {self.obj_value}, " \
               f"x = {self.opt_x}"


class OptimizationGPSResult(object):
    def __init__(self, opt_m: Set[int], opt_x: List[float], obj_value: float):
        self.opt_m = opt_m
        self.opt_x = opt_x
        self.obj_value = obj_value

    def __str__(self) -> str:
        return f"obj_value = {self.obj_value}, M = {self.opt_m}, " \
               f"x = {self.opt_x}"
