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
import os
import re
import struct
import sys
import fnmatch

class EncryptionFile(object):
    def __init__(self, filename):
        self.filename = filename
    
    def encry_algorithm(self, val):
        """ to be done""" 
        pass

    def decipher_algorith(self, val):
        """ to be done"""
        pass

    def encry(self):
        encry_filename = "{}.enc".format(self.filename)
        
        assert os.access(self.filename, os.R_OK)
        with open(self.filename, 'rb') as f:
            content = f.read() # read always return str.
    
        nfd = open(encry_filename, 'wb')
        assert  nfd != -1

        for char in content:
            val = int(struct.unpack('B', char)[0])
            nval = ~val + 1
            persist_nval = struct.pack('i', nval) 
            # r = "char:{} val:{} type(val):{}  nval:{} type(nval):{}".format(char, val, type(val), nval, type(nval))
            # print(r) 
            # print  nval, persist_nval
            nfd.write(persist_nval)
        
        nfd.close()

    def decipher(self):
        assert os.access(self.filename, os.R_OK)
        if not fnmatch.fnmatch(self.filename, "*.enc"):
            assert False
        decipher_filename =  re.split("\\.enc$", filename)[0]
        
        nfd = open(decipher_filename, "wb")

        with open(self.filename, 'rb') as f:
            while True:
                content = f.read(4)
                if content:
                    val = struct.unpack('i', content)[0]
                    nval = ~(val - 1)
                    persist_nval = struct.pack('B', nval)
                    nfd.write(persist_nval)                    
                    #print val
                else:
                    break
        nfd.close()
    
    def __del__(self):
        os.unlink(self.filename)

    def __call__(self):
        return self.encry()


def usage():
    print sys.argv[0], "[e|d]" "[filename [filename [filename]]]"
    sys.exit()


if __name__ == '__main__':
    if len(sys.argv) < 3:
        usage()

    if sys.argv[1] == 'e':
        for filename in sys.argv[2:]: 
            EncryptionFile(filename)()
    elif sys.argv[1] == 'd':
        for filename in sys.argv[2:]:
            EncryptionFile(filename).decipher()
    else:
        usage()
