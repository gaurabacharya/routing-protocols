class Node:
    """
    Represents a node in the network topology.

    Attributes:
    - node_id: the unique identifier of the node
    - neighbors: a dictionary of neighbor nodes and their associated costs

    Methods:
    - add_neighbor(neighbor_id, cost): add a neighbor node with the given cost
    - remove_neighbor(neighbor_id): remove the neighbor node with the given id
    """
    def __init__(self, node_id):
        self.node_id = node_id
        self.neighbors = {}

    def add_neighbor(self, neighbor_id, cost):
        self.neighbors[neighbor_id] = cost

    def remove_neighbor(self, neighbor_id):
        del self.neighbors[neighbor_id]


def read_topology_file(topology_file):
    """
    Read the network topology from the given file and create the corresponding nodes.

    Args:
    - topology_file: the file containing the network topology information

    Returns:
    - A dictionary of nodes, where the key is the node_id and the value is the Node object.
    """
    nodes = {}
    with open(topology_file, 'r') as file:
        for line in file:
            node_id, neighbor_id, cost = map(int, line.strip().split())
            if node_id not in nodes:
                nodes[node_id] = Node(node_id)
            if neighbor_id not in nodes:
                nodes[neighbor_id] = Node(neighbor_id)
            # Add neighbors to each node
            nodes[node_id].add_neighbor(neighbor_id, cost)
            nodes[neighbor_id].add_neighbor(node_id, cost)
    return nodes


def read_message_file(message_file):
    """
    Read the messages from the given file.

    Args:
    - message_file: the file containing the messages to be sent

    Returns:
    - A list of messages, where each message is a tuple (src_node_id, dest_node_id, msg_text)
    """
    msgs = []
    with open(message_file, 'r') as file:
        for line in file:
            src_node_id, dest_node_id, msg_text = line.split(maxsplit=2)
            msgs.append((int(src_node_id), int(dest_node_id), msg_text))
    return msgs


def read_topology_change_file(changes_file):
    """
    Read the topology changes from the given file.

    Args:
    - changes_file: the file containing the topology changes

    Returns:
    - A list of topology changes, where each change is a tuple (node_id, neighbor_id, cost)
    """
    changes = []
    with open(changes_file, 'r') as file:
        for line in file:
            node_id, neighbor_id, cost = map(int, line.split(maxsplit=2))
            changes.append((int(node_id), int(neighbor_id), cost))
    return changes


def find_next_hop(link_state):
    """
    Find the next hop for each destination in the link state information.

    Args:
    - link_state: the link state information for each node

    Returns:
    - The updated link state information with the next hop for each destination.
    """
    for src_node_id, (d, p) in link_state.items():
        n = {}

        for dst_node_id, prev_hop_node_id in p.items():
            curr_node_id = dst_node_id
            while prev_hop_node_id and (prev_hop_node_id != src_node_id):
                curr_node_id = prev_hop_node_id
                prev_hop_node_id = p[prev_hop_node_id]

            # If the while loop ends, the previous hop of curr_node_id is None (unreachable) or the source node
            if not prev_hop_node_id:
                n[dst_node_id] = None
            else:
                # Set the next hop from the source to get to dst to be the current node (who's previous hop is the source node)
                n[dst_node_id] = curr_node_id

        link_state[src_node_id] = (d, p, n)
    
    return link_state


def count_unreachable_nodes(nodes):
    """
    Count the number of unreachable nodes in the network.

    Args:
    - nodes: a dictionary of nodes in the network

    Returns:
    - A set of node_ids that are unreachable from any other node.
    """
    unreachable_nodes = set()
    for node_id, node in nodes.items():
        # If the node has no neighbors, it is unreachable
        if len(node.neighbors) == 0:
            unreachable_nodes.add(node_id)
    return unreachable_nodes


def get_hops(link_state, src_node_id, dest_node_id):
    """
    Get the sequence of nodes to traverse from the source node to the destination node.

    Args:
    - link_state: the link state information for each node

    Returns:
    - A list of node_ids representing the sequence of nodes to traverse from the source to the destination.
    """
    hops = []
    curr_node_id = src_node_id
    while curr_node_id != dest_node_id:
        # If a next hop is not specified for the current node to the destination node, the destination is unreachable
        if not link_state[curr_node_id][2][dest_node_id]:
            return None

        # Add the current node to the hops list
        hops.append(curr_node_id)

        # Get the next node to traverse to
        next_node_id = link_state[curr_node_id][2][dest_node_id]

        # If the next node is the same as the current node, the destination is unreachable
        if next_node_id == curr_node_id:
            return None
        
        curr_node_id = next_node_id

    return hops


def update_nodes(nodes):
    """
    Update the link state information for each node in the network.

    Args:
    - nodes: a dictionary of nodes in the network

    Returns:
    - A dictionary of link state information for each node, where the key is the node_id and the value is a tuple (d, p, n),
      where d is the path cost to each destination, p is the previous hop to each destination, and n is the next hop to each destination.
    """
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
                    # Check if the cost is less than the current min_cost or if the cost is equal to the current min_cost and the node_id is less (tie breaking)
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

    # Append the hops dictionary to the link state
    link_state = find_next_hop(link_state)

    # Link state should be a dictionary of node_id -> (d, p, n)
    # where d is the path cost to each destination, p is the previous hop of each destination, and n is the next hop to reach each destination
    # Ex. link_state[1][0][4] is the path cost from node 1 to node 4
    # Ex. link_state[2][1][3] is the previous hop of node 3 when coming from node 2
    # Ex. link_state[3][2][1] is the next hop to reach node 1 from node 3
    return link_state


def change_topology(changes, index, nodes):
    """
    Change the network topology based on the given changes.

    Args:
    - changes: a list of topology changes
    - index: the index of the change to apply
    - nodes: a dictionary of nodes in the network

    Returns:
    - The updated link state information after applying the change.
    """
    node_id, neighbor_id, cost = changes[index]

    # Remove links if cost is -999
    if cost == -999:
        nodes[node_id].remove_neighbor(neighbor_id)
        nodes[neighbor_id].remove_neighbor(node_id)
    # Otherwise update the costs
    else:
        nodes[node_id].neighbors[neighbor_id] = cost
        nodes[neighbor_id].neighbors[node_id] = cost

    # Update the link state information
    updated_state = update_nodes(nodes)
    return updated_state


def write_topology(link_state, file):
    """
    Write the node topology information to the given file.

    Args:
    - link_state: the link state information for each node
    - file: the file to write the information to
    """
    for i in range(1, len(link_state)+1):
        for j in range(1, len(link_state)+1):
            dest = j
            next_hop = link_state[i][2][j]
            path_cost = link_state[i][0][j]

            if path_cost != float('inf'):
                file.write(f'{dest} {next_hop} {path_cost}\n')
        file.write('\n')


def write_messages(link_state, msgs, file):
    """
    Write the messages and their corresponding paths to the given file.

    Args:
    - link_state: the link state information for each node
    - msgs: a list of messages to be sent
    - file: the file to write the information to
    """
    for src_node_id, dest_node_id, msg_text in msgs:
        hops = get_hops(link_state, src_node_id, dest_node_id)
        cost = link_state[src_node_id][0][dest_node_id]

        if cost == float('inf'):
            file.write(f'from {src_node_id} to {dest_node_id} cost infinite hops unreachable message {msg_text}\n')
        else:
            file.write(f'from {src_node_id} to {dest_node_id} cost {cost} hops {" ".join(str(x) for x in hops)} message {msg_text}\n')


def link_state_routing(topology_file, message_file, changes_file, output_file='output.txt'):
    """
    Execute the link state routing algorithm using the given files as input.

    Args:
    - topology_file: the file containing the network topology information
    - message_file: the file containing the messages to be sent
    - changes_file: the file containing the topology changes
    - output_file: the file to write the output to

    Returns:
    - A file containing the output of the link state routing algorithm
    """
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