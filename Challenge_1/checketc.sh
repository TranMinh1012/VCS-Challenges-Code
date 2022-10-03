#!/bin/bash

echo "[Log checketc - `date +%T` `date +%d'/'%m'/'%Y`]" >> /var/log/checketc.log

BASEDIR="/etc"

#1.Kiem tra thu muc /etc xem co file nao duoc tao moi khong
echo -e "\n=== Danh sach file tao moi ====\n" >> /var/log/checketc.log
ls -A $BASEDIR > newfiles
CHECKNEWFILE=$(diff oldfiles newfiles | cut -f 2 -d "")
for file in $CHECKNEWFILE
do
   if [ -e $BASEDIR/$file ]
   then
      echo $file >> /var/log/checketc.log
      ls -A $BASEDIR > oldfiles
      FILETYPE=$(file $BASEDIR/$file | cut -d" " -f2)
      if [[ $FILETYPE = "ASCII" ]]
      then
         LINE=$(head -10 $BASEDIR/$file)
         echo -e "\n10 dong dau tien cua file la: \n$LINE" >> /var/log/checketc.log
      fi
   fi
done

#2.Kiem tra thu muc /etc co file nao thay doi khong
echo -e "\n=== Danh sach file sua doi ===\n" >> /var/log/checketc.log
listfileModified=$(sudo find /etc -mmin -15)
echo $listfileModified >> /var/log/checketc.log

#3.Kiem tra thu muc /etc co file nao bi xoa khong
echo -e "\n=== Danh sach file bi xoa ===\n" >> /var/log/checketc.log
ls -A $BASEDIR > currentfiles
while read -r file;
do
   check=$(grep -w $file -m 1 currentfiles)
   if [ ! $check ]
   then
      echo $file >> /var/log/checketc.log
   fi
done < oldfiles
ls -A $BASEDIR > oldfiles

#4. Day log ra file /var/log/checketc.log
#5. Gui email cho quan tri vien root@localhost
#mail -s "Log checketc" root@localhost < /var/log/checketc.log
