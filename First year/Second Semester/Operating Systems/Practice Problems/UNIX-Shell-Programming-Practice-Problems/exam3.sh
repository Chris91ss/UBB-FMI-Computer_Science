#!/bin/bash

#Write a shell script that will read inputs from keyboard until the user writes "stop"

#For each input, the script will have to do the following:

#-if the input is a directory, it will print the latest modified .txt file in that directory.
#-if  the input is a file, it will delete all the lines containing word "ana" (case insensitive)
#-if the input it is neither a directory or a file, it will pint a proper message on the screen.

#At the end the script will print on the screen what is the percentage of directories , files and other aruments



# Initialize variables to count directories, files, and other inputs
dir_count=0
file_count=0
other_count=0

# Loop to read inputs until "stop" is entered
while :
do
    # Read input from keyboard
    read -p "Enter a directory, file, or 'stop' to exit: " input

    # Check if input is "stop"
    if [ "$input" == "stop" ]; then
        break
    fi

    # Check if input is a directory
    if [ -d "$input" ]; then
        # Increment directory count
        ((dir_count++))

        # Find the latest modified .txt file in the directory
        latest_txt=$(find "$input" -type f -name "*.txt" -printf "%T@ %p\n" | sort -n | tail -1 | cut -d ' ' -f 2)

        if [ -z "$latest_txt" ]; then
            echo "No .txt files found in $input"
        else
            echo "Latest modified .txt file in $input: $latest_txt"
        fi

    # Check if input is a file
    elif [ -f "$input" ]; then
        # Increment file count
        ((file_count++))

        # Delete lines containing "ana" (case insensitive)
        sed -i '/ana/Id' "$input"
        echo "Lines containing 'ana' deleted from $input"

    # If input is neither a directory nor a file
    else
        # Increment other count
        ((other_count++))
        echo "Input '$input' is neither a directory nor a file"
    fi
done

# Calculate percentages
total_inputs=$((dir_count + file_count + other_count))
dir_percentage=$((100 * dir_count / total_inputs))
file_percentage=$((100 * file_count / total_inputs))
other_percentage=$((100 * other_count / total_inputs))

# Print percentages
echo "Percentage of directories: $dir_percentage%"
echo "Percentage of files: $file_percentage%"
echo "Percentage of other inputs: $other_percentage%"
