import MySQLdb, urllib2, subprocess

#User inputs sql loggin details
#username = raw_input("Put in the username you set for the sql database: ")
password = raw_input("Type the password you set to log into sql database: ")

db = MySQLdb.connect("localhost", "root", password)
cursor = db.cursor()
try:
	cursor.execute("create DATABASE radius")
	cursor.execute('GRANT ALL ON radius.* TO root@localhost IDENTIFIED BY "radiuspassword"')
	cursor.execute("FLUSH PRIVILEGES;")
	db.commit()
	print "all good"
	urllib.urlretrieve ("https://raw.githubusercontent.com/jhooper94/ucrm-freeradius-auth/master/stage3.sh", "stage3.sh")
	subprocess.call(['chmod', '+x', 'stage3.sh'])
	
	print "Type: sudo su"
	print "once logged in as root type ./stage3.sh"
except:
	db.rollback()
	print "It didn't work"
