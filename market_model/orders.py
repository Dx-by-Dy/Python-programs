import numpy as np


class Config():
    time = 0
    scale_of_time_distibution = 8

    count_of_price_levels = 21
    probability_of_binomial_distibution_for_price_levels = 0.5

    probability_of_ask_side = 0.5

    probability_of_market_order = 0.16
    mean_volume_for_market_orders = 30
    standard_deviation_of_volume_for_market_orders = 1

    probability_of_limit_order = 0.8
    probability_of_trade_for_limit_order = 0.05
    # intensity_of_distibution_levels_for_limit_order = 0.1
    mean_volume_for_limit_orders = 10
    standard_deviation_of_volume_for_limit_orders = 1
    probability_of_FOK_type = 0.1
    probability_of_IOC_type = 0.1

    intensity_of_distibution_levels_for_cancel_order = 1
    mean_volume_for_cancel_orders = 10
    standard_deviation_of_volume_for_cancel_orders = 1


class MarketOrder():
    def __init__(self, time, side, volume) -> None:
        self.time = time
        self.side = side
        self.volume = volume

    def __str__(self):
        return f"MarketOrder[time={self.time}, side={self.side}, volume={self.volume}]"


class LimitOrder():
    def __init__(self, time, side, is_trade, level, volume, _type) -> None:
        self.time = time
        self.side = side
        self.is_trade = is_trade
        self.level = level
        self.volume = volume
        self._type = _type

    def __str__(self):
        return f"LimitOrder[time={self.time}, side={self.side}, is_trade={self.is_trade}, level={self.level}, volume={self.volume}, type={self._type}]"


class CancelOrder():
    def __init__(self, time, side, level, volume) -> None:
        self.time = time
        self.side = side
        self.level = level
        self.volume = volume

    def __str__(self):
        return f"CancelOrder[time={self.time}, side={self.side}, level={self.level}, volume={self.volume}]"


class OrderGenerator():
    def __init__(self, config, rng) -> None:
        self.rng = rng

        self.scale_of_time_distibution = config.scale_of_time_distibution
        self.time = config.time

        self.count_of_price_levels = config.count_of_price_levels
        self.probability_of_binomial_distibution_for_price_levels = config.probability_of_binomial_distibution_for_price_levels

        self.probability_of_ask_side = config.probability_of_ask_side

        self.probability_of_market_order = config.probability_of_market_order
        self.mean_volume_for_market_orders = config.mean_volume_for_market_orders
        self.standard_deviation_of_volume_for_market_orders = config.standard_deviation_of_volume_for_market_orders

        self.probability_of_limit_order = config.probability_of_limit_order
        self.probability_of_trade_for_limit_order = config.probability_of_trade_for_limit_order
        self.mean_volume_for_limit_orders = config.mean_volume_for_limit_orders
        self.standard_deviation_of_volume_for_limit_orders = config.standard_deviation_of_volume_for_limit_orders
        self.probability_of_FOK_type = config.probability_of_FOK_type
        self.probability_of_IOC_type = config.probability_of_IOC_type
        # self.intensity_of_distibution_levels_for_limit_order = config.intensity_of_distibution_levels_for_limit_order

        self.intensity_of_distibution_levels_for_cancel_order = config.intensity_of_distibution_levels_for_cancel_order
        self.mean_volume_for_cancel_orders = config.mean_volume_for_cancel_orders
        self.standard_deviation_of_volume_for_cancel_orders = config.standard_deviation_of_volume_for_cancel_orders

        self.unif, self.iter_unif = [], 0
        self.bin, self.iter_bin = [], 0
        self.expo, self.iter_expo = [], 0
        self.norm_market, self.norm_limit, self.norm_cancel, self.iter_norm_market, self.iter_norm_limit, self.iter_norm_cancel = [], [], [], 0, 0, 0
        self.size_gen = 1000000

    def get_uniform(self):
        if len(self.unif) == 0 or len(self.unif) <= self.iter_unif:
            self.unif = self.rng.uniform(0, 1, self.size_gen)
            self.iter_unif = 0
        self.iter_unif += 1
        return self.unif[self.iter_unif - 1]
    
    def get_normal_market(self):
        if len(self.norm_market) == 0 or len(self.norm_market) <= self.iter_norm_market:
            self.norm_market = np.round(self.rng.normal(self.mean_volume_for_market_orders, self.standard_deviation_of_volume_for_market_orders, self.size_gen), 3)
            self.iter_norm_market = 0
        self.iter_norm_market += 1
        return self.norm_market[self.iter_norm_market - 1]
    
    def get_normal_limit(self):
        if len(self.norm_limit) == 0 or len(self.norm_limit) <= self.iter_norm_limit:
            self.norm_limit = np.round(self.rng.normal(self.mean_volume_for_limit_orders, self.standard_deviation_of_volume_for_limit_orders, self.size_gen), 3)
            self.iter_norm_limit = 0
        self.iter_norm_limit += 1
        return self.norm_limit[self.iter_norm_limit - 1]
    
    def get_normal_cancel(self):
        if len(self.norm_cancel) == 0 or len(self.norm_cancel) <= self.iter_norm_cancel:
            self.norm_cancel = np.round(self.rng.normal(self.mean_volume_for_cancel_orders, self.standard_deviation_of_volume_for_cancel_orders, self.size_gen), 3)
            self.iter_norm_cancel = 0
        self.iter_norm_cancel += 1
        return self.norm_cancel[self.iter_norm_cancel - 1]
    
    def get_binomial(self):
        if len(self.bin) == 0 or len(self.bin) <= self.iter_bin:
            self.bin = self.rng.binomial(2 * self.count_of_price_levels - 1, self.probability_of_binomial_distibution_for_price_levels, self.size_gen)
            self.iter_bin = 0
        self.iter_bin += 1
        return self.bin[self.iter_bin - 1]
    
    def get_exponential(self):
        if len(self.expo) == 0 or len(self.expo) <= self.iter_expo:
            self.expo = self.rng.exponential(self.scale_of_time_distibution, self.size_gen)
            self.iter_expo = 0
        self.iter_expo += 1
        return self.expo[self.iter_expo - 1]

    def generate_market_order(self):
        side_type = "ask" if self.get_uniform() < self.probability_of_ask_side else "bid"
        volume = self.get_normal_market()
        return  MarketOrder(self.time, side_type, volume)
    
    def generate_limit_order(self):
        type_limit_order_id = self.get_uniform()
        if type_limit_order_id < self.probability_of_FOK_type:
            type_limit_order_id = "FOK"
        elif type_limit_order_id < self.probability_of_IOC_type + self.probability_of_FOK_type:
            type_limit_order_id = "IOC"
        else:
            type_limit_order_id = "GTC"

        level = self.get_binomial()
        if level - self.count_of_price_levels < 0:
            side_type = "bid"
            level = self.count_of_price_levels - level % self.count_of_price_levels - 1
        else:
            side_type = "ask"
            level = level % self.count_of_price_levels

        is_trade = True if self.get_uniform() < self.probability_of_trade_for_limit_order else False
        volume = self.get_normal_limit()
        return LimitOrder(self.time, side_type, is_trade, level, volume, type_limit_order_id)
    
    def generate_cancel_order(self):
        level = self.get_binomial()
        if level - self.count_of_price_levels < 0:
            side_type = "bid"
            level = self.count_of_price_levels - level % self.count_of_price_levels - 1
        else:
            side_type = "ask"
            level = level % self.count_of_price_levels

        volume = self.get_normal_cancel()
        return CancelOrder(self.time, side_type, level, volume)

    def generate_order(self):
        self.time = round(self.time + self.get_exponential(), 3)

        order_type_id = self.get_uniform()

        if order_type_id < self.probability_of_market_order:
            return self.generate_market_order()
        elif order_type_id < self.probability_of_limit_order + self.probability_of_market_order:
            return self.generate_limit_order()
        else:
            return self.generate_cancel_order()
        

#поменять все на decimal