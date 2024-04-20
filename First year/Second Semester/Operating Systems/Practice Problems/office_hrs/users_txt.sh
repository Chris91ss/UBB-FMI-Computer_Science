#!/bin/bash

# Script ./users.sh     user1    n1    user2   n2    user3    n3   ...
# Write a message if user1 connected n1 times on the system

if [ `expr $# % 2` -eq 1 ]; then
	echo "We need an even number of arguments."
	exit 1
fi

echo ""> sol.txt

while [ $# -gt 0 ]; do
	echo $1 $2
	if grep -E -q "^$1:" /etc/passwd ; then
		echo $1 is a valid user from the system.
		if echo $2 | grep -E -q "^[1-9][0-9]*$" ; then
			echo $2 is a number.
			nr=`last | grep -E "Fri[ ]*Apr" | grep -E -c "^$1"`
			if [ $nr -ge $2 ] ; then
				echo $1 logged in of a minimum $2 times in the system on Friday of April. >> sol.txt
			else
				echo $1 logged in to few times. >> sol.txt
			fi
		else 
			echo $2 is not a number, ignore the tuple of arguments.
		fi
	else 
		echo $1 is not a valid user from the system, we ignore it.
	fi
	shift 2
done

cat sol.txt | sort
