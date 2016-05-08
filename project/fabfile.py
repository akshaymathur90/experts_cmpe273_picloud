from fabric.api import env,run,execute,hosts

# make sure this package is installed on all the server - sudo apt-get install python-virtualenv

# 1 - Set the (global) host_string
machine = "samata@54.215.224.150"
env.host_string = machine
env.passwords = { machine + ':22': '273project'}
def install_env(url,port):
  #port ="8777"
  #url = "https://bitbucket.org/SamSirsikar/273project.git"
  #run("kill `lsof -t -i:"+port+"`")
  project_name = url.rsplit("/", 1)[1]
  run("rm -rf ./" + project_name)
  run("rm -rf /tmp/venv/")
  run("virtualenv /tmp/venv")
  
  run("git clone " + url + " " + project_name)
  output =""
  output = run("cat " + project_name + "/config.txt")
  output = output.split('\n')
  #run("sudo cd /hello && ./update.sh")
  for i in range(0,len(output)-1):
      temp = output[i]
      run("cd " + project_name + " && PATH=/tmp/venv/bin:$PATH "+ temp.rstrip('\r'))
      
  #run("echo \"tmux new-session -d -s my_session '" + output[1].rstrip('\r') + "' && tmux detach -s my_session\" > /tmp/venv/run.sh")
  # run("echo \"  " + output[1].rstrip('\r') + "\" > /tmp/venv/run.sh")
  # run("echo \" " + output[1].rstrip('\r') + " >& /dev/null < /dev/null &\" > /tmp/venv/run.sh")
  
  '''Forcing the app to run on a particular port'''
  #run("cd " + project_name + " && PORT=" + port + " PATH=/tmp/venv/bin:$PATH "+ output[1].rstrip('\r') )
  app_name = output[1].rstrip('\r').split(" ")
  
  run("set -m; PORT=" + port + " PATH=/tmp/venv/bin:$PATH python ./"+ project_name+"/"+app_name[1].rstrip('\r')+" nohup sleep 100 >> /tmp/xxx 2>&1 < /dev/null & pty=False" )

def install(url,port):
	execute(install_env,url,port)