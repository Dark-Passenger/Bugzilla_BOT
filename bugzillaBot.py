import bugzilla
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from sys import argv


try:
  build_number = argv[1]
except IndexError:
  build_number = ''

html_header = """
<html><body>
<p>
Hi all,
</p>
<p>
Below are the resolved bugs for %s build
</p>
<table border="1" cellpadding="4" style="border: 1px solid #000000; border-collapse: collapse;"
""" %(build_number)
html_header_row = "<tr><td>Bug ID</td><td>Criticality</td><td>Summary</td><td>Reporter</td><td>Assignee</td></tr>"

html_footer = """
</table>
<p style="font-size:14px; color:grey; font-style:italic;">
This is an automated mail, please do not reply to this mail
</p>
</body></html>"""

mail = html_header+html_header_row

bz = bugzilla.Bugzilla(url='http://<private-bugzilla-ip>/xmlrpc.cgi')

try:
   bz.login('username', 'passwd');
   print('Authorization cookie received.')

except bugzilla.BugzillaError:
   print(str(sys.exc_info()[1]))
   sys.exit(1)

print("Getting Bugs ...")

#getting all the bug ID's and displaying them
query = bz.build_query(product='<Private>',status='RESOLVED')
bugs = bz.query(query)

print("Generating Mail ... ")

bugs.sort(key=lambda bug: bug.severity, reverse=False)
 
for bug in bugs:
    	
  reporter_name = bug.creator.replace('@','.').replace('1','').split('.')
  reporter_fname = reporter_name[0].title()
  reporter_lname = reporter_name[1].title()

  assignee_name = bug.creator.replace('@','.').replace('1','').split('.')
  assignee_fname = assignee_name[0].title()
  assignee_lname = assignee_name[1].title()

  severity = bug.severity.split('(',1)[1].replace(')','')

  mail = mail+"\n<tr><td>"+str(bug.id)+"</td><td>"+severity+"</td><td>"+bug.summary+"</td><td>"+reporter_fname+" "+reporter_lname+"</td><td>"+assignee_fname+" "+assignee_lname+"</td></tr>"
    	

mail = mail+html_footer

print("Mail Generated sending now ...")

sender = "<Private>"
sender_name = "Bugzilla Bot"
sender_passwd = "<Private>"
recipient = "<Private>"
server = "<Private>"
	
msg = MIMEMultipart('alternative')

msg['Subject'] = "Bugzilla bug report for build "+build_number
msg['From'] = sender_name
msg['To'] = recipient

msg.attach(MIMEText(mail, "html"))

	
# Send the message via SMTP server.
smtpserver = smtplib.SMTP(server,587)
smtpserver.starttls()
smtpserver.login(sender, sender_passwd)
smtpserver.sendmail(sender, recipient, msg.as_string())
smtpserver.close()
print("Mail Sent Successfully")