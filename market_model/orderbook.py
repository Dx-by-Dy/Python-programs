from orders import *

class TradeInfo():
    def __init__(self) -> None:
       self.ask_info = []
       self.bid_info = []

class Orderbook():
    def __init__(self, OG : OrderGenerator, TI : TradeInfo) -> None:
       self.ask = [0 for i in range(Config.count_of_price_levels)]
       self.bid = [0 for i in range(Config.count_of_price_levels)]
       self.TI = TI
       self.midprice_bias = 0

    def __str__(self):
        text = "Ask side\n"
        for level in range(Config.count_of_price_levels - 1, -1, -1):
            text += f"\t{level} : {self.ask[level]}\n"
        text += "Bid side\n"
        for level in range(Config.count_of_price_levels):
            text += f"\t{level} : {self.bid[level]}\n"
        return text

    def insert_limit_order(self, LO : LimitOrder):
        pass

    def insert_cancel_order(self, CO : CancelOrder):
        orderbook_side = getattr(self, CO.side)
        orderbook_side[CO.level] = max(orderbook_side[CO.level] - CO.volume, 0)

        if CO.level == 0 and orderbook_side[CO.level] == 0:
            self.reinit()#args

    def insert_market_order(self, MO : MarketOrder):
        orderbook_side = getattr(self, MO.side)
        volume = -MO.volume

        for level in range(Config.count_of_price_levels):
            volume += orderbook_side[level][1]
            if volume > 0:
                orderbook_side[level] = volume
                # TradeInfo
                break
            else:
                orderbook_side[level] = 0

            if level == Config.count_of_price_levels - 1:
                # TradeInfo
                # Warning! side empty
                pass


OG = OrderGenerator(Config(), np.random.default_rng(42))
O = Orderbook(OG, TradeInfo())

O.ask = [i * 10 for i in range(Config.count_of_price_levels)]
O.bid = [i * 10 for i in range(Config.count_of_price_levels)]

O.insert_cancel_order(OG.generate_cancel_order())
O.insert_cancel_order(OG.generate_cancel_order())
O.insert_cancel_order(OG.generate_cancel_order())

print(O)