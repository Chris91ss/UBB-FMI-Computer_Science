#!/bin/bash

if [ $# -ne 1 ]; then
	echo "Invalid arguments"
	exit 1
fi

files=$(find $1 -type f -perm -o=w)
for file in $files
do
	echo $file
	stat -c "%a %n" $file
	chmod o-w $file
	stat -c "%a %n" $file
done

