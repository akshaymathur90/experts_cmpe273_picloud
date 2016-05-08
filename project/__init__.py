# project/__init__.py

from flask import Flask, request, jsonify, session, render_template
from fabric.api import env,run,execute,hosts
from flask.ext.bcrypt import Bcrypt
from flask.ext.sqlalchemy import SQLAlchemy
import fabfile
import sqlite3
import modifyHAProxy
import databaseConn
from subprocess import call
from project.config import BaseConfig



# config

app = Flask(__name__)
app.config.from_object(BaseConfig)


bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
from project.models import User


# routes


@app.route('/api/register', methods=['POST'])
def register():
    json_data = request.json
    user = User(
        username = json_data['username'],
        email=json_data['email'],
        password=json_data['password']
    )
    try:
        db.session.add(user)
        db.session.commit()
        session['logged_in'] = True
        status = 'success'
    except:
        status = 'this user is already registered'
    db.session.close()
    return jsonify({'result': status})


@app.route('/api/login', methods=['GET','POST'])
def login():
    json_data = request.json
    user = User.query.filter_by(email=json_data['email']).first()
    if user and bcrypt.check_password_hash(
            user.password, json_data['password']):
        session['logged_in'] = True
        status = True
    else:
        status = False
    return jsonify({'result': status})

#@app.route('/')
#def index():
 #   return app.send_static_file('AddApp.html')
@app.route('/')
def index():
    return app.send_static_file('index.html')


#@app.route('/register', methods=['GET', 'POST'])
#def register():
  #  pass

@app.route('/api/logout', methods=['GET', 'POST'])
def logout():
     session.pop('logged_in', None)
     return jsonify({'result': 'success'})

@app.route('/api/status')
def status():
    if session.get('logged_in'):
        if session['logged_in']:
            return jsonify({'status': True})
    else:
        return jsonify({'status': False})     
		
@app.route('/newapp',methods=['POST'])
def signUp():
    appName = request.form['inputAppName']
    gitURL= request.form['inputGitURL']
    fabfile.install(gitURL,'8777')
    #Input data to DB
    
    
    aclName='is_'+appName
    pathName='/'+appName
    backendName='backend_'+appName
    serverName='serv_'+appName
    databaseConn.add_instance(appName, pathName, '54.215.224.150', 8777)
    print gitURL,appName
    
    #Modify HA Proxy
    modifyHAProxy.insertNewApp(aclName, pathName, backendName, serverName, '54.215.224.150', '8777')
    return json.dumps({'html':'<span>All fields good !!</span>'})

#if __name__ == "__main__":
 #   app.run(debug=True)		

