import os, os.path
import re
import sqlite3
import json
from datetime import date, timedelta
from jinja2 import Environment, FileSystemLoader, select_autoescape
from replace import do_replace
from db import prepare_db

def _sqlite_dict_row_factory(cursor, row):
    fields = [i[0] for i in cursor.description]
    return {key: value for key, value in zip(fields, row)}

REPLACEMENTS = { "&": "\\&", "%": "\\%", "$": "\\$", "#": "\\#", "_": "\\_", 
                 "{": "\\{", "}": "\\}", "\\": "\\textbackslash{}", 
                 "~": "\\textasciitilde{}", "^": "\\textasciicircum{}",
                 "–": "--", "…": "\\ldots{}",}
ESCAPE_PATTERN = re.compile("[{}]".format("".join(map(re.escape, REPLACEMENTS.keys()))))

def _tex_quote_escape(s):
    '''Replace straight quotes with smart tex quotes.'''
    return re.sub(r'"([^"]*)"', r"``\1''", s)

def _tex_escape(s):
    '''Take care of special chars in tex.'''
    s = ESCAPE_PATTERN.sub(lambda mo: REPLACEMENTS.get(mo.group()), s)
    return _tex_quote_escape(s)

def _tex_period_space_escape(s):
    '''Avoid extra space after a period.'''
    return s.replace('. ', '.~')

_months = {6: 'June', 9: 'September', 10: 'October'}
def _date_range_formatter(start, end):
    '''A nice formatter for editions start/end dates.'''
    if start.month == end.month:
        return f'{start.day}/{end.day} {_months[start.month]}'
    else: 
        return f'{start.day} {_months[start.month]}/ {end.day} {_months[end.month]}'

with open('template/common.json', 'r', encoding='utf8') as f:
    COMMON = json.load(f)

TEMPLATE_FOLDER = 'template'
OUTPUT_FOLDER = 'output'


class DataProvider:
    def __init__(self, db="prix_winners.grist"):
        prepare_db(db)
        self.con = sqlite3.connect(db, detect_types=sqlite3.PARSE_COLNAMES)

    def get_languages(self):
        '''Languages needed for tex output.'''
        c = self.con.cursor()
        c.execute('SELECT DISTINCT lang_title FROM winners ORDER BY lang_title;')
        langs = [i[0] for i in c.fetchall()]
        for i in ('', 'english', 'japanese', 'korean', 'chinese', 'nolanguage', 'tsonga'):
            langs.remove(i)
        return langs

    def get_editions(self):
        '''Data about editions.'''
        c = self.con.cursor()
        c.execute('''SELECT editions.year, city, startdate AS "startdate [date]", 
                     enddate AS "enddate [date]", president, secretary, radio, tv, 
                     web, radio_sp, tv_sp, web_sp, special
                     FROM editions;''')
        editions = {year:rest for year, *rest in c.fetchall()}
        c.execute('''SELECT year, count(year) 
                     FROM participants 
                     JOIN broadcasters ON broadcasters.id=broadcaster_id 
                     WHERE broadcasters.status>2 AND radio+tv+web+sp_prize>0
                     GROUP BY year;''')
        broad_participants = {year:part for year, part in c.fetchall()}
        c.execute('''SELECT year, count(year) 
                     FROM participants 
                     JOIN broadcasters ON broadcasters.id=broadcaster_id 
                     WHERE broadcasters.status<3 AND broadcasters.status>0 
                           AND radio+tv+web+sp_prize>0
                     GROUP BY year;''')
        other_participants = {year:part for year, part in c.fetchall()}
        c.execute('''SELECT year, count(c) 
                     FROM 
                       (SELECT DISTINCT year, countries.country AS c
                       FROM participants 
                       JOIN broadcasters ON broadcasters.id= broadcaster_id 
                       JOIN countries ON broadcasters.country=countries.country
                       WHERE broadcasters.status>0 AND radio+tv+web+sp_prize>0
                             AND countries.is_country=1)
                     GROUP BY year''')
        countries = {year:country for year, country in c.fetchall()}
        return editions, broad_participants, other_participants, countries

    def get_winners(self, winners_only, prixitalia_only, exclude_unknowns, 
                    start_year=1948, end_year=9999):
        '''Data about winning/mentioned programmes.'''
        sql = '''SELECT id, year, city, acronym, name, acr_name, country, country_abbr, 
                 iso3166, or_title, rom_title, en_title, lang_title, credits, weblink, 
                 prize, prize_abbr, result, reasoning, note 
                 FROM vPrixWinners WHERE year>=? AND year<=?'''
        if winners_only:
            sql += ' AND result="winner"'
        if prixitalia_only:
            sql += ' AND "Special Prize" not in kind'
        if exclude_unknowns:
            sql += ' AND broadcaster_id!="UNKNOWN"'
        sql += ';'
        c = self.con.cursor()
        c.row_factory = _sqlite_dict_row_factory
        winners = c.execute(sql, (start_year, end_year)).fetchall()
        return winners

    def get_persons(self):
        '''Data about credited persons.'''
        sql = '''SELECT vPrixPersons.name, surname, disamb, surname_ord, role, year, 
                 vPrixPersons.acronym, status AS broad_kind, result, programme_id 
                 FROM vPrixPersons 
                 JOIN broadcasters ON broadcasters.id=vPrixPersons.id_acronym;'''
        c = self.con.cursor()
        return c.execute(sql).fetchall()

    def get_genius(self):
        '''Data about notable people ("the prix italia geniuses").'''
        sql = '''SELECT sort, full_name, surname, surname_ord, description 
                 FROM genius 
                 ORDER BY sort;'''
        c = self.con.cursor()
        c.row_factory = _sqlite_dict_row_factory
        return c.execute(sql).fetchall()

    def get_milestones(self):
        '''Data about milestones.'''
        sql = 'SELECT year, milestone FROM milestones ORDER BY year;'
        c = self.con.cursor()
        return c.execute(sql).fetchall()

    def get_bibliography(self):
        '''Data about bibliography.'''
        sql = '''SELECT edition, author, title, notes, publisher, year
                 FROM bibliography 
                 WHERE category=? 
                 ORDER BY edition, sort;'''
        biblio = {}
        c = self.con.cursor()
        for section in ('annex', 'meeting', 'event', 'art', 'artother', 
                        'prixbook', 'study', 'radiocorriere'):
            biblio[section] = c.execute(sql, (section,)).fetchall()
        return biblio

    def get_win_broadcasters(self):
        '''Data about the winning broadcasters.'''
        # this is tailored for the silver book only
        # a more general version for the big book is in get_participant_broadcasters
        sql = '''SELECT acronym, name, acr_name, country_abbr, 
                 group_concat(year, ", ") AS year
                 FROM 
                    (SELECT DISTINCT vPrixWinners.acronym, vPrixWinners.name, 
                    vPrixWinners.acr_name, vPrixWinners.country_abbr, year, 
                    broadcasters.first, countries.sort 
                    FROM vPrixWinners
                    JOIN broadcasters ON vPrixWinners.broadcaster_id=broadcasters.id 
                    JOIN countries ON vPrixWinners.country = countries.country
                    WHERE result="winner" AND broadcasters.status>2)
                 GROUP BY acronym, name, acr_name, country_abbr
                 ORDER BY sort, first;'''
        c = self.con.cursor()
        c.row_factory = _sqlite_dict_row_factory
        return c.execute(sql).fetchall()

    def get_participant_broadcasters(self):
        '''Data about the participant broadcasters, and their result.'''
        c = self.con.cursor()
        c.row_factory = _sqlite_dict_row_factory
        sql = '''SELECT participants.year, participants.broadcaster_id, 
                 broadcasters.acronym, broadcasters.name, broadcasters.acr_name, 
                 countries.country_abbr, participants.radio, participants.tv, 
                 participants.web, participants.sp_prize 
                 FROM participants 
                 JOIN broadcasters ON participants.broadcaster_id=broadcasters.id 
                 JOIN countries ON broadcasters.country=countries.country 
                 WHERE broadcasters.status>2 
                 ORDER BY countries.sort, broadcasters.sort, broadcasters.first, 
                 broadcasters.name, participants.year;'''
        participants = c.execute(sql).fetchall()
        c = self.con.cursor()
        sql = '''SELECT broadcaster_id, winners.year, 
                 json_extract(prizes.kind, '$[0]') as prog_kind, 
                 count(result) as progs, result
                 FROM winners 
                 JOIN broadcasters ON winners.broadcaster_id=broadcasters.id 
                 JOIN prizes ON winners.prize_id=prizes.id 
                 JOIN _sort_results ON result=_sort_results.item
                 JOIN _sort_sections ON prog_kind=_sort_sections.item 
                 WHERE broadcasters.status>2 
                 GROUP BY winners.year, broadcaster_id, prog_kind, result
                 ORDER BY broadcaster_id, winners.year, 
                 _sort_sections.value, _sort_results.value;'''
        results = {}
        for id, year, kind, progs, res in c.execute(sql).fetchall():
            try:
                results[id, year].append((kind, progs, res))
            except KeyError:
                results[id, year] = [(kind, progs, res)]
        return participants, results

    def get_participants_other(self):
        '''Data about the non-broadcaster participants.'''    # for the book only
        sql = '''SELECT participants.year, broadcasters.name, countries.country_abbr 
                 FROM participants 
                 JOIN broadcasters ON participants.broadcaster_id=broadcasters.id 
                 JOIN countries ON broadcasters.country=countries.country 
                 WHERE broadcasters.status<3 and broadcasters.status>0
                 ORDER BY countries.sort, broadcasters.name;'''
        c = self.con.cursor()
        c.row_factory = _sqlite_dict_row_factory
        return c.execute(sql).fetchall()


class BaseFormatter:
    def __init__(self, db='prix_winners.grist', outputtype='tex', 
                 template_folder=None):
        self.db = DataProvider(db)
        self.languages = self.db.get_languages() # useful for tex output
        self.template_folder = template_folder or TEMPLATE_FOLDER
        if outputtype: # to allow setting the output later
            self.set_outputtype(outputtype)

    def set_outputtype(self, outputtype):
        '''Set rules for different output types ('tex', 'html' or 'txt').'''
        self.outputtype = outputtype
        if self.outputtype == 'tex':
                self.jinja = Environment(
                            loader=FileSystemLoader(self.template_folder),
                            autoescape=select_autoescape(['html', 'htm', 'xml']), 
                            trim_blocks=True, lstrip_blocks=True)
                self.jinja.filters["texescape"] = _tex_escape
                self.jinja.filters["quotescape"] = _tex_quote_escape
                self.jinja.filters["periodspacescape"] = _tex_period_space_escape
        elif self.outputtype == 'txt':
                self.jinja = Environment(
                            loader=FileSystemLoader(self.template_folder),
                            autoescape=select_autoescape(['html', 'htm', 'xml']), 
                            trim_blocks=True, lstrip_blocks=True)
        else:
                self.jinja = Environment(
                            loader=FileSystemLoader(self.template_folder),
                            autoescape=select_autoescape(['html', 'htm', 'xml']))
        self.jinja.filters["daterangeformat"] = _date_range_formatter

    def get_output(self, template_file, **context):
        '''Return an output, give a template and context.
        'template_file' is a path relative to self.template_folder
        Note: I find that extra-space in latex can be tricky. 
        Since it's pretty difficult to hunt down every single extra-space 
        at template level, we run a manual strip here.
        '''
        template = self.jinja.get_template(template_file)
        if self.outputtype == 'tex':
            res = template.render(languages=self.languages, common=COMMON, **context)
            return '\n'.join([l.strip() for l in res.splitlines()])
        elif self.outputtype == 'txt':  # extra space on the right may be formatting
            res = template.render(common=COMMON, **context)
            return '\n'.join([l.rstrip() for l in res.splitlines()])
        else:  # html doesn't really care about extra space 
            return template.render(common=COMMON, **context)

    def finalize_output(self, output, replacements):
        '''After an output has been produced, apply necessary "manual" edits.
           'output' is the output as a string
           'replacements' is a repl. set ('silver winners', ...) see replace.py
        '''
        return do_replace(output, replacements, self.outputtype)

    def write_output(self, output, out_file):
        '''Write an output to a file. 
           'out_file' is a path relative to OUTPUT_FOLDER
        '''
        out_file = os.path.join(OUTPUT_FOLDER, out_file)
        try:
            os.remove(out_file)
        except OSError:
            pass
        with open(out_file, 'a', encoding='utf8') as out:
            out.write(output)
        
    def publish(self, template_file, out_file, replacements, **context):
        '''Publish an output. 
        'template_file' is a path relative to self.template_folder
        'context' is the context for the template
        'out_file' is a path relative to OUTPUT_FOLDER
        'replacements' is a repl. set ('silver winners', ...) see replace.py
        '''
        out = self.get_output(template_file, **context)
        out = self.finalize_output(out, replacements)
        self.write_output(out, out_file)

    def publish_book(self):
        '''Publish the whole thing.'''
        # this is the basic output type, always required 
        raise NotImplementedError("This method MUST exist!")
        

class PrixSilverFormatter(BaseFormatter):
    '''The formatter for the silver booklet.'''
    def __init__(self, db='prix_winners.grist', outputtype='tex'):
        template_folder = os.path.join(TEMPLATE_FOLDER, 'silver')
        super().__init__(db, outputtype, template_folder)
        self.winner_display = {
                               'acronym': True,
                               'name': False,
                               'full_country': False,
                               'short_country': True,
                               'iso_country': False,
                               'full_prize': False,
                               'short_prize': True,
                               'credits': True,
                               'weblink': False,
                               'reasoning': False,
                               'note': True,
                              }

    def publish_intro(self):
        # this is a flat file, no data from db
        the_file = 'intro.' + self.outputtype
        self.publish(the_file, the_file, 'silver intro', 
                     standalone=True)

    def publish_winners(self):
        winners = self.db.get_winners(winners_only=True, 
                    prixitalia_only=False, exclude_unknowns=True)
        the_file = 'winners.' + self.outputtype
        self.publish(the_file, the_file, 'silver winners',
                     winners=winners, display=self.winner_display, standalone=True)

    def publish_win_broadcasters(self):
        broadcasters = self.db.get_win_broadcasters()
        the_file = 'win_broadcasters.' + self.outputtype
        self.publish(the_file, the_file, 'silver broadcasters',
                     broadcasters=broadcasters, standalone=True)

    def publish_milestones(self):
        milestones = self.db.get_milestones()
        the_file = 'milestones.' + self.outputtype
        self.publish(the_file, the_file, 'silver milestones', 
                     milestones=milestones, standalone=True)

    def publish_book(self):
        winners = self.db.get_winners(winners_only=True, 
                    prixitalia_only=False, exclude_unknowns=True)
        broadcasters = self.db.get_win_broadcasters()
        milestones = self.db.get_milestones()
        the_template = 'book.' + self.outputtype
        the_output = 'silver_book.' + self.outputtype
        self.publish(the_template, the_output, 'silver book', 
                     winners=winners, display=self.winner_display,
                     broadcasters=broadcasters, milestones=milestones, 
                     standalone=False)


class PrixCompanionFormatter(BaseFormatter):
    '''The formatter for the companion book.'''
    def __init__(self, db='prix_winners.grist', outputtype='tex'):
        template_folder = os.path.join(TEMPLATE_FOLDER, 'book')
        super().__init__(db, outputtype, template_folder)
        self.winner_display = {
                               'acronym': True,
                               'name': False,
                               'full_country': False,
                               'short_country': True,
                               'iso_country': False,
                               'full_prize': True,
                               'short_prize': False,
                               'credits': True,
                               'weblink': True,
                               'reasoning': True,
                               'note': True,
                               }

    def publish_winners(self):
        winners = self.db.get_winners(winners_only=False, 
                    prixitalia_only=False, exclude_unknowns=True)
        editions, broad_participants, other_participants, countries = self.db.get_editions()
        the_file = 'winners.' + self.outputtype
        self.publish(the_file, the_file, 'book winners',
                     editions=editions, broad_participants=broad_participants, 
                     other_participants=other_participants, countries=countries,
                     winners=winners, display=self.winner_display, 
                     standalone=True)

    def publish_win_broadcasters(self):
        participants, results = self.db.get_participant_broadcasters()
        others = self.db.get_participants_other()
        the_file = 'win_broadcasters.' + self.outputtype
        self.publish(the_file, the_file, 'book broadcasters',
                     participants=participants, results=results, 
                     others=others, standalone=True)

    def publish_persons(self):
        persons = self.db.get_persons()
        the_file = 'persons.' + self.outputtype
        self.publish(the_file, the_file, 'book persons',
                     persons=persons, standalone=True)

    def publish_milestones(self):
        milestones = self.db.get_milestones()
        the_file = 'milestones.' + self.outputtype
        self.publish(the_file, the_file, 'book milestones', 
                     milestones=milestones, standalone=True)

    def publish_bibliography(self):
        biblio = self.db.get_bibliography()
        the_file = 'bibliography.' + self.outputtype
        self.publish(the_file, the_file, 'book biblio', 
                     biblio=biblio, standalone=True)

    def publish_genius(self):
        genius = self.db.get_genius()
        the_file = 'genius.' + self.outputtype
        self.publish(the_file, the_file, 'book genius', 
                     genius=genius, standalone=True)

    def publish_book(self):
        editions, participants = self.db.get_editions() # XXX see db function
        winners = self.db.get_winners(winners_only=False, 
                    prixitalia_only=False, exclude_unknowns=True)
        persons = self.db.get_persons()
        milestones = self.db.get_milestones()
        bibliography = self.db.get_bibliography()
        genius = self.db.get_genius()
        the_file = 'book.' + self.outputtype
        self.publish(the_file, the_file, 'book book',
                     editions=editions, participants=participants, 
                     display=self.winner_display, winners=winners, persons=persons, 
                     milestones=milestones, bibliography=bibliography, 
                     genius=genius, standalone=False)


class GeniusFormatter(BaseFormatter):
    '''The formatter for the "75genius" booklet.'''
    def __init__(self, db='prix_winners.grist', outputtype='tex'):
        template_folder = os.path.join(TEMPLATE_FOLDER, 'booklets')
        super().__init__(db, outputtype, template_folder)

    @staticmethod
    def _tex_lettrine_escape(s, lettrine_specs):
        '''A Jinja filter to apply a tex lettrine to paragraph.
           This is a very specific filter, tailor-made for this formatter.'''
        s = _tex_escape(s)
        head, tail = s.split(' ', maxsplit=1)
        if head.startswith('<'):  
        # we have a leading tag, could be <b> or <i>
            if head.endswith('>'): 
            # this is a single word, enclosed with tags -> we drop tags altogether
                newhead = f'\\lettrine{lettrine_specs}{{{head[3]}}}{{{head[4:-4]}}}'
                newtail = tail
            else:
            # we move the leading tag to the front of the tail
                newhead = f'\\lettrine{lettrine_specs}{{{head[3]}}}{{{head[4:]}}}'
                newtail = f'{head[0:3]}{tail}'
        else:
            # a normal first word, no tags to worry about
            newhead = f'\\lettrine{lettrine_specs}{{{head[0]}}}{{{head[1:]}}}'
            newtail = tail
        if len(head) == 1:
            return f'{newhead}{newtail}' # this is nicer
        else:
            return f'{newhead} {newtail}'

    def set_outputtype(self, outputtype):
        '''Add a tex filter to the Jinja engine.'''
        super().set_outputtype(outputtype)
        if self.outputtype == 'tex':
            self.jinja.filters["texlettrine"] = self._tex_lettrine_escape

    def publish_book(self):
        genius = self.db.get_genius()
        the_file = 'genius.' + self.outputtype
        self.publish(the_file, the_file, 'genius book', 
                     genius=genius, standalone=False)




class SpecialFormatter(BaseFormatter):
    '''A formatter for test and ad-hoc outputs.'''
    # NOTE: these are not mapped in the argparse module api
    # this class should be instantiated at runtime instead
    # also, we do our sql directly to avoid cluttering the db class
    # also, not all output types are available for each method
    # so make sure to call set_outputtype every time first
    def __init__(self, db='prix_winners.grist', outputtype='tex'):
        template_folder = os.path.join(TEMPLATE_FOLDER, 'special')
        super().__init__(db, outputtype, template_folder)

    # ad-hoc (special) and test outputs
    # -----------------------------------------------------------------------
    def publish_the_wall(self): # HTML template only 
        # "the wall" is the full list of historical broadcasters
        sql = '''SELECT  former, broadcasters.country_abbr, name 
                 FROM broadcasters 
                 JOIN countries ON broadcasters.country=countries.country 
                 WHERE is_wall=True 
                 ORDER BY countries.sort, broadcasters.sort, broadcasters.first;'''
        c = self.db.con.cursor()
        broadcasters = c.execute(sql).fetchall()
        the_file = 'special_wall.' + self.outputtype
        out = self.get_output(the_file, broadcasters=broadcasters, 
                              standalone=True)
        self.write_output(out, the_file)


    def publish_special_prixsite(self): # HTML template only
    # what is needed for the prix website
        sql = '''SELECT year, city, acronym, name, acr_name, country_abbr, 
                 or_title, en_title, prize_abbr 
                 FROM vPrixWinners 
                 WHERE result="winner" AND acronym!="UNKNOWN";'''
        c = self.db.con.cursor()
        c.row_factory = _sqlite_dict_row_factory
        winners = c.execute(sql).fetchall()
        the_file = 'special_prixsite.' + self.outputtype
        self.publish(the_file, the_file, '',
                     winners=winners, standalone=True)

    def publish_test_langs(self): # TEX template only
    # a list of titles in various languages
        sql = '''SELECT year, lang_title, or_title, en_title 
                 FROM winners 
                 WHERE or_title != "" AND or_title != "_null" 
                 AND lang_title != "english" AND lang_title != "italian" 
                 ORDER BY lang_title, year;'''
        c = self.db.con.cursor()
        titles = c.execute(sql).fetchall()
        the_file = 'test_langs.' + self.outputtype
        self.publish(the_file, the_file, '', 
                     titles=titles, standalone=True)

    def publish_test_winners_short(self): # TXT output only
    # a winner-only shorter list
        sql = '''SELECT year, city, acronym, country, or_title, en_title, 
                 credits, prize_abbr, program_type 
                 FROM vPrixWinners
                 WHERE result="winner";'''
        c = self.db.con.cursor()
        c.row_factory = _sqlite_dict_row_factory
        winners = c.execute(sql).fetchall()
        the_file = 'test_winners_short.' + self.outputtype
        self.publish(the_file, the_file, '', 
                     winners=winners, standalone=True)






if __name__ == '__main__':
    import argparse
    outputs = ('silver', 'book', '75genius')
    sections = {# for the silver booklet
                'intro': 'publish_intro',
                # for the book
                'persons': 'publish_persons',
                'biblio': 'publish_bibliography', 
                'genius': 'publish_genius',
                # for both
                'broadcasters': 'publish_win_broadcasters', 
                'milestones': 'publish_milestones',
                'winners': 'publish_winners', 

                # for everything (base option, always present)
                'book': 'publish_book',
                }
    parser = argparse.ArgumentParser(description='Prix Italia book processing.')
    parser.add_argument('output', choices=outputs, 
                        help='the output ("book" or "silver")')
    parser.add_argument('section', choices=sections.keys(), 
                        help='section to output ("book" is the entire book)')
    parser.add_argument('-t', '--txt', action='store_true', default=False, help='produce txt output')
    parser.add_argument('-l', '--html', action='store_true', default=False, help='produce html output')
    parser.add_argument('-x', '--tex', action='store_true', default=False, help='produce tex output')
    parser.add_argument('--db', default='prix_winners.grist', help='path to prix sqlite db file')
    args = parser.parse_args()
    
    if args.output == 'silver':
        klass = PrixSilverFormatter
    elif args.output == 'book':
        klass = PrixCompanionFormatter
    elif args.output == '75genius':
        klass = GeniusFormatter

    f = klass(db=args.db, outputtype=None)
    for outputtype in ('txt', 'html', 'tex'):
        if getattr(args, outputtype):
            f.set_outputtype(outputtype)
            getattr(f, sections[args.section])()
