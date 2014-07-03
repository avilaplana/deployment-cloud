# from fabric.api import local, env
# from fabric.operations import run, put
# from fabric.context_managers import lcd

from __future__ import with_statement
from fabric.api import local, settings, abort, run, cd
from fabric.contrib.console import confirm

def prepare_deploy():
	local("rm -fr $HOME/tmp")
	local("mkdir $HOME/tmp")
	with lcd('$HOME/tmp'):
		local("git clone git@github.com:avilaplana/freview-api.git")    

def tag():
	with lcd('$HOME/tmp/freview-api'):
		local()

def set_version():
	with lcd('$HOME/tmp/freview-api'):
		local()

def dist():			
	with lcd('$HOME/tmp/freview-api'):
		local("sbt dist")

def stop():
	run('ps aux | grep FREEVIEW_API | grep -v \'grep\' | awk \'{print $2}\'')
def copy():
	run('rm -fr /tmp/deployment')
	run('mkdir -p /tmp/deployment')
    # put('$HOME/tmp/freview-api/target/universal/surferstv-1.0-SNAPSHOT.zip', '/tmp/deployment')	


# prepare_deploy()
# dist()
# copy()		
stop()