#!/usr/bin/python
import sqlite3

def add_instance(nodeName, path, ipadd, portno):
	conn=sqlite3.connect('mydatabase.db')
	curs=conn.cursor()
	curs.execute("SELECT count(*) from instances")
	maxVal = 0
	row = curs.fetchone()
	if row is None:
   		print "No instances"
	else:
   		maxVal = int(row[0])
		maxVal = maxVal + 1
	
	# I used triple quotes so that I could break this string into
	# two lines for formatting purposes.
	curs.execute("""INSERT INTO instances values((?), (?), (?),
    	(?), (?))""", (maxVal, path, nodeName, ipadd, portno))
	# commit the changes
	conn.commit()
	conn.close()
	# end add_instance

def add_worker(workerIP):
	conn=sqlite3.connect('mydatabase.db')
	curs=conn.cursor()
	curs.execute("SELECT count(*) from workers")
	maxVal = 0
	row = curs.fetchone()
	if row is None:
   		print "No instances"
	else:
   		maxVal = int(row[0])
		maxVal = maxVal + 1
	#insert into workers table
	curs.execute('INSERT INTO workers values ((?), (?))',(maxVal,workerIP))
	# commit the changes
	conn.commit()
	conn.close()
	
def check_dups(appName):
	h =0
	conn=sqlite3.connect('mydatabase.db')
	cursor = conn.cursor()
	q = 'SELECT * from instances where nodeName = \''+appName+'\''
	print q
	howMany = cursor.execute(q)
	h = len(howMany.fetchall())
	#print "length of the cursor "+str(len(howMany.fetchall()))
	print "row count for "+appName+ " = "+str(h)
	if (h > 1):
		print "Duplicate entry: " + appName
		conn.close()
	# end check_dups
	return h

def get_workerIP():
	conn=sqlite3.connect('mydatabase.db')
	cursor = conn.cursor()
	cursor.execute('SELECT ip from workers')
	retIP = cursor.fetchone()[0]
	print retIP
	return retIP
	
def get_availablePorts(ip):
	conn=sqlite3.connect('mydatabase.db')
	conn.row_factory = lambda cursor, row: row[0]
	cursor = conn.cursor()
	allPorts = ['8777','8778','8779']
	q= 'SELECT port from instances where IPAddress =\''+ip+'\''
	
	ports = cursor.execute(q).fetchall()
	#portArr = []
	#for portTuple in ports
		#portArr.append(portTuple)
	print "ports taken in db"
	print ports
	for item in allPorts:
		print "item = "+ item
		if int(item) not in ports:
			print "Selected port num = "+item
			return item
	return -1	

def check_db():
	conn=sqlite3.connect('mydatabase.db')
	curs=conn.cursor()
	#curs.execute("CREATE TABLE instances (instanceNum NUMERIC, path TEXT, nodeName TEXT, IPAddress TEXT, port NUMERIC); ")
	print "\nEntire database contents:\n"
	for row in curs.execute("SELECT * FROM instances"):
		print row
	#print "\nDatabase entries for the first instance:\n"
	#for row in curs.execute("SELECT * FROM instances where instanceNum=0"):
	#	print row
	#add_instance('Node1', '/root', '80.5.4.3', 5000)
	conn.close()
