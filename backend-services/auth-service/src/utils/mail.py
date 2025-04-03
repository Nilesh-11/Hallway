import smtplib
from email.message import EmailMessage
from src.config.config import MY_MAIL, MY_MAIL_PASS
from pydantic import EmailStr
from src.utils.auth import generate_otp
from src.schemas.mail import html_formatted_otp

def send_gmail_otp(to_mail: EmailStr):
    otp = generate_otp()
    msg = EmailMessage()
    try:
        print("sending mail...")
        html_content = html_formatted_otp(otp, MY_MAIL)
        msg.set_content(f"This is a test mail. To register with Hallway, enter the following OTP: {otp}")
        msg.add_alternative(html_content, subtype="html")
        msg["Subject"] = "Test Email: Registration OTP"
        msg["From"] = MY_MAIL
        msg["To"] = to_mail
        
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(MY_MAIL, MY_MAIL_PASS)
            server.send_message(msg)
        print("mail sent.")
    except Exception as e:
        print("Error occured in sending otp: ", e)
        return {"type": "error"}
    except:
        return {"type": "error"}
    return {"type": "ok", "otp": otp}