def check_for_print():
    import ast
    wast = ast.parse(open('wallet.py','r').read())
    for node in ast.walk(wast):
        if isinstance(node, ast.Name):
            if node.id == 'print':
                return "remove all prints from wallet.py before running tests"
            if node.id == '__builtins__': 
                return "don't use __builtins__ in wallet.py"
            if node.id == 'locals': 
                return "don't use locals in wallet.py"
            if node.id == 'globals': 
                return "don't use globals in wallet.py"
            if node.id == '__package__': 
                return "don't use __package__ in wallet.py"
    return False


def test_hedgehog():
    from subprocess import Popen, PIPE, TimeoutExpired
    assert not check_for_print()
    ws = Popen(["python3", "hedgehog-simple.py"], stderr=PIPE, stdout=PIPE)
    try:
        ws.wait(1)
        out = ws.stdout.read().decode('utf-8')
        assert 'Remaining Hedgehog Food 🐛: 200' in out
        assert 'Hedgehogs 🦔: 100' in out
    except TimeoutExpired:
        ws.kill()
        assert not 'hedgehog-simple.py did not terminate'

def test_rat():
    from subprocess import Popen, PIPE, TimeoutExpired
    assert not check_for_print()
    ws = Popen(["python3", "hedgehog-rat.py"], stderr=PIPE, stdout=PIPE)
    try:
        ws.wait(1)
        out = ws.stdout.read().decode('utf-8')
        assert 'Hedgehogs 🦔: 100' in out
        assert 'Rats 🐀: 100' in out
    except TimeoutExpired:
        ws.kill()
        assert not 'hedgehog-rat.py did not terminate'

def test_ping_pong():
    from subprocess import Popen, PIPE, TimeoutExpired
    assert not check_for_print()
    ws = Popen(["python3", "ping-pong.py"], stderr=PIPE, stdout=PIPE)
    try:
        ws.wait(1)
        err = ws.stderr.read()
        assert 18000 <= len(err) < 18002
        assert err.count('↑↓'.encode('utf-8')) > 2000
    except TimeoutExpired:
        ws.kill()
        assert not 'ping-pong.py did not terminate'

def test_ping_pong_transaction():
    from subprocess import Popen, PIPE, TimeoutExpired
    assert not check_for_print()
    ws = Popen(["python3", "ping-pong-transaction.py"], stderr=PIPE, stdout=PIPE)
    try:
        ws.wait(1)
        out = ws.stdout.read()
        err = ws.stderr.read()
        assert 18000 <= len(err) < 18002
        assert b'Should start with '+err[0:3] in out
        assert err.count('↑↓'.encode('utf-8')) > 2000
    except TimeoutExpired:
        ws.kill()
        assert not 'ping-pong-transaction.py did not terminate\n'

def test_degree():
    from subprocess import Popen, PIPE, TimeoutExpired
    assert not check_for_print()
    ws = Popen(["python3", "degree.py"], stderr=PIPE, stdout=PIPE)
    try:
        ws.wait(1)
        out = ws.stdout.read().decode('utf-8').strip()
        assert 'Your wallet contains a degree!' in out
    except TimeoutExpired:
        ws.kill()
        assert not 'degree.py did not terminate'

def test_gacha():
    from subprocess import Popen, PIPE, TimeoutExpired
    assert not check_for_print()
    ws = Popen(["python3", "gacha.py"], stderr=PIPE, stdout=PIPE)
    try:
        ws.wait(1)
        out = ws.stdout.read().decode('utf-8').strip()
        assert 'wallet' not in out
    except TimeoutExpired:
        ws.kill()
        assert not 'gacha.py did not terminate'
