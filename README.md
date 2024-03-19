# elec331-pa2

**Main objectives:**
* Write one implementation of link state routing 
* Write one implementation of distance vector protocol 
Both will read and use the same file format for the network topology 

## Routers:
* Maintain collection of virtual routing nodes 
* Nodes are data structures in the program 
* Once tables converge
write node’s forwarding table and have some nodes send data to some other nodes
* One at a time applying each line in the topology changes file in order
* Repeat previous instructions after each change 
* Nodes in distances vector should use the DV and LS algorithms respectively to arrive at the correct forwarding table for the network they are in 

## Tie Breaking
Distance Vector Routing:
2 equally good paths are available 
Current node should choose the one whose next-hop node ID is lower
Link state:
If tie 
Choose the path whose last node before the destination has the smaller ID 
Ex. source is 1 
Current best path to 9 is `1 -> 4 -> 12 -> 9` 
Then we are adding node 11 to the finished set 
So there exists a path `1 -> 4 -> 5 -> 11 -> 9` which is the same cost so we will switch to the new path since `11 < 12`

## Input:
Read 3 files: 
* Topology file -> initial topology
* Topology changes file -> represents sequence of changes to topology to be applied one by one 

### Message file 
* describes which nodes should send data to whom once the routing tables converge 
* Tables should converge before the topology changes start, as well as after each change 
* All messages in message gile are sent every time the tables converge 
If there are 2 message lines in the message file: 

 2 changes in changes file -> 2 initial file read + 2 (after first change in changesFile has been applied) + 2 (second line in changesFile has been applied) = 6 messages should be sent 

## File structure:
* All files have items delimited by newlines
* A line in the topology file represents a link between 2 nodes 
```
<ID of a node> <ID of another node> <Cost of the link between them>
```
Topology changes file has the same format
* first line in the changes is the first change to apply and remaining lines are changes to be applied in order 
* Cost of -999 indicates that the previously existing link between two nodes is broken
* Real link costs are always positive 
A line in the message file looks like 
```
<source node ID> <dest node ID> <message text>
```

## Output:
All output is written to output.txt 
Forwarding table format is: 
```
<destination> <nextHop> <pathCost>
```
### nextHop:
* is neighbor to which the node forwards packets intended for destination to 
### pathCost 
Is the total cost of the path to the destination 

Ex. 
```
1 5 6
2 2 0
3 3 3
4 5 5
5 5 4
```
* A node’s entry for itself will list nextHop as itself and a pathCost of 0 
* If destination is not reachable froma node then that destination will not appear in the forwarding table 
* Each entry of the forwarding table is in its own line and each component is separated by a single space 
* You should write the forwarding for each node sorted by smallest node identifier first 
* Forward table for node 2 should be preceded by forward table for node 1 and should be succeeded by the forwarding tables for nodes 3, 4 

When a message is to be sent - output file will contain a line with source, destination, the cost of path, the path taken.
Specific format: 
```
From <x> to <y> cost <pathCost> hops <hop1> <hop2> <...> message <message>
```
Ex.
```
from 2 to 1 cost 6 hops 2 5 4 message here is a message from 2 to 1
```

Print messages in the order they were specific in the messages 
If destination is not reachable then output is
```
from <x> to <y> cost infinite hops unreachable message <message>
```

* Don’t write anything else 
* If messageFile and changesFile are empty, program should just print the forwarding table 

## Running the files 
Project must include a Makefile whose default target makes executables called 
dvr 
lsr 
Command line format is:
```
./lsr <topologyFile> <messageFile> <changesFile> [outputFile]`
./dvr <topologyFile> <messageFile> <changesFile> [outputFile]
```

If outputFile is not specified then output should be written to output.txt 

