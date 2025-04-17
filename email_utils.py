import smtplib
import random
from email.message import EmailMessage
import toml  # For reading secrets.toml

# Load credentials from .streamlit/secrets.toml
secrets = toml.load(".streamlit/secrets.toml")

# SMTP configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Get credentials from secrets
SENDER_EMAIL = secrets["SENDER_EMAIL"]
SENDER_PASSWORD = secrets["SENDER_PASSWORD"]
SENDER_NAME = secrets["SENDER_NAME"]

# Function to generate and send OTP
def send_otp(receiver_email):
    otp = str(random.randint(100000, 999999))  # Generate random 6-digit OTP
    
    # Compose the email
    msg = EmailMessage()
    msg["Subject"] = "Your OTP Verification Code"
    msg["From"] = f"{SENDER_NAME} <{SENDER_EMAIL}>"
    msg["To"] = receiver_email
    msg.set_content(f"Your OTP code is: {otp}")

    # Send the email via Gmail SMTP
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()  # Upgrade the connection to secure
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
        return otp
    except Exception as e:
        print("❌ Failed to send email:", e)
        return None

# Test by running the script
if __name__ == "__main__":
    email = input("Enter receiver's email: ")
    code = send_otp(email)
    if code:
        print(f"✅ OTP sent successfully: {code}")
    else:
        print("❌ OTP sending failed.")
