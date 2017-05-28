#!/usr/bin/python
import getpass
import MySQLdb
import sys
import os

os.system('clear')
passwd = getpass.getpass("Enter your pwv password: ")

# Open database connection
db = MySQLdb.connect("localhost","root",passwd,"pwv" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

# Create table as per requirement
sql = 'CREATE TABLE entry (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,\
        name VARCHAR(300), mfile VARCHAR(300))'

cursor.execute(sql)

# disconnect from server
db.close()


