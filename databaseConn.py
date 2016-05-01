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
	
def check_db():
	conn=sqlite3.connect('mydatabase.db')
	curs=conn.cursor()
	#curs.execute("CREATE TABLE instances (instanceNum NUMERIC, path TEXT, nodeName, TEXT, IPAddress TEXT, port NUMERIC); ")
	print "\nEntire database contents:\n"
	for row in curs.execute("SELECT * FROM instances"):
		print row
	#print "\nDatabase entries for the first instance:\n"
	#for row in curs.execute("SELECT * FROM instances where instanceNum=0"):
	#	print row
	#add_instance('Node1', '/root', '80.5.4.3', 5000)
	conn.close()
