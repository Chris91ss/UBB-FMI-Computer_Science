#!/bin/bash

#Write a shell script that will read inputs from keyboard until the user writes "stop".

#For each input, the script will have to do the following:
#    - if the input is an existing user (you can use /etc/passwd) it will print the number of directories existing in the user homepath (recursive)
#    - if the input is a file, it will perform a replace operation that will uppercase all lowercase vowels and it will overwrite the content of the file.
#    - if the input it is neiter an user or file, it will print a proper message on the screen.

#At the end the script will print on the screen what is the percentage of users, files and others arguments read from keyboard during the script lifetime.


user_count=0
file_count=0
other_count=0
while :
do
     read input
     if [ "$input" == "stop" ]; then
         break
     fi

     if grep -q "^$input:" /etc/passwd; then
         ((user_count++))
         home_dir=$(grep "^$input:" /etc/passwd | awk -F: '{print $6}')
         nr_dir=$(find "$home_dir" -type d | wc -l)
         echo $nr_dir
     elif [ -f $input ]; then
         ((file_count++))
         sed -i 's/[aeiou]/\U&/g' "$input"
     else
         ((other_count++))
         echo "$input is neither an user nor a file"
     fi
 done

total_arg=$((user_count + file_count + other_count))
user_percentage=$((user_count * 100 / total_arg))
file_percentage=$((file_count * 100 / total_arg))
other_percentage=$((other_count * 100 / total_arg))
 
echo "Percentage of users: $user_percentage%"
echo "Percentage of files: $file_percentage%"
echo "Percentage of other: $other_percentage%"


