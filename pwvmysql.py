#!/usr/bin/python

import MySQLdb

# Open database connection
db = MySQLdb.connect("localhost","root","pw","pwv" )

# prepare a cursor object using cursor() method
cursor = db.cursor()

# Create table as per requirement
sql = """CREATE TABLE EMPLOYEE (
         FIRST_NAME  CHAR(20) NOT NULL,
         LAST_NAME  CHAR(20),
         AGE INT,  
         SEX CHAR(1),
         INCOME FLOAT )"""

cursor.execute(sql)


# disconnect from server
db.close()
