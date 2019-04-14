# replicator

[![Python versions](https://img.shields.io/pypi/pyversions/bsonrpc.svg)](#replicator)

|\>\> [1. Objective](#1-objective)

|\>\> [2. Goals](#2-goals)

|\>\> [3. Non-goals](#3-non-goals)

|\>\> [4. Assumptions](#4-assumptions)

|\>\> [5. Design](#5-design)

|\>\> [6. Fault-Tolerance](#6-fault-tolerance)

|\>\> [7. System Requirements](#7-system-requirements)

|\>\> [8. Deployment](#8-deployment)

|\>\> [9. Testing](#9-testing)

|\>\> [10. Extensibility and maintenance](#10-extensibility-and-maintenance)

|\>\> [11. Trade-offs and limitations](#11-trade-offs-and-limitations)

|\>\> [Authors](#authors)


## 1. Objective
This is Python/Flask web-application. It is a self-replicating GitHub repository.
It means that if you follow the link of this application the application creates a repository in your GitHub account that includes files of this web-application.

## 2. Goals


## 3. Non-goals
The application cannot get the users' password and cannot get access to users' private repositories.

## 4. Assumptions


## 5. Design


## 6. Fault-Tolerance
If some files (in settings.FILES) is not exist application will create "error.log" file.


## 7. System Requirements
```text
python >= 2.7
Flask==1.0.2
Werkzeug==0.15.2
requests==2.21.0
requests-oauthlib==1.2.0
```

## 8. Deployment
The application deployed on pythonanywhere.com
There are points why I choose it:
* easy to deploy
* cheep or free (it is up to your choice)
* it is python oriented host

* Create account on pythonanywhere.com:
    - go to https://www.pythonanywhere.com
    - click button "Start running Python online in less than a minute!"
    - click button "Create a Beginner account"
    - fill in the form and push button "Register"
    - on top right side click on link "Account" 
    - push on tab "API Token" and create API Token
    
* Create GitHub account:
    - go to https://github.com
    - fill in the form 
    - click button "Sign up for GitHub"
   
* Create GitHub OAuth App: [more details here](https://developer.github.com/apps/building-oauth-apps/creating-an-oauth-app)
    - in the upper-right corner of any GitHub page, click your profile photo, then click Settings.
    - in the left sidebar, click Developer settings.
    - click OAuth Apps.
    - click Register New OAuth App.
    - in "Application name", type the name of your app.
    - in "Homepage URL", type the full URL to your app's website. (Example: https://<pythonanywhereNickName>.pythonanywhere.com)
    - in "Application description", type a description of your app that users will see.
    - in "Authorization callback URL", type the callback URL of your app. (Example: https://<pythonanywhereNickName>.pythonanywhere.com/callback)
    - click Register application.
    
    
* Create new Bash console:
    - come back to pythonanywhere.come
    - click on link "Consoles"
    - click on link "Bash"

* Clone the repository:
    - execute bash command:
```bash
git clone https://github.com/VadymKhodak/replicator.git
```
or
```bash
git clone git@github.com:VadymKhodak/replicator.git

```

* Create file settings.py that includes:
    - go back to Dashboard (https://www.pythonanywhere.com)
    - click on link "Files"
    - click on directory link "replicator"
    - enter file name "settings.py" into File name field and push button "New file"
    - type following script into settings.py change <YOUR_CLIENT_ID> and <YOUR_CLIENT_SECRET> to Client ID and Client Secret from GitHub OAuth App:
```python
CLIENT_ID = '<YOUR_CLIENT_ID>' # from OAuth App 
CLIENT_SECRET = '<YOUR_CLIENT_SECRET>' # from OAuth App

FILES = ('.gitignore',
         'README.md',
         'requirements.txt',
         'application.py',
         'templates/404.html',
         'static/css/style.css',
         'bg.jpg'
         )
```
   - push button save

* Create WEB application:
    - go back to Dashboard (https://www.pythonanywhere.com) 
    - click on link "Web"
    - push button "Add a new web app"
    - push button "Next"
    - choice "Manual configuration (including virtualenvs)"
    - choice python version (Example "Python 3.6" )
    - push button "Next"
    - enter "/home/YourUserName/replicator" in field "Source code:" and click button "V"
    - enable "Force HTTPS:"
    - click on link "/var/www/replicator_pythonanywhere_com_wsgi.py" to edit wsgi.py file
    - modify the file contents with the following code and edit "path":
```python
import sys

path = '/home/<YourUserName>/replicator'
if path not in sys.path:
    sys.path.append(path)

from application import app as application  # noqa

```
   - push button "Save"
   - go back to page "Web""
   - push button "Reload"

## 9. Testing

## 10. Extensibility and maintenance
You can make your application bigger, but do not forget to add additional files to settings.py file

## 11. Trade-offs and limitations
Using Django framework was traded-off, because it is the too big framework for the too simple application.


## Authors

* [**Vadym Khodak**](https://github.com/VadymKhodak)



