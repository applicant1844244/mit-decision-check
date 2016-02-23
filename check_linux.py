import cups #for printing
from twill.commands import * #for retrieving data
import html2text #for "as name suggests"
import subprocess #for speaking out decisions aloud
import time #for adding delays
import getpass #to input password without echoing on terminal

##Emotional words
acceptance = ['congratulat', 'enjoy', 'party']
rejection = ['sorry', 'unfortunately', 'disappoint']

##function to login and save the html
def retrieve(usrname, passwd):
    
    go('https://decisions.mit.edu/decision.php')

    fv("1", "username", usrname) 
    fv("1", "password", passwd) 
    formaction('f','https://decisions.mit.edu/decision.php')
    submit()
    save_html('decision.html')

##function to check if the applicant has been accepted
def check():
    global acceptance, rejection

    html = open("decision.html").read()

    with open("decision.txt", "w") as text_file:
        text_file.write(html2text.html2text(html))

    converted = html2text.html2text(html).lower()

    if any(x in converted for x in acceptance):
        return "Congratulations! You have been admitted to the class of 2020"
        #command to be spoken in case of acceptance
    elif any(x in converted for x in rejection):
        return "I am extremely sorry. Unfortunately, you couldn't be admitted"
        #command to be spoken in case of rejection
    else:
        print "Unable to identify"
        return -1

##function to print the decision
def printit(accname):
    conn = cups.Connection()
    printers = conn.getPrinters()
    printer_name = printers.keys()[1]
    cups.setUser(accname)
    conn.printFile(printer_name, "decision.txt", "",{})

print "-------------------------------------------"
print "The awesomest way to check your MIT-ision!!"
time.sleep(1)
print "-------------------------------------------"
print "Enter your credentials"
usrname=raw_input("Username: ")
passwd=getpass.getpass()
print "-------------------------------------------"
accname=raw_input("Enter linux username: ")
print "-------------------------------------------"
frequency=float(raw_input("Enter the frequency for checking decisions (in seconds)"))
print "---- DECISIONS ARE BEING CHECKED ----------"

while True:
    retrieve(usrname, passwd)
    command=check()
    if command!=-1:
        printit(accname)
        subprocess.call(['speech-dispatcher'])        #start speech dispatcher
        subprocess.call(['spd-say', command])         #say the command
        break
    time.sleep(frequency)
