#!/bin/bash

touch mail.txt oldlist.txt newlist.txt

who > newlist.txt

while read -r line
do
   check=$(grep -w "$line" -m 1 oldlist.txt)
   if [ ! $check ];
   then
      echo -e "User" "$(echo "$line" | awk '{print $1}')" "dang nhap thanh cong vao thoi gian"
              "$(echo "$line" | awk '{print $4}') $(echo "$line" | awk '{print $3}')" > mail.txt
   fi
done < newlist.txt
cat mail.txt | mail -s "SSH login log" root@localhost
cat newlist.txt > oldlist.txt
