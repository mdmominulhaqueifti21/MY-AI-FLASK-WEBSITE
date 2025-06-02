from flask import Flask, request
import smtplib
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
TO_EMAIL = os.getenv('TO_EMAIL')

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        first = request.form['first_name']
        last = request.form['last_name']
        full_name = f"{first} {last}"

        # Save to file
        with open('submissions.txt', 'a') as f:
            f.write(full_name + '\n')

        # Send email
        send_email(full_name)

        return f"<h1>Hello, {full_name}</h1>"

    return '''
        <form method="POST">
            First Name: <input type="text" name="first_name"><br><br>
            Last Name: <input type="text" name="last_name"><br><br>
            <input type="submit" value="Submit">
        </form>
    '''

def send_email(name):
    subject = "New Form Submission"
    body = f"Someone submitted: {name}"
    message = f"Subject: {subject}\n\n{body}"

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, TO_EMAIL, message)
        server.quit()
        print("Email sent!")
    except Exception as e:
        print("Email failed:", e)

if __name__ == '__main__':
    app.run(debug=True)
