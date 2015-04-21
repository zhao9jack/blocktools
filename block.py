from blocktools import *
import hashlib
import redis
import g

def rhash(s):
    h1 = hashlib.new('ripemd160')
    h1.update(hashlib.sha256(s).digest())
    return h1.digest()

class BlockHeader:
	def __init__(self, blockchain):
		self.version = uint4(blockchain)
		self.previousHash = hash32(blockchain)
		#print "Previous Hash\t %s" % hashStr(self.previousHash)
		self.merkleHash = hash32(blockchain)
		self.time = uint4(blockchain)
		self.bits = uint4(blockchain)
		self.nonce = uint4(blockchain)
	def toString(self):
		#print "Version:\t %d" % self.version
		#print "Merkle Root\t %s" % hashStr(self.merkleHash)
		#print "Time\t\t %s" % str(self.time)
		#print "Difficulty\t %8x" % self.bits
		#print "Nonce\t\t %s" % self.nonce
                pass

class Block:
	def __init__(self, blockchain):
		self.magicNum = uint4(blockchain)
		self.blocksize = uint4(blockchain)
		self.setHeader(blockchain)
		self.txCount = varint(blockchain)
		self.Txs = []

		for i in range(0, self.txCount):
			tx = Tx(blockchain)
			self.Txs.append(tx)

	def setHeader(self, blockchain):
		self.blockHeader = BlockHeader(blockchain)

	def toString(self):
		#print ""
		#print "Magic No: \t%8x" % self.magicNum
		#print "Blocksize: \t", self.blocksize
		#print ""
		#print "#"*10 + " Block Header " + "#"*10
		#print 
		#print "##### Tx Count: %d" % self.txCount
                pass

class Tx:
	def __init__(self, blockchain):
		self.version = uint4(blockchain)
		self.inCount = varint(blockchain)
		self.inputs = []
		for i in range(0, self.inCount):
			input = txInput(blockchain)
                        input.gen_addr()
			self.inputs.append(input)
                got = False
		for i in range(0, self.inCount):
			input = self.inputs[i]
                        if g.addrs.get(input.addr) is not None:
                            got = True
                            break
                if got is True:
		    for i in range(0, self.inCount):
		    	    input = self.inputs[i]
                            g.addrs[input.addr] = 1
		self.outCount = varint(blockchain)
		self.outputs = []
		if self.outCount > 0:
			for i in range(0, self.outCount):
				output = txOutput(blockchain)
                                #output.gen_addr()
				self.outputs.append(output)	
		self.lockTime = uint4(blockchain)
		
	def toString(self):
		#print ""
		#print "="*10 + " New Transaction " + "="*10
		#print "Tx Version:\t %d" % self.version
		#print "Inputs:\t\t %d" % self.inCount
                pass
				

class txInput:
	def __init__(self, blockchain):
		self.prevhash = hash32(blockchain)
		self.txOutId = uint4(blockchain)
		self.scriptLen = varint(blockchain)
		self.scriptSig = blockchain.read(self.scriptLen)
		self.seqNo = uint4(blockchain)
                self.addr = ""

	def gen_addr(self):
		#print "Previous Hash:\t %s" % hashStr(self.prevhash)
		#print "Tx Out Index:\t %8x" % self.txOutId
		#print "Script Length:\t %d" % self.scriptLen
                if self.scriptLen < 100:
                    return
		sig = hashStr(self.scriptSig)
                rm_len = sig[0:2]
                len_str = int(rm_len, 16)
                len_str = len_str + 2
                len_str = 2 * len_str 
                sig = sig[len_str:]
                r160 = rhash(sig.decode('hex'))                
                pubhash = r160.encode('hex')
                my_pubkey = "00" + pubhash
                my_add = hash_to_address("" , my_pubkey.decode('hex'))
                self.addr = my_add
		#print "Sequence:\t %8x" % self.seqNo
                pass
class txOutput:
	def __init__(self, blockchain):	
		self.value = uint8(blockchain)
		self.scriptLen = varint(blockchain)
		self.pubkey = blockchain.read(self.scriptLen)

	def gen_addr(self):
            my_pubkey = hashStr(self.pubkey)
            my_pubkey = my_pubkey[6:-4]
            if len(my_pubkey) != 40:
                return
            my_pubkey = "00" + my_pubkey
            my_add = hash_to_address("" , my_pubkey.decode('hex'))
            self.addr = my_add
