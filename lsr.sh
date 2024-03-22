#!/bin/bash

# Check if correct number of arguments are provided
if [ $# -lt 3 ] || [ $# -gt 4 ]; then
    echo "Usage: $0 <topologyFile> <messageFile> <changesFile> [outputFile]"
    exit 1
fi

topologyFile=$1
messageFile=$2
changesFile=$3
outputFile=$4

# Check if Python is installed
if ! command -v python &> /dev/null; then
    echo "Python is not installed. Please install Python to run this script."
    exit 1
fi

# Check if topology file exists
if [ ! -f "$topologyFile" ]; then
    echo "Topology file not found: $topologyFile"
    exit 1
fi

# Check if message file exists
if [ ! -f "$messageFile" ]; then
    echo "Message file not found: $messageFile"
    exit 1
fi

# Check if changes file exists
if [ ! -f "$changesFile" ]; then
    echo "Changes file not found: $changesFile"
    exit 1
fi

# Execute Distance Vector Routing
if [ -z "$outputFile" ]; then
    python src/linkstate.py "$topologyFile" "$messageFile" "$changesFile"
else
    python src/linkstate.py "$topologyFile" "$messageFile" "$changesFile" > "$outputFile"
fi
