#!/bin/bash

# Create files if they don't exist
touch file-reports.info user-reports.info errors-report.info

# Initialize counters
file_count=0
user_count=0
error_count=0
total_lines=0
total_chars=0

# Function to calculate average number of lines and characters in a file
calculate_average() {
    local file="$1"
    local lines=$(wc -l < "$file")
    local chars=$(wc -m < "$file")
    total_lines=$((total_lines + lines))
    total_chars=$((total_chars + chars))
}

# Loop through command line arguments
for arg in "$@"; do
    if [ -f "$arg" ]; then
        # File exists
        calculate_average "$arg"
        ((file_count++))
    elif grep -q "^$arg:" /etc/passwd; then
        # User exists
        user_info=$(grep "^$arg:" /etc/passwd)
        username=$(echo "$user_info" | cut -d: -f1)
        family_name=$(echo "$user_info" | cut -d: -f5 | cut -d, -f1)
        homedir=$(echo "$user_info" | cut -d: -f6)
        echo "$username $family_name $homedir" >> user-reports.info
        ((user_count++))
    else
        # Not found
        echo "$arg" >> errors-report.info
        ((error_count++))
    fi
done

# Calculate percentages
total_args=$#
file_percent=$((file_count * 100 / total_args))
user_percent=$((user_count * 100 / total_args))
error_percent=$((error_count * 100 / total_args))

# Calculate average number of lines and characters
if [ "$file_count" -ne 0 ]; then
    avg_lines=$((total_lines / file_count))
    avg_chars=$((total_chars / file_count))
fi

# Print info message
echo "Files: $file_percent%"
echo "Usernames: $user_percent%"
echo "Errors: $error_percent%"
echo "Average lines in files: $avg_lines"
echo "Average characters in files: $avg_chars"

#Write a shell script that will receive as command line arguments a list of possible files or usernames.
    
#for the arguments that are files, it will be stored in a file named file-reports.info the number of files found, the average number of lines and characters.
#if the argument indicates the name of an existing usernames (you can use /etc/passwd), it will store in a file named user-reports.info the username, its family name (can be found right after the group) and the homedirectory.
#if it was not found a file/user with the value of the argument, the script will store the values in a file name errors-report.info

#    At the end, the script will have to print an info message telling what was the percentage of arguments that were files, usernames or none of them.

#Note: file-reports.info, user-reports.info, errors-report.info must be created if they do not exist.
