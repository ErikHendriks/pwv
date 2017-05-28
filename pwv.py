#!/usr/bin/env python
import sys
import os
import MySQLdb
import gnupg
import getpass
import hashlib
import re

# Main definition - constants
menu_actions = {}
os.system("clear")
passwd = getpass.getpass("Enter your pwv password: ")
hash_object = hashlib.sha512(passwd)
hex_dig = hash_object.hexdigest()
hashdata = "$HOME/.pwv/hashdata"
with open(hashdata, 'w') as f: f.write(hex_dig)
hashfile = "$HOME/.pwv/hashfile"
test_lines = open(hashdata).readlines()
correct_lines = open(hashfile).readlines()
for test, correct in zip(test_lines, correct_lines):
    if test != correct:
        print "Sorry Bad Password!"
        sys.exit()
else:
    os.system("clear")
    print "\nWelcome to PassWordVault,\n"


def CheckPassword(password):
    strength = ['Blank', 'Very weak password consider updating ',
                'Weak password consider updating',
                'Medium password consider updating',
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


# Main menu
def main_menu():
    print "1. List entries"
    print "2. Add password"
    print "3. Retrieve password"
    print "4. Remove password"
    # printt "5. Key managment"
    # print "6. GnuPG jobs"
    print "q. Quit"
    choice = raw_input(" >>  ")
    exec_menu(choice)
    return


# Execute menu
def exec_menu(choice):
    os.system("clear")
    ch = choice.lower()
    if ch == '':
        menu_actions['main_menu']()
    else:
        try:
            menu_actions[ch]()
        except KeyError:
            print "Invalid selection, please try again.\n"
            menu_actions['main_menu']()
    return


# Menu 1
def menu1():
    db = MySQLdb.connect("localhost", "root", passwd, "pwv")
    cursor = db.cursor()
    sql = "SELECT * FROM entry"
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            print row[0], row[1]
    except:
        print "Error: unable to fecth data"
    db.close()
    print "\n"
    print "b. Back"
    print "q. Quit"
    choice = raw_input(" >>  ")
    exec_menu(choice)
    return


# Menu 2
def menu2():
    os.system("clear")
    print "Only azAZ09-_. characters are allowed"
    entryname = raw_input("Enter name of entry: ")
    cmdmkdir = "mkdir -p $HOME/.pwv/database/"+entryname
    os.system(cmdmkdir)
    login = raw_input("Enter your login name: ")
    mpasswd = raw_input("Enter your password: ")
    os.system("clear")
    print CheckPassword(mpasswd)
    print "\n"
    data = "$HOME/.pwv/database/"+entryname+"/"+entryname
    with open(data, 'a') as f: f.write(login)
    with open(data, 'a') as f: f.write('\n')
    with open(data, 'a') as f: f.write(mpasswd)
    gpg_home = "~/.gnupg"
    gpg = gnupg.GPG(gnupghome=gpg_home)
    savefile = data+".asc"
    afile = open(data, "r")
    gpg.encrypt_file(afile, recipients=None,
                     symmetric='AES256',
                     passphrase=passwd, output=savefile)
    afile.close()
    cmdrm = "rm -f "+data
    os.system(cmdrm)
    db = MySQLdb.connect("localhost", "root", passwd, "pwv")
    cursor = db.cursor()
    sql = "INSERT INTO entry(name, mfile) VALUES ('%s', '%s')" % (entryname,
                                                                  savefile)
    try:
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
    db.close()
    print "\n"
    print "1. List entries"
    print "2. Add password"
    print "3. Retrieve password"
    print "4. Remove password"
    # print "5. Key managment"
    # print "6. GnuPG jobs"
    print "q. Quit"
    choice = raw_input(" >>  ")
    exec_menu(choice)
    return


# Menu 3
def menu3():
    passwd = getpass.getpass("Enter your pwv password: ")
    os.system("clear")
    db = MySQLdb.connect("localhost", "root", passwd, "pwv")
    cursor = db.cursor()
    sql = "SELECT * FROM entry"
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            print row[0], row[1]
    except:
        print "Error: unable to fecth data"
    db = MySQLdb.connect("localhost", "root", passwd, "pwv")
    cursor = db.cursor()
    print "\n"
    retrievechoice = raw_input("Enter row number: ")
    sql = "SELECT mfile FROM entry WHERE id = "+retrievechoice
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        line = str(row).translate(None, "()',")
        data1 = "$HOME/.pwv/results1"
        with open(data1, 'w') as f: f.write(line)
    with open(data1) as myfile:
        data2 = myfile.read().replace('\n', '')
    gpg_home = "~/.gnupg"
    gpg = gnupg.GPG(gnupghome=gpg_home)
    # data = "$HOME/.pwv/database/oaslkd/oaslkd.asc"
    afile = open(data2, "rb")
    encrypted_ascii_data = gpg.decrypt_file(afile, passphrase=passwd)
    afile.close()
    os.system("clear")
    print encrypted_ascii_data
    print "\n"
    print "1. List entries"
    print "2. Add password"
    print "3. Retrieve password"
    print "4. Remove password"
    # print "5. Key managment"
    # print "6. GnuPG jobs"
    print "q. Quit"
    choice = raw_input(" >>  ")
    exec_menu(choice)
    return


# Menu 4
def menu4():
    passwd = getpass.getpass("Enter your pwv password: ")
    os.system("clear")
    db = MySQLdb.connect("localhost", "root", passwd, "pwv")
    cursor = db.cursor()
    sql = "SELECT * FROM entry"
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            print row[0], row[1]
    except:
        print "Error: unable to fecth data"
    db = MySQLdb.connect("localhost", "root", passwd, "pwv")
    cursor = db.cursor()
    retrievechoice = raw_input("Enter row number: ")
    sql = "SELECT mfile FROM entry WHERE id = "+retrievechoice
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        line = str(row).translate(None, "()',")
    sql0 = "DELETE FROM entry WHERE id = "+retrievechoice
    cursor.execute(sql0)
    db.commit()
    sql1 = "ALTER TABLE `entry` DROP `id`;"
    cursor.execute(sql1)
    db.commit()
    sql2 = "ALTER TABLE `entry` AUTO_INCREMENT = 1;"
    cursor.execute(sql2)
    db.commit()
    sql3 = "ALTER TABLE `entry` ADD `id` int UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY FIRST;"
    cursor.execute(sql3)
    db.commit()
    cmdrm = "rm -f "+line
    os.system(cmdrm)
    os.system("clear")
    print line+" is removed"
    print "\n"
    print "1. List entries"
    print "2. Add password"
    print "3. Retrieve password"
    print "4. Remove password"
    # print "5. Key managment"
    # print "6. GnuPG jobs"
    print "q. Quit"
    choice = raw_input(" >>  ")
    exec_menu(choice)
    return


# Menu 5
def menu5():
    print "\n"
    print "1. List entries"
    print "2. Add password"
    print "3. Retrieve password"
    print "4. Remove password"
    # print "5. Key managment"
    # print "6. GnuPG jobs"
    print "q. Quit"
    choice = raw_input(" >>  ")
    exec_menu(choice)
    return


# Menu 6
def menu6():
    print "\n"
    print "1. List entries"
    print "2. Add password"
    print "3. Retrieve password"
    print "4. Remove password"
    # print "5. Key managment"
    # print "6. GnuPG jobs"
    print "q. Quit"
    choice = raw_input(" >>  ")
    exec_menu(choice)
    return


# Back to main menu
def back():
    menu_actions['main_menu']()


# Exit program
def exit():
    sys.exit()

# Menu definition
menu_actions = {
    'main_menu': main_menu,
    '1': menu1,
    '2': menu2,
    '3': menu3,
    '4': menu4,
    '5': menu5,
    '6': menu6,
    'b': back,
    'q': exit,
}

# Main Program
if __name__ == "__main__":
    # Launch main menu
    main_menu()
