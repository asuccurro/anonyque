#!/usr/bin/python3
#**************************************
#**    author: Antonella Succurro    **
#**email:asuccurro[AT]protonmail.com **
#**                                  **
#**    created:       2019/02/05     **
#**    last modified: 2019/02/05     **
#************************************

import json
import argparse
import csv
import random
import string

def main():
    args = options()
    verbose = args.verbose
    mydel = args.delimiter
    mykey = args.key
    pasteids = args.pasteids.split(';')
    idlen = int(args.lenghtid)

    uniqueids = {}
    with open(args.infilename) as infile:
        csvr = csv.reader(infile, delimiter=mydel)
        l = 0
        for row in csvr:
            if l < 1:
                header = row
                try:
                    k = header.index(mykey)
                except:
                    print(f'{mykey} is not in the column names, fix the input or choose a new key among: {", ".join(header)}')
                    return
                print(f'Assigning a unique identifier to {header[k]}')
                if len(pasteids[0]) > 0:
                    print(f'The unique identifier will also contain the fields: {", ".join(pasteids)}')
                    pasteids = [header.index(x) for x in pasteids]
                else:
                    pasteids = []
            else:
                tmpid = ''.join([row[x] for x in pasteids]).lower()+''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(idlen))
                while tmpid in uniqueids.values():
                    print(f'{tmpid} already used, re-generate')
                    tmpid = ''.join([row[x] for x in pasteids]).lower()+''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(idlen))
                uniqueids[row[k]] = tmpid
            l += 1
        print(uniqueids)
            
                    
def options():
    '''in-line arguments read by the parser'''
    parser = argparse.ArgumentParser(description='Parsing options')
    parser.add_argument('-V', '--verbose', help='increase output verbosity', action='store_true')
    parser.add_argument('-i', '--infilename', help='', default='../input/test.csv')
    parser.add_argument('-d', '--delimiter', help='', default=',')
    parser.add_argument('-p', '--pasteids', help='', default='')
    parser.add_argument('-k', '--key', help='', default='email')
    parser.add_argument('-l', '--lenghtid', help='', default='6')
    args = parser.parse_args()
    if args.verbose:
        print('Verbosity ON')
        print(args)
    return args

if __name__=="__main__":
    main()
