# replacements for tex post-production
#-------------------------------------
import os

    # old,   new,   expected replacements
# THE SILVER BOOKLET
silver_intro_txt = tuple()
silver_intro_html = tuple()
silver_intro_tex = tuple()
silver_winners_txt = tuple()
silver_winners_html = tuple()
silver_winners_tex = (
    # PART 1 -- line-level fixes
    # ==========================
    # these should not compromise page breaking,
    # but even if so... we need them anyway
    # fixing some overfull boxes
    # --------------------------
    ("Ministry of Rights and Equal Opportunities Sp.~Prize", 
     "Ministry of Rights and Equal Opportunities Sp.~Pr.", 1),
    ("Sp.~Prize ``Programmes That Effect Social Change''", 
     "Sp.~Pr.~``Programmes That Effect Social Change''", 3),
    ("Prix Italia Web, Best Trans-Media for Young Adult Public",
     "Prix Italia Web,\\\\Best Trans-Media for Young Adult Public", 1),
    ("Pasja, czyli misterium Męki Pańskiej w Kalwarii Zebrzydowskiej widziane",
     "Pasja, czyli misterium Męki Pańskiej w Kalwarii Zebrzydow\\-skiej widziane", 1),
    # various fixes
    # -------------
    # not sure about these: maybe use unicode chars instead?
    ("textfrench{VIIIe Station",
     "textfrench{VIII\\textsuperscript{e} Station", 1),
    ("itshape VIIIth Station",
     "itshape VIII\\textsuperscript{th} Station", 1),
    # this is to avoid the correct but ugly blank line
    # in the 1991 Presidents' Prize
    ("\n\n%460>%\n\\\\ \\\\\n", "\\\\\n", 1),
    # these are because the Euro Prize was awarded to a Country, 
    # not a programme
    ("Italy (Italy)", 
     "{\\large Italy}", 1),
    ("Austria (Austria)", 
     "{\\large Austria}", 1),
    ("United Kingdom (United Kingdom)", 
     "{\\large United Kingdom}", 1),
    # these are for the Honorary Prix Italia 1998
    # maybe should be {\large NAME}\\COUNTRY\\
    # but we are consistent with the 1991 Presidents' Prize format
    ("\n\n%2157>%\n\\\\ \\\\\n", "\\\\\n", 1),
    ("\n\n%2156>%\n\\\\ \\\\\n", "\\\\\n", 1),
    ("\n\n%2160>%\n\\\\ \\\\\n", "\\\\\n", 1),
    ("\n\n%2159>%\n\\\\ \\\\\n", "\\\\\n", 1),
    ("\n\n%2158>%\n\\\\ \\\\\n", "\\\\\n", 1),
    ("\n\n%2155>%\n\\\\ \\\\\n", "\\\\\n", 1),
    # This is for the Euro Prize (honorary) 2000
    # should be smaller (see 1991 and 1998 above) 
    # but it would be odd-looking in the page context
    ("Romano Prodi (Italy)", 
     "{\\large Romano Prodi}\\\\ Italy", 1),
    # This is for the sp. prize web 2000
    ("Kataweb (Italy)", 
     "{\\large Kataweb}\\\\ Italy", 1),
    # This is a fix for the latex parser in Cardine 2001
    ("\n\n%691>%\n\\\\ \\\\\n", "\n\\\\ \\\\\n", 1),
    # This is for the multimedia section prize 2012
    ("Il Post (Italy)", 
     "Italy", 1),
    # This is for the multimedia section prize 2013
    ("Piccolo Teatro Milano (Italy)", 
     "Italy", 1),
    # ugly linebreaks: avoid with mbox
    # --------------------------------
    ("Producer: Bert van der Zouw. Script: J Bernlef", 
     "Producer: Bert van der Zouw. Script: \\mbox{J Bernlef}", 1),
    ("Actors: Evgenia Dobrovolskaya", 
     "Actors: \\mbox{Evgenia} Dobrovolskaya", 1),
    ("ukrainischen Leihmüttern", 
     "ukrainischen Leih\\-müttern", 1),
    # these make overfull boxes... whatever
    ("Pertti Saloma, Seppo Partanen, Martti Timonen.}",
     "Pertti Saloma, Seppo Partanen, Martti \\mbox{Timonen}.}", 1),
    ("Sten Holmberg, Jonas Hallqvist.", 
     "Sten Holmberg, Jonas \\mbox{Hallqvist}.", 1),
    # forced linebreaks
    # -----------------
    ("Prime Minister Sp.~Prize TV Programme from a Book",
     "Prime Minister Sp.~Prize\\\\TV Programme from a Book", 1),
    ("Best TV Campaign, Non-Euro Country",
     "Best TV Campaign,\\\\Non-Euro Country", 1),
    ("Prix Italia Radio Doc.~Cultural and General Interest",
     "Prix Italia Radio Doc.\\\\Cultural and General Interest", 4),
    ("Prix Italia TV Doc.~Cultural and General Interest",
     "Prix Italia TV Doc.\\\\Cultural and General Interest", 14),
    ("Archives Web Site / Le site Web des archives",
     "Archives Web Site/\\\\Le site Web des archives", 1),
    ("フィリピン・ムスリムの兄と妹", 
     "フィリピン・\\\\ムスリムの兄と妹", 1),
    ("Students' Jury Sp.~Prize TV Drama Serials and Series", 
     "Students' Jury Sp.~Prize\\\\TV Drama Serials and Series", 4),
    ("Students' Jury Sp.~Prize TV Doc.~Cultural and General Interest", 
     "Students' Jury Sp.~Prize\\\\TV Doc.~Cultural and General Interest", 1),
    ("Sp.~Prize Outstanding Innovative/Creative Web Project", 
     "Sp.~Prize Outstanding Innovative/Creative\\\\Web Project", 2),
    ("Sp.~Prixe Expo 2015 -- Young Independent Film-Makers", 
     "Sp.~Prixe Expo 2015 -- Young Independent\\\\Film-Makers", 1),
    ("Prix Italia Radio Music Attracting a Broader Audience", 
     "Prix Italia Radio Music Attracting\\\\a Broader Audience", 1),
    ("Prix Italia Radio Doc.~and Reportage -- Documentary", 
     "Prix Italia Radio Doc.~and Reportage --\\\\Documentary", 1),

    # PART 2 -- page-level fixes
    # ==========================
    # these will force different pagebreaks and are sorted by year
    # 1957 [spread more, just for good looking - no forced pagebreak]
    ("\n%48>%", "\\medskip\n%48>%", 1),
    ("\n%49>%", "\\medskip\n%49>%", 1),
    ("\n%50>%", "\\medskip\n%50>%", 1),
    ("\n%51>%", "\\medskip\n%51>%", 1),
    ("\n%52>%", "\\medskip\n%52>%", 1),
    ("\n%53>%", "\\medskip\n%53>%", 1),
    # -----------------------------------------------------------------
    # 1962 [shrink the page adding negative space]
    ("\n%94>%", "\\vspace{-2pt}\n%94>%", 1), 
    ("\n%95>%", "\\vspace{-2pt}\n%95>%", 1), 
    ("\n%96>%", "\\vspace{-2pt}\n%96>%", 1), 
    ("\n%97>%", "\\vspace{-2pt}\n%97>%", 1), 
    ("\n%98>%", "\\vspace{-2pt}\n%98>%", 1), 
    # ...and a gentle hint for the last line
    ("A Man of No Importance}\\nopagebreak[2]\\\\ RTF",
     "A Man of No Importance}\\nopagebreak[0]\\\\ RTF", 1),
    # -----------------------------------------------------------------
    # 1969 [spread more and force pagebreak]
    ("\n%166>%", "\\medskip\n%166>%", 1),
    ("\n%167>%", "\\medskip\n%167>%", 1),
    ("\n%168>%", "\\medskip\n%168>%", 1),
    ("\n%169>%", "\\medskip\n%169>%", 1),
    ("\n%170>%", "\\medskip\n%170>%", 1),
    ("\n%171>%", "\\medskip\n%171>%", 1),
    ("%172>%", "%172>%\n\\pagebreak", 1),
    # -----------------------------------------------------------------
    # 1972 [spread more and force pagebreak]
    ("\n%196>%", "\\medskip\n%196>%", 1),
    ("\n%197>%", "\\medskip\n%197>%", 1),
    ("\n%198>%", "\\medskip\n%198>%", 1),
    ("\n%199>%", "\\medskip\n%199>%", 1),
    ("\n%200>%", "\\medskip\n%200>%", 1),
    ("\n%201>%", "\\medskip\n%201>%", 1),
    ("%202>%", "%202>%\n\\pagebreak", 1),
    # -----------------------------------------------------------------
    # 1978 [add a line to bottom]
    ("%272>%", "%272>%\n\\enlargethispage{1\\baselineskip}", 1),
    # -----------------------------------------------------------------
    # 1984 [add a line to bottom]
    ("%356>%", "%356>%\n\\enlargethispage{1\\baselineskip}", 1),
    # -----------------------------------------------------------------
    # 1989 [add a line to bottom]
    ("%417>%", "%417>%\n\\enlargethispage{1\\baselineskip}", 1),
    # -----------------------------------------------------------------
    # 1990 [spread more and force pagebreak]
    ("\n%436>%", "\\medskip\n%436>%", 1),
    ("\n%438>%", "\\medskip\n%438>%", 1),
    ("\n%440>%", "\\medskip\n%440>%", 1),
    ("\n%430>%", "\\medskip\n%430>%", 1),
    ("\n%432>%", "\\medskip\n%432>%", 1),
    ("\n%434>%", "\\medskip\n%434>%", 1),
    ("%437>%", "%437>%\n\\pagebreak", 1),
    # -----------------------------------------------------------------
    # 1991 [add a line to bottom]
    ("%445>%", "%445>%\n\\enlargethispage{1\\baselineskip}", 1),
    # -----------------------------------------------------------------
    # 1992 [spread for good looking, no pagebreak at the end]
    ("\n%465>%", "\\medskip\n%465>%", 1),
    ("\n%467>%", "\\medskip\n%467>%", 1),
    ("\n%477>%", "\\medskip\n%477>%", 1),
    ("\n%471>%", "\\medskip\n%471>%", 1),
    ("\n%472>%", "\\medskip\n%472>%", 1),
    ("\n%474>%", "\\medskip\n%474>%", 1),
    ("\n%476>%", "\\medskip\n%476>%", 1),
    # -----------------------------------------------------------------
    # 1994 / 1 [add a line to bottom]
    ("%492>%", "%492>%\n\\enlargethispage{1\\baselineskip}", 1),
    # -----------------------------------------------------------------
    # 1994 / 2 [add a line to bottom]
        # NOTE: this is the "right" place to add the command
        # on the same line of \subsection. Strangely enough, if we 
        # add the command on a single line, *and* there is a box full 
        # to the limit, latex will add extra space here.
        # Perhaps we should change the others "\enlarge" substitutions 
        # above, even if they seem to work because there's no full box 
        # around. This is the "wrong" way:
        #("%1863>%", "%1863>%\n\\enlargethispage{1\\baselineskip}", 1),
    ("%<1861%\n", "%<1861%\n\\enlargethispage{1\\baselineskip}", 1),
    # -----------------------------------------------------------------
    # 1995 [add a line to bottom]
    ("%546>%", "%546>%\n\\enlargethispage{1\\baselineskip}", 1),
    # -----------------------------------------------------------------
    # 1996 [add a line to bottom]
    ("%553>%", "%553>%\n\\enlargethispage{1\\baselineskip}", 1),
    # -----------------------------------------------------------------
    # 1999 [spread more for good looking, no forced pagebreak]
    ("\n%606>%", "\\medskip\n%606>%", 1),
    ("\n%612>%", "\\medskip\n%612>%", 1),
    ("\n%500>%", "\\medskip\n%500>%", 1),
    ("\n%613>%", "\\medskip\n%613>%", 1),
    ("\n%614>%", "\\medskip\n%614>%", 1),
    ("\n%609>%", "\\medskip\n%609>%", 1),   # note: these 3 are the
    ("\n%610>%", "\\medskip\n%610>%", 1),   # already-replaced
    ("\n%611>%", "\\medskip\n%611>%", 1),   # 1999 Euro Prizes
    # -----------------------------------------------------------------
    # 2000 [shrink the page adding negative space, add a line to bottom]
    ("\n%<615%", "\\vspace{-2pt}\n%<615%", 1),
    ("\n%<616%", "\\vspace{-2pt}\n%<616%", 1),
    ("\n%<619%", "\\vspace{-2pt}\n%<619%", 1),
    ("\n%<622%", "\\vspace{-2pt}\n%<622%", 1),
    ("\n%<623%", "\\vspace{-2pt}\n%<623%", 1),
    ("\n%<626%", "\\vspace{-2pt}\n%<626%\n\\enlargethispage{1\\baselineskip}", 1),
    # -----------------------------------------------------------------
    # 2002 [add a line to bottom]
    ("%708>%", "%708>%\n\\enlargethispage{1\\baselineskip}", 1),
    # -----------------------------------------------------------------
    # 2005 [spread more, the pagebreak will happen "naturally"]
    ("\n%839>%", "\\bigskip\n%839>%", 1),
    ("\n%510>%", "\\bigskip\n%510>%", 1),
    ("\n%844>%", "\\bigskip\n%844>%", 1),
    ("\n%842>%", "\\bigskip\n%842>%", 1),
    ("\n%848>%", "\\bigskip\n%848>%", 1),
    ("\n%851>%", "\\bigskip\n%851>%", 1),
    # -----------------------------------------------------------------
    # 2006 / 1 [shrink the page adding negative space, add a line to bottom]
    ("\n%1852>%", "\\vspace{-2pt}\n%1852>%", 1),
    ("\n%873>%", "\\vspace{-10pt}\n%873>%", 1),
    ("\n%877>%", "\\vspace{-2pt}\n%877>%", 1),
    ("\n%880>%", "\\vspace{-2pt}\n%880>%", 1),
    ("\n%883>%", "\\vspace{-2pt}\n%883>%", 1),
    ("\n%887>%", "\\vspace{-2pt}\n%887>%\n\\enlargethispage{1\\baselineskip}", 1),
    # -----------------------------------------------------------------
    # 2006 / 2 [spread more, pagebreak will happen "naturally"]
    ("\n%893>%", "\\bigskip\n%893>%", 1),
    ("\n%896>%", "\\bigskip\n%896>%", 1),
    ("\n%899>%", "\\bigskip\n%899>%", 1),
    ("\n%901>%", "\\bigskip\n%901>%", 1),
    ("\n%904>%", "\\bigskip\n%904>%", 1),
    ("\n%907>%", "\\bigskip\n%907>%", 1),
    ("\n%910>%", "\\bigskip\n%910>%", 1),
    # 2007 [spread more and force pagebreak]
    ("\n%511>%", "\\medskip\n%511>%", 1),
    ("\n%512>%", "\\medskip\n%512>%", 1),
    ("\n%941>%", "\\medskip\n%941>%", 1),
    ("\n%513>%", "\\medskip\n%513>%", 1),
    ("\n%945>%", "\\medskip\n%945>%", 1),
    ("\n%947>%", "\\medskip\n%947>%", 1),
    ("\n%514>%", "%514>%\n\\pagebreak", 1),
    # -----------------------------------------------------------------
    # 2008 [spread more and force pagebreak]
    ("\n%986>%", "\\medskip\n%986>%", 1),
    ("\n%988>%", "\\medskip\n%988>%", 1),
    ("\n%991>%", "\\medskip\n%991>%", 1),
    ("\n%994>%", "\\medskip\n%994>%", 1),
    ("\n%997>%", "\\medskip\n%997>%", 1),
    ("\n%999>%", "%999>%\n\\pagebreak", 1),
    # -----------------------------------------------------------------
    # 2011 [add a line to bottom]
    ("%<1223%\n", "%<1223%\n\\enlargethispage{1\\baselineskip}", 1),
    # -----------------------------------------------------------------
    # 2012 / 1 [shrink the page adding negative space, add a line to bottom]
    ("\n%1229>%", "\\vspace{-2pt}\n%1229>%", 1),
    ("\n%1232>%", "\\vspace{-2pt}\n%1232>%", 1),
    ("\n%1235>%", "\\vspace{-2pt}\n%1235>%", 1),
    ("\n%1238>%", "\\vspace{-2pt}\n%1238>%", 1),
    ("\n%1241>%", "\\vspace{-2pt}\n%1241>%", 1),
    ("\n%518>%", "\\vspace{-2pt}\n%518>%", 1),
    ("\n%1246>%", "\\vspace{-2pt}\n%1246>%\n\\enlargethispage{1\\baselineskip}", 1),
    # -----------------------------------------------------------------
    # 2012 / 2 [spread more, pagebreak will happen "naturally"]
    ("\n%1249>%", "\\bigskip\n%1249>%", 1),
    ("\n%1253>%", "\\bigskip\n%1253>%", 1),
    ("\n%1256>%", "\\bigskip\n%1256>%", 1),
    ("\n%1259>%", "\\bigskip\n%1259>%", 1),
    ("\n%1262>%", "\\bigskip\n%1262>%", 1),
    ("\n%1269>%", "\\bigskip\n%1269>%", 1),
    # -----------------------------------------------------------------
    # 2014 [spread more, just for good looking - no pagebreak at the end]
    ("\n%1362>%", "\\medskip\n%1362>%", 1),
    ("\n%1366>%", "\\medskip\n%1366>%", 1),
    ("\n%1363>%", "\\medskip\n%1363>%", 1),
    ("\n%1369>%", "\\medskip\n%1369>%", 1),
    ("\n%1370>%", "\\medskip\n%1370>%", 1),
    # -----------------------------------------------------------------
    # 2015 [spread more and force pagebreak]
    ("\n%1391>%", "\\medskip\n%1391>%", 1),
    ("\n%1399>%", "\\medskip\n%1399>%", 1),
    ("\n%1402>%", "\\medskip\n%1402>%", 1),
    ("\n%1403>%", "\\medskip\n%1403>%", 1),
    ("\n%1404>%", "\\medskip\n%1404>%", 1),
    ("\n%1405>%", "\\medskip\n%1405>%", 1),
    ("\n%1407>%", "%1407>%\n\\pagebreak", 1),
    # -----------------------------------------------------------------
    # 2017 [add a line to bottom]
    ("%<1422%\n", "%<1422%\n\\enlargethispage{1\\baselineskip}", 1),
    # -----------------------------------------------------------------
    # 2018 [spread more, pagebreak will happen "naturally"]
    ("\n%1437>%", "\\medskip\n%1437>%", 1), 
    ("\n%1438>%", "\\medskip\n%1438>%", 1), 
    ("\n%1440>%", "\\medskip\n%1440>%", 1), 
    ("\n%1442>%", "\\medskip\n%1442>%", 1), 
    ("\n%526>%", "\\medskip\n%526>%", 1), 
    ("\n%1444>%", "\\medskip\n%1444>%", 1), 
    # -----------------------------------------------------------------
    # 2023 / 1 [shrink the page adding negative space, add a line to bottom]
    ("\n%1544>%", "\\vspace{-2pt}\n%1544>%", 1),
    ("\n\n%2165>%", "\\vspace{-2pt}\n%2165>%", 1), # a little different...
    ("\n\n%2167>%", "\\vspace{-8pt}\n%2167>%", 1), # a little different...
    ("\n%2076>%", "\\vspace{-2pt}\n%2076>%", 1),
    ("\n%2083>%", "\\vspace{-2pt}\n%2083>%", 1),
    ("\n%2090>%", "\\vspace{-2pt}\n%2090>%\n\\enlargethispage{1\\baselineskip}", 1),
    # -----------------------------------------------------------------
    # 2023 / 2 [spread more, pagebreak will happen "naturally"]
    ("\n%2104>%", "\\bigskip\n%2104>%", 1),
    ("\n%2111>%", "\\bigskip\n%2111>%", 1),
    ("\n%2118>%", "\\bigskip\n%2118>%", 1),
    ("\n%2125>%", "\\bigskip\n%2125>%", 1),
    ("\n%2132>%", "\\bigskip\n%2132>%", 1),
    ("\n%2142>%", "\\bigskip\n%2142>%", 1),
    )
silver_broadcasters_txt = tuple()
silver_broadcasters_html = tuple()
silver_broadcasters_tex = (
    # forced linebreaks (to avoid overfull boxes)
    ("Belgische Radio- en Televisieomroep/ Radio-Télévision Belge",
     "Belgische Radio- en Televisieomroep/\\\\Radio-Télévision Belge", 2),
    ("Canadian Broadcasting Corporation/ Société Radio-Canada",
     "Canadian Broadcasting Corporation/\\\\Société Radio-Canada", 1),
    ("ARTE Groupement Européen d'Intérêt Économique}}2022",
     "ARTE\\\\Groupement Européen d'Intérêt Économique}}2022", 1),
    # forced linebreaks (aesthetics only)
    ("Société européenne de programmes de télévision}}1992", 
     "Société européenne de programmes\\\\de télévision}}1992", 1),
    ("National Association of Commercial Broadcasters in Japan", 
     "National Association of Commercial Broadcasters\\\\in Japan", 1),
    ("al'urduniyi/ Jordan Radio", 
     "al'urduniyi/\\\\Jordan Radio", 1),
    ("Bangsong Gongsa/ Korean Broadcasting",
     "Bangsong Gongsa/\\\\Korean Broadcasting", 1), 
    ("Munhwa Bangsong/ Munhwa Broadcasting",
     "Munhwa Bangsong/\\\\Munhwa Broadcasting", 1), 
    ("Television Authority/ Independent Television", 
     "Television Authority/\\\\Independent Television", 1), 
    ("Broadcasting Authority/ Independent Television", 
     "Broadcasting Authority/\\\\Independent Television", 1), 
    ("voor de Radio-omroep/ Institut National de Radiodiffusion", 
     "voor de Radio-omroep/\\\\Institut National de Radiodiffusion", 1),
                          )
silver_milestones_txt = tuple()
silver_milestones_html = tuple()
silver_milestones_tex = (
    # this is to spread the milestones a little, to avoid the last orphan
    ("\\subsection*{{\\color{DarkRed}19", 
     "\\medskip\\subsection*{{\\color{DarkRed}19", 29),
    ("\\subsection*{{\\color{DarkRed}20", 
     "\\medskip\\subsection*{{\\color{DarkRed}20", 16),
    )

# THE BIG BOOK
book_editions_tex = tuple()
book_editions_html = tuple()
book_editions_txt = tuple()
book_winners_tex = tuple()
book_winners_html = tuple()
book_winners_txt = tuple()
book_persons_tex = tuple()
book_persons_html = tuple()
book_persons_txt = tuple()
book_milestones_tex = tuple()
book_milestones_html = tuple()
book_milestones_txt = tuple()
book_bibliography_tex = tuple()
book_bibliography_html = tuple()
book_bibliography_txt = tuple()
book_genius_tex = tuple()
book_genius_html = tuple()
book_genius_txt = tuple()


REPLACEMENTS = { 
    ('silver intro', 'txt'): silver_intro_txt,
    ('silver intro', 'html'): silver_intro_html,
    ('silver intro', 'tex'): silver_intro_tex,

    ('silver winners', 'txt'): silver_winners_txt,
    ('silver winners', 'html'): silver_winners_html,
    ('silver winners', 'tex'): silver_winners_tex,

    ('silver broadcasters', 'txt'): silver_broadcasters_txt,
    ('silver broadcasters', 'html'): silver_broadcasters_html,
    ('silver broadcasters', 'tex'): silver_broadcasters_tex,

    ('silver milestones', 'txt'): silver_milestones_txt,
    ('silver milestones', 'html'): silver_milestones_html,
    ('silver milestones', 'tex'): silver_milestones_tex,

    ('silver book', 'txt'): (silver_intro_txt + silver_winners_txt 
                             + silver_broadcasters_txt + silver_milestones_txt),
    ('silver book', 'html'): (silver_intro_html + silver_winners_html 
                              + silver_broadcasters_html+ silver_milestones_html),
    ('silver book', 'tex'): (silver_intro_tex + silver_winners_tex 
                             + silver_broadcasters_tex + silver_milestones_tex),


    ('book editions', 'tex'): book_editions_tex,
    ('book editions', 'html'): book_editions_html,
    ('book editions', 'txt'): book_editions_txt,

    ('book winners', 'tex'): book_winners_tex,
    ('book winners', 'html'): book_winners_html,
    ('book winners', 'txt'): book_winners_txt,

    ('book persons', 'tex'): book_persons_tex,
    ('book persons', 'html'): book_persons_html,
    ('book persons', 'txt'): book_persons_txt,

    ('book milestones', 'tex'): book_milestones_tex,
    ('book milestones', 'html'): book_milestones_html,
    ('book milestones', 'txt'): book_milestones_txt,

    ('book biblio', 'tex'): book_bibliography_tex,
    ('book biblio', 'html'): book_bibliography_html,
    ('book biblio', 'txt'): book_bibliography_txt,

    ('book genius', 'tex'): book_genius_tex,
    ('book genius', 'html'): book_genius_html,
    ('book genius', 'txt'): book_genius_txt,

    ('book book', 'tex'): (book_editions_tex + book_winners_tex 
                           + book_persons_tex + book_milestones_tex 
                           + book_bibliography_tex + book_genius_tex),
    ('book book', 'html'): (book_editions_html + book_winners_html 
                            + book_persons_html + book_milestones_html 
                            + book_bibliography_html + book_genius_html),
    ('book book', 'txt'): (book_editions_txt + book_winners_txt 
                           + book_persons_txt + book_milestones_txt 
                           + book_bibliography_txt + book_genius_txt),
}



def do_replace(txt, repl_set, out_type, verbose=True):
    """Custom replacements for tex post-production.
    txt: the raw input text
    repl_set: the replacements set ('silver winners'...)
    out_type: 'txt', 'html', 'tex' 
    verbose: warns when repl. number is different than expected
    """
    replacements = REPLACEMENTS[(repl_set, out_type)]
    if replacements:
        for old, new, num in replacements:
            occurrences = txt.count(old)
            txt = txt.replace(old, new)
            if occurrences != num and verbose:
                print(f'Replacement >{old}< {occurrences} found, {num} expected.')
    else:
        if verbose:
            print(f'No replacements found for {repl_set} / {out_type}.')
    return txt
