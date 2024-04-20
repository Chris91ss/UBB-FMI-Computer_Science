#!/bin/bash


#Write a shell script that will receive as command line arguments a list of possible files or usernames.   
	#if the argument indicates the name of an existing file (recursive), it will store in a file named file-reports.info the full path of the file, its size and the last modified date.
	#if the argument indicates the name of an existing test usernames (you can use /etc/passwd), it will store in a file named user-reports.info the username and its group.
	#if it was not found a file/user with the value of the argument, the script will store the values in a file name errors-report.info

        #At the end, the script will have to print an info message telling what was the percentage of arguments that were files, usernames or none of them.


touch file-reports.info user-reports.info errors-reports.info


number_files=0
number_usernames=0
number_errors=0

for arg in "$@"; do

	if [ -f "$arg" ]; then
		echo "File: $arg" >> file-reports.info
		echo "Size: $(du -h "$arg" | cut f1)" >> file-reports.info
		echo "Last Modified: $(stat -c %y "$arg")" >> file-reports.info
		((number_files++))
	elif grep -q "^$arg:" passwd.fake; then
		echo $arg >> user-reports.info
		grep "^$arg:" passwd.fake | awk -F/ '{print $4}' >> user-reports.info
		((number_usernames++))
	else
		echo "$arg" >> errors-reports.info
		((number_errors++))
	fi
done


if [ $# -ne 0 ]; then
	total_args=$#
	file_percentage=$((number_files * 100 / total_args))
	user_percentage=$((number_usernames * 100 / total_args))
	errors_percentage=$((number_errors * 100 / total_args))

	echo $file_percentage
	echo $user_percentage
	echo $errors_percentage
fi

