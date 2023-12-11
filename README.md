# ucrm-freeradius v1.5

# Type command bellow in a fresh ubuntu 18.04 server to get started and follow the prompts as they pop up.

# wget https://raw.githubusercontent.com/jhooper94/ucrm-freeradius-auth/master/setup.sh && chmod +x setup.sh && ./setup.sh

This script will set up the tools needed to pull the mac address and package from ucrm and push the information into free radius database. 
You will use daloradius to set the packages so this script can pull the package name from ucrm and pass it into the database and that will que up the speeds. You will need to add your packages to daloradius with the same name you are using in ucrm and that will allow the mikrotik routers to set speed limits on your customers. 
This script currently does not have live sync and the way I have it implemented currently is everytime a package change or device mac address is added or changed you will have to run it. But live sync is planned for the future. 

#Roadmap
enable live syncing and trigger syncing through the use of ucrm pluggins.
