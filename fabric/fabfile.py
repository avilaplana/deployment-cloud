from __future__ import with_statement
from fabric.api import local, settings, abort, run, cd, put, lcd, sudo, env
from fabric.contrib.console import confirm
from fabric.context_managers import shell_env
import os
import json


def clone():
	print "------ CLONE --------"
	local("rm -fr " + localFolder)
	local("mkdir -p " + localFolder)
	with lcd(localFolder):
		local("git clone https://github.com/" + gitUser + "/"+ gitRepo + '.git')    

def tagging(tag = None):
	print "------ TAGGING --------"
	if tag:
		print("Tagging to release/" + tag)
		with lcd(localFolder + '/' + gitRepo):
			local(gitTag + tag)
			local(gitPushTag +  tag)
	else:
		print("No Tagging")
	

def dist(tag = None):		
	print "------ DIST --------"	
	with lcd(localFolder + '/' + gitRepo):
		if tag:
			with shell_env(FREEAPI_VIEW_VERSION=tag):
				local("env | grep FREEAPI_VIEW_VERSION")
				local("sbt dist")
		else:
			local("sbt dist")
					
def stop():
	print "------ STOP --------"
	sudo('service ' + serviceName + ' stop', pty=False)

def start():
	print "------ START --------"
	sudo('service ' + serviceName + ' start', pty=False)
	
def copy(tag = None):
	print "------ COPY --------"
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
	print "------ DEPLOY --------"
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

env.user = os.environ['user']
env.hosts = [os.environ['server_cloud']]

localFolder = os.environ['localFolder']
gitRepo = os.environ['gitRepo']
gitUser = os.environ['gitUser']
gitTag = os.environ['gitTag']
gitPushTag = os.environ['gitPushTag']
distName = os.environ['distName']
version = os.environ['version']

remoteFolder = os.environ['remoteFolder']
deployFolder = os.environ['deployFolder']
serviceName = os.environ['serviceName']