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

def read_message_file(message_file):
    msgs = []
    with open(message_file, 'r') as file:
        for line in file:
            msgs.append(list(map(int, line.strip().split())))

def find_next_hop(link_state):
    for node_id, (d, p) in link_state.items():
        n = {}

        for p_node_id, prev_hop in p.items():
            curr_node_id = p_node_id
            while prev_hop != node_id:
                curr_node_id = prev_hop
                prev_hop = p[prev_hop]

            n[p_node_id] = curr_node_id

        link_state[node_id] = (d, p, n)
    
    return link_state

def update_nodes(nodes):
    link_state = {}

    for node_id, node in nodes.items():
        n_prime = set()
        n_prime.add(node_id)

        d = {node_id: float('inf') for node_id in nodes}
        p = {node_id: None for node_id in nodes}

        d[node_id] = 0
        p[node_id] = node_id

        # Initialize step
        for neighbor, cost in node.neighbors.items():
            d[neighbor] = cost
            p[neighbor] = node_id

        while len(n_prime) < len(nodes):
            min_cost = float('inf')
            min_node_id = None
            min_node = None

            # Find the node not in n' with the smallest d
            for alt_node_id, alt_node in nodes.items():
                if alt_node_id not in n_prime:
                    if d[alt_node_id] < min_cost or (min_node_id and d[alt_node_id] == min_cost and (alt_node_id < min_node_id)):
                        min_cost = d[alt_node_id]
                        min_node_id = alt_node_id
                        min_node = alt_node
                        
            # Add the node to n'
            n_prime.add(min_node_id)

            # Update d and p
            for neighbor, cost in min_node.neighbors.items():
                if neighbor not in n_prime:
                    d[neighbor] = min(d[neighbor], d[min_node_id] + cost)
                    p[neighbor] = min_node_id
                    
        link_state[node_id] = (d, p)

    link_state = find_next_hop(link_state)
    return link_state

def print_topology(link_state):
    for i in range(1, len(link_state)+1):
        for j in range(1, len(link_state)+1):
            print(f'{j} {link_state[i][2][j]} {link_state[i][0][j]}')
        print()

    return


def link_state_routing(topology_file, message_file, changes_file, output_file='output.txt'):
    nodes = read_topology_file(topology_file)
    link_state = update_nodes(nodes)
    print_topology(link_state)


    # Implement the rest of the link-state routing algorithm here
    # For example, you can run Dijkstra's algorithm from each node to calculate shortest paths

    # Sample usage:
    # print(link_state[1])


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
