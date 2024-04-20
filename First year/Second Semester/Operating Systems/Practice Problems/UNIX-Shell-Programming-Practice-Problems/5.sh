#!/bin/bash

while true
do
	programs=$(ps -e | awk '{print $4}' | tail -n +2)
	for program in $programs
	do
		for argument in "$@"
		do
			if [ "$argument" = "$program" ]; then
				kill -9 $(pgrep "$program")
				echo "Killed $program"
			fi
		done
	done
	sleep 1
done

