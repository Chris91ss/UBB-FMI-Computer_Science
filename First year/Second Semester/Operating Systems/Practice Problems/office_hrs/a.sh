#!/bin/bash

# par 1 - file ; par 2 ... letters
# for each letter create a file with all the words from f.txt that start with the respective letter

 
if [ ! -f $1 ]; then
	echo $1 needs to be a file.
	exit 1
fi

file=$1
shift 

for letter in $@; do
	if [[ $letter =~ ^[a-z]$ ]]; then
		grep -E -i -o "\<$letter[a-z]*\>" $file > "${letter}.txt"
	else
		echo $letter is not a letter
	fi
done
