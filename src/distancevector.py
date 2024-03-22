class Node:
    def __init__(self, node_id):
        self.node_id = node_id
        self.routing_table = {}  # destination: (next_hop, path_cost)
        self.neighbors = {}

    def add_neighbor(self, neighbor_id, cost):
        self.neighbors[neighbor_id] = cost

    def remove_neighbor(self, neighbor_id):
        del self.neighbors[neighbor_id]

    def update_routing_table(self, destination, next_hop, path_cost):
        self.routing_table[destination] = (next_hop, path_cost)

    # def bellman_ford(self, nodes):
    #     distance = {node.node_id: (node.node_id, 0) if node.node_id == self.node_id else (None, float('inf')) for node in nodes}

    #     for _ in range(len(nodes) - 1):
    #         for node in nodes:
    #             for dest, (next_hop, path_cost) in node.routing_table.items():
    #                 # print(f"node: {node.node_id}")
    #                 # print(f"dest: {dest}")
    #                 # print(f"next hop: {next_hop}")
    #                 # print(f"path cost: {path_cost}")
    #                 # print(f"distnace[node.node_id][1]: {distance[node.node_id][1]}")
    #                 # print(f"distance[dest][1]: {distance[dest][1]}")
    #                 # dst = U, dst+1 = V
    #                 # check if cost(U) + cost(U->V) < cost(V)
    #                 if distance[node.node_id][1] + path_cost < distance[dest][1]:
    #                     print(f"distances[dest]: {distance[dest]}")
    #                     # cost(V) = 
    #                     distance[dest] = (node.node_id, distance[node.node_id][1] + path_cost)
    #                 # print("\n")
    #                 # print(f"node: {node.node_id}")
    #                 # print(f"dest: {dest}")
    #                 # print(f"next hop: {next_hop}")
    #                 # print(f"path cost: {path_cost}")
    #                 # print(f"distnace[node.node_id][1]: {distance[node.node_id][1]}")
    #                 # print(f"distance[dest][1]: {distance[dest][1]}")
    #     return distance

# def read_topology_file(topology_file):
#     nodes = {}
#     with open(topology_file, 'r') as file:
#         for line in file:
#             node_id, neighbor_id, cost = map(int, line.strip().split())
#             if node_id not in nodes:
#                 nodes[node_id] = Node(node_id)
#             if neighbor_id not in nodes:
#                 nodes[neighbor_id] = Node(neighbor_id)
#             nodes[node_id].update_routing_table(neighbor_id, neighbor_id, cost)
#             nodes[neighbor_id].update_routing_table(node_id, node_id, cost)
#     return nodes
            
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

def bellman_ford(dst, routers, links):
    INFINITY = float('inf')
    distance = {r: INFINITY for r in routers}
    nexthop = {r: None for r in routers}
    distance[dst] = 0

    for _ in range(len(routers) - 1):
        for (r1, r2, dist) in links:
            if distance[r1] + dist < distance[r2]:
                distance[r2] = distance[r1] + dist
                nexthop[r2] = r1
    return distance, nexthop

def update_distance_vector(node, distance_vector, nexthop):
    for destination, cost in distance_vector.items():
        if destination != node.node_id and destination in nexthop and cost != float('inf'):
            nextNode = 0
            if nexthop[destination] == node.node_id:
                nextNode = destination
                node.update_routing_table(destination, nextNode, cost)
            else:
                nextNode = nexthop[destination] 

                while nexthop[nextNode] != None and nexthop[nextNode] != node.node_id:
                    if nextNode == None:
                        break
                    nextNode = nexthop[nextNode]
                node.update_routing_table(destination, nextNode, cost)
    print(node.routing_table)

# def run_bellman_ford(nodes, output_file):
#     # Perform Bellman-Ford on each node
#     for node_id, node in nodes.items():
#         distances = node.bellman_ford(list(nodes.values()))

#         # Update routing tables
#         for dest, (next_hop, path_cost) in distances.items():
#             # if path_cost != 0:  # Exclude self-route
#             nodes[node_id].routing_table[dest] = (next_hop, path_cost)
#         print(node_id)
#         print(nodes[node_id].routing_table)
#         # Write routing table to output file
#         node.write_routing_table(output_file)
            
def run_bellman_ford(nodes, routers, links):
    for node_id, node in nodes.items():
        distance_vector, nexthop = bellman_ford(node_id, routers, links)
        update_distance_vector(node, distance_vector, nexthop)
    

# def initialize_distance_vector(nodes):
#     distance_vector = {}
#     for node_id, node in nodes.items():
#         distance_vector[node_id] = {destination: float('inf') for destination in nodes}
#         distance_vector[node_id][node_id] = 0  # distance to self is 0
#         for neighbor, (next_hop, cost) in node.routing_table.items():
#             distance_vector[node_id][neighbor] = cost
#     return distance_vector

# def distance_vector_routing(topology_file, message_file, changes_file, output_file='output.txt'):
#     nodes = read_topology_file(topology_file)
#     for node_id, node in nodes.items():
#         print(node_id)
#         print(node.routing_table)
#     open(output_file, 'w')
#     run_bellman_ford(nodes, output_file)

    # Implement the rest of the distance vector routing algorithm here
        
def write_routing_table(nodes, output_file):
    for node_id, node in nodes.items():
        sorted_table = sorted(node.routing_table.items(), key=lambda x: x[0])
        with open(output_file, 'a') as f:
            for dest, (next_hop, path_cost) in sorted_table:
                f.write(f"{dest} {next_hop} {path_cost}\n")
            f.write("\n")

def get_links(nodes):
    links = []
    for node_id, node in nodes.items():
        for neighbor_id, cost in node.neighbors.items():
            links.append((node_id, neighbor_id, cost))
    return links

def write_messages(nodes, msgs):
    output_messages = []
    with open(output_file, 'a') as f:
        for msg in msgs:
            if nodes[msg[1]] not in nodes[msg[0]].routing_table.keys():
                f.write(f"from {msg[0]} to {msg[1]} cost infinite hops unreachable message {msg[2]}")
            # elif nodes[msg[1] in nodes[msg[1]]]:
                #need to add logic for each hop in messages


def distance_vector_routing(topology_file, message_file, changes_file, output_file='output.txt'):
    nodes = read_topology_file(topology_file)
    routers = list(nodes.keys())
    links = get_links(nodes)  # list of (r1, r2, dist)
 
    open(output_file, 'w')
    run_bellman_ford(nodes, routers, links)
    write_routing_table(nodes, output_file)
    msgs = read_message_file(message_file)
    print(msgs)
    
    # with open(changes_file, 'r') as changes_file:
    #     for line in changes_file:
    #         # Apply changes from the changes file
    #         # You need to update the node neighbors accordingly
    #         pass


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 4:
        print("Usage: python src/distancevector.py <topologyFile> <messageFile> <changesFile> [outputFile]")
        sys.exit(1)

    topology_file = sys.argv[1]
    message_file = sys.argv[2]
    changes_file = sys.argv[3]
    output_file = sys.argv[4] if len(sys.argv) >= 5 else "output.txt"

    distance_vector_routing(topology_file, message_file, changes_file, output_file)