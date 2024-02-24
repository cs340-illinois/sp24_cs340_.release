import threading
import socket
from wallet import Wallet

wallet = Wallet() # the only global variable you should use

def create_wallet_server(local_port):
  ... # implement this function
  # you will need to use threads, which requires adding additional functions or classes
  # make to properly close the listening socket even on a KeyboardInterrupt exception
      
    
    

if __name__ == '__main__':
  # parses command-line arguments, ensuring all implementations are invoked the same way
  import getopt
  import sys
  
  local_port = 34000
  optlist, args = getopt.getopt(sys.argv[1:], 'p:')
  for arg in optlist:
    if arg[0] == '-p': local_port = int(arg[1])
  print("Launching wallet server on :"+str(local_port))
  create_wallet_server(local_port)
