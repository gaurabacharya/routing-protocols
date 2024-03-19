class Node:
    def __init__(self, node_id):
        self.node_id = node_id
        self.routing_table = {}  # destination: (next_hop, path_cost)

    def update_routing_table(self, destination, next_hop, path_cost):
        self.routing_table[destination] = (next_hop, path_cost)


def read_topology_file(topology_file):
    nodes = {}
    with open(topology_file, 'r') as file:
        for line in file:
            node_id, neighbor_id, cost = map(int, line.strip().split())
            if node_id not in nodes:
                nodes[node_id] = Node(node_id)
            if neighbor_id not in nodes:
                nodes[neighbor_id] = Node(neighbor_id)
            nodes[node_id].update_routing_table(neighbor_id, neighbor_id, cost)
            nodes[neighbor_id].update_routing_table(node_id, node_id, cost)
    return nodes


def initialize_distance_vector(nodes):
    distance_vector = {}
    for node_id, node in nodes.items():
        distance_vector[node_id] = {destination: float('inf') for destination in nodes}
        distance_vector[node_id][node_id] = 0  # distance to self is 0
        for neighbor, (next_hop, cost) in node.routing_table.items():
            distance_vector[node_id][neighbor] = cost
    return distance_vector

def distance_vector_routing(topology_file, message_file, changes_file, output_file='output.txt'):
    nodes = read_topology_file(topology_file)
    distance_vector = initialize_distance_vector(nodes)

    # Implement the rest of the distance vector routing algorithm here


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 4:
        print("Usage: python dvr.py <topologyFile> <messageFile> <changesFile> [outputFile]")
        sys.exit(1)

    topology_file = sys.argv[1]
    message_file = sys.argv[2]
    changes_file = sys.argv[3]
    output_file = sys.argv[4] if len(sys.argv) >= 5 else "output.txt"

    distance_vector_routing(topology_file, message_file, changes_file, output_file)