import sys
import os

WARNING = '\033[31m'
MASSAGE = '\033[32m'
text = '\033[37m'
#get the list of miners and stop them 
containers_list = os.popen('docker ps -aq').read()
containers_list = containers_list.splitlines()
num_container = len(containers_list)
print(MASSAGE+'Stoping all miners......')
for x in xrange(0,num_container):
		response = os.popen('docker ' + 'exec ' + '-it ' + containers_list[x] + ' bitcoin-cli setgenerate false').read()
	    	print(MASSAGE+'Miner%d was stoped'%(x+1))
