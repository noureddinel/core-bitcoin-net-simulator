#A script to generate a local bitcoin testnet network using docker. 
#----------------------------------------------------------------------
import sys
import os
import time
import sys, getopt
#----------------------------------------------------------------------
WARNING = '\033[31m'
MASSAGE = '\033[32m'
num_nodes = 2 #default: number of mining nodes.
num_cores = [] #default: number of cores for each node.
block_time = 2 #default block time 2 mi 
dockerfile = 'Dockerfile'
bitcoin_config = 'bitcoin.conf'
docker_compose = 'docker-compose.yml'
files_list =[dockerfile,bitcoin_config,docker_compose]
missing_files = []
container_id =''
containers_list = []
delays_list = []
jitter_list = []
jitter_type = []
jitter_response = 0
delay_response = 0
#---------------------------------------------------------------------
#User's input :
print(MASSAGE +'*********Welcome**********')
print(MASSAGE +'Simulation Setup and Configuration.......')
print(MASSAGE+'Tearing down existing setup')
tearDownState = os.popen('python teardown.py').read()
print(tearDownState)
print('Please enter the desired parameters to setup your simulation')
#Network size (number of nodes): 
num_nodes = int(raw_input(MASSAGE+"- Number of nodes:")) 

#Validate the number of nodes entered by the user:
if num_nodes < 2:
  print(WARNING +'\r\nERROR: Network generation process can not start with 0 nodes\r\n')
  exit()

#Setup a docker-compose.yml:
file = open(docker_compose,"w+") 
file.write('version: \'3\'\n')
file.write('services:\n')
ip = 2
if num_nodes != 0:
  for i in range(1,num_nodes+1,1):
      file.write('  node%d: \r\n\
      build: .\r\n\
      cap_add: \r\n\
        - ALL \r\n\
      volumes:\r\n\
        - ./bitcoin.conf:/root/.bitcoin/bitcoin.conf\r\n\
      command: bitcoind  -testnet  -server  -listen   -rpcuser=rpc -rpcpassword=x  -rpcport=10345 -port=12333 '%(i))
      for j in range(1,num_nodes+1,1):
        
         file.write('-addnode=10.7.0.%d:12333 ' % (j))
      file.write('\n      networks:\r\n\
        vpcbr:\r\n\
          ipv4_address: 10.7.0.%d\r\n\
      ports:\r\n\
          - "%d:12333"\r\n\n\n' % (i+1,i+12341))
file.write('networks:\r\n\
  vpcbr:\r\n\
    driver: bridge\r\n\
    ipam:\r\n\
     config:\r\n\
       - subnet: 10.7.0.0/16')
file.close()

#verfiy files existance and build docker continers:
print(MASSAGE +'Checking required files....')

if (os.path.isfile(bitcoin_config) and  os.path.isfile(docker_compose) and os.path.isfile(dockerfile)): 
    print(MASSAGE +'All files exist....\r\nGenerating docker containers....')
    print(MASSAGE+'It will take long time if this is the first simulation you run....')
    #Execute a shell command to generate and run docker containers:

    os.system('docker-compose up -d --build')
    #Attach shells to each container and execute the miner command:
    containers_list = os.popen('docker ps -aq').read()
    containers_list = containers_list.splitlines()
    time.sleep(5)
    print(MASSAGE+"Continers are created successfully.....")
    containers_names_list = os.popen('docker ps --format {{.Names}}').read()#get containers names
    containers_names_list = containers_names_list.splitlines()


    #Number of mining cores for each miner:
    for x in xrange(0,num_nodes): 
      C_names_only = containers_names_list[x][27:32]
      num_cores.append(int(raw_input('- Number of cores for node  %s : '%(C_names_only))))
      
    #Block time:
    #B_time = int(raw_input("- Block time:"))

    #Network emulation parameters:
    while(1) :
      delay_response = raw_input('- Apply network emulation?(y/n):')
      delay_response = delay_response.replace(" ","")
      if delay_response == 'y' or delay_response == 'Y':
              delay_response = 1
              while(1):
                d_nodes = int(raw_input(MASSAGE+'Number of nodes to be delayed:'))
                if d_nodes > num_nodes:
                  print(WARNING+"Invalid input! should be equal or less than the total number of nodes.")
                else:
                  break;
              for x in xrange(0,d_nodes):
                   C_names_only = containers_names_list[x][27:32]

                   while(1):
                       delay = (raw_input('Delay for Node %s (ms):'%(C_names_only)))
                       if (unicode(delay).isnumeric()):
                           delays_list.append(delay)
                           break;
                       else:
                          print(WARNING+'Invalid input ! please enter numeric values only')
                          print(MASSAGE)
              jitter_response = raw_input('Add delay Jitter?(y/n):')
              if jitter_response == 'y' or jitter_response == 'Y' :
                    jitter_response = 1
                    for x in xrange(0,d_nodes):
                        C_names_only = containers_names_list[x][27:32]
                        while(1):
                        	jitter = (raw_input('Delay Jitter for Node %s (ms):'%(C_names_only)))
                        	if (unicode(jitter).isnumeric()):
	                        	jitter_list.append(jitter)
                           		break;
		                else:
		                        print(WARNING+'Invalid input ! please enter numeric values only')
		                        print(MASSAGE)
		                while(1):
                       		 j_type = (raw_input('Delay distribution for Node %s (normal/pareto):'%(C_names_only)))
                       		 if j_type == 'normal ' or j_type == 'Normal' or j_type == 'pareto' or j_type =='Pareto':
                       		    jitter_type.append(j_type)
                       		    break;
                       		 else:
                       		 	print(WARNING+'Invalid input ! please enter normal or pareto')
		                        print(MASSAGE)
                    break;
              elif jitter_response == 'n' or jitter_response == 'N' :
                    jitter_response = 0
                    break;
              else :
                  print(WARNING + 'Invalid input!')
      elif delay_response == 'n' or delay_response == 'N' :
             delay_response = 0
             break;
              
      else :
             print(WARNING + 'Invalid input!')

    #Time duration of the experiment: 
    Duration_r = raw_input("- Experiment Duration (h) or (m):")
    Duration = Duration_r.replace(" ","")

    if Duration.endswith('m') | Duration.endswith('M'):
       Duration = Duration[0:len(Duration)-1]
       Duration = int(Duration)*60

    elif Duration.endswith('h') | Duration.endswith('H'):
        Duration = Duration[0:len(Duration)-1]
        Duration = int(Duration)*60*60 

    #Setup the miner in each node: 
    for k in range(0,num_nodes):
       miner_startup = os.system('docker exec -it ' + containers_list[k] + ' bitcoin-cli setgenerate true %d' %(num_cores[k]))
    #Record the start of the experiment:
    start = time.time()
    print(MASSAGE +'Testnet is up and running for %s .....\nA performance report will be generated and saved in the current directory at the end of the simulation....'%(Duration_r))
#Notify the user if any file is missing or if the setup faild: 
for j in range(0,3):
  if os.path.isfile(files_list[j]) == 0:
     missing_files.append(files_list[j])
if len(missing_files) != 0: 
  print(WARNING +'WARNING!...Can not generate the network,the following files do not exist in the current directory:\r\n\
  %s')%(missing_files)

#Apply network emulation:

if delay_response == 1:
    duration_h = (Duration/60)/60
    if jitter_response == 1:
        for x in xrange(0,d_nodes):
            print('pubmba%d'%(x))
            os.system('pumba -l info  netem --duration %s  delay --time %s %sms -d %s %s &'%(str(Duration_r),delays_list[x],jitter_list[x],jitter_type[x],str(containers_names_list[x])))
    else:
        for x in xrange(0,d_nodes):
            os.system('pumba -l info netem --duration ' + str(Duration_r) + ' delay --time ' + delays_list[x] +' '+str(containers_names_list[x]) +' &')
            #            os.system('pumba -l info netem --duration %s delay --time %s %s &'%(str(Duration_r)),delays_list[x],str(containers_names_list[x]))
    print(MASSAGE+'Network emulation is running......')
print(MASSAGE+'Local Bitcoin testing network is up and running.....')
#Monitor experiment timer:
while (1):
  #when the spacified duration is done:
  if (time.time()-start >= Duration):  
      break; 

#Display the performance report and save it to a log file:
if os.path.isfile('performanceReport'):
   run_performance = os.system('python getperformance.py > performanceReport_Recent.txt')
else:   
   run_performance = os.system('python getperformance.py > performanceReport.txt')
print('  ')
print('Perfomance report was generated successfully...')

#Stop the miners in each node:
time.sleep(4)
stopminers = os.system('python stopminers.py')
try:
  sys.stdout.close()
except:
  pass
try:
  sys.stderr.close()
except:
  pass

