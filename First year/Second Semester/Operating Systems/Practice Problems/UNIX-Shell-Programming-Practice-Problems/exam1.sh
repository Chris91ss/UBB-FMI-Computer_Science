#!/bin/bash

# Create files if they don't exist
touch file-reports.info user-reports.info errors-report.info

# Initialize counters
file_count=0
user_count=0
error_count=0

# Loop through command line arguments
for arg in "$@"; do
    if [ -f "$arg" ]; then
        # File exists
        echo "File: $arg" >> file-reports.info
        echo "Size: $(du -h "$arg" | cut -f1)" >> file-reports.info
        echo "Last Modified: $(stat -c %y "$arg")" >> file-reports.info
        ((file_count++))
    elif grep -q "^$arg:" /etc/passwd; then
        # User exists
        echo "$arg: $(id -gn "$arg")" >> user-reports.info
        ((user_count++))
    else
        # Not found
        echo "$arg" >> errors-report.info
        ((error_count++))
    fi
done


if [ "$#" -ne 0 ]; then

	# Calculate percentages
	total_args=$#
	file_percent=$((file_count * 100 / total_args))
	user_percent=$((user_count * 100 / total_args))
	error_percent=$((error_count * 100 / total_args))

	# Print info message
	echo "Files: $file_percent%"
	echo "Usernames: $user_percent%"
	echo "Errors: $error_percent%"
fi

#Write a shell script that will receive as command line arguments a list of possible files or usernames.
    
#if the argument indicates the name of an existing file (recursive), it will store in a file named file-reports.info the full path of the file, its size and the last modified date.
#if the argument indicates the name of an existing test usernames (you can use /etc/passwd), it will store in a file named user-reports.info the username and its group.
#if it was not found a file/user with the value of the argument, the script will store the values in a file name errors-report.info

#    At the end, the script will have to print an info message telling what was the percentage of arguments that were files, usernames or none of them.

#Note: file-reports.info, user-reports.info, errors-report.info must be created if they do not exist.
