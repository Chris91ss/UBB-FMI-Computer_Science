#!/bin/bash

# delete the appearances of the multiple of 3 of a word, from a file


if [ ! -f $1 ]; then
	echo $1 is not a file.
fi

while read line ; do
	count=0
	for word in $line; do
		if [ $word = $2 ] ; then
			count=`expr $count + 1`
			if [ `expr $count % 3` -ne 0 ]; then
				echo $word appears $count times 
			fi		
		else
			echo $word	
		fi
	done
		
done < $1  # reads line by line from the file
