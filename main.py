# import requirements needed
from flask import Flask, render_template, request, redirect
from utils import get_base_url
import flask

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


# set up the routes and logic for the webserver
@app.route(f'{base_url}')
def home():
    return render_template('index.html')


@app.route('/home/')
def home_page():
    return render_template('index.html')


@app.route('/project/')
def project_page():
    return render_template('project.html')


@app.route('/about_us/')
def about_us_page():
    return render_template('about_us.html')


@app.route('/email/', methods=['POST'])
def email():
    if 'email' not in request.form:
        flask.abort(403)
    # email_address = request.form['email']
    return redirect('home')


@app.route('/live_demo/')
def live():
    return render_template("demo.html")


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
