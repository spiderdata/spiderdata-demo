import select
import sys
from websocket import create_connection


ws = create_connection('ws://127.0.0.1:5000/message/tom/tony')
stdin = sys.stdin

rlist = [stdin, ws]
wlist = []
msg = None

while True:
    rs, wss, xs = select.select(rlist, wlist, [])

    for r in rs:
        if r is ws:
            print(r.recv())
        else:
            msg = r.readline()
            wlist.append(ws)

    for w in wss:
        w.send(msg)
        wlist.remove(w)
        msg = None
