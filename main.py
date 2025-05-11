from alpaca.trading.stream import TradingStream
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from helper import *

trading_stream = TradingStream(api_key, api_secret, paper=True)

def send_email(subject, body):
    """Send an email with the given subject and body."""
    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(email_user, email_password)
            server.sendmail(email_user, receiver_email, msg.as_string())
            print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")

async def handle_portfolio_update(data):
    """Handle portfolio updates and send an email notification."""

    print("Portfolio updated:", data)
    subject = "Portfolio Update Notification"
    body = f"Portfolio Update:\n{data}"
    send_email(subject, body)

# Subscribe to account and portfolio updates
trading_stream.subscribe_trade_updates(handle_portfolio_update)

if __name__ == "__main__":
    try:
        print("Starting trading stream...")
        trading_stream.run()
    except Exception as e:
        print("Stopping trading stream...")
        trading_stream.stop()