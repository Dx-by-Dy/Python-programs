from orders import *
from p_mid import conf_interval
from tqdm import tqdm

class TradeInfo():
    def __init__(self) -> None:
       self.log = []
       self.batchs = []

    def __str__(self):
        text = 'Trade log:\n'
        for log in self.log:
            text += f'\tTrade[time={log[0]}, midprice_bias={log[1]}, volume={log[2]}, side={log[3]}]\n'
        return text
    
    def print_last_bias(self):
        print(self.batchs[-1][-1][1])

    def add_trade(self, time, midprice_bias, volume, side):
        if side == 'ask':
            self.log += [[time, midprice_bias, volume, side]]

    def reinit(self):
        self.batchs += [self.log]
        self.log = []


class Orderbook():
    def __init__(self, OG : OrderGenerator, TI : TradeInfo, file_name) -> None:
       self.ask = [0 for _ in range(Config.count_of_price_levels)]
       self.bid = [0 for _ in range(Config.count_of_price_levels)]
       self.OG = OG
       self.TI = TI
       self.last_time_reinit = 0
       self.time_reinit = 100
       self.ask_price_best_bias = 0
       self.file = open(f"{file_name}.csv", "a")

       self.file.write("Best player price,Best model price lower,Best model price upper,Real price,Delta execution,Num of obs\n")

    def __str__(self):
        text = "Ask side\n"
        for level in range(Config.count_of_price_levels - 1, -1, -1):
            text += f"\t{level} : {self.ask[level]}\n"
        text += f'ask price best bias : {self.ask_price_best_bias}\n'
        text += "Bid side\n"
        for level in range(Config.count_of_price_levels):
            text += f"\t{level} : {self.bid[level]}\n"
        text += f"last time reinit : {self.last_time_reinit}"
        return text
    
    def add_new_best_level(self, side, volume):
        orderbook_side = getattr(self, side)
        orderbook_side = [volume] + orderbook_side
        self.ask_price_best_bias += (-1 if side == "ask" else 0)
        setattr(self, side, orderbook_side)
    
    def change_midprice(self, side):
        orderbook_side = getattr(self, side)

        for level in range(Config.count_of_price_levels):
            if orderbook_side[level] != 0:
                if level == 0:
                    break
                
                orderbook_side = orderbook_side[level:] + [0 for _ in range(level)]
                setattr(self, side, orderbook_side)
                self.ask_price_best_bias += (1 if side == "ask" else 0) * level
                break

    def insert_limit_order(self, LO : LimitOrder):
        orderbook_side = getattr(self, LO.side).copy()
        trades = []

        if LO.is_trade:
            volume = LO.volume

            for level in range(LO.level):
                if orderbook_side[level] >= volume:
                    orderbook_side[level] = round(orderbook_side[level] - volume, 3)
                    trades += [[LO.time, self.ask_price_best_bias + level, volume, LO.side]]
                    volume = 0
                    break
                else:
                    volume -= orderbook_side[level]
                    trades += [[LO.time, self.ask_price_best_bias + level, orderbook_side[level], LO.side]]
                    orderbook_side[level] = 0

            if LO._type == "GTC":
                if volume > 0: self.add_new_best_level(LO.side, volume)
                setattr(self, LO.side, orderbook_side)
                for trade in trades:
                    self.TI.add_trade(trade[0], trade[1], trade[2], trade[3])
            elif LO._type == "IOC":
                setattr(self, LO.side, orderbook_side)
                for trade in trades:
                    self.TI.add_trade(trade[0], trade[1], trade[2], trade[3])
            else:
                if volume == 0:
                    setattr(self, LO.side, orderbook_side)
                    for trade in trades:
                        self.TI.add_trade(trade[0], trade[1], trade[2], trade[3])
 
            self.change_midprice(LO.side)

        else:
            if LO._type == "GTC":
                orderbook_side[LO.level] = round(orderbook_side[LO.level] + LO.volume, 3)
                setattr(self, LO.side, orderbook_side)

    def insert_cancel_order(self, CO : CancelOrder):
        orderbook_side = getattr(self, CO.side)
        orderbook_side[CO.level] = max(round(orderbook_side[CO.level] - CO.volume, 3), 0)
        setattr(self, CO.side, orderbook_side)

        if CO.level == 0 and orderbook_side[CO.level] == 0:
            self.change_midprice(CO.side)

    def insert_market_order(self, MO : MarketOrder):
        orderbook_side = getattr(self, MO.side)
        volume = MO.volume

        for level in range(Config.count_of_price_levels):

            if orderbook_side[level] >= volume:
                orderbook_side[level] = round(orderbook_side[level] - volume, 3)
                self.TI.add_trade(MO.time, self.ask_price_best_bias + level, volume, MO.side)
                break
            else:
                volume -= orderbook_side[level]
                self.TI.add_trade(MO.time, self.ask_price_best_bias + level, orderbook_side[level], MO.side)
                orderbook_side[level] = 0

        self.change_midprice(MO.side)

    def player_best_price(self):
        if len(self.TI.batchs[-1]) == 0:
            return 0
        return self.TI.batchs[-1][-1][1]

    def write_res(self, res_model, player_best_price):
        self.file.write(f"{player_best_price},{res_model[0]},{res_model[1]},{self.ask_price_best_bias},{res_model[3]},{res_model[2]}\n")

    def reinit(self):
        self.TI.reinit()
        self.write_res(self.model(), self.player_best_price())
        self.last_time_reinit += self.time_reinit
        self.ask_price_best_bias = 0

    def model(self):
        trade_log = self.TI.batchs[-1]

        if len(trade_log) < 3:
            if len(trade_log) == 0:
                return 0, 0, 0, self.time_reinit
            else:
                return trade_log[-1][1], trade_log[-1][1], len(trade_log), self.last_time_reinit + self.time_reinit - trade_log[-1][0]

        times, prices = [], []
        last_time = self.last_time_reinit
        for trade in trade_log:
            times += [np.log(trade[0] - last_time)]
            last_time = trade[0]
            prices += [np.sign(trade[1]) * np.sqrt(abs(trade[1]))]

        inter = conf_interval(times, prices)

        return inter[0], inter[1], len(trade_log), self.last_time_reinit + self.time_reinit - trade_log[-1][0]

    def insert_order(self, order):

        if order.time > self.last_time_reinit + self.time_reinit:
            self.reinit()

        if isinstance(order, MarketOrder):
            self.insert_market_order(order)
        elif isinstance(order, CancelOrder):
            self.insert_cancel_order(order)
        else:
            self.insert_limit_order(order)

    def init(self):
        for _ in range(10000):
            self.insert_order(self.OG.generate_limit_order())
        for _ in range(20000):
            self.insert_order(self.OG.generate_order())
        self.OG.time = 0
        self.last_time_reinit = 0
        self.ask_price_best_bias = 0
        self.TI.batchs = []
        self.TI.log = []

    def start(self):
        for _ in tqdm(range(10 ** 7)):
            self.insert_order(self.OG.generate_order())

for i in range(1, 21):
    Config.scale_of_time_distibution = i / 2
    Config.probability_of_market_order = (i - 1) / 100 + 0.002
    Config.probability_of_limit_order = 0.8
    Config.probability_of_trade_for_limit_order = 0.01

    O = Orderbook(OrderGenerator(Config(), np.random.default_rng(42)), TradeInfo(), f"res_{i}_5")
    O.init()
    O.start()