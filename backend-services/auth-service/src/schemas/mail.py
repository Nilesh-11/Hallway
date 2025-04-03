def html_formatted_otp(otp, my_mail):
    response = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>OTP Verification - Hallway Software</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 0;
            }}
            .container {{
                width: 100%;
                max-width: 600px;
                margin: 30px auto;
                background: #ffffff;
                padding: 20px;
                text-align: center;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }}
            .logo {{
                width: 150px;
                margin-bottom: 20px;
            }}
            .otp-box {{
                font-size: 22px;
                font-weight: bold;
                color: #333;
                background: #f8f8f8;
                padding: 15px;
                display: inline-block;
                border-radius: 5px;
                letter-spacing: 4px;
            }}
            .text {{
                font-size: 16px;
                color: #555;
                margin-bottom: 20px;
            }}
            .footer {{
                font-size: 12px;
                color: #888;
                margin-top: 20px;
            }}
            .button {{
                background: #007BFF;
                color: white;
                padding: 12px 25px;
                text-decoration: none;
                border-radius: 5px;
                font-weight: bold;
                display: inline-block;
                margin-top: 15px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <img src="https://i.postimg.cc/c4NYYHPk/hallwaylogo.jpg" alt="Hallway Software Logo" class="logo">  
            <h2>🔐 Your OTP Code</h2>
            <p class="text">Use the OTP below to complete your authentication. It expires in 10 minutes.</p>
            <div class="otp-box">{otp}</div>
            <p class="text">If you did not request this OTP, please ignore this email.</p>
            <a href="#" class="button">Verify Now</a>
            <p class="footer">Need help? Contact us at <a href="mailto:{my_mail}">{my_mail}</a></p>
        </div>
    </body>
    </html>
    '''
    return response
