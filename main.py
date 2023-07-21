# import requirements needed
from flask import Flask, render_template, request, redirect, Response
from utils import get_base_url
import flask
import cv2
from skimage import io
from model import *
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(subject, body, from_email, to_email, smtp_server, smtp_port, smtp_username, smtp_password):
    message = MIMEMultipart()
    message['From'] = from_email
    message['To'] = to_email
    message['Subject'] = subject

    # Attach the body of the email
    message.attach(MIMEText(body, 'plain'))

    try:
        # Connect to the SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()

        # Log in to the SMTP server if needed
        if smtp_username and smtp_password:
            server.login(smtp_username, smtp_password)

        # Send the email
        server.sendmail(from_email, to_email, message.as_string())

        # Close the connection to the server
        server.quit()

        print("Email sent successfully.")
    except Exception as e:
        print("Error sending email:", e)


camera = cv2.VideoCapture(0)

# set up the webserver
# port may need to be changed if there are multiple flask servers running on same server
port = 12345
base_url = get_base_url(port)

# if the base url is not empty, then the server is running in development, and we need to specify the static folder
# so that the static files are served
if base_url == '/':
    app = Flask(__name__)
else:
    app = Flask(__name__, static_url_path=base_url + 'static')

UPLOAD_FOLDER = 'static/assets/img'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024


# Generate frames for live video
def gen_frames():
    camera = cv2.VideoCapture(0)
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:

            frame = run_model(frame)
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


def response_frames():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


# set up the routes and logic for the webserver
@app.route(f'{base_url}')
def home():
    return render_template('index.html')


@app.route('/home/')
def home_page():
    return render_template('index.html')


@app.route('/project/', methods=['POST'])
def upload_model():
    if 'file' not in request.files:
        flask.abort(403)
    file_v = request.files['file']
    path = UPLOAD_FOLDER + "/frame.png"
    if os.path.isfile(path):
        os.remove(path)

    file_v.save(path)

    img = io.imread(path)

    SmarterModel.run_model(img)
    remedy = ""
    if SmarterModel.active_drowning:
        remedy += "Stop actively drowning\n"
    if SmarterModel.passive_drowning:
        remedy += "Stop passively drowning\n"
    if SmarterModel.running:
        remedy += "Stop running\n"
    img = "../static/assets/results/frame.png"
    return render_template("results.html", img=img, remedy=remedy)


@app.route('/project/', methods=['GET'])
def project():
    return render_template("project.html")


@app.route('/about_us/')
def about_us_page():
    return render_template('about_us.html')


@app.route('/email/', methods=['POST'])
def email():
    if 'email' not in request.form:
        flask.abort(403)
    email_address = request.form['email']
    print(email_address)
    subject = "Welcome to the Aquasentinels Community!"
    body = "Hey there!\n\nThis Bob, from Aquasentinels, emailing you in regards to welcoming you to the Aquasentinels " \
           "community, where we strive to make life thrive. This is a confirmation that you have successfully " \
           "subscribed to the monthly newsletter of Aquasentinels, where you will receive latest updates about " \
           "recently drowned people. We will also be sending out promotions for our latest products.\n\nSincerely," \
           "\nBob from Aquasentinels "
    send_email(subject, body, 'aquasentinels@outlook.com', email_address, "smtp-mail.outlook.com", 587,
               "aquasentinels@outlook.com", "Merrymockingbirds")
    with open("evil.txt", "a") as f:
        f.write(f",\n{email_address}")
    return render_template("index.html")


@app.route('/video_feed/', methods=["GET"])
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/live_demo/')
def live():
    if camera.isOpened():
        return render_template("live.html")
        # return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        return render_template("error.html")


# define additional routes here
# for example:
# @app.route(f'{base_url}/team_members')
# def team_members():
#     return render_template('team_members.html') # would need to actually make this page

if __name__ == '__main__':
    # IMPORTANT: change url to the site where you are editing this file.
    website_url = 'https://www.arivisawesome.com/'
    print(f'Try to open\n\n    https://{website_url}' + base_url + '\n\n')
    app.run(host='0.0.0.0', port=port, debug=True)
