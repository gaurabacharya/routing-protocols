class Node:
    """! Represents a node in the network topology.

    Attributes:
    - nodeId: the unique identifier of the node
    - neighbors: a dictionary of neighbor nodes and their associated costs

    Methods:
    - add_neighbor(neighborId, cost): add a neighbor node with the given cost
    - remove_neighbor(neighborId): remove the neighbor node with the given id
    """
    def __init__(self, nodeId):
        """! Initializing the Node object.

        @param nodeId The unique identifier of the node.
        """
        self.nodeId = nodeId
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


def read_topology_file(topologyFile):
    """! Read the network topology from the given file and create the corresponding nodes.

    @param topologyFile the file containing the network topology information

    @return A dictionary of nodes, where the key is the nodeId and the value is the Node object.
    """
    nodes = {}
    with open(topologyFile, 'r') as file:
        for line in file:
            nodeId, neighborId, cost = map(int, line.strip().split())
            if nodeId not in nodes:
                nodes[nodeId] = Node(nodeId)
            if neighborId not in nodes:
                nodes[neighborId] = Node(neighborId)
            # Add neighbors to each node
            nodes[nodeId].add_neighbor(neighborId, cost)
            nodes[neighborId].add_neighbor(nodeId, cost)
    return nodes


def read_message_file(messageFile):
    """! Read the messages from the given file.

    @param messageFile the file containing the messages to be sent

    @return A list of messages, where each message is a tuple (srcNodeId, dstNodeId, msgText)
    """
    msgs = []
    with open(messageFile, 'r') as file:
        for line in file:
            srcNodeId, dstNodeId, msgText = line.split(maxsplit=2)
            msgs.append((int(srcNodeId), int(dstNodeId), msgText))
    return msgs


def read_topology_change_file(changeFile):
    """! Read the topology changes from the given file.

    @param changeFile the file containing the topology changes

    @return A list of topology changes, where each change is a tuple (nodeId, neighborId, cost)
    """
    changes = []
    with open(changeFile, 'r') as file:
        for line in file:
            nodeId, neighborId, cost = map(int, line.split(maxsplit=2))
            changes.append((int(nodeId), int(neighborId), cost))
    return changes


def find_next_hop(linkState):
    """! Find the next hop for each destination in the link state information.

    @param linkState The link state information for each node

    @return The updated link state information with the next hop for each destination.
    """
    for srcNodeId, (d, p) in linkState.items():
        n = {}

        for dstNodeId, prevHopNodeId in p.items():
            currNodeId = dstNodeId
            while prevHopNodeId and (prevHopNodeId != srcNodeId):
                currNodeId = prevHopNodeId
                prevHopNodeId = p[prevHopNodeId]

            # If the while loop ends, the previous hop of currNodeId is None (unreachable) or the source node
            if not prevHopNodeId:
                n[dstNodeId] = None
            else:
                # Set the next hop from the source to get to dst to be the current node (who's previous hop is the source node)
                n[dstNodeId] = currNodeId

        linkState[srcNodeId] = (d, p, n)
    
    return linkState


def count_unreachable_nodes(nodes):
    """! Count the number of unreachable nodes in the network.

    @param nodes A dictionary of nodes in the network

    @return A set of node_ids that are unreachable from any other node.
    """
    unreachableNodes = set()
    for nodeId, node in nodes.items():
        # If the node has no neighbors, it is unreachable
        if len(node.neighbors) == 0:
            unreachableNodes.add(nodeId)
    return unreachableNodes


def get_hops(linkState, srcNodeId, dstNodeId):
    """! Get the sequence of nodes to traverse from the source node to the destination node.

    @param linkState the link state information for each node
    @param srcNodeId the nodeId of the source node
    @param dstNodeId the nodeId of the destination node

    @return A list of nodeIds representing the sequence of nodes to traverse from the source to the destination.
    """
    hops = []
    currNodeId = srcNodeId
    while currNodeId != dstNodeId:
        # If a next hop is not specified for the current node to the destination node, the destination is unreachable
        if not linkState[currNodeId][2][dstNodeId]:
            return None

        # Add the current node to the hops list
        hops.append(currNodeId)

        # Get the next node to traverse to
        nextNodeId = linkState[currNodeId][2][dstNodeId]

        # If the next node is the same as the current node, the destination is unreachable
        if nextNodeId == currNodeId:
            return None
        
        currNodeId = nextNodeId

    return hops


def update_nodes(nodes):
    """! Update the link state information for each node in the network.

    @param nodes a dictionary of nodes in the network

    @return A dictionary of link state information for each node, where the key is the nodeId and the value is a tuple (d, p, n),
      where d is the path cost to each destination, p is the previous hop to each destination, and n is the next hop to each destination.
    """
    linkState = {}

    # Get unreachable nodes
    unreachableNodes = count_unreachable_nodes(nodes)

    for nodeId, node in nodes.items():
        # Intialize n'
        nPrime = set()
        nPrime.add(nodeId)

        # Initialize d and p
        d = {nodeId: float('inf') for nodeId in nodes}
        p = {nodeId: None for nodeId in nodes}

        d[nodeId] = 0
        p[nodeId] = nodeId

        # Initialize step for all neighbors
        for neighbor, cost in node.neighbors.items():
            d[neighbor] = cost
            p[neighbor] = nodeId

        # Check that the node is reachable and that there are still nodes to add to n' that are reachable
        while nodeId not in unreachableNodes and (len(nPrime) < (len(nodes) - len(unreachableNodes))):
            minCost = float('inf')
            minNodeId = None
            minNode = None

            # Find the node not in n' with the smallest d
            for altNodeId, altNode in nodes.items():
                if altNodeId not in nPrime:
                    # Check if the cost is less than the current minCost or if the cost is equal to the current minCost and the nodeId is less (tie breaking)
                    if d[altNodeId] < minCost or (minNodeId and d[altNodeId] == minCost and (altNodeId < minNodeId)):
                        minCost = d[altNodeId]
                        minNodeId = altNodeId
                        minNode = altNode
                        
            if minNode is not None:
                # Add the node to n'
                nPrime.add(minNodeId)

                # Update d and p
                for neighbor, cost in minNode.neighbors.items():
                    if neighbor not in nPrime:
                        if d[minNodeId] + cost < d[neighbor]:
                            d[neighbor] = d[minNodeId] + cost
                            p[neighbor] = minNodeId
                    
        linkState[nodeId] = (d, p)

    # Append the hops dictionary to the link state
    linkState = find_next_hop(linkState)

    # Link state should be a dictionary of nodeId -> (d, p, n)
    # where d is the path cost to each destination, p is the previous hop of each destination, and n is the next hop to reach each destination
    # Ex. linkState[1][0][4] is the path cost from node 1 to node 4
    # Ex. linkState[2][1][3] is the previous hop of node 3 when coming from node 2
    # Ex. linkState[3][2][1] is the next hop to reach node 1 from node 3
    return linkState


def change_topology(changes, index, nodes):
    """! Change the network topology based on the given changes.

    @param changes a list of topology changes
    @param index   the index of the change to apply
    @param nodes   a dictionary of nodes in the network

    @return The updated link state information after applying the change.
    """
    nodeId, neighborId, cost = changes[index]

    # Remove links if cost is -999
    if cost == -999:
        nodes[nodeId].remove_neighbor(neighborId)
        nodes[neighborId].remove_neighbor(nodeId)
    # Otherwise update the costs
    else:
        nodes[nodeId].neighbors[neighborId] = cost
        nodes[neighborId].neighbors[nodeId] = cost

    # Update the link state information
    updatedState = update_nodes(nodes)
    return updatedState


def write_topology(linkState, file):
    """! Write the node topology information to the given file.

    @param linkState the link state information for each node
    @param file the file to write the information to
    """
    for i in range(1, len(linkState)+1):
        for j in range(1, len(linkState)+1):
            dest = j
            next_hop = linkState[i][2][j]
            path_cost = linkState[i][0][j]

            if path_cost != float('inf'):
                file.write(f'{dest} {next_hop} {path_cost}\n')
        file.write('\n')


def write_messages(linkState, msgs, file):
    """! Write the messages and their corresponding paths to the given file.

    @param linkState    the link state information for each node
    @param msgs         a list of messages to be sent
    @param file         the file to write the information to
    """
    for srcNodeId, dstNodeId, msgText in msgs:
        hops = get_hops(linkState, srcNodeId, dstNodeId)
        cost = linkState[srcNodeId][0][dstNodeId]

        if cost == float('inf'):
            file.write(f'from {srcNodeId} to {dstNodeId} cost infinite hops unreachable message {msgText}\n')
        else:
            file.write(f'from {srcNodeId} to {dstNodeId} cost {cost} hops {" ".join(str(x) for x in hops)} message {msgText}\n')


def link_state_routing(topologyFile, messageFile, changeFile, outputFile='output.txt'):
    """! Execute the link state routing algorithm using the given files as input.

    @param topologyFile    the file containing the network topology information
    @param messageFile     the file containing the messages to be sent
    @param changeFile      the file containing the topology changes
    @param outputFile      the file to write the output to

    @return A file containing the output of the link state routing algorithm
    """
    nodes = read_topology_file(topologyFile)
    msgs = read_message_file(messageFile)
    changes = read_topology_change_file(changeFile)
    file = open(outputFile, 'w')
    file = open(outputFile, 'a')

    linkState = update_nodes(nodes)
    write_topology(linkState, file)
    write_messages(linkState, msgs, file)
    
    for i in range(len(changes)):
        file.write('\n')
        linkState = change_topology(changes, i, nodes)
        write_topology(linkState, file)
        write_messages(linkState, msgs, file)

    file.close()


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 4:
        print("Usage: python lsr.py <topologyFile> <messageFile> <changesFile> [outputFile]")
        sys.exit(1)

    topologyFile = sys.argv[1]
    messageFile = sys.argv[2]
    changeFile = sys.argv[3]
    outputFile = sys.argv[4] if len(sys.argv) >= 5 else "output.txt"

    link_state_routing(topologyFile, messageFile, changeFile, outputFile)