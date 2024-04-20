#!/bin/bash

# Check if directory argument is provided
if [ $# -ne 1 ]; then
    echo "Invalid arguments"
    exit 1
fi

# Find recursively in the specified directory for files with write permissions for everyone
find "$1" -type f -perm -o=w | while read -r file; do
    # Display file name
    echo "File: $file"

    # Display permissions before removing write permission
    echo "Permissions before removing write permission:"
    ls -l "$file" | awk '{print $1}'

    # Remove write permission for everybody
    chmod a-w "$file"

    # Display permissions after removing write permission
    echo "Permissions after removing write permission:"
    ls -l "$file" | awk '{print $1}'

    echo "---------------------------------------------"
done
