from orders import *

class TradeInfo():
    def __init__(self) -> None:
       self.log = []

    def __str__(self):
        text = 'Trade log:\n'
        for log in self.log:
            text += f'\tTrade[time={log[0]}, midprice_bias={log[1]}, volume={log[2]}]\n'
        return text

    def add_trade(self, time, midprice_bias, volume):
        self.log += [[time, midprice_bias, volume]]


class Orderbook():
    def __init__(self, OG : OrderGenerator, TI : TradeInfo) -> None:
       self.ask = [0 for _ in range(Config.count_of_price_levels)]
       self.bid = [0 for _ in range(Config.count_of_price_levels)]
       self.OG = OG
       self.TI = TI
       self.midprice_bias = 0

    def __str__(self):
        text = "Ask side\n"
        for level in range(Config.count_of_price_levels - 1, -1, -1):
            text += f"\t{level} : {self.ask[level]}\n"
        text += f'midprice bias : {self.midprice_bias}\n'
        text += "Bid side\n"
        for level in range(Config.count_of_price_levels):
            text += f"\t{level} : {self.bid[level]}\n"
        return text
    
    def change_midprice(self, side):
        orderbook_side = getattr(self, side)

        for level in range(Config.count_of_price_levels):
            if orderbook_side[level] != 0:
                if level == 0:
                    break
                
                orderbook_side = orderbook_side[level:] + [0 for _ in range(level)]
                setattr(self, side, orderbook_side)
                self.midprice_bias += (1 if side == "ask" else -1) * level
                break

    def insert_limit_order(self, LO : LimitOrder):
        pass

    def insert_cancel_order(self, CO : CancelOrder):
        orderbook_side = getattr(self, CO.side)
        orderbook_side[CO.level] = max(orderbook_side[CO.level] - CO.volume, 0)
        setattr(self, CO.side, orderbook_side)

        if CO.level == 0 and orderbook_side[CO.level] == 0:
            self.change_midprice(CO.side)

    def insert_market_order(self, MO : MarketOrder):
        orderbook_side = getattr(self, MO.side)
        volume = MO.volume

        for level in range(Config.count_of_price_levels):

            if orderbook_side[level] >= volume:
                orderbook_side[level] -= volume
                self.TI.add_trade(MO.time, self.midprice_bias, volume)
                break
            else:
                volume -= orderbook_side[level]
                self.TI.add_trade(MO.time, self.midprice_bias, orderbook_side[level])
                orderbook_side[level] = 0

        self.change_midprice(MO.side)


OG = OrderGenerator(Config(), np.random.default_rng(42))
O = Orderbook(OG, TradeInfo())

O.ask = [i * 10 + 1 for i in range(Config.count_of_price_levels)]
O.bid = [i * 10 + 1 for i in range(Config.count_of_price_levels)]

print(O)

O.insert_market_order(OG.generate_market_order())
O.insert_market_order(OG.generate_market_order())
O.insert_market_order(OG.generate_market_order())

print(O)
print(O.TI)