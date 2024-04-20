#!/bin/bash

# Initialize a counter to keep track of the number of files found
count=0

# Find recursively in the specified directory for .c files and loop over the results
find $1 -type f -name "*.c" | while read -r file
do
    # Count the lines in the current file
    lines=$(wc -l < "$file")

    # Check if the number of lines exceeds 500
    if [ "$lines" -gt 500 ]; then
        # Print the filename and the number of lines
        echo "$file has $lines lines."

        # Increment the counter
        count=$(expr $count + 1)

        # Check if we have found 2 files
        if [ "$count" -eq 2 ]; then
            echo "Found 2 files with more than 500 lines. Exiting."
            break
        fi
    fi
done
