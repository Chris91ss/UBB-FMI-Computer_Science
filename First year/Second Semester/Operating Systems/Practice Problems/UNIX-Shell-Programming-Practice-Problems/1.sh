#!/bin/bash

users=`awk '{print $1}' who.fake`

for user in $users
do
	cnt=`grep "^$user" ps.fake | wc -l`
	echo $user $cnt
done
