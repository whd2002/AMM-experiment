import numpy as np
from collections import defaultdict
import heapq

class AutomatedMarketMaker:
    def __init__(self, reserve_x, reserve_y):
        self.reserve_x = reserve_x  
        self.reserve_y = reserve_y  

    def get_price(self, delta_x):
        new_reserve_x = self.reserve_x + delta_x
        new_reserve_y = self.reserve_x * self.reserve_y / new_reserve_x
        delta_y = self.reserve_y - new_reserve_y
        return delta_y

    def trade(self, delta_x):
        delta_y = self.get_price(delta_x)
        self.reserve_x += delta_x
        self.reserve_y -= delta_y
        return delta_y

class User:
    def __init__(self, id, power_demand, funds):
        self.id = id
        self.power_demand = power_demand 
        self.funds = funds  

class StorageUnit:
    def __init__(self, id, capacity):
        self.id = id
        self.capacity = capacity  

class Graph:
    def __init__(self):
        self.edges = defaultdict(list)  
        self.nodes = set()  

    def add_edge(self, from_node, to_node, loss):
        self.edges[from_node].append((to_node, loss))
        self.nodes.add(from_node)
        self.nodes.add(to_node)

    def dijkstra(self, start):
        pq = [(0, start)] 
        shortest_paths = {node: float('inf') for node in self.nodes}
        shortest_paths[start] = 0
        previous_nodes = {node: None for node in self.nodes}
        visited = set()

        while pq:
            current_loss, current_node = heapq.heappop(pq)

            if current_node in visited:
                continue
            visited.add(current_node)

            for neighbor, loss in self.edges[current_node]:
                new_loss = current_loss + loss
                if new_loss < shortest_paths[neighbor]:
                    shortest_paths[neighbor] = new_loss
                    previous_nodes[neighbor] = current_node
                    heapq.heappush(pq, (new_loss, neighbor))

        return shortest_paths, previous_nodes

    def reconstruct_path(self, start, end, previous_nodes):
        path = []
        current_node = end
        while current_node is not None:
            path.insert(0, current_node)
            current_node = previous_nodes[current_node]
        return path if path[0] == start else []

users = [User(id=f"U{i}", power_demand=np.uniform(-10, 10), funds=) for i in range(30)]  
storage_units = [StorageUnit(id=f"S{i}", capacity=) for i in range(10)]  
intermediate_nodes = [f"N{i}" for i in range(50)]  
graph = Graph()

for user in users:
    for node in np.choice(intermediate_nodes, size=10, replace=False): 
        loss = np.uniform(0.1, 0.5)
        graph.add_edge(user.id, node, loss)

for node in intermediate_nodes:
    for su in np.choice(storage_units, size=5, replace=False):  
        loss = np.uniform(0.1, 0.5)
        graph.add_edge(node, su.id, loss)

for _ in range(100):  # 增加复杂连接
    from_node, to_node = np.choice(intermediate_nodes, size=2, replace=False)
    loss = np.uniform(0.05, 0.3)
    graph.add_edge(from_node, to_node, loss)

amm = AutomatedMarketMaker(reserve_x=20000, reserve_y=20000)

for transaction_id in range(1, 101):
    user = np.choice(users)  
    if user.power_demand > 0:  
        shortest_paths, previous_nodes = graph.dijkstra(user.id)
        target_su = min((su.id for su in storage_units), key=lambda su_id: shortest_paths.get(su_id, float('inf')))
        storage_unit = next(su for su in storage_units if su.id == target_su)
        path = graph.reconstruct_path(user.id, target_su, previous_nodes)
        loss = shortest_paths[target_su]

        price = amm.get_price(user.power_demand)
        if user.funds >= price and storage_unit.capacity >= user.power_demand:
            user.funds -= price
            storage_unit.capacity -= user.power_demand
            amm.trade(user.power_demand)
            print(f"第 {transaction_id} 次交易: {user.id} 从 {target_su} 购买 {user.power_demand:.2f} 电力")
            print(f"路径: {' -> '.join(path)}，传输损耗: {loss:.2f}")
            print(f"支付: {price:.2f} money token，剩余资金: {user.funds:.2f}")
            print(f"交易所剩余: {amm.reserve_y:.2f} money token, {amm.reserve_x:.2f} electricity token\n")
    elif user.power_demand < 0:  
        shortest_paths, previous_nodes = graph.dijkstra(user.id)
        target_su = min((su.id for su in storage_units), key=lambda su_id: shortest_paths.get(su_id, float('inf')))
        storage_unit = next(su for su in storage_units if su.id == target_su)
        path = graph.reconstruct_path(user.id, target_su, previous_nodes)
        loss = shortest_paths[target_su]

        
        power_to_sell = -user.power_demand
        price = amm.get_price(power_to_sell)
        if storage_unit.capacity + power_to_sell <= 1000:
            user.funds += price
            storage_unit.capacity += power_to_sell
            amm.trade(-power_to_sell)
            print(f"第 {transaction_id} 次交易: {user.id} 向 {target_su} 出售 {power_to_sell:.2f} 电力")
            print(f"路径: {' -> '.join(path)}，传输损耗: {loss:.2f}")
            print(f"获得: {price:.2f} money token，总资金: {user.funds:.2f}")
            print(f"交易所剩余: {amm.reserve_y:.2f} money token, {amm.reserve_x:.2f} electricity token\n")
