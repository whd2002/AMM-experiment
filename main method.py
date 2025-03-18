import heapq


class UniswapV2AMM:
    def __init__(self, initial_money, initial_power):
        self.money = initial_money
        self.power = initial_power
        self.k = self.money * self.power

    def get_price_for_power(self, power_demand):

        if power_demand >= self.power:
            return float('inf')

        new_power = self.power - power_demand
        new_money = self.k / new_power
        money_required = new_money - self.money
        return max(money_required, 1)

    def get_power_for_money(self, money_received):

        if money_received >= self.money:
            return float('inf')

        new_money = self.money + money_received
        new_power = self.k / new_money
        power_provided = self.power - new_power
        return max(power_provided, 0)

    def update_pool_buy(self, power_demand, money_paid):

        self.power -= power_demand
        self.money += money_paid
        self.k = self.money * self.power

    def update_pool_sell(self, power_provided, money_received):

        self.power += power_provided
        self.money -= money_received
        self.k = self.money * self.power


def dijkstra(paths_graph, start, end):

    queue = [(0, start, [])]
    visited = set()

    while queue:
        total_loss, node, path = heapq.heappop(queue)

        if node in visited:
            continue
        visited.add(node)

        path = path + [node]

        if node == end:
            return total_loss, path

        for neighbor, loss in paths_graph.get(node, []):
            if neighbor not in visited:
                heapq.heappush(queue, (total_loss + loss, neighbor, path))

    return float('inf'), []


def find_best_amm_and_path(amms, demand, paths_graph, start_node, end_nodes, is_buying):
    best_total_cost = float('inf')
    best_amm = None
    best_path = None
    best_loss = 0

    for amm, end_node in zip(amms, end_nodes):

        total_loss, path = dijkstra(paths_graph, start_node, end_node)


        if total_loss == float('inf') or path[-1] != end_node:
            continue

        if is_buying:

            effective_power = demand / (1 - total_loss)
            cost = amm.get_price_for_power(effective_power)
        else:

            effective_money = demand / (1 - total_loss)
            cost = effective_money


        total_cost = cost + total_loss * demand

        if total_cost < best_total_cost:
            best_total_cost = total_cost
            best_amm = amm
            best_path = path
            best_loss = total_loss

    return best_amm, best_path, best_total_cost, best_loss


if __name__ == "__main__":
    amms = [
        UniswapV2AMM(initial_money=, initial_power=),
        UniswapV2AMM(initial_money=, initial_power=),
        UniswapV2AMM(initial_money=, initial_power=)
    ]


    paths_graph = {
        "user": [("node1", 0.01), ("node2", 0.03)],
    }

    start_node = "user"
    end_nodes = ["amm1"]


    for user_id in range(1, 101):
        is_buying = choice([True, False])
        demand = uniform()

        if is_buying:

            best_amm, best_path, best_cost, best_loss = find_best_amm_and_path(
                amms, demand, paths_graph, start_node, end_nodes, is_buying=True
            )
        else:

            best_amm, best_path, best_cost, best_loss = find_best_amm_and_path(
                amms, demand, paths_graph, start_node, end_nodes, is_buying=False
            )

        if best_amm is None:
            print(f"第{user_id}次交易失败，没有可用路径或满足需求的 AMM。")
            continue

        if is_buying:

            actual_power_received = demand * (1 - best_loss)
            best_amm.update_pool_buy(demand / (1 - best_loss), best_cost)
            print(f"第{user_id}次交易：用户买电，买入 {demand:.2f} 电力token，实际获得 {actual_power_received:.2f} 电力token，"
                  f"最佳路径是 {best_path}，需要 {best_cost:.2f} Money token，损耗了 {best_loss:.2%}")
        else:

            actual_money_received = demand * (1 - best_loss)
            best_amm.update_pool_sell(demand / (1 - best_loss), best_cost)
            print(f"第{user_id}次交易：用户卖电，卖出 {demand:.2f} 电力token，实际获得 {actual_money_received:.2f} Money token，"
                  f"最佳路径是 {best_path}，损耗了 {best_loss:.2%}")

        print(f"交易后 AMM 状态:")
        for i, amm in enumerate(amms):
            print(f"AMM {i} -> 剩余Electricity token: {amm.power:.2f}，剩余Money token: {amm.money:.2f}")
        print("----")

    print("\n最终 AMM 状态:")
    for i, amm in enumerate(amms):
        print(f"AMM {i} -> 剩余Electricity token: {amm.power:.2f}，剩余Money token: {amm.money:.2f}")


