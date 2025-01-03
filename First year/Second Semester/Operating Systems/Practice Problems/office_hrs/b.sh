#!/bin/bash

#dir1 file1 dir2 file2 ...
# check if file in dir
# count nr of occurances of file in dir1 and subdirectories


if [ `expr $# % 2` -eq 1 ]; then
	echo "Nr of arguments must be even"
	exit 1
fi

echo "" > prob.txt

while [ $# -gt 0 ]; do
	dir=$1
	file=$2
	if [ ! -d $dir ]; then
		echo "$dir - not a directory!"
		exit 1
	fi
	#if [ ! -f "${dir}/${file}" ]; then
	#	echo "$file - not a file!"
	#	exit 1
	#fi
	
	shift 2
	
	count=`find $dir | grep -E -c "$file$"`

	if [ $count -eq 0 ]; then
		countzero=`expr $countzero + 1`
	fi
	
	echo "$dir $file $count" >> prob.txt		
done

sort -n -r -k3 prob.txt

echo "$countzero files do not appear even once"
