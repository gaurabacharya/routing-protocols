"""! @brief Defines the sensor classes."""

##
# @file distancevector.py

class Node:
    """! @brief Defines a node in the network topology.

    Attributes:
    - nodeId: the unique identifier of the node.
    - routingTable: a dictionary of the routing table with the key as the 
      destination and the next hop and pathCost as values.
    - neighbors: a dictionary of neighbor nodes and their associated costs.

    Methods:
    - add_neighbor(neighborId, cost): add a neighbor node with the given cost.
    - remove_neighbor(neighborId): remove the neighbor node with the given id.
    - update_routing_table(destination, nextHop, pathCost): add an element to the routing table dictionary.
    """
    def __init__(self, nodeId):
        """! Initializing the Node object.

        @param nodeId The unique identifier of the node.

        @return An instance of the Node class initialized with the specified name.
        """
        self.nodeId = nodeId
        self.routingTable = {}  # destination: (nextHop, pathCost)
        self.neighbors = {}

    def add_neighbor(self, neighborId, cost):
        """! Add a neighbor to the current node object.

        @param neighborId   The unique identifier of a neighbor node.
        @param cost         Cost of the link between the node and the neighbor.

        @return An instance of the node with an added neighbor.
        """
        self.neighbors[neighborId] = cost

    def remove_neighbor(self, neighborId):
        """! Remove a neighbor from the current node object.

        @param neighborId   The unique idenifier of a neighbor node.

        @return An instance of the node with a removed neighbor.
        """
        del self.neighbors[neighborId]

    def update_routing_table(self, destination, nextHop, pathCost):
        """! Update the routing table of the Node.

        @param destination  The nodeId of the destination node.
        @param nextHop      The nodeId of the nextHop from this node to the destination that creates the shortest path.
        @param pathCost     The total pathCost from this node to the destination.

        @return An instance of the node with an updated routing table.
        """
        self.routingTable[destination] = (nextHop, pathCost)
            
def read_topology_file(topologyFile):
    """! Read the network topology from the given file and create the corresponding nodes.

    Args:
    - topologyFile: the file containing the network topology information.

    Returns:
    - A dictionary of nodes, where the key is the node_id and the value is the Node object.
    """
    nodes = {}
    with open(topologyFile, 'r') as file:
        for line in file:
            nodeId, neighborId, cost = map(int, line.strip().split())
            if nodeId not in nodes:
                nodes[nodeId] = Node(nodeId)
            if neighborId not in nodes:
                nodes[neighborId] = Node(neighborId)
            nodes[nodeId].add_neighbor(neighborId, cost)
            nodes[neighborId].add_neighbor(nodeId, cost)
    return nodes          

def read_message_file(messageFile):
    """
    Read the messages from the given file.

    Args:
    - messageFile: the file containing the messages to be sent.

    Returns:
    - A list of messages, where each message is a tuple (srcNodeId, destNodeId, msgText).
    """
    msgs = []
    with open(messageFile, 'r') as file:
        for line in file:
            srcNodeId, destNodeId, msgText = line.split(maxsplit=2)
            msgs.append((int(srcNodeId), int(destNodeId), msgText))

    return msgs

def read_topology_change_file(changesFile):
    """
    Read the topology changes from the given file.

    Args:
    - changes_file: the file containing the topology changes.

    Returns:
    - A list of topology changes, where each change is a tuple (nodeId, neighborId, cost).
    """
    changes = []
    with open(changesFile, 'r') as file:
        for line in file:
            nodeId, neighborId, cost = map(int, line.split(maxsplit=2))
            changes.append((int(nodeId), int(neighborId), cost))
    return changes

def bellman_ford(dst, routers, links):
    """
    Run bellman_ford algorithm to find the distances from one to all other possible nodes with a route.

    Args:
    - dst: A nodeId of specific node. 
    - routers: A list of all nodes in the topology. 
    - links: A list of tuples that establish a connection between nodes in the form (nodeId, neighborId, cost).

    Returns:
    - distance: a dictionary where each key is a destination node, and each value is a tuple containing the nextHop and pathCost.
    - nexthop: a dictionary of where each key is a node, and each value is the next hop of the key to the destination node dst. 
    """
    INFINITY = float('inf')
    distance = {r: INFINITY for r in routers}
    nexthop = {r: None for r in routers}
    distance[dst] = 0

    for _ in range(len(routers) - 1):
        for (r1, r2, dist) in links:
            if distance[r1] + dist < distance[r2]:
                distance[r2] = distance[r1] + dist
                nexthop[r2] = r1
    print(nexthop)
    return distance, nexthop

def update_distance_vector(node, distanceVector, nexthop):
    """ 
    Update the distance vector routing table for a specific node. 

    Args:
    - node: a node in the topology.
    - distanceVector: a dictionary where each key is a destination node, and each value is a tuple containing the nextHop and pathCost.
    - nexthop: a dictionary of where each key is a node, and each value is the next hop of the key to the destination node dst.
    """
    for destination, cost in distanceVector.items():
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
    """
    Loop through each node in the topology to run the bellman_form algorithm and update the routing table.

    Args:
    - nodes: A dictionary of nodes, where the key is the node_id and the value is the Node object.
    - routers: A list of all nodes in the topology.
    - links: A list of tuples that establish a connection between nodes in the form (nodeId, neighborId, cost).
    """
    for nodeId, node in nodes.items():
        distanceVector, nexthop = bellman_ford(nodeId, routers, links)
        nexthop[nodeId] = nodeId
        update_distance_vector(node, distanceVector, nexthop)
        
def write_routing_table(nodes, outputFile):
    """
    Write the routing table to the outputFile for each node.

    Args:
    - nodes: A dictionary of nodes, where the key is the node_id and the value is the Node object.
    - outputFile: A file where all the output results and messages are written to.
    """
    sortedNodes = dict(sorted(nodes.items()))
    for nodeId, node in sortedNodes.items():
        sortedTable = sorted(node.routingTable.items(), key=lambda x: x[0])
        with open(outputFile, 'a') as f:
            for dest, (nextHop, pathCost) in sortedTable:
                f.write(f"{dest} {nextHop} {pathCost}\n")
            f.write("\n")

def get_links(nodes):
    """
    Get all links and the costs between nodes.

    Args:
    - nodes: A dictionary of nodes, where the key is the node_id and the value is the Node object.

    Returns:
    - links: A list of tuples that establish a connection between nodes in the form (nodeId, neighborId, cost).
    """
    links = []
    for nodeId, node in nodes.items():
        for neighborId, cost in node.neighbors.items():
            links.append((nodeId, neighborId, cost))
    return links

def write_messages(nodes, msgs, outputFile):
    """
    Write the results from the messages based on the current network topology.

    Args:
    - nodes: A dictionary of nodes, where the key is the node_id and the value is the Node object.
    - msgs: A list containing important items from the message file where each item is a tuple in the form (sourceNode, destinationNode, message).
    - outputFile: A file where all the output results and messages are written to.
    """
    with open(outputFile, 'a') as f:
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
    """
    Changes the nodes in the topology based on a change from the topology changes file.

    Args:
    - nodes: A dictionary of nodes, where the key is the node_id and the value is the Node object.
    - change: A tuple containing the changes involved in the form with a new link cost between nodes (nodeId, neighbourId, linkCost).
    """
    r1 = change[0]
    r2 = change[1]
    pathCost = change[2]
    if pathCost == -999:
        nodes[r1].remove_neighbor(r2)
        nodes[r2].remove_neighbor(r1)
    else:
        nodes[r1].add_neighbor(r2, pathCost)
        nodes[r2].add_neighbor(r1, pathCost)

def distanceVector_routing(topologyFile, messageFile, changesFile, outputFile='output.txt'):
    """
    The controller functions which runs the distance vector routing including reading the initial topology, reading messages, and reading changes.

    Args:
    - topologyFile: The filepath of the initial topology of the network.
    - messageFile: The filepath of the messages that need to be considered to route to. 
    - changesFile: The filepath of the changes to add in the network topology.
    - outputFile: A filepath where all the output results and messages are written to.

    """
    nodes = read_topology_file(topologyFile)
    routers = list(nodes.keys())
    links = get_links(nodes)  # list of (r1, r2, dist)
 
    open(outputFile, 'w')
    run_bellman_ford(nodes, routers, links)
    write_routing_table(nodes, outputFile)
    msgs = read_message_file(messageFile)
    write_messages(nodes, msgs, outputFile)
    changes = read_topology_change_file(changesFile)

    for change in changes:
        change_nodes(nodes, change)
        routers = list(nodes.keys())
        links = get_links(nodes)
        run_bellman_ford(nodes, routers, links)
        write_routing_table(nodes, outputFile)
        write_messages(nodes, msgs)

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 4:
        print("Usage: python src/distancevector.py <topologyFile> <messageFile> <changesFile> [outputFile]")
        sys.exit(1)

    topologyFile = sys.argv[1]
    messageFile = sys.argv[2]
    changesFile = sys.argv[3]
    outputFile = sys.argv[4] if len(sys.argv) >= 5 else "output.txt"

    distanceVector_routing(topologyFile, messageFile, changesFile, outputFile)