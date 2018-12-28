#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 28 14:15:16 2018

@author: sammacorpy
"""


import os
from Crypto.Cipher import AES
from Crypto import Random
import codecs
#import argparse

def find_all_file_loc(outputkey):
    allfiles=[]
    with open(outputkey,'r') as f:
        enckey=bytes(f.readline(),'utf-8')
        ivlocfile = Random.new().read(AES.block_size)
        cipherlocfile = AES.new(keylocfile, AES.MODE_CFB, ivlocfile)
        deckey=cipherlocfile.decrypt(codecs.decode(enckey,"hex"))[len(ivlocfile):]
        allfiles= bytes.decode(deckey)
        allfiles=allfiles.split("|")[:-1]
   
    combine=[]

    for file in allfiles:
        with open(file,'r') as f: 
            filecontent=bytes(f.readline(),'utf-8')
            iv = Random.new().read(AES.block_size)
            cipherk = AES.new(key, AES.MODE_CFB, iv)
            decfilecont=cipherk.decrypt(codecs.decode(filecontent,"hex"))[len(iv):]
            fc=bytes.decode(decfilecont)
            combine.append(fc)
        os.remove(file)
    lencombine=len(combine)
    for i in range(lencombine):
        for j in range(i+1,lencombine):
            if(int(combine[i].split("|~|~|~|")[-1]) > int(combine[j].split("|~|~|~|")[-1])):
                combine[i],combine[j]=combine[j],combine[i]
    os.remove(outputkey)
    with open(outputkey,'w') as f:
        for i in combine:
            towr= i.split("|~|~|~|")[:-1]
            towr="|~|~|~|".join(towr)
            f.write(towr)
    print("File decrypted successfully :)")
        
    
if __name__ == "__main__":
    """PRIVATE_KEY="-k"
    PUBLIC_KEY="-p"
    FILE = "-f"
    DESCRIPTION="Program to decrypt the random bases decentralized encrypted file"
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument(PRIVATE_KEY, help="private key for decrypting each segment of decentralized files", type=str, dest="private")
    parser.add_argument(PUBLIC_KEY, help="public key for localizing each segment of decentralized files", dest="public")
    parser.add_argument(FILE, help="FILE to be decrypted", dest="file")
    main_args = parser.parse_args()
    if main_args.private and main_args.public:
        key=bytes(main_args.private,'utf-8')
        keylocfile=bytes(main_args.public,'utf-8')
        outputkey=main_args.file
        find_all_file_loc(outputkey)
    
    else:
        parser.print_help()"""
    key = bytes(input("key: "),'utf-8')
    keylocfile=bytes(input("lock key: "),'utf-8')
    
    outputkey=input("enter filename to decrypt: ")
    find_all_file_loc(outputkey)
    