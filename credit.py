from glossary import (ROLES, ROLES_SINGULAR, ROLES_PLURAL, 
                      role_singular2plural, role_plural2singular)

def unpack(component): # str -> list
    # unpacks a single component (roles or persons)
    return [i.strip(' .:') for i in component.split(',')]

def pack(component): # list -> str
    # packs a single component (roles or persons)
    # omits the trailing ":" or ".", so that pack(unpack(x)) != x
    return ', '.join([i.strip() for i in component])

def unpack_credit(credit): # str -> list
    # unpacks a single credit (role, role: person, person.)
    if not credit:
        return [[''], ['']]
    if credit == '_null':
        return [['_null'], ['_null']]
    roles, persons = credit.split(':')
    roles = unpack(roles)
    persons = unpack(persons)
    return [roles, persons]

def pack_credit(credit): # list -> str
    # packs a single credit (role, role: person, person.)
    # must be pack_credit(unpack_credit(x)) == x
    if credit == [[''], ['']]:
        return ''
    if credit == [['_null'], ['_null']]:
        return '_null'
    roles, persons = credit
    roles = pack(roles)
    persons = pack(persons)
    return f'{roles}: {persons}.'

def unpack_creditlist(creditlist): # str -> list
    # unpacks the credit list for a programme (credit. credit.)
    return [unpack_credit(i) for i in creditlist.split('.')]

def pack_creditlist(creditlist): # list -> str
    # packs the credit list for a programme (credit. credit.)
    # must be pack_creditlist(unpack_creditlist(x)) == x
    return ' '.join([pack_credit(c) for c in creditlist]).strip()

def unpack_allcredits(allcredits): # multiline str -> list
    # unpacks the entire credits from the database
    return [unpack_creditlist(i) for i in allcredits.splitlines()]

def pack_allcredits(allcredits): # list -> multiline str
    # packs the entire credits from the database
    # must be pack_allcredits(unpack_allcredits(x)) == x
    return '\n'.join([pack_creditlist(i) for i in allcredits])


# ------------------------------------------------------------------------------
# checks

from difflib import SequenceMatcher

def check_similar_persons(all_credits):
    # accepts an already unpacked list of credits
    persons = enumerate_persons(all_credits)
    errors = []
    for n, person1 in enumerate(persons):
        for person2 in persons[n+1:]:
            if SequenceMatcher(None, person1, person2).quick_ratio() > 0.85:
                errors.append([person1, person2])
    return errors


# ------------------------------------------------------------------------------
# enumerations
# (naive enumerations! In fact, the same programme can be listed twice, and 
# the same role/person can be listed twice in the same programme)

from collections import Counter

def enumerate_roles(all_credits):
    # accepts an already unpacked list of credits
    bag = []
    for creditline in all_credits:
        for roles, persons in creditline:
            for role in roles:
                bag.append(role)
    return Counter(bag)


def enumerate_persons(all_credits):
    # accepts an already unpacked list of credits
    bag = set()
    for creditline in all_credits:
        for roles, persons in creditline:
            for person in persons:
                bag.add(person)
    return sorted(list(bag))


# ------------------------------------------------------------------------------
#  credit roles and persons replacement
#  note: this work ONLY with separate text files, as a safety measure: 
#  the workflow is: 1) copy all credits (from Grist interface) to a credit_list.txt 
#  file; 2) run_credit_replace() will output an out.txt; 3) run a diff between the 
#  two files to ensure that only the wanted changes have been produced; 4) paste 
#  back the result into the Gris interface (assuming you don't have changed the 
#  sorting in the meantime!).


def run_credit_replace(roles_or_persons):
    with open('credit_list.txt', 'r', encoding='utf8') as f:
        db_credits = f.read()
    credits = unpack_allcredits(db_credits)
    if roles_or_persons == 'roles':
        new_credits = roles_replace(credits)
    elif roles_or_persons == 'persons':
        new_credits = persons_replace(credits)
    else:
        raise TypeError
    assert len(credits) == len(new_credits)
    for n, o in zip(credits, new_credits):
        assert len(n) == len(o)
    with open('out.txt', 'a', encoding='utf8') as f:
        f.write(pack_allcredits(new_credits))


def roles_replace(all_credits):
    # accepts an already unpacked list of credits
    new_all_credits = []
    for creditline in all_credits:
        new_creditline = []
        for credit in creditline:
            roles, persons = credit
            new_roles = []
            for role in roles:
                new_role = _custom_replace(role)
                new_roles.append(new_role)
            new_credit = [new_roles, persons]
            new_creditline.append(new_credit)
        new_all_credits.append(new_creditline)
    return new_all_credits


def persons_replace(all_credits):
    # accepts an already unpacked list of credits
    new_all_credits = []
    for creditline in all_credits:
        new_creditline = []
        for credit in creditline:
            roles, persons = credit
            new_persons = []
            for person in persons:
                new_person = _custom_replace(person)
                new_persons.append(new_person)
            new_credit = [roles, new_persons]
            new_creditline.append(new_credit)
        new_all_credits.append(new_creditline)
    return new_all_credits


def _custom_replace(s):
    if s == '': s = ''
    elif s == '': s = ''    
    return s


# ------------------------------------------------------------------------------
#  utilities

def credit2persons(credits):
    '''Convert a credit list into a (tentative) person list.
       Input: multiline str (id \\t creditlist)
       Output: multiline str (name \\t surname \\t surname_ord \\t role \\t id)
    '''
    out = ''
    for credit in credits.splitlines():
        id_, credit = credit.split('\t')
        credit = unpack_creditlist(credit)
        for roles, persons in credit:
            for person in persons:
                try: 
                    name, surname = person.split(' ', maxsplit=1)
                except ValueError:
                    name = ''
                    surname = person
                # careful! we don't strip non-ASCII chars
                surname_ord = surname.lower() + ' ' + name.lower()
                for role in roles:
                    if role not in ROLES_SINGULAR:
                        role = ROLES_SINGULAR[ROLES_PLURAL.index(role)]
                    out += f'{name}\t{surname}\t{surname_ord}\t{role}\t{id_}\n'
    return out

#  SINGULAR/PLURAL ROLES FIXING: "Director: foo, bar." -> "DirectorS: foo, bar." etc.
#  note: this work ONLY with separate text files, as a safety measure: 
#  the workflow is: 1) copy all credits (from Grist interface) to a credit_list.txt 
#  file; 2) fix_plurals() will output an out.txt; 3) run a diff between the 
#  two files to ensure that only the wanted changes have been produced; 4) mostly, 
#  DOUBLE CHECK corner cases like "dancer/s", "participant/s" and collective names; 
#  5) paste back the result into the Grist interface (assuming you don't have changed 
#  the sorting in the meantime!).

def fix_credit_plurals(credit):
    # accepts an already unpacked credit (not a credit list!)
    singular = len(credit[1]) == 1
    new_credit = [[], credit[1][:]]
    for role in credit[0]:
        if singular:
            new_credit[0].append(role_plural2singular(role))
        else:
            new_credit[0].append(role_singular2plural(role))
    return new_credit

def fix_allcredits_plural(all_credits):
    # accepts an unpacked all-creditlists database
    new_credits = []
    for creditlist in all_credits:
        new_creditlist = []
        for credit in creditlist:
            new_creditlist.append(fix_credit_plurals(credit))
        new_credits.append(new_creditlist)
    return new_credits

def fix_plurals():
    with open('credit_list.txt', 'r', encoding='utf8') as f:
        db_credits = f.read()
    credits = unpack_allcredits(db_credits)
    new_credits = fix_allcredits_plural(credits)
    assert len(credits) == len(new_credits)
    for n, o in zip(credits, new_credits):
        assert len(n) == len(o)
    with open('out.txt', 'a', encoding='utf8') as f:
        f.write(pack_allcredits(new_credits))

# ------------------------------------------------------------------------------
#  test for credit packing/unpacking

def test_pack():
    t = ('Mark, Mike', 'Mark', '', '_null')
    for i in t:
        assert pack(unpack(i)) == i
    t = ('Script: Mark, Mike.', 'Text, Script: Mark.', '', '_null')
    for i in t:
        assert pack_credit(unpack_credit(i)) == i
    t = ('Script: Mark, Mike. Text, Script: Mark.', '', '_null')
    for i in t:
        assert pack_creditlist(unpack_creditlist(i)) == i

