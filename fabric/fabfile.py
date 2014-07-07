# from fabric.api import local, env
# from fabric.operations import run, put
# from fabric.context_managers import lcd

from __future__ import with_statement
from fabric.api import local, settings, abort, run, cd, put, lcd, sudo
from fabric.contrib.console import confirm

localFolder="~/tmp"
gitRepo="freview-api"
gitUser="avilaplana"
distName="surferstv-1.0-SNAPSHOT"

remoteFolder="~/tmp"
deployFolder="/opt/freview-api"
serviceName="freeview-api"


def clone():
	local("rm -fr " + localFolder)
	local("mkdir -p " + localFolder)
	with lcd(localFolder):
		local("git clone git@github.com:" + gitUser + "/"+ gitRepo + '.git')    

# def tag():
# 	with lcd(workPath + '/freview-api'):
# 		local()

# def set_version():
# 	with lcd(workPath + '/freview-api'):
# 		local()

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

def deploy_cloud():
	clone()
	dist()
	copy()
	stop()
	deploy()
	start()
	

