#!/bin/bash

# Check if directory argument is provided
if [ $# -ne 1 ]; then
    echo "Usage: $0 <directory>"
    exit 1
fi

# Find all files in the directory hierarchy and calculate their checksums
find "$1" -type f -exec md5sum {} + |\
# Use awk to group files by checksum and print those with more than one occurrence
awk '{if (++count[$1] == 2) print $2}'

