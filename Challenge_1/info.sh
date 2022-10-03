#!/bin/bash

echo "[Thong tin he thong]"

NAME=$(uname -o)
echo "Ten may: $NAME\n"

DISTRIBUTIONS=$(lsb_release -d)
echo -e "Ten ban phan phoi: \n$DISTRIBUTIONS\n"

VERSION=$(uname -v)
echo -e "Phien ban he dieu hanh: $VERSION\n"

CPUINFO=$(lscpu)
echo -e "Thong tin CPU: \n$CPUINFO\n"

RAMINFO=$(free -h)
echo -e "Thong tin bo nho vat ly: \n$RAMINFO\n"

FREEDISK=$(df)
echo -e "Thong tin o dia con trong: \n$FREEDISK\n"

IPLIST=$(ip addr show | grep "inet")
echo -e "Danh sach dia chi IP cua he thong: \n$IPLIST\n"

USERLIST=$(cut -d: -f1 /etc/passwd | sort)
echo -e "Danh sach user tren he thong: \n$USERLIST\n"

ROOTPROCESS=$(ps -f -U root -u root)
echo -e "Thong tin cac tien trinh dang chay voi quyen root: \n$ROOTPROCESS\n"

OPENPORT=$(ss -lnptu)
echo -e "Thong tin cac port dang mo: \n$OPENPORT\n"

OTHER_CAN_WRITE=$(find / -type d -perm /o=w)
echo -e "Danh sach cac thu muc tren he thong cho phep other co quyen ghi: \n$OTHER_CAN_WRITE\n"

INSTALLED=$(dpkg -l)
echo -e "Danh sach cac goi phan mem duoc cai dat tren he thong: \n$INSTALLED\n"
