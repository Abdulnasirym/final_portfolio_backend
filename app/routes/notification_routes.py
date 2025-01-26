from flask import Blueprint, request, jsonify
from app.utils.email_utils import send_email

notifications = Blueprint('notifications', __name__)

@notifications.route('/send-notification', methods=['POST'])
def send_notification():
	data = request.json
	recipient = data.get('recipient')
	subject = data.get('subject', "Health Reminder")
	body = data.get('body', "This is a reminder to take your supplement.")

	if not recipient:
		return jsonify({"error": "Recipient email is required"}), 400

	try:
		send_email(subject, recipient, body)
		return jsonify({"message": "Email sent successfully!"}), 200
	except Exception as e:
		return jsonify({"Error": str(e)}), 500
