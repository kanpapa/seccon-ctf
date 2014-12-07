import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("number.quals.seccon.jp",31337))

for l in range(100):
    print l
    recvstr = s.recv(4096)
    print "recvstr:",recvstr

    line = recvstr.splitlines()
    line1 = line[0]
    line2 = line[1]
    print "line1:",line1
    print "line2:",line2

    strlist = line1.split(',')
    print "strlist:",strlist

    numlist = map(int, strlist)
    print "numlist:",numlist

    numlist.sort()
    print "numlist(sort):",numlist

    if line2.find("maximum") != -1:
       numlist.reverse()

    sendstr = str(numlist[0])+'\n'
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

recvstr = s.recv(4096)
print "recvstr:",recvstr

recvstr = s.recv(4096)
print "recvstr:",recvstr

recvstr = s.recv(4096)
print "recvstr:",recvstr

recvstr = s.recv(4096)
print "recvstr:",recvstr

s.close()
