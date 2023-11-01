import os, os.path
import re
import sqlite3
import json
from datetime import date, timedelta
from jinja2 import Environment, FileSystemLoader, select_autoescape
from replace import do_replace

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

OUTPUT = {'html': {'editions': ('output/editions.html', 'book/editions.html'),
                   'winners': ('output/winners.html', 'book/winners.html'),
                   'persons': ('output/persons.html', 'book/persons.html'),
                   'milestones': ('output/milestones.html', 'book/milestones.html'),
                   'bibliography': ('output/bibliography.html', 'book/bibliography.html'),
                   'book': ('output/book.html', 'book/book.html'),
                   # the silver booklet
                   'winners': ('output/winners.html', 'silver/winners.html'),
                   'win_broadcasters': ('output/win_broadcasters.html', 'silver/win_broadcasters.html'),
                   'book': ('output/book.html', 'silver/book.html'),
                   # test, various
                   'special_prixsite': ('output/special_prixsite.html', 'special_prixsite.html'),
                   },
          'txt': {'editions': ('output/editions.txt', 'book/editions.txt'),
                  'winners': ('output/winners.txt', 'book/winners.txt'),
                  'persons': ('output/persons.txt', 'book/persons.txt'),
                  'milestones': ('output/milestones.txt', 'book/milestones.txt'),
                  'bibliography': ('output/bibliography.txt', 'book/bibliography.txt'),
                  'book': ('output/book.txt', 'book/book.txt'),
                   # the silver booklet
                  'winners': ('output/winners.txt', 'silver/winners.txt'),
                  'win_broadcasters': ('output/win_broadcasters.txt', 'silver/win_broadcasters.txt'),
                  'book': ('output/book.txt', 'silver/book.txt'),
                   # test, various
                  'test_winners_short': ('output/test_winners_short.txt', 'test_winners_short.txt'),
                  },
          'tex': {'editions': ('output/editions.tex', 'book/editions.tex'),
                  'winners': ('output/winners.tex', 'book/winners.tex'),
                  'persons': ('output/persons.tex', 'book/persons.tex'),
                  'milestones': ('output/milestones.tex', 'book/milestones.tex'),
                  'bibliography': ('output/bibliography.tex', 'book/bibliography.tex'),
                  'book': ('output/book.tex', 'book/book.tex'),
                   # the silver booklet
                  'winners': ('output/winners.tex', 'silver/winners.tex'),
                  'win_broadcasters': ('output/win_broadcasters.tex', 'silver/win_broadcasters.tex'),
                  'book': ('output/book.tex', 'silver/book.tex'),
                   # test, various
                  'test_langs': ('output/test_langs.tex', 'test_langs.tex'),
                  },  
          }


class PrixFormatter:
    def __init__(self, db='prix_winners.grist', outputtype='tex', template_folder='book'):
        self.con = sqlite3.connect(db, detect_types=sqlite3.PARSE_COLNAMES)
        if outputtype:
            self.set_outputtype(outputtype)

    def set_outputtype(self, outputtype):
        self.outputtype = outputtype
        if self.outputtype == 'tex':
                self.jinja = Environment(loader=FileSystemLoader('template'),
                            autoescape=select_autoescape(['html', 'htm', 'xml']), 
                            trim_blocks=True, lstrip_blocks=True)
                self.jinja.filters["texescape"] = _tex_escape
                self.jinja.filters["quotescape"] = _tex_quote_escape
                self.jinja.filters["periodspacescape"] = _tex_period_space_escape
        elif self.outputtype == 'txt':
                self.jinja = Environment(loader=FileSystemLoader('template'),
                            autoescape=select_autoescape(['html', 'htm', 'xml']), 
                            trim_blocks=True, lstrip_blocks=True)
        else:
                self.jinja = Environment(loader=FileSystemLoader('template'),
                            autoescape=select_autoescape(['html', 'htm', 'xml']))

    def _get_lang_tags(self):
        c = self.con.cursor()
        c.execute('SELECT DISTINCT lang_title FROM winners ORDER BY lang_title;')
        langs = [i[0] for i in c.fetchall()]
        for i in ('', 'english', 'japanese', 'korean', 'chinese', 'nolanguage', 'tsonga'):
            langs.remove(i)
        return langs

    def _publish(self, output, **context):
        outfile = OUTPUT[self.outputtype][output][0]
        try:
            os.remove(outfile)
        except OSError:
            pass
        template = self.jinja.get_template(OUTPUT[self.outputtype][output][1])
        with open(outfile, 'a', encoding='utf8') as out:
            if self.outputtype == 'tex':
                languages = self._get_lang_tags()
                out.write(template.render(languages=languages, common=COMMON, **context))
            else:
                out.write(template.render(common=COMMON, **context))
        return outfile

    def get_context_editions(self):
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
        
    def publish_editions(self):
        editions, participants = self.get_context_editions()
        self._publish('editions', editions=editions, 
                      participants=participants, standalone=True)

    def get_context_winners(self, 
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
        '''The winner list.'''
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

        sql = '''SELECT year, city, acronym, name, acr_name, country, country_abbr, 
                 iso3166, or_title, en_title, lang_title, credits, weblink, prize, prize_abbr, 
                 result, reasoning, note 
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
        return display, winners

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
        display, winners = self.get_context_winners(
            start_year, end_year, shortname, shortcountry, shortprize, credits, weblink, 
            reasoning, note, winners_only, prixitalia_only, exclude_unknowns)
        self._publish('winners', winners=winners, display=display, standalone=True)

    def get_context_persons(self):
        sql = '''SELECT vPrixPersons.name, surname, disamb, surname_ord, role, year, 
                 vPrixPersons.acronym, status AS broad_kind, result, programme_id 
                 FROM vPrixPersons 
                 JOIN broadcasters ON broadcasters.id=vPrixPersons.id_acronym;'''
        c = self.con.cursor()
        return c.execute(sql).fetchall()

    def publish_persons(self):
        persons = self.get_context_persons()
        self._publish('persons', persons=persons, standalone=True)

    def get_context_milestones(self):
        sql = 'SELECT year, milestone FROM milestones ORDER BY year;'
        c = self.con.cursor()
        return c.execute(sql).fetchall()

    def publish_milestones(self):
        milestones = self.get_context_milestones()
        self._publish('milestones', milestones=milestones, standalone=True)

    def get_context_bibliography(self):
        sql = '''SELECT edition, category, author, title, notes, publisher, year
                 FROM bibliography 
                 ORDER BY edition, sort;'''
        c = self.con.cursor()
        return c.execute(sql).fetchall()

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


    # the silver booklet
    # -----------------------------------------------------------------------

    def get_context_win_broadcasters(self):
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

    def publish_win_broadcasters(self):
        broadcasters = self.get_context_win_broadcasters()
        self._publish('win_broadcasters', broadcasters=broadcasters, standalone=True)

    def publish_silver_booklet(self):
        # this is a first stab at the silver booklet
        display, winners = self.get_context_winners(shortname='acro', shortprize='short', 
                               credits=True, weblink=False, reasoning=False, 
                               note=True, winners_only=True, prixitalia_only=False, 
                               exclude_unknowns=True)
        broadcasters = self.get_context_win_broadcasters()
        milestones = self.get_context_milestones()
        outfile = self._publish('book', winners=winners, broadcasters=broadcasters, 
                       milestones=milestones, display=display, standalone=False)
        do_replace('silver', outfile)

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
    
    from db import prepare_db
    prepare_db()
    
    f = PrixFormatter(db=args.db, outputtype=None)
    for outputtype in ('txt', 'html', 'tex'):
        if getattr(args, outputtype):
            f.set_outputtype(outputtype)
            for section in args.sections:
                getattr(f, choices[section])()
