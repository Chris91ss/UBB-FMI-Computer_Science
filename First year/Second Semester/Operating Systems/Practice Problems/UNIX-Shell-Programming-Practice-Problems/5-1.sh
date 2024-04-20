#!/bin/bash

# Check if dangerous program names are provided as command-line arguments
if [ $# -eq 0 ]; then
    echo "Usage: $0 <dangerous_program1> [<dangerous_program2> ...]"
    exit 1
fi

# Infinite loop to continuously monitor processes
while true; do
    # Iterate over each dangerous program provided as argument
    for program in "$@"; do
        # Check if any process matching the program name is running
        pgrep -x "$program" > /dev/null
        if [ $? -eq 0 ]; then
            echo "Dangerous program '$program' is running. Killing..."
            pkill -x "$program"
        fi
    done
    # Sleep for a while before checking again
    sleep 5
done
