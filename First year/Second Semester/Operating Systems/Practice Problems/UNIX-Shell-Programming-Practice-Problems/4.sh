#!/bin/bash

if [ $# -ne 1 ]; then
	echo "Invalid arguments"
	exit 1
fi

files=$(find $1 -type l)
for file in $files
do
	if [ test ! -e $file ]; then
		echo "$file points to a non-existent file/directory"
	fi
done


