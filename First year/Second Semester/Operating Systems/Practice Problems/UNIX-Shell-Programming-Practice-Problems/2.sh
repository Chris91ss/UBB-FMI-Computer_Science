#!/bin/bash

if [ $# -ne 1 ]; then
	echo "Invalid arguments"
	exit 1
fi

cnt=0
files=$(find $1 -type f -name "*.c")
for file in $files
do
	lines=$(wc -l < "$file")
	if [ $lines -gt 500 ]; then
		echo $file
		cnt=$((cnt+1))
	fi
	if [ $cnt -eq 2 ]; then
		break
	fi
done


