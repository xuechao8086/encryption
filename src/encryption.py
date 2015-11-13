#!/usr/bin/env python2.7
#coding=utf8

"""
Author:         charliezhao
Filename:       encryption.py
Create Time:  2015-11-12 16:21
Description:
    encryption a filename
    decipher a filename
ToDo:
    it is too native too simple, update encryption wigh gpg
"""
from __future__ import print_function

# import hashlib
import os
import re
import struct
import sys
import fnmatch

class EncryptionFile(object):
    def __init__(self, filename):
        self.filename = filename
        self.begin = 0x20151112
        self.end = 0x11122015

    def encry_algorithm(self, val):
        """reverse uint8_t, then exchange the highest 4 bit and the lowest 4 bit""" 
        nval = 0
        for i in xrange(0, 8):
            if val & 0x1<<i:
                nval |= 0x1<<(7-i)
        
        # print("bin(nval) = {}".format(bin(nval)))
        nval = ((nval&0x0f)<<4) + ((nval&0xf0)>>4)
        # print("bin(nval) = {}".format(bin(nval)))
        return nval        

    def decipher_algorith(self, val):
        """reverse uint8_t, then exchange the highest 4 bit and the lowest 4 bit""" 
        nval= 0 
        for i in xrange(0, 8):
            if val & 0x1<<i:
                nval |= 0x1<<(7-i)
        
        nval = ((nval&0x0f)<<4) + ((nval&0xf0)>>4)
        return nval 
    
    def test(self):
        a = 0b10100001
        ena = self.encry_algorithm(a)
        print("a = {}".format(a))
        print("ena = {}".format(ena))            
        
        dea = self.decipher_algorith(ena)
        print("dea = {}".format(dea))
    

    def encry(self):
        encry_filename = "{}.enc".format(self.filename)
        
        assert os.access(self.filename, os.R_OK)
        with open(self.filename, 'rb') as f:
            content = f.read() # read always return str.
    
        nfd = open(encry_filename, 'wb')
        assert  nfd != -1
        
        # write magic head
        nfd.write(struct.pack("I", self.begin))
        
        # write len
        nfd.write(struct.pack("I", len(content)))

        for char in content:
            val = int(struct.unpack('B', char)[0])
            nval = self.encry_algorithm(val) 
            persist_nval = struct.pack('B', nval) 
            nfd.write(persist_nval)
        
        # write magic end
        nfd.write(struct.pack("I", self.end))
        
        nfd.close()

    def decipher(self):
        assert os.access(self.filename, os.R_OK)
        if not fnmatch.fnmatch(self.filename, "*.enc"):
            assert False
        decipher_filename =  re.split("\\.enc$", filename)[0]
        
        nfd = open(decipher_filename, "wb")

        with open(self.filename, 'rb') as f:
            begin = struct.unpack('I', f.read(4))[0]
            if begin != self.begin:
                assert False

            clen = struct.unpack('I', f.read(4))[0]
            
            for i in xrange(0, clen):
                content = f.read(1)
                if content:
                    val = struct.unpack('B', content)[0]
                    nval = self.decipher_algorith(val) 
                    persist_nval = struct.pack('B', nval)
                    nfd.write(persist_nval)                    
                    #print val
                else:
                    break

            end = struct.unpack('I', f.read(4))[0]
            if end != self.end:
                assert False
        nfd.close()
    
    def __del__(self):
        os.unlink(self.filename)

    def __call__(self):
        return self.encry()


def usage():
    print(sys.argv[0], "[e|d] [filename [filename [filename[...]]]]")
    print("\t\t e for encry")
    print("\t\t d for decipher")
    print("\t\t t for test")
    sys.exit()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        usage()

    if sys.argv[1] == 'e':
        for filename in sys.argv[2:]: 
            EncryptionFile(filename)()
    elif sys.argv[1] == 'd':
        for filename in sys.argv[2:]:
            EncryptionFile(filename).decipher()
    elif sys.argv[1] == 't':
        EncryptionFile("/tmp/charlie.dat").test()
    else:
        usage()
