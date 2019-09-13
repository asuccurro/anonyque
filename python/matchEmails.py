#!/usr/bin/python3
#**************************************
#**    author: Antonella Succurro    **
#**email:asuccurro[AT]protonmail.com **
#**                                  **
#**    created:       2019/02/05     **
#**    last modified: 2019/02/25     **
#************************************

import json
import argparse
import csv
import random
import string
import unidecode

ROWWARN=''
VERBOSITY=1

def main():
    '''
    Match names listed in the csv file "namesfile" (with columns Surname,Title,Firstname, index not hardcoded), with emails listed in the csv file "emailfile"
    Runs without arguments, change the input/output file names directly in the code:
    * emailfile
    * namesfile
    * ofile
    '''

    global ROWWARN
    
    #emailfile = "../../contacts/emails.csv"
    #namesfile = "../../contacts/names.csv"
    #emailfile = "../../contacts/emails_20190906.csv"
    #namesfile = "../../contacts/names_20190906.csv"
    emailfile = "../../contacts/emails_20190913.csv"
    namesfile = "../../contacts/names_20190913.csv"

    name_surname = []
    emails = []

    srnm_emails = {}
    emails_srnm = {}

    unmatched_names = []
    unmatched_emails = []

    #ofile = open("../../contacts/matched_emails.csv", 'w')
    #ofile = open("../../contacts/matched_emails_20190906.csv", 'w')
    ofile = open("../../contacts/matched_emails_20190913.csv", 'w')
    
    with open(emailfile) as infile:
        csvr = csv.reader(infile, delimiter=',')
        l = 0
        for row in csvr:
            if l < 1:
                k = row.index("Email")
            else:
                emails.append(row[k].lower())
            l+=1

    with open(namesfile) as infile:
        csvr = csv.reader(infile, delimiter=',')
        l=0
        for row in csvr:
            if l < 1:
                ks = row.index("Surname")
                kn = row.index("Name")
                row.append("email")
                ofile.write(f'{",".join(row)}\n')
            else:
                ROWWARN=''
                nm = row[kn].lower().replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue').replace(' ','-')
                srnm = row[ks].lower().replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue').replace(' ','-')
                nm_srnm = f'{nm}_{srnm}'
                if nm_srnm in name_surname:
                    print(f'***WARNING*** {nm_srnm} is duplicated! Quitting.\n')
                    return
                else:
                    name_surname.append(nm_srnm)
                    match = 0
                    for e in emails:
                        if srnm in e:
                            match+=1
                            if srnm_emails.get(nm_srnm, False):
                                srnm_emails[nm_srnm].append(e)
                            else:
                                srnm_emails[nm_srnm] = [e]
                            if emails_srnm.get(e, False):
                                emails_srnm[e].append(nm_srnm)
                            else:
                                emails_srnm[e] = [nm_srnm]
                        # elif len(srnm.split('-')) > 1:
                        #     tbmtc = len(srnm.split('-'))
                        #     mtc = 0
                        #     for srnms in srnm.split('-'):
                        #         if srnms in e:
                        #             mtc+=1
                        #     if mtc > tbmtc/2.:
                        #         match+=1
                        #         if srnm_emails.get(nm_srnm, False):
                        #             srnm_emails[nm_srnm].append(e)
                        #         else:
                        #             srnm_emails[nm_srnm] = [e]
                        #         if emails_srnm.get(e, False):
                        #             emails_srnm[e].append(nm_srnm)
                        #         else:
                        #             emails_srnm[e] = [nm_srnm]
                                
                    if match < 1:
                        rematch = 0
                        for e in emails:
                            if tryMatchSep(' ', srnm, e):
                                rematch += 1
                                row.append(e)
                            if tryMatchSep('-', srnm, e):
                                rematch += 1
                                row.append(e)
                            if rematch < 1 and tryMatchRed(srnm, e):
                                rematch += 1
                                row.append(e)
                        if rematch == 1:
                            ofile.write(f'{ROWWARN}{",".join(row)}\n')
                            emails_srnm[row[-1]] = [nm_srnm]
                        else:
                            unmatched_names.append(nm_srnm)
                    elif match > 1:
                        rematch = 0
                        for e in srnm_emails[nm_srnm]:
                            if nm in e:
                                rematch += 1
                                row.append(e)
                        if rematch == 1:
                            ofile.write(f'{ROWWARN}{",".join(row)}\n')
                            emails_srnm[row[-1]] = [nm_srnm]
                        else:
                            print(f'***WARNING*** {nm_srnm} matches more emails and could not univocally match name and surname\n')
                            print(srnm_emails[nm_srnm])
                        ### TO DO: fix case when mail is duplicated! example: ['andreas.weber@uni-duesseldorf.de', 'aweber@hhu.de'] are the same person: andreas_weber
                        ### but there is no warning about aweber@hhu.de being removed from list
                    else:
                        tmpe = srnm_emails[nm_srnm][0]
                        nmsrnme = tmpe.split('@')[0].split('.')
                        if len(nmsrnme[0]) == 1:
                            if nm[0] != nmsrnme[0]:
                                if VERBOSITY > 0:
                                    print(f'* Please cross-check: matched "{nm_srnm}" with {tmpe}, "{nm}" initial does not match\n')
                                ROWWARN = "@CHECK@"
                        elif len(nmsrnme) > 1 or len(nmsrnme[0]) > 2+len(srnm):
                            if nm not in tmpe:
                                if VERBOSITY > 0:
                                    print(f'* Please cross-check: matched "{nm_srnm}" with {tmpe}, "{nm}" does not match\n')
                                ROWWARN = "@CHECK@"
                        row.append(tmpe)
                        ofile.write(f'{ROWWARN}{",".join(row)}\n')
            l +=1 

    ofile.close()

    if len(unmatched_names) > 0:
        strunmt="\n\t".join(unmatched_names)
        print(f'***WARNING*** these names did not match any email:\n\t{strunmt}\n')
    else:
        print(f'* All names were matched to emails :)')


    for e in emails:
        if not emails_srnm.get(e, False):
            unmatched_emails.append(e)
        # if emails_srnm.get(e, False):
        #     if len(emails_srnm[e]) > 1:
        #         print(f'***WARNING*** {e} matches more names')
        #         print(emails_srnm[e])
        # else:
        #     print(f'***WARNING*** {e} does not match any name')

    print("\n")

    if len(unmatched_emails) > 0:
        strunmt="\n\t".join(unmatched_emails)
        print(f'***WARNING*** these emails did not match any name:\n\t{strunmt}\n')
    
    return

def tryMatchRed(srnm, email):
    global ROWWARN
    if len(srnm) > 7:
        if srnm[:7] in email:
            if VERBOSITY > 0:
                print(f'* Please cross-check: matched "{srnm}" abbreviated with {email}\n')
            ROWWARN = '@CHECK@'
            return True
    return False

def tryMatchSep(sep, srnm, email):
    global ROWWARN
    sn = srnm.split(sep)
    m = 0
    for s in sn:
        if len(s) > 3:
            if s in email:
                if VERBOSITY > 0:
                    print(f'* Please cross-check: matched "{srnm}" composed with {email}\n')
                ROWWARN = '@CHECK@'
                m +=1
    if m >= 1:
        return True
    
    return False

if __name__=="__main__":
    main()
