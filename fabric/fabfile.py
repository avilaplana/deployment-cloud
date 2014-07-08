# from fabric.api import local, env
# from fabric.operations import run, put
# from fabric.context_managers import lcd

from __future__ import with_statement
from fabric.api import local, settings, abort, run, cd, put, lcd, sudo
from fabric.contrib.console import confirm
from fabric.context_managers import shell_env


localFolder="~/tmp"
gitRepo="freview-api"
gitUser="avilaplana"
gitTag="git tag release/"
gitPushTag="git push origin release/"
distName="surferstv-1.0-SNAPSHOT"

remoteFolder="~/tmp"
deployFolder="/opt/freview-api"
serviceName="freeview-api"


def clone():
	local("rm -fr " + localFolder)
	local("mkdir -p " + localFolder)
	with lcd(localFolder):
		local("git clone git@github.com:" + gitUser + "/"+ gitRepo + '.git')    

def tag(tag = "no tag"):
	if tag !="no tag":
		print("Tagging to release/" + tag)
		with lcd(workPath + '/' + gitRepo):
			local(gitTag + tag)
			local(gitPushTag +  tag)
	else:
		print("No Tagging to " + tag)
	

def set_version_env(tag = "no tag"):
	if tag !="no tag":
		with shell_env(FREEAPI_VIEW_VERSION=tag):
			local("env | grep FREEAPI_VIEW_VERSION")


def dist():			
	with lcd(localFolder + '/' + gitRepo):
		local("sbt dist")

def stop():
	sudo('service ' + serviceName + ' stop', pty=False)

def start():
	sudo('service ' + serviceName + ' start', pty=False)
	
def copy():
	run('rm -fr ' + remoteFolder)
	run('mkdir -p ' + remoteFolder)
	put(localFolder + '/' + gitRepo + '/target/universal/' + distName + '.zip', remoteFolder) 
	run('unzip '+ remoteFolder + '/' + distName + '.zip' +  ' -d ' + remoteFolder)		
	run('mv ' + remoteFolder + '/' + distName + ' ' + remoteFolder + '/freeview-api')

def deploy():
	sudo('rm -fr ' + deployFolder)	
	sudo('mv ' + remoteFolder + '/freeview-api ' + deployFolder)
	sudo('chown -R playframework:nogroup ' + deployFolder)

def deploy_cloud(tag="no tag"):
	clone()
	set_version_env(tag)
	dist()
	# clone()
	# dist()
	# copy()
	# stop()
	# deploy()
	# start()