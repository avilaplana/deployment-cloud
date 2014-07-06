# from fabric.api import local, env
# from fabric.operations import run, put
# from fabric.context_managers import lcd

from __future__ import with_statement
from fabric.api import local, settings, abort, run, cd, put, lcd
from fabric.contrib.console import confirm

workPath = "./tmp/deployment"
optPath = "/opt/freeview-api"

def clone():
	local("rm -fr ./tmp")
	local("mkdir -p " + workPath)
	with lcd(workPath):
		local("git clone git@github.com:avilaplana/freview-api.git")    

def tag():
	with lcd(workPath + '/freview-api'):
		local()

def set_version():
	with lcd(workPath + '/freview-api'):
		local()

def dist():			
	with lcd(workPath + '/freview-api'):
		local("sbt dist")

def stop():
	run('sudo service freeview-api stop')

def start():
	run('sudo service freeview-api start')
	
def copy():
	run('rm -fr ./tmp')
	run('mkdir -p ' + workPath)
	put(workPath + '/freview-api/target/universal/surferstv-1.0-SNAPSHOT.zip', './tmp')	
	run('unzip ./tmp/surferstv-1.0-SNAPSHOT.zip -d ' + workPath)		
	run('mv ' + workPath + '/surferstv-1.0-SNAPSHOT ' + workPath + '/freeview-api')

def deploy():
	run('sudo rm -fr ' + optPath)	
	run('sudo mv ' + workPath + '/freeview-api ' + optPath)
	run('sudo chown -R playframework:nogroup ' + optPath)

def all():
	deploy()
	start()

