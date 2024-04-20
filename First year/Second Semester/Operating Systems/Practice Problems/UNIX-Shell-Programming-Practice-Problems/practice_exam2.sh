#!/bin/bash


#Write a shell script that will read inputs from keyboard until the user writes "stop"
#For each input, the script will have to do the following:
    #-if the input is a directory, it will print the latest modified .txt file in that directory.
    #-if  the input is a file, it will delete all the lines containing word "ana" (case insensitive)
    #-if the input it is neither a directory or a file, it will pint a proper message on the screen.
    #At the end the script will print on the screen what is the percentage of directories , files and other aruments


dir_count=0
file_count=0
error_count=0

while :
do
	read input
	
	if [ "$input" == "stop" ]; then
		break
	fi

	if [ -d "$input" ]; then
		((dir_count++))
		
		lates_txt_file=$(find "$input" -type -f -name "*.txt" -printf "%T@ %p\n" | sort -n | tail -1 | cut -d ' ' -f 2)

		if [ -z "$latest_txt" ]; then
                	echo "No .txt files found in $input"
                else
                	echo "Latest modified .txt file in $input: $latest_txt"
                fi
	elif [ -f "$input" ]
		((file_count++))
		sed -i "/ana/Id" "$input"
		echo "Lines containing ana were deleted from $input" 		
	else
		((error_count++))
		echo "$input is neither a directory nor a file!"
	fi

done

total_arg=$((dir_count + file_count + error_count))
dir_percentage=$((dir_count * 100 / total_arg))
file_percentage=$((file_count * 100 / total_arg))
error_percentage=$((error_count * 100 / total_arg))

echo $dir_percentage
echo $file_percentage
echo $error_percentage

