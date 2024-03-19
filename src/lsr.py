from collections import defaultdict
import heapq

class Node:
    def __init__(self, node_id):
        self.node_id = node_id
        self.neighbors = {}  # neighbor_id: cost

    def add_neighbor(self, neighbor_id, cost):
        self.neighbors[neighbor_id] = cost


def read_topology_file(topology_file):
    nodes = {}
    with open(topology_file, 'r') as file:
        for line in file:
            node_id, neighbor_id, cost = map(int, line.strip().split())
            if node_id not in nodes:
                nodes[node_id] = Node(node_id)
            if neighbor_id not in nodes:
                nodes[neighbor_id] = Node(neighbor_id)
            nodes[node_id].add_neighbor(neighbor_id, cost)
            nodes[neighbor_id].add_neighbor(node_id, cost)
    return nodes


def initialize_link_state(nodes):
    link_state = {}
    for node_id, node in nodes.items():
        link_state[node_id] = {neighbor: float('inf') for neighbor in nodes}
        link_state[node_id][node_id] = 0  # distance to self is 0
        for neighbor, cost in node.neighbors.items():
            link_state[node_id][neighbor] = cost
    return link_state


def dijkstra(nodes, source):
    distances = {node_id: float('inf') for node_id in nodes}
    distances[source] = 0
    visited = set()
    queue = [(0, source)]  # (distance, node_id)

    while queue:
        current_distance, current_node = heapq.heappop(queue)
        if current_node in visited:
            continue
        visited.add(current_node)

        for neighbor, cost in nodes[current_node].items():
            distance = current_distance + cost
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(queue, (distance, neighbor))

    return distances


def link_state_routing(topology_file, message_file, changes_file, output_file='output.txt'):
    nodes = read_topology_file(topology_file)
    link_state = initialize_link_state(nodes)

    # Implement the rest of the link-state routing algorithm here
    # For example, you can run Dijkstra's algorithm from each node to calculate shortest paths

    # Sample usage:
    distances_from_node_1 = dijkstra(link_state, 1)
    print(distances_from_node_1)
    print("ho")


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 4:
        print("Usage: python lsr.py <topologyFile> <messageFile> <changesFile> [outputFile]")
        sys.exit(1)

    topology_file = sys.argv[1]
    message_file = sys.argv[2]
    changes_file = sys.argv[3]
    output_file = sys.argv[4] if len(sys.argv) >= 5 else "output.txt"

    link_state_routing(topology_file, message_file, changes_file, output_file)
