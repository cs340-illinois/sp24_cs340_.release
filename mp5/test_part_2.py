
def test_blocking():
    assert not run_one_test(case_blocking, should_block=True)

def case_blocking():
    from wallet import Wallet
    w = Wallet()
    w.change('deficit',5)
    w.change('deficit',-7)
    assert not "unreachable"

def test_nonblocking():
    assert not run_one_test(case_nonblocking)

def case_nonblocking():
    from wallet import Wallet
    w = Wallet()
    w.try_change('money',5)
    if w.try_change('money',-7) is not False:
        return 'expected failed withdrawal to return False'
    w.try_change('money',5)
    if w.try_change('money',-7) != 3:
        return 'expected successful withdrawal to return new value'

def test_mix():
    assert not run_one_test(case_mix)

def case_mix():
    from wallet import Wallet
    w = Wallet()
    if w.try_change('thing_1',5) != 5: return 'first try failed'
    if w.change('thing_2',7) != 7: return 'first change failed'
    if w.try_change('thing_2',-5) != 2: return 'change+try failed'
    if w.change('thing_1',-3) != 2: return 'try+change failed'
    if w.get('thing_1') != 2: return 'wrong final value'
    if w.get('thing_2') != 2: return 'wrong final value'

def test_not_busy_wait():
    assert not run_one_test(case_not_busy_wait, should_block=True, timeout=2)

def case_not_busy_wait():
    from wallet import Wallet
    import resource
    resource.setrlimit(resource.RLIMIT_CPU, (1,1))
    w = Wallet()
    w.change('deficit',5)
    w.change('deficit',-7)
    assert not "unreachable"
    
def test_wait_wakeup():
    assert not run_one_test(case_wait_wakeup, timeout=0.02)

def case_wait_wakeup():
    from wallet import Wallet
    w = Wallet()
    from threading import Thread
    import time
    messages = []
    def waiter(w):
        w.change('cash',-4)
        w.change('cash',+6)
        if w.change('cash',-8) != 2:
            messages.append('final value incorrect')
    def unwaiter(w):
        w.change('cash',+4)
        w.change('cash',-4)
        w.change('cash',+8)

    tw = Thread(target=waiter, args=(w,))
    tu = Thread(target=unwaiter, args=(w,))
    tw.start()
    time.sleep(0.01)
    if not tw.is_alive(): return 'Initial thread should have blocked'
    tu.start()
    tu.join()
    tw.join()
    if len(messages): return messages[0]

def test_work_while_waiting():
    assert not run_one_test(case_work_while_waiting, timeout=0.02)

def case_work_while_waiting():
    from wallet import Wallet
    w = Wallet()
    from threading import Thread
    import time
    def waiter(w):
        w.change('cash',-4)
    def worker(w):
        w.change('cattle',+40)
        w.change('hogs',+20)
        w.change('cash',+2)
        w.change('cattle',-20)
    def unwaiter(w):
        w.change('cash',+6)

    tw = Thread(target=waiter, args=(w,))
    tr = Thread(target=worker, args=(w,))
    tu = Thread(target=unwaiter, args=(w,))
    tw.start()
    time.sleep(0.01)
    tr.start()
    tr.join()
    if not tw.is_alive(): return 'Initial thread should have blocked'
    if w.get('cash') != 2: return 'Deposit should go through even with pending withdrawal'
    tu.start()
    tu.join()
    tw.join()
    if w.get('cash') != 4: return 'Cash account incorrect'
    if w.get('cattle') != 20: return 'Cattle count incorrect'
    if w.get('hogs') != 20: return 'Hogs count incorrect'

def test_multi_wallet_nonblocking():
    assert not run_one_test(case_multi_wallet_nonblocking)

def case_multi_wallet_nonblocking():
    from wallet import Wallet
    w1 = Wallet()
    w2 = Wallet()
    w1.try_change('cash',5)
    w2.try_change('cash',8)
    if w1.try_change('cash',-6) is not False:
        return 'Wallet 1 should not have completed action'
    if w2.try_change('cash',-6) != 2:
        return 'Wallet 2 should have completed action'
    if w1.get('cash') != 5:
        return 'Wallet 1 ended with wrong value'
    if w2.get('cash') != 2:
        return 'Wallet 2 ended with wrong value'

def test_multi_wallet_blocking():
    assert not run_one_test(case_multi_wallet_blocking, timeout=0.1)

def case_multi_wallet_blocking():
    from wallet import Wallet
    w1 = Wallet()
    w2 = Wallet()
    from threading import Thread
    import time
    
    def waiter(w1,w2):
        w1.change('cash',-10)
        w2.change('cash',-10)
    def half_wait(w1,w2):
        w1.try_change('cash',15)
        w2.change('cash',-5)
    def unwaiter(w1,w2):
        w2.change('cash',25)

    t1 = Thread(target=waiter, args=(w1,w2))
    t2 = Thread(target=half_wait, args=(w1,w2))
    t3 = Thread(target=unwaiter, args=(w1,w2))

    t1.start()
    time.sleep(0.01)
    if not t1.is_alive(): return 'Thread 1 failed to block on wallet 1'

    t2.start()
    time.sleep(0.01)
    if not t1.is_alive(): return 'Thread 1 failed to block on wallet 2'
    if not t2.is_alive(): return 'Thread 2 failed to block'
    if w1.get('cash') != 5: return 'Threads 1 and 2 failed to manipulate wallet 1 correctly'

    t3.start()
    [t.join() for t in (t1,t2,t3)]
    if w1.get('cash') != 5: return 'Wallet 1 ends with wrong value'
    if w2.get('cash') != 10: return 'Wallet 2 ends with wrong value'



def run_one_test(fn, should_block=False, args=(), timeout=0.05):
    from multiprocessing import Queue, Process
    q = Queue()
    def wrapper(q):
        try:
            q.put(fn(*args))
        except BaseException as ex:
            q.put(ex)
    p = Process(target=wrapper, args=(q,))
    p.start()
    p.join(timeout)
    msg = [q.get()] if not q.empty() else []
    if should_block and not p.is_alive():
        msg.append('Expected to block, but did not')
    elif not should_block and p.is_alive():
        msg.append('Blocked, but should have finished in under {} seconds'.format(timeout))
    if p.is_alive(): p.kill()
    return msg[0] if msg else None

