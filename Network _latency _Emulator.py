import sys
import os 

WARNING = '\033[31m'
MASSAGE = '\033[32m'
text = '\033[37m'


containers_list = os.popen('docker ps --format {{.Names}}').read() #get containers names
containers_list = containers_list.splitlines()
delays_list = []
#User's preferances:
Num_nodes = int(raw_input('Number of nodes to be delayed: '))
for x in xrange(0,Num_nodes):
	delays_list.append(int(raw_input('Delay for Node%d(%s) (ms):'%(x,containers_list[x]))))
Emulator_run_duration = int(raw_input('Emulator runnning duration (h):'))
#verify pumba:
# pumba_version = os.popen('pumba --version').read()
# print(MASSAGE+'Verifying pumba version....')

# if(pumba_version )
# 	print(WARNING+'pumba is not installed !')
# 	print(MASSAGE+'Installing pumba .....')
# 	os.popen('sudo curl -L https://github.com/alexei-led/pumba/releases/download/0.5.2/pumba_linux_amd64 -o /usr/bin/pumba && sudo chmod +x /usr/bin/pumba')
# 	print(MASSAGE+'pumba is installed .')
# print(MASSAGE+pumba_version)

#Run pumba: 
for x in xrange(0,Num_nodes+1):
	print(containers_list[x])
	os.popen('pumba -l info  netem --duration %sh  delay --time %s %s '%(str(Emulator_run_duration),str(delays_list[x]),str(containers_list[x])))
	print("finished:%d"%(x))
print(MASSAGE+'Network Emulator is running...')
