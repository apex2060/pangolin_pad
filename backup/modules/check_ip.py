#!/usr/bin/python

# ----- IP EMAIL -----

# Sends the Pi's current IP to a Specified address.
# Use the following commands in the terminal to make this run automatically
# at every start-up:

# sudo check_ip.py
# sudo cp check_ip.py /etc/init.d/
# cd /etc/init.d/
# sudo update-rc.d check_ip.py defaults 19

# --------------------

# To access email functions:
import smtplib
import string
# To print the time:
import datetime
# To get IP address:
import subprocess

# Change your settings here:
recipient = 'rpitwitter@outlook.com' 	# Specify where to send the IP email
sender = 'gmurden22@gmail.com' 		# Your gmail email address
password = 'youtube2211'		# Your gmail password

# Storing the password here in plain text is a bit of a security risk, but I can't find
# a way around it whilst still allowing the program to run at startup. You may want to
# set up a new dedicated gmail account to save compromising your main one.

def hostname():
	# New, simplified IP-finding method:
	output = subprocess.check_output("sudo hostname", shell=True)
	return output

def wifiIP():
	# New, simplified IP-finding method:
	output = subprocess.check_output("sudo hostname -I", shell=True)
	return output

def timeStamp():
	# Fromat timestamp:
	now = datetime.datetime.now()
	timeStr = now.strftime('%H:%M:%S on %d/%m/%y')
	return timeStr

def sendMail(FROM, TO, BODY):
	# Send the email:
	try:
		server = smtplib.SMTP_SSL('smtp.gmail.com', 465)     # This is the GMAIL SSL port, other providers are untested
		server.login(sender, password)
		server.sendmail(FROM, [TO], BODY)
		server.quit()
		return True
	except:
		return False

def main():
	# Create the email:
	SUBJECT = 'IP Address from %s Raspberry Pi at %s' % (hostname(), timeStamp())
	TO = recipient
	FROM = sender
	text = "The current IP address is: %s" % wifiIP()
	BODY = string.join((
	    'From: %s' % FROM,
	    'To: %s' % TO,
	    'Subject: %s' % SUBJECT,
	    '',
	    text
	    ), '\r\n')
	
	if sendMail(FROM, [TO], BODY) == True:
		print text
	else:
		print "[check_ip]: Error: Email failed to send"


if __name__ == "__main__":
	main()
