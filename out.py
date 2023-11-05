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
        editions = c.execute(
            '''SELECT editions.year, city, startdate AS "startdate [date]", 
               enddate AS "enddate [date]", president, secretary, radio, tv, 
               web, special, radio_sp, tv_sp, web_sp 
               FROM editions;''').fetchall()
        c.execute('SELECT year, count(year) FROM participants GROUP BY year;')
        participants = {year:part for year, part in c.fetchall()}
        return editions, participants

    def get_winners(self, winners_only, prixitalia_only, exclude_unknowns, 
                    start_year=1948, end_year=9999):
        '''Data about winning/mentioned programmes.'''
        sql = '''SELECT year, city, acronym, name, acr_name, country, country_abbr, 
                 iso3166, or_title, en_title, lang_title, credits, weblink, 
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

    def get_milestones(self):
        '''Data about milestones.'''
        sql = 'SELECT year, milestone FROM milestones ORDER BY year;'
        c = self.con.cursor()
        return c.execute(sql).fetchall()

    def get_bibliography(self):
        '''Data about bibliography.'''
        sql = '''SELECT edition, category, author, title, notes, publisher, year
                 FROM bibliography 
                 ORDER BY edition, sort;'''
        c = self.con.cursor()
        return c.execute(sql).fetchall()

    def get_win_broadcasters(self):
        '''Data about the winning broadcasters.'''
        #XXX at the moment this is tailored for the silver book only
        # but it should be more general (not only winners, not only broad.)
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


class BaseFormatter:
    def __init__(self, db='prix_winners.grist', outputtype='tex', 
                 template_folder=None):
        self.db = DataProvider(db)
        self.languages = self.db.get_languages() # useful for tex output
        if outputtype: # to allow setting the output later
            self.set_outputtype(outputtype)
        self.template_folder = template_folder or TEMPLATE_FOLDER

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

    def get_output(self, template_file, **context):
        '''Return an output, give a template and context.
        'template_file' is a path relative to self.template_folder
        '''
        template = self.jinja.get_template(os.path.join(self.template_folder, template_file))
        if self.outputtype == 'tex':
            return template.render(languages=self.languages, common=COMMON, **context)
        else:
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
        with open(os.path.join(OUTPUT_FOLDER, out_file), 'a', encoding='utf8') as out:
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
        

class PrixSilverFormatter(BaseFormatter):
    '''The formatter for the silver booklet.'''
    def __init__(self, db='prix_winners.grist', outputtype='tex'):
        template_folder = os.path.join(TEMPLATE_FOLDER, 'silver')
        self.winner_display = {
                               'acronym': 'acro',
                               'name': True,
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
        super().__init__(self, db, outputtype, template_folder)

    def publish_intro(self):
        # this is a flat file, no data from db
        out_file = 'intro.' + self.outputtype
        self.publish('intro', out_file, 'silver intro', 
                     standalone=True)

    def publish_winners(self):
        winners = self.db.get_winners(winners_only=True, 
                    prixitalia_only=False, exclude_unknowns=True)
        out_file = 'winners.' + self.outputtype
        self.publish('winners', out_file, 'silver winners',
                     winners=winners, display=self.winner_display, standalone=True)

    def publish_win_broadcasters(self):
        broadcasters = self.db.get_win_broadcasters()
        out_file = 'win_broadcasters.' + self.outputtype
        self.publish('win_broadcasters', out_file, 'silver broadcasters',
                     broadcasters=broadcasters, standalone=True)

    def publish_milestones(self):
        milestones = self.db.get_milestones()
        out_file = 'milestones.' + self.outputtype
        self.publish('milestones', out_file, 'silver milestones', 
                     milestones=milestones, standalone=True)

    def publish_book(self):
        winners = self.db.get_winners(winners_only=True, 
                    prixitalia_only=False, exclude_unknowns=True)
        broadcasters = self.db.get_win_broadcasters()
        milestones = self.db.get_milestones()
        out_file = 'book.' + self.outputtype
        self.publish('book', out_file, 'silver book', 
                     winners=winners, display=self.winner_display,
                     broadcasters=broadcasters, milestones=milestones, 
                     standalone=True)





# XXX rewrite the code here according to the new api
class PrixCompanionFormatter(BaseFormatter):
    '''The formatter for the companion book.'''
    def __init__(self, db='prix_winners.grist', outputtype='tex'):
        template_folder = os.path.join(TEMPLATE_FOLDER, 'book')
        super().__init__(self, db, outputtype, template_folder)

    def publish_editions(self):
        editions, participants = self.get_context_editions()
        self._publish('editions', editions=editions, 
                      participants=participants, standalone=True)

    def publish_winners(self, 
                        start_year=1949,        # star year (first Prix Italia: 1949)
                        end_year=9999,          # end year
                        shortname='acro|name',  # broadcaster display: 'acro', 'name', 'acro|name'
                        shortcountry='short',   # coutry display: 'name', 'short', 'iso'
                        shortprize='name',      # prize name display: 'name', 'short'
                        credits=True,           # include credit list?
                        weblink=True,           # include web link?
                        reasoning=True,         # include reasoning?
                        note=True,              # include note?
                        winners_only=False,     # list winners only?
                        prixitalia_only=False,  # list prix italia only (not sp. prizes)?
                        exclude_unknowns=False  # exclude unknowns
                        ):
        display = {}
        display['acronym'] = 'acro' in shortname
        display['name'] = 'name' in shortname
        display['full_country'] = (shortcountry == 'name')
        display['short_country'] = (shortcountry == 'short')
        display['iso_country'] = (shortcountry == 'iso')
        display['full_prize'] = (shortprize == 'name')
        display['short_prize'] = (shortprize == 'short')
        display['credits'] = credits
        display['weblink'] = weblink
        display['reasoning'] = reasoning
        display['note'] = note
        winners = self.get_context_winners(
            start_year, end_year, shortname, shortcountry, shortprize, credits, weblink, 
            reasoning, note, winners_only, prixitalia_only, exclude_unknowns)
        self._publish('winners', winners=winners, display=display, standalone=True)

    def publish_persons(self):
        persons = self.get_context_persons()
        self._publish('persons', persons=persons, standalone=True)

    def publish_milestones(self):
        milestones = self.get_context_milestones()
        self._publish('milestones', milestones=milestones, standalone=True)

    def publish_bibliography(self):
        bibliography = self.get_context_bibliography()
        self._publish('bibliography', bibliography=bibliography, standalone=True)

    def publish_book(self):
        editions, participants = self.get_context_editions()
        display, winners = self.get_context_winners()
        persons = self.get_context_persons()
        milestones = self.get_context_milestones()
        bibliography = self.get_context_bibliography()
        self._publish('book', editions=editions, participants=participants, 
                      display=display, winners=winners, persons=persons, 
                      milestones=milestones, bibliography=bibliography, 
                      standalone=False)






    # ad-hoc (special) and test outputs
    # -----------------------------------------------------------------------
    def publish_special_prixsite(self): # what is needed for the prix website
        sql = '''SELECT year, city, acronym, name, acr_name, country_abbr, 
                 or_title, en_title, prize_abbr 
                 FROM vPrixWinners 
                 WHERE result="winner" AND acronym!="UNKNOWN";'''
        c = self.con.cursor()
        c.row_factory = _sqlite_dict_row_factory
        winners = c.execute(sql).fetchall()
        self._publish('special_prixsite', winners=winners, standalone=True)

    def publish_test_langs(self): # a list of titles in various languages
        sql = '''SELECT year, lang_title, or_title, en_title 
                 FROM winners 
                 WHERE or_title != "" AND or_title != "_null" 
                 AND lang_title != "english" AND lang_title != "italian" 
                 ORDER BY lang_title, year;'''
        c = self.con.cursor()
        titles = c.execute(sql).fetchall()
        self._publish('test_langs', titles=titles, standalone=True)

    def publish_test_winners_short(self): # a winner-only shorter list
        sql = '''SELECT year, city, acronym, country, or_title, en_title, 
                 credits, prize_abbr, program_type 
                 FROM vPrixWinners
                 WHERE result="winner";'''
        c = self.con.cursor()
        c.row_factory = _sqlite_dict_row_factory
        winners = c.execute(sql).fetchall()
        self._publish('test_winners_short', winners=winners, standalone=True)






if __name__ == '__main__':
    # XXX rewrite the code here according to the new api
    import argparse
    choices = {'editions': 'publish_editions', 
               'winners': 'publish_winners', 
               'persons': 'publish_persons',
               'milestones': 'publish_milestones', 
               'biblio': 'publish_bibliography', 
               'book': 'publish_book',
               'silver': 'publish_silver_booklet',
               }
    parser = argparse.ArgumentParser(description='Prix Italia book processing.')
    parser.add_argument('sections', nargs='*', choices=choices.keys(), 
                        help='section(s) to output ("book" is the entire book)')
    parser.add_argument('-t', '--txt', action='store_true', default=False, help='produce txt output')
    parser.add_argument('-l', '--html', action='store_true', default=False, help='produce html output')
    parser.add_argument('-x', '--tex', action='store_true', default=False, help='produce tex output')
    parser.add_argument('--db', default='prix_winners.grist', help='path to prix sqlite db file')
    args = parser.parse_args()
    

    
    f = PrixFormatter(db=args.db, outputtype=None)
    for outputtype in ('txt', 'html', 'tex'):
        if getattr(args, outputtype):
            f.set_outputtype(outputtype)
            for section in args.sections:
                getattr(f, choices[section])()
