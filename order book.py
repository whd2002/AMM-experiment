import heapq

class Order:
    def __init__(self, user, quantity, price, order_type, is_buy):

        self.user = user
        self.quantity = quantity
        self.price = price
        self.order_type = order_type
        self.is_buy = is_buy

class Path:
    def __init__(self, from_user, to_storage, loss):

        self.from_user = from_user
        self.to_storage = to_storage
        self.loss = loss

class OrderBook:
    def __init__(self):
        self.buy_orders = []
        self.sell_orders = []
        self.paths = []

    def add_path(self, path):

        self.paths.append(path)

    def add_order(self, order):

        if order.is_buy:
            heapq.heappush(self.buy_orders, (-order.price, order))
        else:
            heapq.heappush(self.sell_orders, (order.price, order))

    def match_orders(self):

        transactions = []

        while self.buy_orders and self.sell_orders:
            buy_price, buy_order = heapq.heappop(self.buy_orders)
            sell_price, sell_order = heapq.heappop(self.sell_orders)


            if -buy_price >= sell_price:

                matched_path = self.get_best_path(buy_order.user, sell_order.user)
                if matched_path is None:
                    continue

                loss = matched_path.loss
                trade_quantity = min(buy_order.quantity, sell_order.quantity) * (1 - loss)


                transactions.append({
                    'buyer': buy_order.user,
                    'seller': sell_order.user,
                    'quantity': trade_quantity,
                    'price': sell_price,
                    'path_loss': loss
                })


                buy_order.quantity -= trade_quantity
                sell_order.quantity -= trade_quantity


                if buy_order.quantity > 0:
                    heapq.heappush(self.buy_orders, (-buy_price, buy_order))
                if sell_order.quantity > 0:
                    heapq.heappush(self.sell_orders, (sell_price, sell_order))
            else:

                heapq.heappush(self.buy_orders, (buy_price, buy_order))
                heapq.heappush(self.sell_orders, (sell_price, sell_order))
                break

        return transactions

    def get_best_path(self, from_user, to_storage):

        possible_paths = [path for path in self.paths if path.from_user == from_user and path.to_storage == to_storage]
        return min(possible_paths, key=lambda p: p.loss, default=None)


if __name__ == "__main__":
    # 创建 order book
    ob = OrderBook()

    # 添加路径
    ob.add_path(Path("User1", "Storage1", 0.05))


    # 添加买单
    ob.add_order(Order("User1", 100, 50, "limit", True))

    # 添加卖单
    ob.add_order(Order("Storage1", 100, 45, "limit", False))

    # 进行交易匹配
    transactions = ob.match_orders()

    # 输出交易结果
    print("\n交易结果：")
    for idx, t in enumerate(transactions):
        print(f"交易 {idx+1}: Buyer: {t['buyer']}, Seller: {t['seller']}, "
              f"Quantity: {t['quantity']:.2f} kWh, Price: {t['price']} , Path Loss: {t['path_loss']:.2%}")

