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
import unidecode

def main():

    args = options()
    verbose = args.verbose

    if args.generate:
        uniqueids(args)

    if args.check:
        checkunique(args)

def checkunique(args):
    '''
    Check a list of IDs (from a csv file with args.key as corresponding column name) against a saved json list
    '''
    verbose = args.verbose
    mydel = args.delimiter
    mykey = args.key
    myids = []
    
    with open(args.jsonfilename, 'r') as infile:
        validid = json.load(infile)
        valididset = set(validid)

    with open(args.infilename, 'r') as infile:
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
                if verbose:
                    print(f'Checking that unique {header[k]} matches recognised values')
            else:
                myids.append(row[k])
            l += 1

    myidset = set(myids)

    # These are the ids that are not found among the valid ones
    notvalid = myidset - valididset
    print(f'These IDs are *not* valid: {", ".join(notvalid)}')

    
    # These are the valid IDs that are not in the input file
    missing = valididset - myidset
    print(f'These IDs are valid and missing in the input: {", ".join(missing)}')

    return 

def uniqueids(args):
    '''
    Read csv file
    '''
    verbose = args.verbose
    mydel = args.delimiter
    mykey = args.key
    pasteids = args.pasteids.split(';')
    idlen = int(args.lenghtid)
    skipentry = []
    updating = False

    try:
        tmpfile = open(args.infilename.replace('.csv', '_dict.json'), 'r')
        if verbose:
            print(f'A dictionary already exists: the previous IDs will be maintained and only new entries will be added')
        updating = True
        uniqueids = json.load(tmpfile)
    except:
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
                if verbose:
                    print(f'Assigning a unique identifier to {header[k]}')
                if len(pasteids[0]) > 0:
                    if verbose:
                        print(f'The unique identifier will also contain the fields: {", ".join(pasteids)}')
                    pasteids = [header.index(x) for x in pasteids]
                else:
                    pasteids = []
            else:
                if row[k] in uniqueids.keys():
                    if verbose:
                        print(f'***WARNING*** {header[k]} {row[k]} already has an ID, skipping!')
                    skipentry.append(l)
                else:
                    tmpid = '_'.join(getIDParts(row, pasteids, idlen))
                    while tmpid in uniqueids.values():
                        if verbose:
                            print(f'{tmpid} already used, re-generate')
                        tmpid = '_'.join(getIDParts(row, pasteids, idlen))
                    uniqueids[row[k]] = tmpid
            l += 1

    if updating:
        fname = args.infilename.replace('.csv', '_wIDs_new.csv').replace('/input/', '/output/')
    else:
        fname = args.infilename.replace('.csv', '_wIDs.csv').replace('/input/', '/output/')
        
    with open(args.infilename.replace('.csv', '_dict.json').replace('/input/', '/output/'), 'w') as ofile:
        json.dump(uniqueids, ofile)

    with open(args.infilename.replace('.csv', '_uniqueIDs.json').replace('/input/', '/output/'), 'w') as ofile:
        json.dump(list(uniqueids.values()), ofile)

    with open(fname, 'w') as ofile:
        with open(args.infilename) as infile:
            csvr = csv.reader(infile, delimiter=mydel)
            l = 0
            for row in csvr:
                if l < 1:
                    k = header.index(mykey)
                    row.append('UniqueID')
                else:
                    row.append(uniqueids[row[k]])
                if l not in skipentry:
                    ofile.write(f'{",".join(row)}\n')
                l+=1

    return

def getIDParts(mystr, compstr, mylen):
    '''
    Return a list of the strings that will compose the ID, starting from a set of pre-defined components (<compstr> list of indexes) and adding a random string of length <mylen>
    The German umlauts are replaced with the alternative writing, all other special letters are simplified by the unidecode function
    '''
    return filter(None, [''.join([unidecode.unidecode(mystr[x].replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue')) for x in compstr]).lower(),
                         ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(mylen))])

def options():
    '''in-line arguments read by the parser'''
    parser = argparse.ArgumentParser(description='Parsing options')
    parser.add_argument('-V', '--verbose', help='increase output verbosity', action='store_true')
    parser.add_argument('-G', '--generate', help='generate unique ids', action='store_true')
    parser.add_argument('-C', '--check', help='check unique ids against a record file', action='store_true')
    parser.add_argument('-i', '--infilename', help='Input file name', default='../input/test.csv')
    parser.add_argument('-o', '--outfilename', help='Output file name', default='../output/testids.json')
    parser.add_argument('-j', '--jsonfilename', help='Input json file name containing the accepted ids', default='../input/myids.json')
    parser.add_argument('-d', '--delimiter', help='Delimiter of the csv input file, by default ","', default=',')
    parser.add_argument('-p', '--pasteids', help='Labels that will be used to define the unique id, separated by ";". Can be left empty and the unique id will only be a random string', default='')
    parser.add_argument('-k', '--key', help='', default='email')
    parser.add_argument('-l', '--lenghtid', help='', default='6')
    args = parser.parse_args()
    if args.verbose:
        print('Verbosity ON')
        print(args)
    return args

if __name__=="__main__":
    main()
