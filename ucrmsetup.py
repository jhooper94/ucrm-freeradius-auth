import urllib2

url = "https://raw.githubusercontent.com/jhooper94/ucrm-freeradius-auth/master/master.py"

file_name = url.split('/')[-1]
u = urllib2.urlopen(url)
f = open(file_name, 'wb')
meta = u.info()
file_size = int(meta.getheaders("Content-Length")[0])
print "Downloading: %s Bytes: %s" % (file_name, file_size)

file_size_dl = 0
block_sz = 8192
while True:
    buffer = u.read(block_sz)
    if not buffer:
        break

    file_size_dl += len(buffer)
    f.write(buffer)
    status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
    status = status + chr(8)*(len(status)+1)
    print status,

f.close()

print "Time to configure"

password = raw_input("Enter the Password to log into the sql server:  ")

ucrm_url = raw_input("Enter in the url for ucrm, can be ip address:  ")

api_key = raw_input("Enter in ucrm api key:  ")

client_number = raw_input("Enter in a number above the number of clients you have:  ")

php = open("/var/www/html/daloradius/library/daloradius.conf.php","a+")
php.write("$configValues['CONFIG_DB_PASS'] = '" + password + "';")
php.close()

file = open("config.ini","a+")
file.write("[Radius]")
file.write("\n")
file.write("address = localhost")
file.write("\n")
file.write("username = root")
file.write("\n")
file.write("password = " + password)
file.write("\n")
file.write("table = radius")
file.write("\n")
file.write("[ucrm]")
file.write("\n")
file.write("ucrm_url = " + ucrm_url)
file.write("\n")
file.write("api_key = " + api_key)
file.write("\n")
file.write("[clients]")
file.write("\n")
file.write(" client_number = " + client_number)
file.close()

print "Just type ,python master.py, into cli to run the script to pull the user's mac address and there package name into freeradius."
print "Go to http://,address of server,/daloradius to change set up the packages name and speed so that it will set speed limits for the clients."
