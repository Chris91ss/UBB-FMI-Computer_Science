#!/bin/bash

df -h | tail -n +2 | awk '{
	usage = substr($2, 1, length($2) - 1)
	freeSpace = 100 - usage
	
	if ($2 < '1GB' || usage < 20 ) {
		print $1 " size " $2 " freeSpace " freeSpace 
	}
}'


