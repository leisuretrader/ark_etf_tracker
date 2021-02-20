import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import config
from changes import *

sender_email = config.SENDER_EMAIL
receiver_emails = config.RECEIVER_EMAILS
# ", ".join(config.RECEIVER_EMAILS)
password = config.SENDER_EMAIL_PASSWORD

message = MIMEMultipart("alternative")
message["Subject"] = "ARK Holdings Change {0} vs. {1}".format(previous_date, current_date)
message["From"] = sender_email
# message["To"] = ", ".join(receiver_emails)
# message["To"] = sender_email
# message["Bcc"] = ", ".join(receiver_emails)

result_data = ark_adding_removed_between_two_dates(current_date, previous_date)

# text = """
# """

html = """\
<html>
  <head></head>
  <body>
    <p> <br>
    ARK holdings between {0} and {1}. Newly added and recent removed tickers <br>
    {2}
    </p>
  </body>
</html>
""".format(previous_date, 
          current_date, 
          result_data.to_html())

# Turn these into plain/html MIMEText objects
# part1 = MIMEText(text, "plain")
part2 = MIMEText(html, "html")

# # Add HTML/plain-text parts to MIMEMultipart message. The email client will try to render the last part first
# message.attach(part1)
message.attach(part2)

# Create secure connection with server and send email
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:  #465
    server.login(sender_email, password)
    server.sendmail(
        sender_email, receiver_emails, message.as_string()
    )

print ("Email Sent")