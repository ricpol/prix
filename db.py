# routine for preparing the db for release, export data, various tests.
#----------------------------------------------------------------------

import sqlite3
import json
from datetime import date, timedelta
import unicodedata 
import string

def prepare_db(db="prix_winners.grist"):
    """Prepare the original Grist sqlite dump for release."""
    con = sqlite3.connect(db)
    c = con.cursor()
    try:
        c.execute('SELECT 1 FROM vPrixWinners;')
        return
    except:
        pass

    # fix prev/next in Broadcasters table
    c.execute('ALTER TABLE broadcasters ADD COLUMN prev_acro2 TEXT;')
    c.execute('ALTER TABLE broadcasters ADD COLUMN next_acro2 TEXT;')
    broadcasters = c.execute('SELECT id, id_acro FROM broadcasters;').fetchall()
    broadcasters = dict(broadcasters)
    c.execute('SELECT id, prev, next FROM broadcasters;')
    for id, prev, next in c.fetchall():
        if prev:  # "no value" could be either None or "[]"
            prev = [broadcasters[i] for i in json.loads(prev)]
            prev = json.dumps(prev) if prev else None
        if next:  # "no value" could be either None or "[]"
            next = [broadcasters[i] for i in json.loads(next)]
            next = json.dumps(next) if next else None
        c.execute('''UPDATE broadcasters SET prev_acro2=?, next_acro2=?
                     WHERE id=?;''', (prev, next, id))

    # fix start/end date in Editions table
    c.execute('ALTER TABLE Editions ADD COLUMN iso_startdate DATE;')
    c.execute('ALTER TABLE Editions ADD COLUMN iso_enddate DATE;')
    editions = c.execute('SELECT id, startdate, enddate FROM editions;').fetchall()
    for id, start, end in editions:
        if start:
            # (Python doesn't handle negative timestamps?! investigate...)
            start = date(1970, 1, 1) + timedelta(seconds=start)
            end = date(1970, 1, 1) + timedelta(seconds=end)
        c.execute('''UPDATE editions set iso_startdate=?, iso_enddate=? 
                     WHERE id=?;''', (start, end, id))

    # rename old tables
    c.execute('ALTER TABLE Broadcasters RENAME TO oBroadcasters')
    c.execute('ALTER TABLE Countries RENAME TO oCountries')
    c.execute('ALTER TABLE Editions RENAME TO oEditions')
    c.execute('ALTER TABLE Participants RENAME TO oParticipants')
    c.execute('ALTER TABLE Prizes RENAME TO oPrizes')
    c.execute('ALTER TABLE Winners RENAME TO oWinners')
    c.execute('ALTER TABLE Persons RENAME TO oPersons')
    c.execute('ALTER TABLE Bibliography RENAME TO oBibliography')
    c.execute('ALTER TABLE Milestones RENAME TO oMilestones')
    c.execute('ALTER TABLE Genius RENAME TO oGenius')
    c.execute('ALTER TABLE Globals RENAME TO oGlobals')

    # create new tables
    c.execute('''CREATE TABLE broadcasters AS
                 SELECT id_acro AS id, acronym, name, acr_name, status, 
                 ocountries.country, first, last, prev_acro2 AS prev, 
                 next_acro2 AS next, group_acronym, obroadcasters.note 
                 FROM obroadcasters 
                 JOIN ocountries ON obroadcasters.country=ocountries.id 
                 ORDER BY ocountries.sort, status DESC, first;''')
    c.execute('CREATE UNIQUE INDEX broadcasters_id ON broadcasters (id);')
    c.execute('''CREATE TABLE countries AS 
                 SELECT country, country_abbr, former, iso3166, region, 
                 subregion, sort, note 
                 FROM ocountries 
                 ORDER BY sort;''')
    c.execute('CREATE UNIQUE INDEX countries_country ON countries (country);')
    c.execute('CREATE UNIQUE INDEX countries_country_abbr ON countries (country_abbr);')
    c.execute('''CREATE TABLE editions AS
                 SELECT year, city, iso_startdate AS startdate, 
                 iso_enddate AS enddate, president, secretary, 
                 radio, tv, web, special, radio_sp, tv_sp, web_sp, radio_cat_max, 
                 radio_max, tv_cat_max, tv_max, web_cat_max, web_max, edition_max, 
                 catalogue_notes AS note
                 FROM oeditions 
                 ORDER BY year;''')
    c.execute('CREATE UNIQUE INDEX editions_year ON editions (year);')
    c.execute('''CREATE TABLE participants AS
                 SELECT id_part AS id, oeditions.year, 
                 obroadcasters.id_acro AS broadcaster_id, 
                 oparticipants.radio, oparticipants.tv, oparticipants.web, 
                 oparticipants.sp_prize 
                 FROM oparticipants 
                 JOIN oeditions ON oparticipants.edition=oeditions.id 
                 JOIN obroadcasters ON oparticipants.broadcaster=obroadcasters.id
                 JOIN ocountries ON obroadcasters.country=ocountries.id
                 ORDER BY oeditions.year, ocountries.sort, obroadcasters.status DESC, 
                 obroadcasters.first;''')
    c.execute('CREATE UNIQUE INDEX participants_id ON participants (id);')
    c.execute('''CREATE TABLE prizes AS
                 SELECT id_prize AS id, prize, prize_abbr, target, kind, operation, 
                 present, first_year
                 FROM oprizes 
                 ORDER BY first_year, kind, target;''')
    c.execute('CREATE UNIQUE INDEX prizes_id ON prizes (id);')
    c.execute('''CREATE TABLE winners AS
                 SELECT id2 AS id, orig_id AS prog_id, oeditions.year, ordering AS sort, 
                 obroadcasters.id_acro AS broadcaster_id, or_title, lang_title, 
                 rom_title, en_title, cat_title, credits, weblink, program_type, 
                 oprizes.id_prize AS prize_id, result, exaequo, reasoning, 
                 owinners.notes AS note
                 FROM owinners 
                 JOIN obroadcasters ON owinners.broadcaster=obroadcasters.id 
                 JOIN oeditions ON owinners.year=oeditions.id
                 JOIN oprizes ON owinners.prize_id=oprizes.id
                 ORDER BY oeditions.year, ordering;''')
    c.execute('CREATE UNIQUE INDEX winners_id ON winners (id);')
    c.execute('''CREATE TABLE persons AS
                 SELECT id, disamb, name, surname, surname_ord, sfirst, role, 
                 gristHelper_Display AS programme_id 
                 FROM oPersons 
                 ORDER BY surname_ord, disamb, programme_id, role;''')
    c.execute('CREATE UNIQUE INDEX persons_id ON persons (id);')
    c.execute('''CREATE TABLE bibliography AS 
                 SELECT id, edition, sort, category, author, title, notes, 
                 publisher, year 
                 FROM oBibliography 
                 WHERE provisional=0 
                 ORDER BY edition, sort;''')
    c.execute('CREATE UNIQUE INDEX bibliography_id ON bibliography (id);')
    c.execute('''CREATE TABLE milestones AS
                 SELECT year, milestone FROM oMilestones 
                 ORDER BY year;''')
    c.execute('CREATE UNIQUE INDEX milestones_year ON milestones (year);')
    c.execute('''CREATE TABLE genius AS
                 SELECT year, full_name, surname, description FROM oGenius 
                 WHERE year!=0 
                 ORDER BY year, surname;''')
    c.execute('''CREATE TABLE globals AS
                 SELECT globkey, globvalue, note FROM oGlobals 
                 ORDER BY sort;''')

    # create some other useful views
    c.execute('''CREATE VIEW vPrixWinners AS
                 SELECT winners.id, prog_id, winners.year, editions.city, 
                 winners.sort, broadcaster_id, broadcasters.acronym, 
                 broadcasters.name, broadcasters.acr_name, countries.country, 
                 countries.country_abbr, countries.iso3166, or_title, lang_title, 
                 rom_title, en_title, cat_title, credits, weblink, program_type, 
                 prizes.id AS prize_id, prizes.prize, prizes.prize_abbr, 
                 prizes.kind, result, exaequo, reasoning, winners.note
                 FROM winners 
                 JOIN broadcasters ON winners.broadcaster_id=broadcasters.id 
                 JOIN countries ON broadcasters.country=countries.country 
                 JOIN editions ON winners.year=editions.year
                 JOIN prizes ON winners.prize_id=prizes.id
                 ORDER BY winners.year, winners.sort;''')
    c.execute('''CREATE VIEW vPrixParticipants AS
                 SELECT participants.id, participants.year, 
                 broadcasters.id AS broadcaster_id, 
                 broadcasters.acronym, broadcasters.name, broadcasters.acr_name, 
                 countries.country, countries.country_abbr,  
                 participants.radio, participants.tv, participants.web, 
                 participants.sp_prize 
                 FROM participants 
                 JOIN editions ON participants.year=editions.year 
                 JOIN broadcasters ON participants.broadcaster_id=broadcasters.id
                 JOIN countries ON broadcasters.country=countries.country
                 ORDER BY participants.year, countries.sort, broadcasters.status DESC, 
                 broadcasters.first;''')
    c.execute('''CREATE VIEW vPrixPersons AS
                 SELECT persons.id, disamb, persons.name, surname, surname_ord, sfirst, role, 
                 programme_id, year, broadcasters.id AS id_acronym, acronym, country, 
                 group_concat(result) AS result  
                 FROM persons 
                 JOIN winners ON programme_id=prog_id 
                 JOIN broadcasters ON winners.broadcaster_id=broadcasters.id 
                 GROUP BY persons.id, disamb, persons.name, surname, surname_ord, sfirst, role, 
                 programme_id, year, acronym, country 
                 ORDER BY surname_ord, disamb, year, acronym, programme_id, role;''')
    # drop unnecessary tables
    tables = c.execute('PRAGMA TABLE_LIST').fetchall()
    for schema, name, type_, ncol, wr, strict in tables:
        if name.startswith('_grist') or name.startswith('o'):
            c.execute(f'DROP TABLE {name};')

    con.commit()
    c.execute('VACUUM;')
    con.close()



# ------------------------------------------------------------------------------
# data dump

import csv

def export_csv(view, dbcursor):
    """Export a single db view as csv file.
       Pass the view name and the cursor object of an open connection."""
    with open(f'prixitalia_{view}.csv', 'a', encoding='utf8', newline='') as output:
        writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL)
        dbcursor.execute(f'SELECT * FROM {view};')
        row = [i[0] for i in dbcursor.description]
        writer.writerow(row)
        for row in dbcursor.fetchall():
            writer.writerow(row)

def export_json(view, dbcursor): 
    """Export a single db view as json file.
       Pass the view name and the cursor object of an open connection."""
    with open(f'prixitalia_{view}.json', 'a', encoding='utf8', newline='') as output:
        dbcursor.execute(f'SELECT * FROM {view};')
        json.dump(dbcursor.fetchall(), output, ensure_ascii=False, indent=2)


def _sqlite_dict_row_factory(cursor, row):
    fields = [i[0] for i in cursor.description]
    return {key: value for key, value in zip(fields, row)}

views = ('broadcasters', 'countries', 'editions', 'participants', 'prizes', 
         'winners', 'persons', 'bibliography', 'genius', 'globals', 
         'vPrixWinners', 'vPrixParticipants', 'vPrixPersons')

def export_all(db="prix_winners.grist", views=views, export_as='json'):
    """Export data in csv and json format."""
    con = sqlite3.connect(db)
    c = con.cursor()
    if export_as == 'csv':
        for view in views:
            export_csv(view, c)
    elif export_as == 'json':
        c.row_factory = _sqlite_dict_row_factory
        for view in views:
            export_json(view, c)
    con.close()

# ------------------------------------------------------------------------------
#tests

'''
TODO -> make exceptions for the following failing tests:
! JRTV wins in 2013 without participating.
! EPTV wins in 2013 without participating.
! CPB/NPR wins in 1998 without participating.
! vWinners: 78, check syntax for Soldier, Soldier....
! vWinners: 78, check syntax for Soldier, Soldier....
! vWinners: 151, check syntax for  חוגה: יומו של אסיר [Chvgh: yvmv shl sr].
! vWinners: 216, check syntax for The World of J.K..
! vWinners: 216, check syntax for The World of J.K..
! vWinners: 429, check syntax for Det ondes problem etc..
! vWinners: 429, check syntax for The Problem of Evil Etc..
! vWinners: 1140, check syntax for Annie M. G..
! vWinners: 1140, check syntax for Annie M. G..
! vWinners: 1161, check syntax for Annie M. G..
! vWinners: 1161, check syntax for Annie M. G..
! vWinners: 1324, check syntax for Disappeared - The M.P.U..
'''

import sys
from collections import Counter
import credit as cr
from glossary import *

unique_colums = (
    ('broadcasters', 'id'), 
    ('countries', 'country'), 
    # ('vCountries', 'country_abbr'),
    ('countries', 'sort'), 
    ('editions', 'year'),
    ('participants', 'id'),
    ('prizes', 'id'),
    ('winners', 'id'),
    ('milestones', 'year'),
    )

def test_unique_columns(cursor, output):
    '''Make sure unique columns are really unique in all our views.'''
    errors = False
    for table, column in unique_colums:
        vals = cursor.execute(f'SELECT {column} FROM {table};')
        vals = Counter([i[0] for i in cursor.fetchall()])
        for i, n in vals.items():
            if n > 1:
                output.write(f'! {table}.{column}: "{i}" is not unique.\n')
                errors = True
    if not errors:
        output.write(f'  all unique columns are ok.\n')
    return not errors

def test_edition_dates(cursor, output):
    '''Check for basic coherence in edition start/end dates.'''
    errors = False
    cursor.execute('''SELECT year, startdate AS "startdate [date]", 
                      enddate AS "enddate [date]" FROM editions;''')
    for year, start, end in cursor.fetchall():
        if start:
            if start.year != year:
                output.write(f'! editions: {start} year should be {year}.\n')
                errors = True
            if end.year != year:
                output.write(f'! editions: {end} year should be {year}.\n')
                errors = True
            if timedelta(days=1) > (end - start) > timedelta(days=20):
                output.write(f'! editions: check {year} start/end date.\n')
                errors = True
    if not errors:
        output.write('  editions: edition dates ok.\n')
    return not errors

def test_edition_max(cursor, output):
    '''A basic check on the max programmes allowed.'''
    errors = False
    cursor.execute('SELECT year, radio_max, tv_max, web_max, edition_max FROM editions;')
    for year, radio_max, tv_max, web_max, edition_max in cursor.fetchall():
        max_progr = radio_max + tv_max + web_max
        if max_progr != edition_max:
            output.write(f'! editions: {year} max should be {max_progr}, not {edition_max}.\n')
            errors = True
    if not errors:
        output.write('  editions: edition max programmes ok.\n')
    return not errors

def test_broadcaster_chain(cursor, output):
    '''Check the start/end dates of chained broadcasters.'''
    errors = False
    cursor.execute('SELECT id, first, last, prev, next FROM broadcasters;')
    broadcasters = cursor.fetchall()
    broadc_first = {id:first for id, first, last, prev, next in broadcasters}
    broadc_last = {id:last for id, first, last, prev, next in broadcasters}
    for id, first, last, prev, next in broadcasters:
        if first > last:
            output.write(f'! broadcasters: {id} first date before last.\n')
            errors = True
        if prev:
            for p in json.loads(prev):
                if broadc_last[p] >= first:
                    output.write(f'! broadcasters: {p} should come before {id}.\n')
                    errors = True
        if next:
            for n in json.loads(next):
                if broadc_first[n] <= last:
                    output.write(f'! broadcasters: {n} should come after {id}.\n')
                    errors = True
    if not errors:
        output.write('  broadcasters: broadcaster chains ok.\n')
    return not errors

def test_participant_year(cursor, output):
    '''A broadcaster should participate only in its active years.'''
    errors = False
    cursor.execute('SELECT id, first, last FROM broadcasters;')
    broadcasters = {id:(first, last) for id, first, last in cursor.fetchall()}
    cursor.execute('SELECT id, year, broadcaster_id FROM participants;')
    for id, year, broadcaster in cursor.fetchall():
        if broadcasters[broadcaster][0] >= year >= broadcasters[broadcaster][1]:
            output.write(f'! participants: {id} year is off range.\n')
            errors = True
    if not errors:
        output.write('  participants: participation years ok.\n')
    return not errors

def test_participant_competition(cursor, output):
    # write a test to find anomalies in participation
    # (eg, a radio broadcaster competing in tv)
    pass

def test_winner_is_participant(cursor, output):
    '''A winning broadcaster *member* should also be a participant.'''
    errors = False
    cursor.execute('''SELECT broadcaster_id, year FROM winners 
                      JOIN broadcasters ON broadcaster_id=broadcasters.id 
                      WHERE status=4;''')
    winners = cursor.fetchall()
    cursor.execute('SELECT id FROM participants;')
    participants = [i[0] for i in cursor.fetchall()]
    for broadcaster, year in winners:
        if f'{year} {broadcaster}' not in participants:
            output.write(f'! {broadcaster} wins in {year} without participating.\n')
            errors = True
    if not errors:
        output.write('  winners: all winners are also participants.\n')
    return not errors

def test_winner_year(cursor, output):
    '''A broadcaster should win only in its active years.'''
    errors = False
    cursor.execute('SELECT id, first, last FROM broadcasters;')
    broadcasters = {id:(first, last) for id, first, last in cursor.fetchall()}
    cursor.execute('SELECT id, year, broadcaster_id FROM winners;')
    for id, year, broadcaster in cursor.fetchall():
        if broadcasters[broadcaster][0] >= year >= broadcasters[broadcaster][1]:
            output.write(f'! winners: {id} year is off range.\n')
            errors = True
    if not errors:
        output.write('  winners: winning years ok.\n')
    return not errors

def test_winner_title(cursor, output):
    '''Basic test on programme titles.'''
    errors = False
    cursor.execute('SELECT id, or_title, en_title, cat_title FROM winners;')
    for id, or_title, en_title, cat_title in cursor.fetchall():
        if or_title.strip() != or_title or or_title.endswith('.'):
            output.write(f'! winners: {id}, check syntax for {or_title}.\n')
            errors = True
        if en_title.strip() != en_title or en_title.endswith('.'):
            output.write(f'! winners: {id}, check syntax for {en_title}.\n')
            errors = True
        if cat_title.strip() != cat_title or cat_title.endswith('.'):
            output.write(f'! winners: {id}, check syntax for {cat_title}.\n')
            errors = True
    if not errors:
        output.write('  winners: titles ok.\n')
    return not errors

def test_double_winners(cursor, output):
    '''Double winners should be the same programme, different prize.'''
    errors = False
    cursor.execute('''SELECT prog_id, broadcaster_id, or_title, en_title, cat_title, 
                      credits, weblink, program_type, prize_id 
                      FROM winners ORDER BY prog_id;''')
    previous = [None, None, None, None, None, None, None, None, None]
    for programme in cursor.fetchall():
        if programme[0] == previous [0]:
            if programme[1:-1] != previous[1:-1]:
                output.write(f'! winners: double winner {programme[0]}, different data.\n')
                errors = True
            if programme[-1] == previous[-1]:
                output.write(f'! winners: double winner {programme[0]}, same prize.\n')
                errors = True
        previous = programme
    if not errors:
        output.write('  double winners: ok.\n')
    return not errors

def test_winner_credits(cursor, output): 
    '''Basic programme credits parsing.'''
    errors = False
    cursor.execute('SELECT id, credits FROM winners;')
    for id, credit in cursor.fetchall():
        creditline = ''
        try:
            creditline = cr.unpack_creditlist(credit)
        except Exception as e:
            output.write(f'! exception when parsing credits for programme {id}.\n')
            errors = True
            continue
        #print(creditline)
        if cr.pack_creditlist(creditline) != credit:
            output.write(f'! credits for programme {id} do not parse ok.\n')
            errors = True
    if not errors:
        output.write('  winners: credit parsing ok.\n')
    return not errors

def check_roles_in_glossary(cursor, output):
    '''Credit roles should be in glossary.'''
    errors = False
    cursor.execute('SELECT id, credits FROM winners;')
    for id, credit in cursor.fetchall():
        #print(credit)
        creditline = cr.unpack_creditlist(credit)
        for roles, persons in creditline:
            for role in roles:
                if role not in cr.ROLES:
                    output.write(f'! programme {id}: role {role} not in glossary.\n')
                    errors = True
    if not errors:
        output.write('  All credit roles in glossary.\n')
    return not errors

def check_roles_plural_form(cursor, output):
    '''If a credit role is plural, there must be more that one person credited.'''
    errors = False
    cursor.execute('SELECT id, credits FROM winners;')
    for id, credit in cursor.fetchall():
        creditline = cr.unpack_creditlist(credit)
        for roles, persons in creditline:
            err_flag = False
            if len(persons) == 1 and any([r not in cr.ROLES_SINGULAR for r in roles]):
                err_flag = True
            elif len(persons) > 1 and any([r not in cr.ROLES_PLURAL for r in roles]):
                err_flag = True
            if err_flag:
                output.write(f'! programme {id}: check {roles} plural form.\n')
                errors = True
    if not errors:
        output.write('  All credit roles plural forms are ok.\n')
    return not errors

def check_double_credits(cursor, output):
    '''Roles and persons should not be repeated in credits.'''
    errors = False
    cursor.execute('SELECT id, credits FROM winners;')
    for id, credit in cursor.fetchall():
        creditline = cr.unpack_creditlist(credit)
        credit_roles = []
        credit_persons = []
        for roles, persons in creditline:
            roles = set(roles)
            persons = set(persons)
            if roles in credit_roles:
                output.write(f'! programme {id}: {roles} repeated.\n')
                errors = True
            if persons in credit_persons:
                output.write(f'! programme {id}: {persons} repeated.\n')
                errors = True
            credit_roles.append(roles)
            credit_persons.append(persons)
    if not errors:
        output.write('  Credit roles and persons unique.\n')
    return not errors

def check_credit_order(cursor, output):
    '''Credits should be listed in a rational order.'''
    # TODO credit ordering is a mess, perhaps better left alone. 
    # For now we ensure that "By" comes first, if present.
    errors = False
    cursor.execute('SELECT id, credits FROM winners;')
    for id, credit in cursor.fetchall():
        creditline = cr.unpack_creditlist(credit)
        first = True
        for roles, persons in creditline:
            if roles == ['By'] and not first:
                output.write(f'! programme {id}: "By" is not the first credit.\n')
                errors = True
            first = False
    if not errors:
        output.write('  Credit roles are well ordered.\n')
    return not errors

def test_long_credits(cursor, output): 
    '''Keep credits short!'''
    errors = False
    cursor.execute('SELECT id, credits FROM winners;')
    for id, credit in cursor.fetchall():
        if len(credit) > 200:
            output.write(f'! {id} credits are too long.\n')
            errors = True
    if not errors:
        output.write('  winners: credits not too long.\n')
    return not errors

def test_punctuation(cursor, output): 
    '''Admitted punctuation only.'''
    errors = False
    cursor.execute('''SELECT id, or_title, credits, 
                      en_title || cat_title || reasoning 
                      FROM winners;''')
    for id, or_title, credits, rest in cursor.fetchall():
        bag = set()
        for char in or_title:
            if (unicodedata.category(char).startswith(('P', 'S', 'Z', 'M', 'C')) 
                and char not in OR_TITLE_PUNCTUATION):
                bag.add(char)
                errors = True
        if bag:
            for item in bag:
                output.write(f'! punctuation in or_title {id}: >|{item}|< ({ord(item)})\n')
        bag = set()
        for char in credits:
            if (unicodedata.category(char).startswith(('P', 'S', 'Z', 'M', 'C')) 
                and char not in CREDIT_PUNCTUATION):
                bag.add(char)
                errors = True
        if bag:
            for item in bag:
                output.write(f'! punctuation in credits {id}: >|{item}|< ({ord(item)})\n')
        bag = set()
        for char in rest:
            if (unicodedata.category(char).startswith(('P', 'S', 'Z', 'M', 'C')) 
                and char not in COMMON_PUNCTUATION):
                bag.add(char)
                errors = True
        if bag:
            for item in bag:
                output.write(f'! punctuation in title/reasoning {id}: >|{item}|< ({ord(item)})\n')
    if not errors:
        output.write('  winners: punctuation ok.\n')
    return not errors

def test_persons_order_ascii_only(cursor, output):
    '''Surname_ord field must be ascii only.'''
    errors = False
    cursor.execute('SELECT surname_ord FROM persons;')
    for i in cursor.fetchall():
        for char in i[0]:
            if char not in (string.ascii_lowercase + "1234567890&-()' "):
                output.write(f'Persons surname_ord not ascii: {i[0]}\n')
                errors = True
    if not errors:
        output.write('  persons: surname_ord ok.\n')
    return not errors

def test_persons_role_in_glossary(cursor, output):
    '''Roles in persons table must be in glossary.'''
    errors = False
    cursor.execute('SELECT role FROM persons;')
    for i in cursor.fetchall():
        if i[0] not in ROLES:
            output.write(f'Persons role not in glossary: {i[0]}\n')
            errors = True
    if not errors:
        output.write('  persons: roles ok.\n')
    return not errors

def test_all(db="prix_winners.grist", output=sys.stdout):
    con = sqlite3.connect(db, detect_types=sqlite3.PARSE_COLNAMES)
    c = con.cursor()
    for test in (test_unique_columns, test_edition_dates, test_edition_max, 
            test_broadcaster_chain, test_participant_year, 
            test_winner_is_participant, test_winner_year, 
            test_winner_title, test_double_winners, 
            test_winner_credits, check_roles_in_glossary, 
            check_roles_plural_form, check_double_credits, 
            check_credit_order, test_long_credits, test_punctuation, 
            test_persons_order_ascii_only, test_persons_role_in_glossary,):
        test(c, output)
        output.write('  ' + '=='*10 + '\n\n')
    con.close()

# test_participant_competition, 

if __name__ == '__main__':
    with open('out.txt', 'a', encoding='utf8') as f:
        test_all(output=f)
