import numpy as np


class Config():
    time = 0
    scale_of_time_distibution = 4

    count_of_price_levels = 10 - 1

    probability_of_ask_side = 0.5

    probability_of_market_order = 0.2
    mean_volume_for_market_orders = 10
    standart_deviation_of_volume_for_market_orders = 1

    probability_of_limit_order = 0.6
    intensity_of_distibution_levels_for_limit_order = 0.1
    mean_volume_for_limit_orders = 15
    standart_deviation_of_volume_for_limit_orders = 1
    probability_of_FOK_type = 0.1
    probability_of_IOK_type = 0.6

    intensity_of_distibution_levels_for_cancel_order = 1
    mean_volume_for_cancel_orders = 40
    standart_deviation_of_volume_for_cancel_orders = 1


class MarketOrder():
    def __init__(self, time, side, volume) -> None:
        self.time = time
        self.side = side
        self.volume = volume


class LimitOrder():
    def __init__(self, time, side, level, volume, _type) -> None:
        self.time = time
        self.side = side
        self.level = level
        self.volume = volume
        self._type = _type


class CancelOrder():
    def __init__(self, time, side, level, volume) -> None:
        self.time = time
        self.side = side
        self.level = level
        self.volume = volume


class OrderGenerator():
    def __init__(self, config, rng) -> None:
        self.rng = rng

        self.scale_of_time_distibution = config.scale_of_time_distibution
        self.time = config.time

        self.count_of_price_levels = config.count_of_price_levels

        self.probability_of_ask_side = config.probability_of_ask_side

        self.probability_of_market_order = config.probability_of_market_order
        self.mean_volume_for_market_orders = config.mean_volume_for_market_orders
        self.standart_deviation_of_volume_for_market_orders = config.standart_deviation_of_volume_for_market_orders

        self.probability_of_limit_order = config.probability_of_limit_order
        self.mean_volume_for_limit_orders = config.mean_volume_for_limit_orders
        self.standart_deviation_of_volume_for_limit_orders = config.standart_deviation_of_volume_for_limit_orders
        self.probability_of_FOK_type = config.probability_of_FOK_type
        self.probability_of_IOK_type = config.probability_of_IOK_type
        self.intensity_of_distibution_levels_for_limit_order = config.intensity_of_distibution_levels_for_limit_order

        self.intensity_of_distibution_levels_for_cancel_order = config.intensity_of_distibution_levels_for_cancel_order
        self.mean_volume_for_cancel_orders = config.mean_volume_for_cancel_orders
        self.standart_deviation_of_volume_for_cancel_orders = config.standart_deviation_of_volume_for_cancel_orders

    def generate_order(self):
        self.time += round(self.rng.exponential(self.scale_of_time_distibution, 1)[0], 3)

        order_type_id = self.rng.uniform(0, 1, 1)[0]
        side_type = "a" if self.rng.uniform(0, 1, 1)[0] < self.probability_of_ask_side else "b"

        if order_type_id < self.probability_of_market_order:
            volume = round(self.rng.normal(self.mean_volume_for_market_orders, self.standart_deviation_of_volume_for_market_orders, 1)[0], 3)
            return MarketOrder(self.time, side_type, volume)
        
        elif order_type_id < self.probability_of_limit_order + self.probability_of_market_order:
            type_limit_order_id = self.rng.uniform(0, 1, 1)[0]
            if type_limit_order_id < self.probability_of_FOK_type:
                type_limit_order_id = "FOK"
            elif type_limit_order_id < self.probability_of_IOK_type + self.probability_of_FOK_type:
                type_limit_order_id = "IOK"
            else:
                type_limit_order_id = "GTC"

            level = min(self.rng.poisson(self.intensity_of_distibution_levels_for_limit_order, 1)[0], self.count_of_price_levels)
            volume = round(self.rng.normal(self.mean_volume_for_limit_orders, self.standart_deviation_of_volume_for_limit_orders, 1)[0], 3)
            return LimitOrder(self.time, side_type, level, volume, type_limit_order_id)
        
        else:
            level = max(self.count_of_price_levels - self.rng.poisson(self.intensity_of_distibution_levels_for_cancel_order, 1)[0], 0)
            volume = round(self.rng.normal(self.mean_volume_for_cancel_orders, self.standart_deviation_of_volume_for_cancel_orders, 1)[0], 3)
            return CancelOrder(self.time, side_type, level, volume)


O = OrderGenerator(Config(), np.random.default_rng())