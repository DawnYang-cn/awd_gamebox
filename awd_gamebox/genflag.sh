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
 curl 127.0.0.1:5000/flag -d $flagpara
 sleep 10
done
