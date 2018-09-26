# ucrm-freeradius
Master.py is the script that you need.
This will pull the mac address and package from ucrm and push the information into free radius database.
Follow this tutorial to set up free radius and daloradius. https://computingforgeeks.com/how-to-install-freeradius-and-daloradius-on-ubuntu-18-04-ubuntu-16-04/
You will use daloradius to set the packages so this script can pull the package name from ucrm and pass it into the database and that will que up the speeds. You will need to add your packages to daloradius with the same name you are using in ucrm and that will allow the mikrotik routers to set speed limits on your customers. 
This script currently does not have live sync and the way I have it implemented currently is everytime a package change or device mac address is added or changed you will have to run it. But live sync is planned for the future. 
