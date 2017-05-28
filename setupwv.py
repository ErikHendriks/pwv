#!/usr/bin/env python

# TODOO
# setup filesystem structure.
# Python libs.
# Check if gnupg and mysql are installed.
# Mysql databas and user setup.
# Manuel, help and comments.

import sys
import os
import MySQLdb
import gnupg
import getpass
import hashlib
import re
from setuptools import setup

# File and directory structure
#os.system('sh setuppwvb')

# Some explaining
explainPasswd = ' It\'s your own responsibility to choose a strong password.\n \
It should at least have az-AZ-09 and special characters in it.\n \
Use a couple of words seperated by special characters and numbers\n \
e.g Carstereo&bathtubes&windows&13February use your own imagination'

explainBlank = ' Blank... You probably wil get some errors along the way'
explainVeryweak = ' Very weak password consider updating.\n \
You could construct a password of multiple words\n \
connected with special signs and numbers.'
explainWeak = ' Weak password consider updating.\n \
You could construct a password of multiple words\n \
connected with special signs and numbers.'
explainMedium = ' Medium password consider updating.\n \
You could construct a password of multiple words\n \
connected with special signs and numbers.'

setup(

    dependency_links=['https://github.com/isislovecruft/python-gnupg/commit/d66b23b896851ebd0682d2f2f4627b075262f962']

)

# Check password strenght
def CheckPassword(password):
    strength = [explainBlank, explainVeryweak, explainWeak, explainMedium,
                'Strong', 'Very Strong']
    score = 1
    if len(password) < 1:
        return strength[0]
    if len(password) < 15:
        return strength[1]
    if len(password) >= 25:
        score = score + 1
    if len(password) >= 35:
        score = score + 1
    if re.search('\d+', password):
        score = score + 1
        if re.search('[a-z]', password) and re.search('[A-Z]', password):
            score = score + 1
    if re.search('.,[,!,@,#,$,%,^,&,*,(,),_,~,-,]', password):
        score = score + 1
    return strength[score]


# Create hashfile to confirm your password
os.system('clear')
print explainPasswd
spasswd = getpass.getpass(' Create your pwv password:')
os.system('clear')
print CheckPassword(spasswd)
entryname = raw_input(' Are you ok with this? y/n')
while entryname == 'n':
        os.system('clear')
        print explainPasswd
        spasswd = getpass.getpass(' Create your pwv password:')
        print CheckPassword(spasswd)
        entryname = raw_input(' Are you ok with this? y/n')

if entryname == 'y':
    hash_object = hashlib.sha512(spasswd)
    hex_dig = hash_object.hexdigest()
    hashfile = '$HOME/.pwv/hashfile'
    with open(hashfile, 'w') as f: f.write(hex_dig)
    os.system('clear')
    cpasswd = getpass.getpass(' Repeat your pwv password: ')
    hash_object = hashlib.sha512(cpasswd)
    hex_dig = hash_object.hexdigest()
    hashdata = '$HOME/.pwv/hashdata'
    with open(hashdata, 'w') as f: f.write(hex_dig)
    hashfile = '$HOME/.pwv/hashfile'
    test_lines = open(hashdata).readlines()
    correct_lines = open(hashfile).readlines()
    for test, correct in zip(test_lines, correct_lines):
        if test != correct:
            print ' Sorry Bad Password!'
            sys.exit()
        else:
            os.system('clear')
            print ' Password hashed'
else:
    print ' Sorry Bad Choice'
    sys.exit()

# Database managment
host = 'localhost'
user = 'root'
mpasswd = getpass.getpass(' Enter your MySql root password: ')
mydb = MySQLdb.connect(host, user, mpasswd)
cursor = mydb.cursor()
try:
    # Create user and password
    mkuser = 'pwvu'
    creation = "CREATE USER '%s'@'%s'" % (mkuser, host)
    results = cursor.execute(creation)
    print " User creation returned", results
    setpass = "SET PASSWORD FOR '%s'@'%s' = PASSWORD('%s')" % (mkuser, host, spasswd)
    results = cursor.execute(setpass)
    print " Setting of password returned", results
    granting = "GRANT ALL ON *.* TO '%s'@'%s'" % (mkuser, host)
    results = cursor.execute(granting)
    print " Granting of privileges returned", results

    # Create database
    db = MySQLdb.connect('localhost', 'pwvu', spasswd)
    cursor = db.cursor()
    sqldatabase = 'CREATE DATABASE pwvd'
    cursor.execute(sqldatabase)
    db.close()

    # Create tables
    db = MySQLdb.connect('localhost', 'pwvu', spasswd, 'pwvd')
    cursor = db.cursor()
    sqltable = 'CREATE TABLE entry (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, name VARCHAR(300), mfile VARCHAR(300))'
    cursor.execute(sqltable)
    db.close()
except MySQLdb.Error, e:
    print e

print ' All Done!'
