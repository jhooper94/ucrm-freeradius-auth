from urllib2 import Request, urlopen
import json, os, MySQLdb, requests, configparser, sys
#v1.5b
#Parse Config File. To fill out the important information needed to make the script work.
config = configparser.ConfigParser()
config.readfp(open(r'config.ini'))
DB_address = config.get('Radius', 'address')
DB_username = config.get('Radius', 'username')
DB_password = config.get('Radius', 'password')
DB_table = config.get('Radius', 'table')
ucrm_url = config.get('ucrm', 'ucrm_url')
ucrm_key = config.get('ucrm', 'api_key')
clients = config.get('clients', 'client_number')
# Set the count to a number above the number of clients you have
count = clients
keywords = ('servicePlanName', 'firstName', 'lastName')
headers = {
  'Content-Type': 'application/json',
  'X-Auth-App-Key': ucrm_key
}
#progressbar
def progressbar(it, prefix="", size=60):
    count = len(it)
    def _show(_id):
        x = int(size*_id/count)
        sys.stdout.write("%s[%s%s] %i/%i\r" % (prefix, "#"*x, "."*(size-x), _id, count))
        sys.stdout.flush()

    _show(0)
    for id, item in enumerate(it):
        yield item
        _show(id+1)
    sys.stdout.write("\n")
    sys.stdout.flush()


# all variables needed. Set the address correctly to the same as what ucrm is running on.

url = "/api/v1.0/clients/services/"
url1 = "/service-devices"
url2 = "/api/v1.0/clients/services/"
url3 = "/api/v1.0/clients/"
sql =  """INSERT INTO radcheck(username, attribute, op, value) VALUES ('"""
sql1 = """','Auth-type', ':=', 'Accept')"""
sql2 = """INSERT INTO radusergroup(username, groupname, priority) VALUES ('"""
sql3 = """'"""
sql4 = """','1')"""
sql5 = """INSERT INTO userinfo (username, firstname, lastname) VALUES ('"""
sql6 = """)"""
# cleans out the database to prevent duplicates from causing errors. Make sure the MySQLdb info is set correctly.
db = MySQLdb.connect(DB_address, DB_username, DB_password, DB_table)
cursor = db.cursor()
try:
	cursor.execute("truncate table radcheck")
	cursor.execute("truncate table radusergroup")
	db.commit()
	print "Table is now empty Prepairing to load clients into database"
except:
	db.rollback()
	print "full table"
db.close()
#Start of for loop range
id = 1
for id in progressbar(range(1,int(count)), "Loading Clients: ", 40):

	# Checks to make sure the url is valid if not skips it
	valid = requests.get(ucrm_url + url + str(id) + url1, headers=headers)
	if valid.status_code == 200:
	# Request the mac address and write them to a file
        	request = Request(ucrm_url + url + str(id) + url1, headers=headers)
        	response_body = urlopen(request).read()
        	file = open(str(id) + ".json","w")
        	file.write(response_body)
        	file.close()

		# Open the file with the mac address and write it to free radius database
		with open(str(id) + '.json') as json_file:
        		for line in json_file.readlines():
				mac = json.loads(line)

		for mac in mac:
			# change database authentication details to match yours.
			db = MySQLdb.connect(DB_address,DB_username,DB_password,DB_table)
			cursor = db.cursor()
			try:
				cursor.execute(sql + mac["macAddress"] + sql1)
				db.commit()
			except:
				db.rollback()
			db.close()

		# request the package and write them to a file
		request1 = Request(ucrm_url + url2 + str(id), headers=headers)
		response_body2 = urlopen(request1).read()
		file = open(str(id) + "-speed.json","w")
		file.write(response_body2)
		file.close()
	
		keywords = ('servicePlanName')
		# opens the files containing the package and writes them to the database
		with open(str(id) + '-speed.json') as json_file:
			# Change authentication details to match yours.
                	db = MySQLdb.connect(DB_address,DB_username,DB_password,DB_table)
                	cursor = db.cursor()
                	for line in json_file.readlines():

                       		json_dict = json.loads(line)
                       		if any(keyword in json_dict['servicePlanName'].lower() for keyword in keywords):
                               		try:
                                       		cursor.execute(sql2 + mac["macAddress"] + sql3 + "," + sql3 + json_dict["servicePlanName"] + sql4)
                                      		db.commit()
                               		except:
                                      		db.rollback()
                               		db.close()
				# Deletes all the files created
				os.remove(str(id)+".json")
				os.remove(str(id)+"-speed.json")
				# starts over the while loop.

print "All Clients loaded."
