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

ROWWARN=''


def main():

    global ROWWARN
    
    emailfile = "../input/wggc_emails.csv"
    namesfile = "../input/wggc_names.csv"

    name_surname = []
    emails = []

    srnm_emails = {}
    emails_srnm = {}

    unmatched_names = []
    unmatched_emails = []

    ofile = open("../output/wggc_matched_emails.csv", 'w')
    
    with open(emailfile) as infile:
        csvr = csv.reader(infile, delimiter=',')
        for row in csvr:
            emails.append(row[2].lower())

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
                nm = row[kn].lower().replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue')
                srnm = row[ks].lower().replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue')
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
                    else:
                        tmpe = srnm_emails[nm_srnm][0]
                        nmsrnme = tmpe.split('@')[0].split('.')
                        if len(nmsrnme[0]) == 1:
                            if nm[0] != nmsrnme[0]:
                                print(f'* Please cross-check: matched "{nm_srnm}" with {tmpe}, "{nm}" initial does not match\n')
                                ROWWARN = "@CHECK@"
                        elif len(nmsrnme) > 1 or len(nmsrnme[0]) > 2+len(srnm):
                            if nm not in tmpe:
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
                print(f'* Please cross-check: matched "{srnm}" composed with {email}\n')
                ROWWARN = '@CHECK@'
                m +=1
    if m == 1:
        return True
    
    return False

if __name__=="__main__":
    main()
