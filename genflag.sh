#!/bin/bash
token="team"
while true :
j=1
do
 for i in {0..1};
  do
   random=$(cat /dev/urandom | head -n 10 | md5sum | head -c 32 )
   left="flag{"
   right="}"
   flag=${left}${random}${right}
   echo $flag > /home/awd/gamebox/awd_gamebox/team$i/flag
   flagpara="flag="${flag}"&token="${token}${i}"&cha=pwn1&round="${j}
   curl 127.0.0.1:5000/flag -d $flagpara
  done
sleep 120
j=j+1
done
