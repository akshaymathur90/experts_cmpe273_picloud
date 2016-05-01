#!flask/bin/python
from pyhaproxy.parse import Parser
from pyhaproxy.render import Render
import pyhaproxy.config as config

def getConfFile():
	cfg_parser = Parser('config.cfg')
	configuration = cfg_parser.build_configuration()
	return configuration
	
def writeConfFile(configuration):
	cfg_render = Render(configuration)
	cfg_render.dumps_to('config.cfg')

def insertNewApp(aclName, newPath, backendName, serverName, serverIP, serverPort):
	
	# Get configuration
	configuration=getConfFile()
	#Create New ACL in FrontEnd.
	the_fe_section = configuration.frontend('http-in')
	aclTest=config.Acl(aclName+' url_beg', newPath)
	the_fe_section.acls().append(aclTest)
	
	#Create New Use_Backend condition
	the_fe_section.usebackends().append(config.UseBackend(backendName, 'if', aclName, False))
	
	#Create a New Backend
	configuration.backends.append(config.Backend(backendName,{'configs':[('balance','roundrobin ')],'servers':[config.Server(serverName,serverIP,serverPort,'')]}))
	
	#write configuration to file
	writeConfFile(configuration)

def addNewBackend(backendName, serverName, serverIP, serverPort):
	# Get configuration
	configuration=getConfFile()
	
	#get the required backend
	the_be_section = configuration.backend(backendName)
	
	#add new server to backend
	servers = the_be_section.servers()  # return list(config.Server)
	#servers.append(config.Server('WEB4','127.0.0.1','5003',''))
	servers.append(config.Server(serverName,serverIP,serverPort,''))
	
	#write configuration to file
	writeConfFile(configuration)
	
def removeApp(aclName, newPath, backendName, serverName, serverIP, serverPort):
	# Get configuration
	configuration=getConfFile()
	the_fe_section = configuration.frontend('http-in')
	#print config.Acl(aclName+' url_beg', newPath)
	the_fe_section.acls().remove(the_fe_section.acl(aclName))
	#the_fe_section.usebackends().remove(config.UseBackend(backendName, 'if', aclName, False))
	
	k=0
	t=-1
	for i in the_fe_section.usebackends():
		print i.backend_name
		if i.backend_name == backendName:
			print "found"
			t=k
		k=k+1
	if t!=-1:
		print the_fe_section.usebackends()[t]
		del the_fe_section.usebackends()[t]
	#configuration.backends.remove(config.Backend(backendName,{'configs':[('balance','roundrobin ')],'servers':[config.Server(serverName,serverIP,serverPort,'')]}))
	print configuration.backend(backendName).name
	configuration.backends.remove(configuration.backend(backendName))
	#write configuration to file
	writeConfFile(configuration)
	