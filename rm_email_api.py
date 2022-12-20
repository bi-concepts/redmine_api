#Python API written by BI-Concepts GmbH
#read imap set value to redmine

import imaplib
import email
from email.header import decode_header
import mysql.connector
from redminelib import Redmine


####
####Emails abrufen
####

# account credentials
username = "ticket@emha-management.de"
password = "C+s[}xB(9)T=9z_*N97p"
imap_server = "imap.ionos.de"

def clean(text):
    # clean text for creating a folder
    return "".join(c if c.isalnum() else "_" for c in text)

# create an IMAP4 class with SSL 
imap = imaplib.IMAP4_SSL(imap_server)
# authenticate
imap.login(username, password)

status, messages = imap.select("INBOX")
# number of top emails to fetch
N = 3
data = ['0','0','0']
# total number of emails
messages = int(messages[0])

j = 0
for i in range(messages, messages-N, -1):
    # fetch the email message by ID
    res, msg = imap.fetch(str(i), "(RFC822)")
    for response in msg:
        if isinstance(response, tuple):
            # parse a bytes email into a message object
            msg = email.message_from_bytes(response[1])
            # decode the email subject
            subject, encoding = decode_header(msg["Subject"])[0]
            if isinstance(subject, bytes):
                # if it's a bytes, decode to str
                subject = subject.decode(encoding)
            # decode email sender
            From, encoding = decode_header(msg.get("From"))[0]
            if isinstance(From, bytes):
                From = From.decode(encoding)
            data[j] = subject
            #print("Subject:", subject)
            #print("From:", From)
            j=j+1

# close the connection and logout
imap.close()
imap.logout()

####
####Daten aufarbeiten
####

j = 0
ticketida = ['0','0','0']
ticketidb = ['0','0','0']
statusa    = ['0','0','0']
mailida   = ['0','0','0']

def getitem(textarray,lborder,rborder,offset):
    # split string vor getting item ids
    ticketid = 0 
    x = textarray.find(lborder)
    y = textarray.find(rborder)
    str_tmp = textarray
    #print(x)
    #print(y)
    #x,y = -1 nicht gefunden
    if(x == -1 or y == -1): 
      ticketid = 0 
    else: 
      ticketid= str_tmp[x+offset:y] 
    return ticketid

#uber das data-array (alle eingelesenen Mails)
for eachArg in data:
   #print(data[j])
   #Albakom Ticket ID
   ticketida[j] = getitem(data[j],"[Ticket#","]",8)
   #BalticTaucher Ticket ID
   ticketidb[j] = getitem(data[j],"@INBT@#","@]",7)
   #Ticket Status Albakom
   statusa[j] = getitem(data[j],"{{ISA#","}}}",6)
   if(statusa[j]=='new'):statusa[j]=1;
   if(statusa[j]=='open'):statusa[j]=2;
   if(statusa[j]=='close'):statusa[j]=3;
   #Albakom Unique ID
   mailida[j] = getitem(data[j],"{{AUI#","@}",6)
#   print(ticketida[j])
#   print(ticketidb[j])
#   print(statusa[j])
#   print(mailida[j])
#   print("--------------------------")
   j = j + 1
   
####
####Daten in MariaDB speichern und neue Daten holen
####
m = n = 0
mailid2check   = ['0','0','0']
config = { 'user': 'redmine', 'password': 'Open9893@q', 'host':'localhost','database':'redmine_api','raise_on_warnings':True}
cnx = mysql.connector.connect(**config)
cursor = cnx.cursor()

#uber das data-array (alle eingelesenen Mails)
for eachArg in data:
	#print(mailida[n])
	#anzahl der id die der mailida entsprechen holen
	query1 = ("SELECT COUNT(ID) FROM ts_interface WHERE mailida= %s")
	tuple1 = (mailida[n],)
	cursor.execute(query1,tuple1)
	myresult1 = cursor.fetchall()
	#wenn datensatz nicht vorhanden dann insert
	if(myresult1[0][0]==0):
		query2 = ("INSERT INTO ts_interface (ticketida,ticketidb,statusa,mailida,transferb) VALUES (%s, %s, %s, %s, %s)")
		tuple2 = (ticketida[n], ticketidb[n], statusa[n], mailida[n],'1')
		cursor.execute(query2,tuple2)
		cnx.commit()
	n = n +1 

#alle Datensaetze die nicht uebertragen sind holen
query3 = ("SELECT * FROM ts_interface WHERE transferb = %s ORDER BY mailida ASC")
tuple3 = ('1',)
cursor.execute(query3,tuple3)
myresult3 = cursor.fetchall()

####
####Redmin abarbeiten
####

redmine = Redmine('http://localhost:3001', username='admin', password='Open9893@q')
project = redmine.project.get(1)

success=False
for dbvalues in myresult3:
	print(dbvalues[0])
	#Ticket neu
	if(dbvalues[3]==1):
		issue = redmine.issue.update (dbvalues[2], status_id=1)
		issue
		if(issue): success=True
	#Ticket in Bearbeitung
	if(dbvalues[3]==2):
		issue = redmine.issue.update (dbvalues[2], status_id=2)
		issue
		if(issue): success=True
	#Ticket geschlossen
	if(dbvalues[3]==3):
		issue = redmine.issue.update (dbvalues[2], status_id=5)
		issue
		issue = redmine.issue.update (dbvalues[2], done_ratio=100)
		issue
		if(issue): success=True		
	#Albakom Ticketnummer
	issue = redmine.issue.update (dbvalues[2], custom_fields=[{'id':4, 'value':dbvalues[1]}]) 
	if(issue): success=True 
	#letzte Uebertragene Nummer
	issue = redmine.issue.update (dbvalues[2], custom_fields=[{'id':5, 'value':dbvalues[4]}])
	if(issue): success=True
	#bei erfolg als verarbeitet kennzeichnen
	if(success):
		query4 = ("UPDATE ts_interface SET transferb='2' WHERE id= %s")
		tuple4 = (dbvalues[0],)
		cursor.execute(query4,tuple4)
		cnx.commit()			

#	print(issue)


cursor.close()
cnx.close()
