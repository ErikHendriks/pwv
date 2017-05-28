#!/usr/bin/python

import MySQLdb

# Open database connection
db = MySQLdb.connect("localhost","root","pw","pwv" )

# prepare a cursor object using cursor() method
cursor = db.cursor()
choice = raw_input("Enter your choice: ") 
# Prepare SQL query to DELETE required records
sql = "DELETE FROM email WHERE id > '%s'" % (choice)
try:
   # Execute the SQL command
   cursor.execute(sql)
   # Commit your changes in the database
   db.commit()
except:
   # Rollback in case there is any error
   db.rollback()

# disconnect from server
db.close()
