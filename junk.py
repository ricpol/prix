# junk, provisional code
#----------------------------------------------------------------------

import sqlite3
from datetime import date, timedelta
import unicodedata
from collections import Counter
from difflib import SequenceMatcher

import credit as cr

def junk():
    import unidecode
    names = open('a.txt', 'r', encoding='utf8').read()
    names = unidecode.unidecode(names)
    names  = names.lower()
    with open('b.txt', 'a', encoding='utf8') as f:
        f.write(names)
    '''
    #con = sqlite3.connect('prix_winners.grist', detect_types=sqlite3.PARSE_COLNAMES)
    #c = con.cursor()
    old = open('oldcredits.txt', 'r', encoding='utf8').read().splitlines()
    new = open('newpers.txt', 'r', encoding='utf8').read().splitlines()
    errors = []
    for person1 in old:
        for person2 in new:
            if person1 != person2:
                if SequenceMatcher(None, person1, person2).quick_ratio() > 0.85:
                    errors.append(['OO ' + person1, 'NN ' + person2])
    with open('out.txt', 'a', encoding='utf8') as f:
        for a, b in errors:
            f.write(f'{a} | {b}\n')
    '''
if __name__ == '__main__':
    junk()
