import smtplib
import csv
from email.message import EmailMessage

# Configuration
ZOHO_SMTP_SERVER = 'smtp.zoho.com'
ZOHO_SMTP_PORT = 587
ZOHO_EMAIL = 'example@zoho.com'
ZOHO_PASSWORD = 'pass'  # Use app password if 2FA is enabled

PDF_ATTACHMENT = 'attachment.pdf'
LINK_URL = 'https://your-link.com'

# Read recipients from CSV
def load_recipients(csv_file):
    recipients = []
    with open(csv_file, newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            recipients.append({
                'name': row['name'],
                'email': row['email']
            })
    return recipients

# Create and send email
def send_email(to_email, to_name, smtp_connection):
    msg = EmailMessage()
    msg['Subject'] = 'Your Document and Link'
    msg['From'] = ZOHO_EMAIL
    msg['To'] = to_email

    # Email body with link
    html_body = f"""
    <html>
        <body>
            <p>Dear {to_name},</p>
            <p>Please find the attached PDF document.</p>
            <p>Also, visit this link: <a href="{LINK_URL}">Click Here</a></p>
            <p>Best regards,<br>Your Name</p>
        </body>
    </html>
    """
    msg.set_content("This email contains HTML. Please view in an HTML-compatible email client.")
    msg.add_alternative(html_body, subtype='html')

    # Attach PDF
    with open(PDF_ATTACHMENT, 'rb') as f:
        file_data = f.read()
        msg.add_attachment(file_data, maintype='application', subtype='pdf', filename=PDF_ATTACHMENT)

    # Send email
    smtp_connection.send_message(msg)
    print(f"Email sent to {to_name} <{to_email}>")

# Main function
def main():
    recipients = load_recipients('recipients.csv')

    with smtplib.SMTP(ZOHO_SMTP_SERVER, ZOHO_SMTP_PORT) as smtp:
        smtp.starttls()
        smtp.login(ZOHO_EMAIL, ZOHO_PASSWORD)

        for person in recipients:
            send_email(person['email'], person['name'], smtp)

if __name__ == '__main__':
    main()
