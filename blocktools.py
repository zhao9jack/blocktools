from base58 import *
import struct
import base58
import Crypto.Hash.SHA256 as SHA256


def uint1(stream):
	return ord(stream.read(1))

def uint2(stream):
	return struct.unpack('H', stream.read(2))[0]

def uint4(stream):
	return struct.unpack('I', stream.read(4))[0]

def uint8(stream):
	return struct.unpack('Q', stream.read(8))[0]

def hash32(stream):
	return stream.read(32)[::-1]

def time(stream):
	time = uint4(stream)
	return time

def varint(stream):
	size = uint1(stream)

	if size < 0xfd:
		return size
	if size == 0xfd:
		return uint2(stream)
	if size == 0xfe:
		return uint4(stream)
	if size == 0xff:
		return uint8(stream)
	return -1

def hashStr(bytebuffer):
	return ''.join(('%02x'%ord(a)) for a in bytebuffer)

def sha256(s):
    return SHA256.new(s).digest()

def double_sha256(s):
    return sha256(sha256(s))


def hash_to_address(version, hash):
    vh = version + hash
    return base58.b58encode(vh + double_sha256(vh)[:4])
