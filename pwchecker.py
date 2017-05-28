#!/usr/bin/env python
import re

def CheckPassword(password):
    strength = ['Blank','Very Weak','Weak','Medium','Strong','Very Strong']
    score = 1

    if len(password) < 1:
        return strength[0]
    if len(password) < 15:
        return strength[1]

    if len(password) >=15:
        score = score + 1
    if len(password) >=25:
        score = score + 1
    
    if re.search('\d+',password):
        score = score + 1
    if re.search('[a-z]',password) and re.search('[A-Z]',password):
        score = score + 1
    if re.search('.,[,!,@,#,$,%,^,&,*,(,),_,~,-,]',password):
        score = score + 1

    return strength[score]
    
def main():
	
		
	mpasswd = raw_input("Check: ")
        print CheckPassword(mpasswd)

if __name__ == "__main__":
	main()



