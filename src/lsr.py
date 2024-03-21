class Node:
    def __init__(self, node_id):
        self.node_id = node_id
        self.neighbors = {}  # neighbor_id: cost

    def add_neighbor(self, neighbor_id, cost):
        self.neighbors[neighbor_id] = cost

    def remove_neighbor(self, neighbor_id):
        del self.neighbors[neighbor_id]


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


def find_next_hop(link_state):
    for node_id, (d, p) in link_state.items():
        n = {}

        for p_node_id, prev_hop in p.items():
            curr_node_id = p_node_id
            while prev_hop != node_id:
                curr_node_id = prev_hop

                if not prev_hop:
                    break

                prev_hop = p[prev_hop]

            if not prev_hop:
                n[p_node_id] = None
            else:
                n[p_node_id] = curr_node_id

        link_state[node_id] = (d, p, n)
    
    return link_state


def count_unreachable_nodes(nodes):
    unreachable_nodes = set()
    for node_id, node in nodes.items():
        if len(node.neighbors) == 0:
            unreachable_nodes.add(node_id)
    return unreachable_nodes


def get_hops(link_state, src_node_id, dest_node_id):
    hops = []
    curr_node_id = src_node_id
    while curr_node_id != dest_node_id:
        if not link_state[curr_node_id][2][dest_node_id]:
            break

        hops.append(curr_node_id)
        next_node_id = link_state[curr_node_id][2][dest_node_id]

        if next_node_id == curr_node_id:
            return None
        
        curr_node_id = next_node_id

    return hops


def update_nodes(nodes):
    link_state = {}

    # Get unreachable nodes
    unreachable_nodes = count_unreachable_nodes(nodes)

    for node_id, node in nodes.items():
        # Intialize n'
        n_prime = set()
        n_prime.add(node_id)

        # Initialize d and p
        d = {node_id: float('inf') for node_id in nodes}
        p = {node_id: None for node_id in nodes}

        d[node_id] = 0
        p[node_id] = node_id

        # Initialize step for all neighbors
        for neighbor, cost in node.neighbors.items():
            d[neighbor] = cost
            p[neighbor] = node_id

        # Check that the node is reachable and that there are still nodes to add to n' that are reachable
        while node_id not in unreachable_nodes and (len(n_prime) < (len(nodes) - len(unreachable_nodes))):
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
                        
            if min_node is not None:
                # Add the node to n'
                n_prime.add(min_node_id)

                # Update d and p
                for neighbor, cost in min_node.neighbors.items():
                    if neighbor not in n_prime:
                        if d[min_node_id] + cost < d[neighbor]:
                            d[neighbor] = d[min_node_id] + cost
                            p[neighbor] = min_node_id
                    
        link_state[node_id] = (d, p)

    link_state = find_next_hop(link_state)
    return link_state


def change_topology(changes, index, nodes):
    node_id, neighbor_id, cost = changes[index]

    if cost == -999:
        nodes[node_id].remove_neighbor(neighbor_id)
        nodes[neighbor_id].remove_neighbor(node_id)
    else:
        nodes[node_id].neighbors[neighbor_id] = cost
        nodes[neighbor_id].neighbors[node_id] = cost

    updated_state = update_nodes(nodes)
    return updated_state


def write_topology(link_state, file):
    for i in range(1, len(link_state)+1):
        for j in range(1, len(link_state)+1):
            dest = j
            next_hop = link_state[i][2][j]
            path_cost = link_state[i][0][j]

            if path_cost != float('inf'):
                file.write(f'{dest} {next_hop} {path_cost}\n')
        file.write('\n')


def write_messages(link_state, msgs, file):
    for src_node_id, dest_node_id, msg_text in msgs:
        hops = get_hops(link_state, src_node_id, dest_node_id)
        cost = link_state[src_node_id][0][dest_node_id]

        if cost == float('inf'):
            file.write(f'from {src_node_id} to {dest_node_id} cost infinite hops unreachable message {msg_text}\n')
        else:
            file.write(f'from {src_node_id} to {dest_node_id} cost {cost} hops {" ".join(str(x) for x in hops)} message {msg_text}\n')


def link_state_routing(topology_file, message_file, changes_file, output_file='output.txt'):
    nodes = read_topology_file(topology_file)
    msgs = read_message_file(message_file)
    changes = read_topology_change_file(changes_file)
    file = open(output_file, 'w')
    file = open(output_file, 'a')

    link_state = update_nodes(nodes)
    write_topology(link_state, file)
    write_messages(link_state, msgs, file)
    
    for i in range(len(changes)):
        file.write('\n')
        link_state = change_topology(changes, i, nodes)
        write_topology(link_state, file)
        write_messages(link_state, msgs, file)

    file.close()


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