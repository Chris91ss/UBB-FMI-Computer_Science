#!/bin/bash

if [ $# -ne 1 ]; then
	echo "Invalid arguments"
	exit 1
fi

emails=""
usernames=$(awk '{print $1}' $1)
for username in $usernames
do
	emails+="$username@scs.ubbcluj.ro,"
done

emails=${emails%,}

echo $emails

