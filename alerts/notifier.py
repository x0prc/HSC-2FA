import smtplib
from email.mime.text import MIMEText
import requests

def send_email_alert(subject, body, recipient, smtp_server, smtp_port, smtp_user, smtp_password):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = smtp_user
    msg['To'] = recipient

    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(smtp_user, smtp_password)
            server.sendmail(smtp_user, [recipient], msg.as_string())
        print("[Notifier] Email alert sent successfully.")
    except Exception as e:
        print(f"[Notifier] Email alert failed: {e}")

def send_slack_alert(webhook_url, message):
    payload = {'text': message}
    try:
        response = requests.post(webhook_url, json=payload)
        if response.status_code == 200:
            print("[Notifier] Slack alert sent successfully.")
        else:
            print(f"[Notifier] Slack alert failed: Status {response.status_code}, Response: {response.text}")
    except Exception as e:
        print(f"[Notifier] Slack alert failed: {e}")

# Note : Make sure to change these based on your configuration / preferences!
if __name__ == "__main__":
    # Email
    # send_email_alert(
    #     subject="HSC-2FA Alert",
    #     body="A honeytoken was triggered by address 0x1234...",
    #     recipient="admin@example.com",
    #     smtp_server="smtp.example.com",
    #     smtp_port=465,
    #     smtp_user="your@email.com",
    #     smtp_password="your-password"
    # )

    # Slack
    # send_slack_alert(
    #     webhook_url="https://hooks.slack.com/services/XXXX/YYYY/ZZZZ",
    #     message="A honeytoken was triggered by address 0x1234..."
    # )
    pass
