#!env python
import sys
import struct

infile = open(sys.argv[1], 'r')
outfile = open(sys.argv[2], 'w')

#for i in range(3):
#    d = infile.readline()
#    outfile.write(d)

data = infile.read()
odata = ''
j = len(data) - 1

for i in range(len(data)):
    low  = ord(data[j]) & 0x0f 
    high = ord(data[j]) >> 4
    odata += chr((low * 16)| high)
    j = j - 1

outfile.write(odata)

infile.close()
outfile.close()

