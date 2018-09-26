 #!/usr/bin/python
from urllib2 import Request, urlopen
import json, os, MySQLdb
# Set the count to a number above the number of clients you have
count = 1700
keywords = ('servicePlanName', 'firstName', 'lastName')
headers = {
  'Content-Type': 'application/json',
  'X-Auth-App-Key': 'put the app auth read key here'
}
# all variables needed. Set the address correctly to the same as what ucrm is running on.
url = "https://"ucrm address here"/api/v1.0/clients/services/"
url1 = "/service-devices"
url2 = "https://"ucrm address here"/api/v1.0/clients/services/"
url3 = "https://"ucrm address here"/api/v1.0/clients/"
sql =  """INSERT INTO radcheck(username, attribute, op, value) VALUES ('"""
sql1 = """','Auth-type', ':=', 'Accept')"""
sql2 = """INSERT INTO radusergroup(username, groupname, priority) VALUES ('"""
sql3 = """'"""
sql4 = """','1')"""
sql5 = """INSERT INTO userinfo (username, firstname, lastname) VALUES ('"""
sql6 = """)"""
# cleans out the database to prevent duplicates from causing errors. Make sure the MySQLdb info is set correctly.
db = MySQLdb.connect("localhost","root","password","radius")
cursor = db.cursor()
try:
        cursor.execute("truncate table radcheck")
        cursor.execute("truncate table radusergroup")
        db.commit()
        print "empty table"
except:
        db.rollback()
        print "full table"
db.close()
# Start of while loop
id = 1
while (id < count):
        # Request the mac address and write them to a file
        request = Request(url + str(id) + url1, headers=headers)
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
                db = MySQLdb.connect("localhost","root","password","radius")
                cursor = db.cursor()
                try:
                        cursor.execute(sql + mac["macAddress"] + sql1)
                        db.commit()
                        print "It works" + str(id)
                except:
                        db.rollback()
                        print "It didn't"
                        print(sql + mac["macAddress"] + sql1)
                db.close()

        # request the package and write them to a file
        request1 = Request(url2 + str(id), headers=headers)
        response_body2 = urlopen(request1).read()
        file = open(str(id) + "-speed.json","w")
        file.write(response_body2)
        file.close()

        keywords = ('servicePlanName')
        # opens the files containing the package and writes them to the database
        with open(str(id) + '-speed.json') as json_file:
                # Change authentication details to match yours.
                db = MySQLdb.connect("localhost","root","password","radius")
                cursor = db.cursor()
                for line in json_file.readlines():

                        json_dict = json.loads(line)
                        if any(keyword in json_dict['servicePlanName'].lower() for keyword in keywords):
                                try:
                                        cursor.execute(sql2 + mac["macAddress"] + sql3 + "," + sql3 + json_dict["servicePlanName"] + sql4)
                                        db.commit()
                                        print "It works" + str(id)
                                except:
                                        db.rollback()
                                        print "It didn't no mac address"
                                db.close()
                        # Deletes all the files created
                        os.remove(str(id)+".json")
                        os.remove(str(id)+"-speed.json")
                        # starts over the while loop.
                        id = id + 1