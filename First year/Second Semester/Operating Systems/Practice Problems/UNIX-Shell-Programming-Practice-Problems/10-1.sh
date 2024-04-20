#!/bin/bash

# Get the current month in MMM format
current_month=$(date +'%b')

# Get sessions for this month using the last command, excluding reboots and wtmp entries
last_output=$(last | grep -v wtmp | grep -v reboot)

# Extract user names and count occurrences of each user for this month
user_sessions=$(echo "$last_output" | awk -v month="$current_month" '$5 ~ month { print $1 }' | sort | uniq -c)

# Sort user sessions by session count in descending order
echo "$user_sessions" | sort -nr

