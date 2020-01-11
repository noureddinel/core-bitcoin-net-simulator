import sys
import os


state = int(os.popen('docker ps | wc -l').read())
if state == 1:
	print('No existing setup running!')
else:
	docker_state = os.popen('docker rm $(docker stop $(docker ps -aq))').read()
