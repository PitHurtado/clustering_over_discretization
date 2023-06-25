"""Proccess of Aggregation of pixels"""
from typing import Optional

import numpy as np
from shapely.geometry import Polygon


class Meta_Pixel:
    """Class of aggregated pixels"""

    def __init__(self, pixel) -> None:
        self.pixels: list = [pixel]
        self.id: Optional[str] = pixel.id
        self.corner_down_left: Optional[tuple] = None
        self.corner_down_right: Optional[tuple] = None
        self.corner_up_right: Optional[tuple] = None
        self.corner_up_left: Optional[tuple] = None
        self.demand: list[float] = []

    def add_pixel(self, pixel) -> None:
        self.pixels.append(pixel)

    def merge_meta_pixel(self) -> None:
        self.corner_down_left = (
            min([p.corner_down_left[0] for p in self.pixels]),
            min([p.corner_down_left[1] for p in self.pixels]),
        )
        self.corner_down_right = (
            max([p.corner_down_right[0] for p in self.pixels]),
            min([p.corner_down_right[1] for p in self.pixels]),
        )
        self.corner_up_right = (
            max([p.corner_up_right[0] for p in self.pixels]),
            max([p.corner_up_right[1] for p in self.pixels]),
        )
        self.corner_up_left = (
            min([p.corner_up_left[0] for p in self.pixels]),
            max([p.corner_up_left[1] for p in self.pixels]),
        )

    def merge_demand(self) -> None:
        self.demand = []
        for p in self.pixels:
            for demand in p.demand:
                self.demand.append(demand)

    def construct_meta_pixel(self) -> None:
        self.merge_meta_pixel()
        self.merge_demand()

    def get_polygon(self):
        return Polygon(
            [
                self.corner_down_left,
                self.corner_down_right,
                self.corner_up_right,
                self.corner_up_left,
            ]
        )

    def get_avg_demand(self) -> float:
        return np.mean(self.demand)  # type: ignore

    def get_std_demand(self) -> float:
        return np.std(self.demand)  # type: ignore

    def get_n_customers(self) -> int:
        return len([i for i in self.demand if i != 0])

    def set_all_belong(self):
        for p in self.pixels:
            p.belong_meta_pixel = True


class Pixel:
    """Class of pixel"""

    def __init__(self, data: dict) -> None:
        self.id = data["id"]
        self.corner_down_left = data["corner_down_left"]
        self.corner_down_right = data["corner_down_right"]
        self.corner_up_right = data["corner_up_right"]
        self.corner_up_left = data["corner_up_left"]
        self.demand: list = [data["demand_daily"]]
        self.pixels_adyacent: list[Pixel] = []
        self.belong_meta_pixel: bool = False

    def add_customer(self, dict_customers: dict) -> None:
        self.demand.append(dict_customers["demand_daily"])

    def get_polygon(self):
        return Polygon(
            [
                self.corner_down_left,
                self.corner_down_right,
                self.corner_up_right,
                self.corner_up_left,
            ]
        )

    def get_avg_demand(self) -> float:
        return np.mean(self.demand)  # type: ignore

    def get_std_demand(self) -> float:
        return np.std(self.demand)  # type: ignore

    def get_n_customers(self) -> int:
        return len([i for i in self.demand if i != 0])

    def add_pixel_adjacent(self, adj):
        if adj.id != self.id and adj.get_total_demand() > 0:
            self.pixels_adyacent.append(adj)

    def get_total_demand(self) -> float:
        return sum(self.demand)
