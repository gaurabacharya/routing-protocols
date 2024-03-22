class Node:
    """
    Represents a node in the network topology.

    Attributes:
    - nodeId: the unique identifier of the node
    - routingTable: a dictionary of the routing table with the key as the 
      destination and the next hop and pathCost as values
    - neighbors: a dictionary of neighbor nodes and their associated costs

    Methods:
    - add_neighbor(neighborId, cost): add a neighbor node with the given cost
    - remove_neighbor(neighborId): remove the neighbor node with the given id
    - update_routing_table(destination, nextHop, pathCost): add an element to the routing table dictionary
    """
    def __init__(self, nodeId):
        self.nodeId = nodeId
        self.routingTable = {}  # destination: (nextHop, pathCost)
        self.neighbors = {}

    def add_neighbor(self, neighborId, cost):
        self.neighbors[neighborId] = cost

    def remove_neighbor(self, neighborId):
        del self.neighbors[neighborId]

    def update_routing_table(self, destination, nextHop, pathCost):
        self.routingTable[destination] = (nextHop, pathCost)
            
def read_topology_file(topology_file):
    nodes = {}
    with open(topology_file, 'r') as file:
        for line in file:
            nodeId, neighborId, cost = map(int, line.strip().split())
            if nodeId not in nodes:
                nodes[nodeId] = Node(nodeId)
            if neighborId not in nodes:
                nodes[neighborId] = Node(neighborId)
            nodes[nodeId].add_neighbor(neighborId, cost)
            nodes[neighborId].add_neighbor(nodeId, cost)
    return nodes          

def read_message_file(message_file):
    msgs = []
    with open(message_file, 'r') as file:
        for line in file:
            src_nodeId, dest_nodeId, msg_text = line.split(maxsplit=2)
            msgs.append((int(src_nodeId), int(dest_nodeId), msg_text))

    return msgs

def read_topology_change_file(changes_file):
    changes = []
    with open(changes_file, 'r') as file:
        for line in file:
            nodeId, neighborId, cost = map(int, line.split(maxsplit=2))
            changes.append((int(nodeId), int(neighborId), cost))
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
        # if destination != node.nodeId and destination in nexthop and cost != float('inf'):
        if destination in nexthop and cost != float("inf"):
            nextNode = 0
            if destination == node.nodeId:
                node.update_routing_table(destination, destination, 0)
            elif nexthop[destination] == node.nodeId:
                nextNode = destination
                node.update_routing_table(destination, nextNode, cost)
            else:
                nextNode = nexthop[destination] 

                while nexthop[nextNode] != None and nexthop[nextNode] != node.nodeId:
                    if nextNode == None:
                        break
                    nextNode = nexthop[nextNode]
                node.update_routing_table(destination, nextNode, cost)
        
def run_bellman_ford(nodes, routers, links):
    for nodeId, node in nodes.items():
        distance_vector, nexthop = bellman_ford(nodeId, routers, links)
        nexthop[nodeId] = nodeId
        update_distance_vector(node, distance_vector, nexthop)
        
def write_routing_table(nodes, output_file):
    sorted_nodes = dict(sorted(nodes.items()))
    for nodeId, node in sorted_nodes.items():
        sorted_table = sorted(node.routingTable.items(), key=lambda x: x[0])
        with open(output_file, 'a') as f:
            for dest, (nextHop, pathCost) in sorted_table:
                f.write(f"{dest} {nextHop} {pathCost}\n")
            f.write("\n")

def get_links(nodes):
    links = []
    for nodeId, node in nodes.items():
        for neighborId, cost in node.neighbors.items():
            links.append((nodeId, neighborId, cost))
    return links

def write_messages(nodes, msgs):
    
    with open(output_file, 'a') as f:
        for msg in msgs:
            if nodes[msg[1]].nodeId not in nodes[msg[0]].routingTable.keys():
                f.write(f"from {msg[0]} to {msg[1]} cost infinite hops unreachable message {msg[2]}")
            else:
                hopString = ""
                source = msg[0]
                destination = msg[1]
                pathCost = nodes[source].routingTable[destination][1]
                nextHop = source
                while nextHop != destination:
                    nextHop = nodes[nextHop].routingTable[destination][0]
                    hopString = f"{hopString} {nextHop}"
                hopString = f"{hopString} {nextHop}"

                f.write(f"from {msg[0]} to {msg[1]} cost {pathCost} hops{hopString} message {msg[2]}")
        f.write("\n")
        f.write("\n")

def change_nodes(nodes, change):
    r1 = change[0]
    r2 = change[1]
    pathCost = change[2]
    if pathCost == -999:
        nodes[r1].remove_neighbor(r2)
        nodes[r2].remove_neighbor(r1)
    else:
        nodes[r1].add_neighbor(r2, pathCost)
        nodes[r2].add_neighbor(r1, pathCost)

def distance_vector_routing(topology_file, message_file, changes_file, output_file='output.txt'):
    nodes = read_topology_file(topology_file)
    routers = list(nodes.keys())
    links = get_links(nodes)  # list of (r1, r2, dist)
 
    open(output_file, 'w')
    run_bellman_ford(nodes, routers, links)
    write_routing_table(nodes, output_file)
    msgs = read_message_file(message_file)
    write_messages(nodes, msgs)
    changes = read_topology_change_file(changes_file)

    for change in changes:
        change_nodes(nodes, change)
        routers = list(nodes.keys())
        links = get_links(nodes)
        run_bellman_ford(nodes, routers, links)
        write_routing_table(nodes, output_file)
        write_messages(nodes, msgs)

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