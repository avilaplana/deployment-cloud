# from fabric.api import local, env
# from fabric.operations import run, put
# from fabric.context_managers import lcd

from __future__ import with_statement
from fabric.api import local, settings, abort, run, cd, put, lcd, sudo
from fabric.contrib.console import confirm
from fabric.context_managers import shell_env
import json


def load_configuration(conf_file):
	with open(conf_file) as json_file:
	    json_data = json.load(json_file)
	    print json_data
    	return json_data

def clone():
	local("rm -fr " + localFolder)
	local("mkdir -p " + localFolder)
	with lcd(localFolder):
		local("git clone git@github.com:" + gitUser + "/"+ gitRepo + '.git')    

def tagging(tag = None):
	if tag:
		print("Tagging to release/" + tag)
		with lcd(localFolder + '/' + gitRepo):
			local(gitTag + tag)
			local(gitPushTag +  tag)
	else:
		print("No Tagging")
	

def dist(tag = None):			
	with lcd(localFolder + '/' + gitRepo):
		if tag:
			with shell_env(FREEAPI_VIEW_VERSION=tag):
				local("env | grep FREEAPI_VIEW_VERSION")
				local("sbt dist")
		else:
			local("sbt dist")
					
def stop():
	sudo('service ' + serviceName + ' stop', pty=False)

def start():
	sudo('service ' + serviceName + ' start', pty=False)
	
def copy(tag = None):
	if tag:
		version_to_use = tag
	else:
		version_to_use = version

	run('rm -fr ' + remoteFolder)
	run('mkdir -p ' + remoteFolder)
	put(localFolder + '/' + gitRepo + '/target/universal/' + distName + version_to_use + '.zip', remoteFolder) 
	run('unzip '+ remoteFolder + '/' + distName + version_to_use + '.zip' +  ' -d ' + remoteFolder)		
	run('mv ' + remoteFolder + '/' + distName + version_to_use +  ' ' + remoteFolder + '/freeview-api')

def deploy():
	sudo('rm -fr ' + deployFolder)	
	sudo('mv ' + remoteFolder + '/freeview-api ' + deployFolder)
	sudo('chown -R playframework:nogroup ' + deployFolder)

def deploy_cloud(tag= None):
	clone()
	tagging(tag)
	dist(tag)
	copy(tag)
	stop()
	deploy()
	start()

configuration = load_configuration("config.json")["production"]
localFolder=configuration["localFolder"]
gitRepo=configuration["gitRepo"]
gitUser=configuration["gitUser"]
gitTag=configuration["gitTag"]
gitPushTag=configuration["gitPushTag"]
distName=configuration["distName"]
version=configuration["version"]

remoteFolder=configuration["remoteFolder"]
deployFolder=configuration["deployFolder"]
serviceName=configuration["serviceName"]