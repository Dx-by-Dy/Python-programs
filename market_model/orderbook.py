from orders import *

class TradeInfo():
    def __init__(self) -> None:
       self.log = []
       self.batchs = []

    def __str__(self):
        text = 'Trade log:\n'
        for log in self.log:
            text += f'\tTrade[time={log[0]}, midprice_bias={log[1]}, volume={log[2]}, side={log[3]}]\n'
        return text

    def add_trade(self, time, midprice_bias, volume, side):
        if side == 'ask':
            self.log += [[time, midprice_bias, volume, side]]

    def reinit(self):
        self.batchs += [self.log]
        self.log = []


class Orderbook():
    def __init__(self, OG : OrderGenerator, TI : TradeInfo) -> None:
       self.ask = [0 for _ in range(Config.count_of_price_levels)]
       self.bid = [0 for _ in range(Config.count_of_price_levels)]
       self.OG = OG
       self.TI = TI
       self.last_time_reinit = 0
       self.time_reinit = 100
       self.ask_price_best_bias = 0

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

        if LO.is_trade:
            volume = LO.volume

            for level in range(LO.level):
                if orderbook_side[level] >= volume:
                    orderbook_side[level] = round(orderbook_side[level] - volume, 3)
                    self.TI.add_trade(LO.time, self.ask_price_best_bias, volume, LO.side)
                    volume = 0
                    break
                else:
                    volume -= orderbook_side[level]
                    self.TI.add_trade(LO.time, self.ask_price_best_bias, orderbook_side[level], LO.side)
                    orderbook_side[level] = 0

            if volume > 0:
                if LO._type == "GTC":
                    self.add_new_best_level(LO.side, volume)
                    setattr(self, LO.side, orderbook_side)
                elif LO._type == "IOC":
                    setattr(self, LO.side, orderbook_side)
                
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
                self.TI.add_trade(MO.time, self.ask_price_best_bias, volume, MO.side)
                break
            else:
                volume -= orderbook_side[level]
                self.TI.add_trade(MO.time, self.ask_price_best_bias, orderbook_side[level], MO.side)
                orderbook_side[level] = 0

        self.change_midprice(MO.side)

    def reinit(self):
        self.last_time_reinit += self.time_reinit
        self.ask_price_best_bias = 0
        self.TI.reinit()

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
        for _ in range(20000):
            self.insert_order(self.OG.generate_limit_order())
        self.OG.time = 0
        self.last_time_reinit = 0
        self.ask_price_best_bias = 0

    def start(self):
        for _ in range(1000000):
            self.insert_order(self.OG.generate_order())

O = Orderbook(OrderGenerator(Config(), np.random.default_rng(42)), TradeInfo())

O.init()
print(O)

O.start()
print(O)