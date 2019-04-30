import socket
import time
import sympy

x = sympy.Symbol('x')

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("zerois-o-reiwa.seccon.jp",23615))

for l in range(100):
    print l

    #num skip
    recvstr = s.recv(4096)
    print "recvstr:",recvstr

    recvstr = s.recv(4096)
    print "recvstr:",recvstr

    line = recvstr.splitlines()
    line1 = line[0]
    line2 = line[1]
    print "line1:",line1
    print "line2:",line2

    line3 = line1.replace('0=', '')
    print "line3:",line3

    line4 = line3.replace('?', 'x')
    print "line4:",line4

    ans = sympy.solve(line4)
    print "ans:",ans

    if not ans:
        ansnum = 0
    else:
        ansnum = ans[0]

    sendstr = str(ansnum) + '\n'
    print "sendstr:",sendstr
    s.sendall(sendstr)

recvstr = s.recv(4096)
print "recvstr:",recvstr

recvstr = s.recv(4096)
print "recvstr:",recvstr

recvstr = s.recv(4096)
print "recvstr:",recvstr

recvstr = s.recv(4096)
print "recvstr:",recvstr

recvstr = s.recv(4096)
print "recvstr:",recvstr

recvstr = s.recv(4096)
print "recvstr:",recvstr

s.close()
