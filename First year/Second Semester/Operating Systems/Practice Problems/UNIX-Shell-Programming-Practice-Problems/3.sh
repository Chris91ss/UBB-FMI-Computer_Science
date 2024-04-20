#!/bin/bash

if [ $# -ne 1 ]; then
	echo "Invalid arguments"
	exit 1
fi

for file in $(find $1 -type f -name "*.log")
do
	sort "$file" -o "$file"
done

