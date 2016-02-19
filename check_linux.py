import cups
from twill.commands import *
import html2text
import subprocess
import time

##Emotional words
acceptance = ['congratulat', 'enjoy', 'party']
rejection = ['sorry', 'unfortunately', 'disappoint']

##function to login and save the html
def retrieve():
    go('https://decisions.mit.edu/decision.php')

    fv("1", "username", "username") #replace with the actual username
    fv("1", "password", "password") #replace with the actual password
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
def printit():
    conn = cups.Connection()
    printers = conn.getPrinters()
    printer_name = printers.keys()[1]
    cups.setUser('username') #replace with the computer's account name
    conn.printFile(printer_name, "decision.txt", "",{})

while True:
    retrieve()
    command=check()
    if command!=-1:
        printit()
        subprocess.call(['speech-dispatcher'])        #start speech dispatcher
        subprocess.call(['spd-say', command])         #say the command
        break
    time.sleep(15) #recheck the decision every 15 seconds
