import sys
import threading
from wallet import Wallet
import time

def test_add_worm(wallet):
  for i in range(500):
    wallet.change('worm',+1)
    sys.stderr.write('🐛')
    time.sleep(0.000001)
    
def test_add_corn(wallet):
  for i in range(500):
    wallet.change('corn',+1)
    sys.stderr.write('🌽')
    time.sleep(0.000001)
    


def test_add_hedghog(wallet):
  for i in range(100):
    wallet.change('worm',-3)
    wallet.change('hedgehog',+1)
    sys.stderr.write('🦔')
    time.sleep(0.0001)

def test_add_rat(wallet):
  for i in range(100):
    if wallet.try_change('worm',-3) is False:
      wallet.change('corn',-3)
      sys.stderr.write('🐁')
    else:
      sys.stderr.write('🐀')
    wallet.change('rat',+1)
    time.sleep(0.0002)


if __name__ == '__main__':
  print("Running Test: Test hedgehogs and rats");
  wallet = Wallet()
  ts = [threading.Thread(target=f, args=[wallet]) for f in [test_add_worm, test_add_corn, test_add_hedghog, test_add_rat]]
  for t in ts: t.start()
  for t in ts: t.join()
  print(file=sys.stderr)
  print('Remaining worms 🐛:', wallet.get('worm'))
  print('Remaining corn 🌽:', wallet.get('corn'))
  print('Hedgehogs 🦔:', wallet.get('hedgehog'))
  print('Rats 🐀:', wallet.get('rat'))
  
