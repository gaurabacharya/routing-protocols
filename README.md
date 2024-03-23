# elec331-pa2
Authors:
* Gaurab Acharya
* Ivan Guo


**PA2 Summary:**
* Wrote one implementation of link state routing: `src/linkstate.py`
* Wrote one implementation of distance vector protocol: `src/distancevector.py`

## Running the Python Files
To run the python files there 2 bash scripts that can be executed to run the specific protocol. 
To run the link state protocol execute: `./lsr.sh <topologyFile> <messageFile> <changesFile> [outputFile]`
To run the distance vector protocol execute: `./dvr.sh <topologyFile> <messageFile> <changesFile> [outputFile]`

## Viewing Doxygen Documentation
To view the Doxygen Documentation please open the html file `html/index.html` in a browser to view the files and the documentation of each function. 
On mac it can be opened through the terminal in the project directory with the command `open html/index.html`. 
