class User:
    def __init__(self, user_id, role, energy, price):
        self.user_id = user_id
        self.role = role  # 'seller' or 'buyer'
        self.energy = energy
        self.price = price  # Price per unit of energy


class EnergyMarket:
    def __init__(self):
        self.users = {}
        self.paths = {}

    def add_user(self, user):
        self.users[user.user_id] = user

    def add_path(self, from_user_id, to_user_id, loss):

        if from_user_id not in self.paths:
            self.paths[from_user_id] = {}
        self.paths[from_user_id][to_user_id] = loss

    def find_paths(self, source, target, visited=None):

        if visited is None:
            visited = set()
        if source == target:
            return [[source]]
        if source in visited or source not in self.paths:
            return []

        visited.add(source)
        all_paths = []
        for neighbor in self.paths.get(source, {}):
            if neighbor not in visited:
                sub_paths = self.find_paths(neighbor, target, visited)
                for sub_path in sub_paths:
                    all_paths.append([source] + sub_path)
        visited.remove(source)
        return all_paths

    def calculate_trade(self):

        trades = []
        for buyer_id, buyer in self.users.items():
            if buyer.role != 'buyer' or buyer.energy >= 0:
                continue

            for seller_id, seller in self.users.items():
                if seller.role != 'seller' or seller.energy <= 0:
                    continue

                paths = self.find_paths(seller_id, buyer_id)
                best_path = None
                best_cost = float('inf')
                best_loss = 0

                for path in paths:
                    total_loss = sum(self.paths[path[i]][path[i + 1]] for i in range(len(path) - 1))
                    effective_price = seller.price * (1 + total_loss)
                    trade_amount = min(abs(buyer.energy), seller.energy)
                    total_cost = effective_price * trade_amount

                    if total_cost < best_cost:
                        best_cost = total_cost
                        best_path = path
                        best_loss = total_loss

                if best_path:
                    trade_amount = min(abs(buyer.energy), seller.energy)
                    trades.append({
                        "buyer": buyer_id,
                        "seller": seller_id,
                        "amount": trade_amount,
                        "total_cost": best_cost,
                        "total_loss": best_loss,
                        "path": best_path
                    })

                    seller.energy -= trade_amount
                    buyer.energy += trade_amount

        return trades

if __name__ == "__main__":
    market = EnergyMarket()

    # Add users
    market.add_user(User(user_id="User1", role="seller", energy=100, price=5))


    # Add paths
    market.add_path("User1", "User2", loss=0.05)

    # Calculate trades
    trades = market.calculate_trade()

    # Display trades
    for trade in trades:
        print(f"Trade: Buyer {trade['buyer']} buys from Seller {trade['seller']}")
        print(f"Amount: {trade['amount']} units, Total Cost: {trade['total_cost']}")
        print(f"Path: {trade['path']}")
        print(f"Total Loss: {trade['total_loss'] * 100:.2f}%")
        print()
