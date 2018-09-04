import socket
import urllib.request
import time
from email.headerregistry import Address
from email.message import EmailMessage
import smtplib

# Gmail details
email_address = ""
email_password = ""

# Recipent
to_address = (
    Address(display_name='Mingze USC', username='mingzeya', domain='usc.edu'),
)

def create_email_message(from_address, to_address, subject, body):
    msg = EmailMessage()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = subject
    msg.set_content(body)
    return msg

def get_ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]

if __name__ == '__main__':
    # Fetch IP from website and store it
    marsUrl = urllib.request.urlopen('http://apps.marstanjx.com/mingze')
    data = marsUrl.read()
    previous_ip = str(data)[2:-1]

    while True:
        ip_address = get_ip_address()
        if ip_address != previous_ip:
            # Update url on website
            some_url = "http://apps.marstanjx.com/mingze/update.php?ip=" + ip_address
            urllib.request.urlopen(some_url)
            msg = create_email_message(
                from_address=email_address,
                to_address=to_address,
                subject='IP Updated',
                body= "Your new IP address for PC is: " + ip_address,
            )
            
            with smtplib.SMTP('smtp.gmail.com', port=587) as smtp_server:
                smtp_server.ehlo()
                smtp_server.starttls()
                smtp_server.login(email_address, email_password)
                smtp_server.send_message(msg)
            # Update email address
            previous_ip = ip_address
        time.sleep(60)
