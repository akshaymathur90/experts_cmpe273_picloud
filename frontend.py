#!/usr/bin/python
from flask import Flask,render_template, json, request
from fabric.api import env,run,execute,hosts
import fabfile
import sqlite3
import modifyHAProxy
import databaseConn
from subprocess import call
app = Flask(__name__)

@app.route("/")
def main():
    return render_template('index.html')

@app.route('/addnewapp')
def showSignUp():
    return render_template('AddApp.html')

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
	#call(['haproxy -D -f /Users/akshaymathur/Documents/StudyMaterial/Labs/273/Finals/Integrate/config.cfg -p /Users/akshaymathur/Documents/StudyMaterial/Labs/273/Finals/Integrate/haproxy.pid -sf $(cat /Users/akshaymathur/Documents/StudyMaterial/Labs/273/Finals/Integrate/haproxy.pid)'])

if __name__ == "__main__":
    app.run(debug=True)
    
