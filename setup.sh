#!/bin/bash

sudo apt-add-repository multiverse && sudo apt-get update

sudo apt-get upgrade

sudo apt install python

sudo apt-get install apache2 

sudo apt-get install php libapache2-mod-php php-gd php-common php-mail php-mail-mime php-mysql php-pear php-db php-mbstring php-xml php-curl

sudo apt-get install software-properties-common

sudo apt-key adv --recv-keys --keyserver hkp://keyserver.ubuntu.com:80 0xF1656F24C74CD1D8

sudo add-apt-repository 'deb [arch=amd64] http://mirror.zol.co.zw/mariadb/repo/10.3/ubuntu bionic main'

sudo apt update

sudo apt -y install mariadb-server mariadb-client

sudo apt install python-pip

sudo pip install MySQL-python

wget https://raw.githubusercontent.com/jhooper94/ucrm-freeradius-auth/master/stage2.py

python stage2.py
