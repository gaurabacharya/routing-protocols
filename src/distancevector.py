class Node:
    def __init__(self, node_id):
        self.node_id = node_id
        self.routing_table = {}  # destination: (next_hop, path_cost)

    def update_routing_table(self, destination, next_hop, path_cost):
        self.routing_table[destination] = (next_hop, path_cost)

    def bellman_ford(self, nodes):
        distance = {node.node_id: (node.node_id, 0) if node.node_id == self.node_id else (None, float('inf')) for node in nodes}

        for _ in range(len(nodes) - 1):
            for node in nodes:
                for dest, (next_hop, path_cost) in node.routing_table.items():
                    # print(f"node: {node.node_id}")
                    # print(f"dest: {dest}")
                    # print(f"next hop: {next_hop}")
                    # print(f"path cost: {path_cost}")
                    # print(f"distnace[node.node_id][1]: {distance[node.node_id][1]}")
                    # print(f"distance[dest][1]: {distance[dest][1]}")
                    # dst = U, dst+1 = V
                    # check if cost(U) + cost(U->V) < cost(V)
                    if distance[node.node_id][1] + path_cost < distance[dest][1]:
                        print(f"distances[dest]: {distance[dest]}")
                        # cost(V) = 
                        distance[dest] = (node.node_id, distance[node.node_id][1] + path_cost)
                    # print("\n")
                    # print(f"node: {node.node_id}")
                    # print(f"dest: {dest}")
                    # print(f"next hop: {next_hop}")
                    # print(f"path cost: {path_cost}")
                    # print(f"distnace[node.node_id][1]: {distance[node.node_id][1]}")
                    # print(f"distance[dest][1]: {distance[dest][1]}")
        return distance
    
    def write_routing_table(self, output_file):
        sorted_table = sorted(self.routing_table.items(), key=lambda x: x[0])

        with open(output_file, 'a') as f:
            for dest, (next_hop, path_cost) in sorted_table:
                f.write(f"{dest} {next_hop} {path_cost}\n")
            f.write("\n")

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

def read_message_file(message_file):
    msgs = []
    with open(message_file, 'r') as file:
        for line in file:
            src_node_id, dest_node_id, msg_text = line.split(maxsplit=2)
            msgs.append((int(src_node_id), int(dest_node_id), msg_text))

    return msgs

def read_topology_change_file(changes_file):
    changes = []
    with open(changes_file, 'r') as file:
        for line in file:
            node_id, neighbor_id, cost = map(int, line.split(maxsplit=2))
            changes.append((int(node_id), int(neighbor_id), cost))
    return changes

def run_bellman_ford(nodes, output_file):
    # Perform Bellman-Ford on each node
    for node_id, node in nodes.items():
        distances = node.bellman_ford(list(nodes.values()))

        # Update routing tables
        for dest, (next_hop, path_cost) in distances.items():
            # if path_cost != 0:  # Exclude self-route
            nodes[node_id].routing_table[dest] = (next_hop, path_cost)
        print(node_id)
        print(nodes[node_id].routing_table)
        # Write routing table to output file
        node.write_routing_table(output_file)

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
    for node_id, node in nodes.items():
        print(node_id)
        print(node.routing_table)
    open(output_file, 'w')
    run_bellman_ford(nodes, output_file)

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