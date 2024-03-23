# elec331-pa2

Authors:
* Gaurab Acharya
* Ivan Guo

**PA2 Summary:**
* Wrote one implementation of link state routing: *src/linkstate.py*
* Wrote one implementation of distance vector protocol: *src/distancevector.py*

## Running the Python Files
To run the python files there 2 bash scripts that can be executed to run the specific protocol. 
To run the link state protocol execute: *./lsr.sh <topologyFile> <messageFile> <changesFile> [outputFile]*
To run the distance vector protocol execute: *./dvr.sh <topologyFile> <messageFile> <changesFile> [outputFile]*

## Viewing Doxygen Documentation
To view the Doxygen Documentation please open the html file *html/index.html* in a browser to view the files and the documentation of each function. 
On Mac/Linux it can be opened through the terminal in the project directory with the command *open html/index.html*. 

Here is the outline of our approach.

1. **Node Structure**:
- We defined two separate node structures for both the distance vector routing algorithm and the link state routing algorithm.
- Distance Vector Routing Algorithm Node Structure:
    - Fields:
        - nodeId: The unique ID of a specific node.
        - routingTable: The routing table of a specific node.
        - neighbors: The neighbors of a specific node.
    - Functions:
        - add_neighbor: Adds a neighbor to a specific node.
        - remove_neighbor: Removes a neighbor from a specific node.
        - update_routing_table: Updates the routing table of a specific node. 

- Link State Routing Algorithm Node Structure:
    - Fields:
		- nodeId: The unique ID of a specific node.
        - neighbors: The neighbors of a specific node.
    - Functions:
        - add_neighbor: Adds a neighbor to a specific node.
        - remove_neighbor: Removes a neighbor from a specific node.

2. **Distance Vector Functions**:
	- *bellman_ford(dst, routers, links)*: Run Bellman-Ford algorithm to find the distances from one to all other possible nodes with a route.
	- *change_nodes(nodes, change)*: Changes the nodes in the topology based on a change from the topology changes file.
	- *distanceVector_routing(topologyFile, messageFile, changesFile, outputFile='output.txt')*: The controller function which runs the distance vector routing including reading the initial topology, reading messages, and reading changes.
	- *get_links(nodes)*: Get all links and the costs between nodes.
	- *read_message_file(messageFile)*: Read the messages from the given file.
	- *read_topology_change_file(changesFile)*: Read the topology changes from the given file.
	- *read_topology_file(topologyFile)*: Read the network topology from the given file and create the corresponding nodes.
	- *run_bellman_ford(nodes, routers, links)*: Loop through each node in the topology to run the Bellman-Ford algorithm and update the routing table.
	- *update_distance_vector(node, distanceVector, nexthop)*: Update the distance vector routing table for a specific node.
	- *write_messages(nodes, msgs, outputFile)*: Write the results from the messages based on the current network topology.
	- *write_routing_table(nodes, outputFile)*: Write the routing table to the outputFile for each node.

3. **Link State Functions**:
	- *linkstate.Node*: Represents a node in the network topology.
	- *change_topology(changes, index, nodes)*: Change the network topology based on the given changes.
	- *count_unreachable_nodes(nodes)*: Count the number of unreachable nodes in the network.
	- *find_next_hop(linkState)*: Find the next hop for each destination in the link state information.
	- *get_hops(linkState, srcNodeId, dstNodeId)*: Get the sequence of nodes to traverse from the source node to the destination node.
	- *link_state_routing(topologyFile, messageFile, changeFile, outputFile='output.txt')*: Execute the link state routing algorithm using the given files as input.
	- *read_message_file(messageFile)*: Read the messages from the given file.
	- *read_topology_change_file(changeFile)*: Read the topology changes from the given file.
	- *read_topology_file(topologyFile)*: Read the network topology from the given file and create the corresponding nodes.
	- *update_nodes(nodes)*: Update the link state information for each node in the network.
	- *write_messages(linkState, msgs, file)*: Write the messages and their corresponding paths to the given file.
	- *write_topology(linkState, file)*: Write the link state information to the given file.
 
4. **Testing and Evaluation**:
	- Evaluated against several different topology, message, and change files.