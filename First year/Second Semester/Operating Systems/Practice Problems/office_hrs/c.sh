#!/bin/bash

# read strings until stop
# count how many start with a vowel

count=0

while true; do
	read string
	if [ $string == "stop" ]; then
		break
	fi
	if echo "$string" | grep -E -q "\<[aeiou][a-z]*\>"; then
		count=`expr $count + 1`	
	fi
done

echo $count words start with a vowel
