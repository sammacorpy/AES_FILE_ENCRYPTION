#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 28 14:14:09 2018

@author: sammacorpy
"""

import os
from random import randint
import hashlib
rn=0
from Crypto.Cipher import AES
from Crypto import Random
import codecs
import uuid
import argparse



def split_encrypt(filename):
    rn=-1
    distributal=[]
    filecontent=""
    with open(filename,'r') as f:
        c=0
        for fc in f:
            if(rn==-1):
                rn=randint(5,20)
            if(rn==0):
                filecontent+="|~|~|~|"+str(c)
                iv = Random.new().read(AES.block_size)
                cipher = AES.new(key, AES.MODE_CFB, iv)
                msg = iv + cipher.encrypt(bytes(filecontent,'utf-8'))
                encodedstring = codecs.encode(msg,"hex")
                distributal.append(encodedstring)
                c+=1
                filecontent=""
                rn= randint(5,20)
            
            filecontent+=fc
            rn=rn-1
        if(len(filecontent)>0):
            filecontent+="|~|~|~|"+str(c)
            iv = Random.new().read(AES.block_size)
            cipher = AES.new(key, AES.MODE_CFB, iv)
            msg = iv + cipher.encrypt(bytes(filecontent,'utf-8'))
            encodedstring = codecs.encode(msg,"hex")
            distributal.append(encodedstring)
            c+=1
            filecontent=""
    #del distributal[0]
    
    for i in distributal:
        c=uuid.uuid4()
        with open("/home/sammacorpy/encrypted/"+str(c)+".txt",'w') as f:
            f.write(bytes.decode(i))
        
        
def add_signatures_and_move(loff,filename):
    ivlocfile = Random.new().read(AES.block_size)
    cipherlocfile = AES.new(keylocfile, AES.MODE_CFB, ivlocfile)
    
    loff=os.listdir("/home/sammacorpy/encrypted")
    destloc=""
    for fname in loff:
        mt = os.stat("/home/sammacorpy/encrypted/"+fname).st_mtime
        ct= os.stat("/home/sammacorpy/encrypted/"+fname).st_ctime
        uid = os.stat("/home/sammacorpy/encrypted/"+fname).st_uid
        size= os.stat("/home/sammacorpy/encrypted/"+fname).st_size
        h=hashlib.sha256(bytes(str(uuid.uuid4())+str(uid)+str(size)+str(ct)+str(mt),'utf-8')).hexdigest()
        rn=randint(0,10) #distribute file randonly  
        destloc+="/home/sammacorpy/distriburaltest/"+str(rn)+"/"+h+"."+fname.split(".")[1]+"|"
       
            
        os.rename("/home/sammacorpy/encrypted/"+fname,"/home/sammacorpy/distriburaltest/"+str(rn)+"/"+h+"."+fname.split(".")[1])
    os.remove(filename)
    with open(filename,'w') as f:
        enc=ivlocfile + cipherlocfile.encrypt(bytes(destloc,'utf-8'))
        f.write(bytes.decode(codecs.encode(enc,"hex"))) 
        print("File encrypted successfully :)")
    
if __name__ == "__main__":
    
    PRIVATE_KEY="-k"
    PUBLIC_KEY="-p"
    FILE = "-f"
    DESCRIPTION="Program to decentralize the segmented part of selected file with added encrypted security"
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument(PRIVATE_KEY, help="private key for encrypting each segment of decentralized files", type=str, dest="private")
    parser.add_argument(PUBLIC_KEY, help="public key for delocalizing each segment of decentralized files", dest="public")
    parser.add_argument(FILE, help="FILE to be encrypted", dest="file")
    main_args = parser.parse_args()
    if main_args.private and main_args.public:
        key=bytes(main_args.private,'utf-8')
        keylocfile=bytes(main_args.public,'utf-8')
        filename=main_args.file
        split_encrypt(filename)
        add_signatures_and_move([],filename)
    
    else:
        parser.print_help()
    #key = bytes(input("key: "),'utf-8')
    #keylocfile=bytes(input("lock key: "),'utf-8')
    #filename =input("enter file name: ")
    #split_encrypt(filename)
    #add_signatures_and_move([],filename)
    
    