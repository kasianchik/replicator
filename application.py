"""
This is Python/Flask web-application. It is a self-replicating GitHub repository.
It means that if you follow the link of this application the application creates
a repository in your GitHub account that includes files of this web-application.
"""
import base64
import json
import os

import requests
from flask import Flask, request, redirect, session, render_template
from requests_oauthlib import OAuth2Session
from datetime import datetime

from settings import CLIENT_ID, CLIENT_SECRET, FILES

app = Flask(__name__)

app.secret_key = os.urandom(24)
AUTHORIZATION_BASE_URL = 'https://github.com/login/oauth/authorize'
TOKEN_URL = 'https://github.com/login/oauth/access_token'
SCOPES = ['user:email', 'public_repo']

API_URL = "https://api.github.com"
API_REPOS_COMMAND = '/user/repos'

ENCODING = 'utf-8'


@app.route("/")
def index():
    """
    This function creates an url to authorize in GitHub and redirect to the url.

    :return: redirect(authorization_url)
    """

    github = OAuth2Session(CLIENT_ID, scope=SCOPES)
    authorization_url, state = github.authorization_url(AUTHORIZATION_BASE_URL)
    session['oauth_state'] = state
    return redirect(authorization_url)


@app.route("/callback", methods=["GET"])
def callback():
    """
    This is a function for retrieving a GitHub access token, and creating a new repository.
    The user has been redirected back from the provider to a registered callback URL.
    With this redirection comes an authorization code included in the redirect URL.
    It uses to obtain an access token. Then the app creates a new repository using GitHub
    API with the created access token and adds application files.

    if application did not have errors:
    :return: redirect('https://github.com/<GitHubUserName>/replicator'
    else:
    :return: redirect('https://github.com/<GitHubUserName>/replicator/blob/master/error.log'

    """

    github = OAuth2Session(CLIENT_ID, state=session['oauth_state'],)
    token = github.fetch_token(TOKEN_URL,
                               client_secret=CLIENT_SECRET,
                               authorization_response=request.url)

    user = github.get('https://api.github.com/user').json()
    session['oauth_token'] = token
    session['oauth_name'] = user.get('login')
    session['oauth_email'] = user.get('email')
    repo = 'replicator'
    description = ''
    payload = {'name': repo, 'description': description, 'auto_init': 'false'}
    errors = str()
    try:
        requests.post("{}{}".format(API_URL, API_REPOS_COMMAND),
                      auth=(session['oauth_name'], session['oauth_token']['access_token']),
                      data=json.dumps(payload),
                      timeout=(4, 10))
    except request.Timeout as error:
        print("Timeout({}): {}.".format(error.errno, error.strerror))
    for file in FILES:
        if os.path.exists("{}/{}/{}".format(os.getcwd(), repo, file)):
            with open("{}/{}/{}".format(os.getcwd(), repo, file), 'rb') as open_file:
                try:
                    byte_content = open_file.read()
                except IOError as error:
                    print("I/O error({}): {}. \nFile {} was not opened".format(error.errno,
                                                                               error.strerror,
                                                                               file))
                    continue
            base64_bytes = base64.b64encode(byte_content)
            base64_string = base64_bytes.decode(ENCODING)
            raw_data = {"message": "Add {}".format(file),
                        "author": {"name": 'VadymKhodak',
                                   "email": 'vaddimart@gmail.com'},
                        "content": base64_string}
            json_data = json.dumps(raw_data, indent=2)
            api_command = '/repos/{}/{}/contents/{}'.format(session['oauth_name'], repo, file)
            try:
                requests.put("{}{}".format(API_URL, api_command),
                             auth=(session['oauth_name'], session['oauth_token']['access_token']),
                             data=json_data,
                             timeout=(4, 10))
            except request.Timeout as error:
                print("Timeout({}): {}. File {} was not create".format(error.errno,
                                                                       error.strerror,
                                                                       file))
        else:
            error = "{} File \"{}/{}/{}\" is not found! \n".format(datetime.now(),
                                                                   os.getcwd(),
                                                                   repo,
                                                                   file)
            errors = errors + error
            print(error)
    if errors:
        errors = bytes(errors, ENCODING)
        base64_bytes = base64.b64encode(errors)
        base64_string = base64_bytes.decode(ENCODING)
        raw_data = {"message": "Add error.log",
                    "author": {"name": 'VadymKhodak',
                               "email": 'vaddimart@gmail.com'},
                    "content": base64_string}
        json_data = json.dumps(raw_data, indent=2)
        api_command = '/repos/{}/{}/contents/{}'.format(session['oauth_name'], repo, 'error.log')
        try:
            requests.put("{}{}".format(API_URL, api_command),
                         auth=(session['oauth_name'], session['oauth_token']['access_token']),
                         data=json_data,
                         timeout=(4, 10))
        except request.Timeout as error:
            print("Timeout({}): {}. File {} was not create".format(error.errno,
                                                                   error.strerror,
                                                                   'error.log'))
        return redirect('https://github.com/{}/{}/blob/master/{}'.format(session['oauth_name'],
                                                                         repo,
                                                                         'error.log'))

    return redirect('https://github.com/{}/{}'.format(session['oauth_name'], repo))


@app.errorhandler(404)
def page_not_found(e):
    """
    This is a function to render 404.html

    :param e:
    :return:
    """
    return render_template('404.html'), 404


if __name__ == "__main__":
    # This allows us to use a plain HTTP callback
    os.environ['DEBUG'] = "1"

    app.secret_key = os.urandom(24)
    app.run(debug=True)
