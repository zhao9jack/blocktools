#!/usr/bin/python
import sys
from blocktools import *
from block import Block, BlockHeader
import g
import json

def parse(blockchain):
	counter = 0
	while True:
		#print counter
                try:
		    block = Block(blockchain)
		    block.toString()
                except:
                    return
		#counter+=1

def main():
    for line in open("addr2.txt", "r"):
        line = line.strip("\n")
        g.addrs[line] = 1
    print len(g.addrs.items())
    f_str = "got2/" + str(1) 
    fp = open(f_str, "w")
    fp.write(json.dumps(g.addrs.items()))
    fp.close()
    for i in range(173, 254):
        print str(i) + '    ' +  str(len(g.addrs.items()))
        f_str = '/bitcoind/blocks/blk00' + str(i) + '.dat'
	with open(f_str, 'rb') as blockchain:
	    parse(blockchain)
        f_str = "got2/" + str(i) 
        fp = open(f_str, "w")
        fp.write(json.dumps(g.addrs.items()))
        fp.close()

if __name__ == '__main__':
	main()
