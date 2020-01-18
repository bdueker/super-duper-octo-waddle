# https://letslearnabout.net/tutorial/how-to-send-beautiful-emails-with-attachments-using-only-python/
# This program will automatically send emails to a resipiant list.
# The resipiant list MUST be named "sendList.txt" and each line must be of the form
# resipiant name, resipiant email
# The program also needs a file named "senderInfo.txt"
# where the first name holds the senders email address 
# and the second line holds the password to the account

import smtplib, ssl
from email.mime.text import MIMEText
from email.utils import formataddr

def getEmailBodyFromHTML(htmlFile = "htmlnewsletter.html"):
    with open(htmlFile,'r') as f:
        email_html = f.read()
    return email_html

def convertList(resLists):
    resNames = []
    resEmails = []
    for resList in resLists:
        splitRes = resList.split(',')
        resNames.append(splitRes[0])
        resEmails.append(splitRes[1])
    return resNames, resEmails

def sendEmail(resList, emailBody):

    receiverNames, receiverEmails = convertList(resList)

    with open("senderInfo.txt",'r') as f:
        info = f.read()
        info = info.split('\n')
        senderEmail = info[0].strip()
        password = info[1].strip()
        senderName = 'Tester'

    for receiverName, receiverEmail in zip(receiverNames, receiverEmails):
        msg = MIMEText(emailBody, 'html')
        print("Sending Email to ", receiverName)
        msg["To"] = formataddr((receiverName, receiverEmail))
        msg["From"] = formataddr((senderName,senderEmail))
        msg["Subject"] = "This is simply a test with multiple people"

        server = smtplib.SMTP('smtp.gmail.com', 587)
        # Encrypts the email
        context = ssl.create_default_context()
        server.starttls(context=context)
        # We log in into our Google account
        server.login(senderEmail, password)
        # Sending email from sender, to receiver with the email body
        server.sendmail(senderEmail, receiverEmail, msg.as_string())

def getSendList():
    with open("sendList.txt",'r') as f:
        lines = f.readlines()
    return lines

if __name__=="__main__":
    sendEmail(getSendList(), getEmailBodyFromHTML())