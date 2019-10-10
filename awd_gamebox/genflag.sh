#!/bin/bash
token="team1"
while true :
do
 random=$(cat /dev/urandom | head -n 10 | md5sum | head -c 32 )
 left="flag{"
 right="}"
 flag=${left}${random}${right}
 echo $flag > /home/ctf/flag
 flagpara="flag="${flag}"&token="${token}
 curl 10.0.75.1:5000/flag -d $flagpara
 sleep 10
done
