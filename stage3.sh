#!/bin/bash

sudo su

apt-get install freeradius freeradius-mysql freeradius-utils

apt-get install freeradius freeradius-mysql freeradius-utils

mysql -u root -p radius < /etc/freeradius/3.0/mods-config/sql/main/mysql/schema.sql

ln -s /etc/freeradius/3.0/mods-available/sql /etc/freeradius/3.0/mods-enabled/

wget https://raw.githubusercontent.com/jhooper94/ucrm-test/master/sql

rm /etc/freeradius/3.0/mods-enabled/sql

mv sql /etc/freeradius/3.0/mods-enabled/sql

chgrp -h freerad /etc/freeradius/3.0/mods-available/sql

chown -R freerad:freerad /etc/freeradius/3.0/mods-enabled/sql

systemctl restart freeradius.service

wget https://raw.githubusercontent.com/jhooper94/ucrm-test/master/ucrmsetup.py

python ucrmsetup.py

