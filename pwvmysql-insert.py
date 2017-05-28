#!/usr/bin/python
import getpass
import MySQLdb
import sys, os

os.system('clear')
passwd = getpass.getpass("Enter your pwv password: ")

# Open database connection
db = MySQLdb.connect("localhost","root",passwd,"pwv" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

name = raw_input("Enter your name: ")
mfile = raw_input("Enter your login: ")
keys = raw_input("Enter your password: ")

# Prepare SQL query to INSERT a record into the database.
sql = "INSERT INTO email(name, mfile, keys) VALUES ('%s', '%s', '%s')" % (name, mfile, keys)
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

