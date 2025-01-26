from flask_mail import Message
from app import mail
import logging
from flask import current_app

def send_email(subject, recipient, body, html_body=None):
	try:
		if isinstance(recipient, str):
			recipient = [recipient]
		sender_email = current_app.config.get('MAIL_DEFAULT_SENDER', 'abdulnasiry03@gmail.com')
		msg = Message(subject, recipients=recipient, sender=sender_email)
		msg.body = body
		if html_body:
			msg.html = html_body
		mail.send(msg)
		logging.info(f"Email sent successfully to {', '.join(recipient)}")
		return True
	except Exception as e:
		logging.error(f"Failed to send email to {', '.join(recipient)}: {str(e)}")
		return False