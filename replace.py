# replacements for tex post-production
#-------------------------------------
import os

    # old,   new,   expected replacements (-1 if we don't care)
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
    ('Czech Rep..', 'Czech Rep.', -1),
    ('Shortlist motivation:', '{\\color{DarkRed}\\textit{Shortlist motivation:}}', -1),
    ('Noa (Achinoam Nin) (Israel)', 'Noa (Achinoam Nin), Israel', 1),
    # country names should *also* be tex-escaped... :-(
    ('Italy – Trieste', 'Italy -- Trieste', -1),
    ('Germany - DDR', 'Germany -- DDR', -1),
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
    ("DreamStation by RADIO FRANCE,",
     "DreamStation by R\\kern-0.1em A\\kern-0.1em D\\kern-0.1em I\\kern-0.1em O F\\kern-0.1em R\\kern-0.1em A\\kern-0.1em N\\kern-0.1em C\\kern-0.1em E,", 1),
    ("salvaguardia dell'agricoltura",
     "salvaguardia dell'agri\\-coltura", 1),
    # whitespace tricks
    ("Producer: Stuart Weiss. Choreography: Pat Birch.", 
     "Producer: Stuart Weiss. Choreography: Pat Birch.~", 1),
    # various fixes
    # -------------
    # not sure about these: maybe use unicode chars instead?
    ("textfrench{VIIIe Station",
     "textfrench{VIII\\textsuperscript{e} Station", 1),
    ("itshape VIIIth Station",
     "itshape VIII\\textsuperscript{th} Station", 1),
    # the golden medal 1983: we use the "Prodi" layout below
    ("Henrik Hahr (Sweden)", 
     "{\\large Henrik Hahr}\\\\ Sweden", 1),
    # prix galileo 1988-1990: we use the "Prodi" layout below
    ("Eckhart Stein (Germany)", 
     "{\\large Eckhart Stein}\\\\ Germany", 1),
    ("Liz Forgan (United Kingdom)", 
     "{\\large Liz Forgan}\\\\ United Kingdom", 1),
    ("Angelo Guglielmi (Italy)",
     "{\\large Angelo Guglielmi}\\\\ Italy", 1), 
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
    ("\n\n%2157>%", "\n", 1),
    ("\n\n%2156>%", "\n", 1),
    ("\n\n%2160>%", "\n", 1),
    ("\n\n%2159>%", "\n", 1),
    ("\n\n%2158>%", "\n", 1),
    ("\n\n%2155>%", "\n", 1),
    # special tribute 1999: we use the "Prodi" layout below
    ("Jeremy Isaacs (United Kingdom)",
     "{\\large Jeremy Isaacs}\\\\ United Kingdom", 1),
    # This is for the Euro Prize (honorary) 2000
    # should be smaller (see 1991 and 1998 above) 
    # but it would be odd-looking in the page context
    ("Romano Prodi (Italy)", 
     "{\\large Romano Prodi}\\\\ Italy", 1),
    # This is for the sp. prize web 2000
    ("Kataweb (Italy)", 
     "{\\large Kataweb}\\\\ Italy", 1),
    # This is a fix for the latex parser in Cardine 2001
    #("\n%691>%\n\\\\ \\\\\n", "\n\\\\ \\\\\n", 1),
    # This is for the multimedia section prize 2012
    ("Il Post (Italy)", 
     "Italy", 1),
    # This is for the multimedia section prize 2013
    ("Piccolo Teatro Milano (Italy)", 
     "Italy", 1),
    # 2015, expo: do not repeat name in credits...
    ("\\\\* {\\footnotesize By: Valentina Landenna.}", "", 1),
    ("\\\\* {\\footnotesize By: Leonardo Ferrari Carissimi.}", "", 1),
    # the short names here are just too long...
    ("La Sept -- Société européenne de programmes de télévision (France)",
     "La Sept (France)", 3),
    ("ARTE Groupement Européen d'Intérêt Économique (France)",
     "ARTE GEIE (France", 1),
    # a programme title...
    ("Annie M. G.", "Annie M.~G.", 2),
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
    ("Peaky Blinders: Rambert",
     "Peaky Blinders:\\\\Rambert", 1),
    # forced no-indents
    ("Chris Dunkley (United Kingdom)", "\\noindent Chris Dunkley (United Kingdom)", 1),
    ("Lennart Ehrenborg (Sweden)", "\\noindent Lennart Ehrenborg (Sweden)", 1),
    ("Maria Teresa Miscovich (Argentina)", "\\noindent Maria Teresa Miscovich (Argentina)", 1),
    ("Diana Palma (Italy)", "\\noindent Diana Palma (Italy)", 1),
    ("Lord George Thomson of Monifieth (United Kingdom)", "\\noindent Lord George Thomson of Monifieth (United Kingdom)", 1),
    ("Ursula von Zallinger (Austria)", "\\noindent Ursula von Zallinger (Austria)", 1),
    # some ex-aequos, must be in the same "samepage" context
    ("%18>%\n", "\n\\bigskip\n\\noindent", 1),
    ("%26>%\n", "\n\\bigskip\n\\noindent", 1),
    ("%691>%\n", "\n\\bigskip\n\\noindent", 1),
    ("%1402>%\n", "\n\\bigskip\n\\noindent", 1),
    ("%460>%\n", "\n\\bigskip\n\\noindent ", 1), # the CNN case need one more space
    # ex-aequo prizes break our template logic for opening/closing the samepage context 
    # and I'm not in the mood of fixing it, so...
    ("\\noindent\\end{samepage}\n%<19%", "\\noindent\n%<19%", 1), 
    ("\\noindent\\end{samepage}\n%<27%", "\\noindent\n%<27%", 1), 
    ("\\noindent \\end{samepage}\n%<461%", "\\noindent\n%<461%", 1), 
    ("\\end{samepage}\n%<2156%", "%<2156%", 1), 
    ("\\end{samepage}\n%<2160%", "%<2160%", 1), 
    ("\\end{samepage}\n%<2159%", "%<2159%", 1), 
    ("\\end{samepage}\n%<2158%", "%<2158%", 1), 
    ("\\end{samepage}\n%<2155%", "%<2155%", 1), 
    ("\\end{samepage}\n%<2161%", "%<2161%", 1), 
    ("\\noindent\\end{samepage}\n%<692%", "\\noindent\n%<692%", 1), 
    ("\\noindent\\end{samepage}\n%<1403%", "\\noindent\n%<1403%", 1), 

    # PART 2 -- page-level fixes
    # ==========================
    # sorted by year

    # this is to keep 1949 and 1950 in the same page
    # note: we *could* just modify the value in winners.tex but
    # we feel that 70pt is the correct value, and we try to keep 
    # all the tweaks in one place, here
    ("\\vspace{70pt}\n\\fancyhead[R]{\\scshape The Winners}", 
     "\\vspace{50pt}\n\\fancyhead[R]{\\scshape The Winners}", 1),
    # The following needs an explanation: 
    # basically, the "samepage" context does a decent job, except it makes tex break too early 
    # sometimes, leaving a lot of space at the bottom of the page. This tends to happen with 
    # the last prize block before a new-year section, probably because we had to remove 
    # all the \fillbreak before a section (because it was too much: tex was then starting a 
    # new page with every section!). Inserting \pagebreak[x] won't work either...
    # Bottom line, we must manually insert a few \nopagebreak and \pagebreak hints.
    #1956
    ("%46>%\n\\end{samepage}\n\\filbreak", "%46>%\n\\end{samepage}\n\\nopagebreak", 1),
    ("\\bigskip\\begin{samepage}\n\\section*{1957, Taormina}", 
     "\\pagebreak\\begin{samepage}\n\\section*{1957, Taormina}", 1),
    #1957
    ("%53>%\n\\end{samepage}\n\\filbreak", "%53>%\n\\end{samepage}\n\\nopagebreak", 1),
    ("\\bigskip\\begin{samepage}\n\\section*{1958, Venezia", 
     "\\pagebreak\\begin{samepage}\n\\section*{1958, Venezia", 1),
    # 1961
    ("%87>%\n\\end{samepage}\n\\filbreak", "%87>%\n\\end{samepage}\n\\nopagebreak", 1),
    ("\\bigskip\\begin{samepage}\n\\section*{1962, Verona", 
     "\\pagebreak\\begin{samepage}\n\\section*{1962, Verona", 1), 
    # 1962
    ("%100>%\n\\end{samepage}\n\\filbreak", "%100>%\n\\end{samepage}\n\\nopagebreak", 1),
    ("\\bigskip\\begin{samepage}\n\\section*{1963, Napoli", 
     "\\pagebreak\\begin{samepage}\n\\section*{1963, Napoli", 1), 
    # 1964
    ("%120>%\n\\end{samepage}\n\\filbreak", "%120>%\n\\end{samepage}\n\\nopagebreak", 1),
    ("\\bigskip\\begin{samepage}\n\\section*{1965, Firenze", 
     "\\pagebreak\\begin{samepage}\n\\section*{1965, Firenze", 1), 
    # 1966
    ("%141>%\n\\end{samepage}\n\\filbreak", "%141>%\n\\end{samepage}\n\\nopagebreak", 1),
    ("\\bigskip\\begin{samepage}\n\\section*{1967, Ravenna", 
     "\\pagebreak\\begin{samepage}\n\\section*{1967, Ravenna", 1),
    # 1969
    ("%171>%\n\\end{samepage}\n\\filbreak", "%171>%\n\\end{samepage}\n\\nopagebreak", 1),
    ("\\bigskip\\begin{samepage}\n\\section*{1970, Firenze", 
     "\\pagebreak\\begin{samepage}\n\\section*{1970, Firenze", 1),  
    # 1971
    ("%191>%\n\\end{samepage}\n\\filbreak", "%191>%\n\\end{samepage}\n\\nopagebreak", 1),
    ("\\bigskip\\begin{samepage}\n\\section*{1972, Torino", 
     "\\pagebreak\\begin{samepage}\n\\section*{1972, Torino", 1),
    # 1975
    ("%236>%\n\\end{samepage}\n\\filbreak", "%236>%\n\\end{samepage}\n\\nopagebreak", 1),
    ("\\bigskip\\begin{samepage}\n\\section*{1976, Bologna", 
     "\\pagebreak\\begin{samepage}\n\\section*{1976, Bologna", 1),
    # 1977
    ("%260>%\n\\end{samepage}\n\\filbreak", "%260>%\n\\end{samepage}\n\\nopagebreak", 1),
    ("\\bigskip\\begin{samepage}\n\\section*{1978, Milano", 
     "\\pagebreak\\begin{samepage}\n\\section*{1978, Milano", 1),
    # 1981
    ("%308>%\n\\end{samepage}\n\\filbreak", "%308>%\n\\end{samepage}\n\\nopagebreak", 1),
    ("\\bigskip\\begin{samepage}\n\\section*{1982, Venezia", 
     "\\pagebreak\\begin{samepage}\n\\section*{1982, Venezia", 1),
    # 1987 
    ("\\end{samepage}\n\\filbreak\n\\bigskip\\begin{samepage}\n\\subsection*{{\\color{DarkRed}Sp.~Prize TV Programme on Ecology}}\n%<398%", 
     "\\end{samepage}\n\\nopagebreak\n\\bigskip\\begin{samepage}\n\\subsection*{{\\color{DarkRed}Sp.~Prize TV Programme on Ecology}}\n%<398%", 1),
    ("\\bigskip\\begin{samepage}\n\\section*{1988, Capri", 
     "\\pagebreak\\begin{samepage}\n\\section*{1988, Capri", 1),
    # 1988
    ("%412>%\n\\end{samepage}\n\\filbreak", "%412>%\n\\end{samepage}\n\\nopagebreak", 1),
    ("\\bigskip\\begin{samepage}\n\\section*{1989, Perugia", 
     "\\pagebreak\\begin{samepage}\n\\section*{1989, Perugia", 1),
    # 1998
    ("%2161>%\n\\end{samepage}\n\\filbreak", "%2161>%\n\\end{samepage}\n\\nopagebreak", 1),
    ("\\bigskip\\begin{samepage}\n\\section*{1999, Firenze/Siena", 
     "\\pagebreak\\begin{samepage}\n\\section*{1999, Firenze/Siena", 1),
    # 1999
    ("%2168>%\n\\end{samepage}\n\\filbreak", "%2168>%\n\\end{samepage}\n\\nopagebreak", 1),
    ("\\bigskip\\begin{samepage}\n\\section*{2000, Bologna/Rimini", 
     "\\pagebreak\\begin{samepage}\n\\section*{2000, Bologna/Rimini", 1),
    # 2002
    ("\\end{samepage}\n\\filbreak\n\\bigskip\\begin{samepage}\n\\subsection*{{\\color{DarkRed}Honorary Prix Italia}}\n%<2246%", 
     "\\end{samepage}\n\\nopagebreak\n\\bigskip\\begin{samepage}\n\\subsection*{{\\color{DarkRed}Honorary Prix Italia}}\n%<2246%", 1),
    ("\\bigskip\\begin{samepage}\n\\section*{2003, Catania/Siracusa", 
     "\\pagebreak\\begin{samepage}\n\\section*{2003, Catania/Siracusa", 1),
    # 2003
    ("\\end{samepage}\n\\filbreak\n\\bigskip\\begin{samepage}\n\\subsection*{{\\color{DarkRed}Signis Award}}\n%<782%", 
     "\\end{samepage}\n\\nopagebreak\n\\bigskip\\begin{samepage}\n\\subsection*{{\\color{DarkRed}Signis Award}}\n%<782%", 1),
    ("\\bigskip\\begin{samepage}\n\\section*{2004, Catania/Taormina", 
     "\\pagebreak\\begin{samepage}\n\\section*{2004, Catania/Taormina", 1),
    # 2004
    ("%1856>%\n\\end{samepage}\n\\filbreak", "%1856>%\n\\end{samepage}\n\\nopagebreak", 1),
    ("\\bigskip\\begin{samepage}\n\\section*{2005, Milano", 
     "\\pagebreak\\begin{samepage}\n\\section*{2005, Milano", 1),
    # 2005
    ("%1852>%\n\\end{samepage}\n\\filbreak", "%1852>%\n\\end{samepage}\n\\nopagebreak", 1),
    ("\\bigskip\\begin{samepage}\n\\section*{2006, Venezia", 
     "\\pagebreak\\begin{samepage}\n\\section*{2006, Venezia", 1),
    # 2006
    ("%922>%\n\\end{samepage}\n\\filbreak", "%922>%\n\\end{samepage}\n\\nopagebreak", 1),
    ("\\bigskip\\begin{samepage}\n\\section*{2007, Verona", 
     "\\pagebreak\\begin{samepage}\n\\section*{2007, Verona", 1),
    # 2007
    ("%965>%\n\\end{samepage}\n\\filbreak", "%965>%\n\\end{samepage}\n\\nopagebreak", 1),
    ("\\bigskip\\begin{samepage}\n\\section*{2008, Cagliari", 
     "\\pagebreak\\begin{samepage}\n\\section*{2008, Cagliari", 1),
    # 2008
    ("\\end{samepage}\n\\filbreak\n\\bigskip\\begin{samepage}\n\\subsection*{{\\color{DarkRed}Signis Award}}\n%<1017%", 
     "\\end{samepage}\n\\nopagebreak\n\\bigskip\\begin{samepage}\n\\subsection*{{\\color{DarkRed}Signis Award}}\n%<1017%", 1),
    ("\\bigskip\\begin{samepage}\n\\section*{2009, Torino", 
     "\\pagebreak\\begin{samepage}\n\\section*{2009, Torino", 1),
    # 2010
    ("%1159>%\n\\end{samepage}\n\\filbreak", "%1159>%\n\\end{samepage}\n\\nopagebreak", 1),
    ("\\bigskip\\begin{samepage}\n\\section*{2011, Torino", 
     "\\pagebreak\\begin{samepage}\n\\section*{2011, Torino", 1),
    # 2012
    ("%2175>%\n\\end{samepage}\n\\filbreak", "%2175>%\n\\end{samepage}\n\\nopagebreak", 1),
    ("\\bigskip\\begin{samepage}\n\\section*{2013, Torino", 
     "\\pagebreak\\begin{samepage}\n\\section*{2013, Torino", 1),
    # 2013
    ("%1343>%\n\\end{samepage}\n\\filbreak", "%1343>%\n\\end{samepage}\n\\nopagebreak", 1),
    ("\\bigskip\\begin{samepage}\n\\section*{2014, Torino", 
     "\\pagebreak\\begin{samepage}\n\\section*{2014, Torino", 1),
    # 2015
    ("%2252>%\n\\end{samepage}\n\\filbreak", "%2252>%\n\\end{samepage}\n\\nopagebreak", 1),
    ("\\bigskip\\begin{samepage}\n\\section*{2016, Lampedusa", 
     "\\pagebreak\\begin{samepage}\n\\section*{2016, Lampedusa", 1),
    # 2016
    ("%525>%\n\\end{samepage}\n\\filbreak", "%525>%\n\\end{samepage}\n\\nopagebreak", 1),
    ("\\bigskip\\begin{samepage}\n\\section*{2017, Milano", 
     "\\pagebreak\\begin{samepage}\n\\section*{2017, Milano", 1),
    # 2017 - with a rare forced break not at the end of the year
    ("\\end{samepage}\n\\filbreak\n\\bigskip\\begin{samepage}\n\\subsection*{{\\color{DarkRed}Prix Italia Radio Drama}}\n%<1424%", 
     "\\end{samepage}\n\\nopagebreak\n\\medskip\\begin{samepage}\n\\subsection*{{\\color{DarkRed}Prix Italia Radio Drama}}\n%<1424%", 1),
    ("%1424>%", "%1424>%\n\\enlargethispage{1\\baselineskip}", 1),
    ("%1434>%\n\\end{samepage}\n\\filbreak", "%1434>%\n\\end{samepage}\n\\nopagebreak", 1),
    ("\\bigskip\\begin{samepage}\n\\section*{2018, Capri", 
     "\\pagebreak\\begin{samepage}\n\\section*{2018, Capri", 1),
    # 2018 - another two...
    ("\\end{samepage}\n\\filbreak\n\\bigskip\\begin{samepage}\n\\subsection*{{\\color{DarkRed}Prix Italia Radio Drama}}\n%<1438%", 
     "\\end{samepage}\n\\nopagebreak\n\\medskip\\begin{samepage}\n\\subsection*{{\\color{DarkRed}Prix Italia Radio Drama}}\n%<1438%", 1),
    ("\\end{samepage}\n\\filbreak\n\\bigskip\\begin{samepage}\n\\subsection*{{\\color{DarkRed}Prix Italia Web Entertainment}}\n%<1447%", 
     "\\end{samepage}\n\\nopagebreak\n\\medskip\\begin{samepage}\n\\subsection*{{\\color{DarkRed}Prix Italia Web Entertainment}}\n%<1447%", 1),
    ("%1447>%", "%1447>%\n\\enlargethispage{1\\baselineskip}", 1),
    # 2019
    ("%1471>%\n\\end{samepage}\n\\filbreak", "%1471>%\n\\end{samepage}\n\\nopagebreak", 1),
    # 2020
    ("\\end{samepage}\n\\filbreak\n\\bigskip\\begin{samepage}\n\\subsection*{{\\color{DarkRed}Signis Sp.~Prize}}\n%<1496%", 
     "\\end{samepage}\n\\nopagebreak\n\\bigskip\\begin{samepage}\n\\subsection*{{\\color{DarkRed}Signis Sp.~Prize}}\n%<1496%", 1),
    ("\\bigskip\\begin{samepage}\n\\section*{2021, Milano", 
     "\\pagebreak\\begin{samepage}\n\\section*{2021, Milano", 1),
    # 2021
    ("\\end{samepage}\n\\filbreak\n\\bigskip\\begin{samepage}\n\\subsection*{{\\color{DarkRed}Signis Sp.~Prize}}\n%<1518%", 
     "\\end{samepage}\n\\nopagebreak\n\\bigskip\\begin{samepage}\n\\subsection*{{\\color{DarkRed}Signis Sp.~Prize}}\n%<1518%", 1),
    ("\\bigskip\\begin{samepage}\n\\section*{2022, Bari", 
     "\\pagebreak\\begin{samepage}\n\\section*{2022, Bari", 1),
    # 2022
    ("\\end{samepage}\n\\filbreak\n\\bigskip\\begin{samepage}\n\\subsection*{{\\color{DarkRed}YLAB Prize -- Communication}}\n%<2167%", 
     "\\end{samepage}\n\\nopagebreak\n\\bigskip\\begin{samepage}\n\\subsection*{{\\color{DarkRed}YLAB Prize -- Communication}}\n%<2167%", 1),
    ("\\bigskip\\begin{samepage}\n\\section*{2023, Bari", 
     "\\pagebreak\\begin{samepage}\n\\section*{2023, Bari", 1),
    # 2023 - this is pretty tortured because the digital interactive motivation is sooo long
    ("\\end{samepage}\n\\filbreak\n\\bigskip\\begin{samepage}\n\\subsection*{{\\color{DarkRed}Prix Italia Radio \\& Podcast Doc.~and Reportage}}\n%<2090%", 
     "\\end{samepage}\n\\nopagebreak\n\\begin{samepage}\n\\subsection*{{\\color{DarkRed}Prix Italia Radio \\& Podcast Doc.~and Reportage}}\n%<2090%", 1),
    ("\\end{samepage}\n\\filbreak\n\\bigskip\\begin{samepage}\n\\subsection*{{\\color{DarkRed}Prix Italia Digital Fiction}}\n%<2125%", 
     "\\end{samepage}\n\\nopagebreak\n\\begin{samepage}\n\\subsection*{{\\color{DarkRed}Prix Italia Digital Fiction}}\n%<2125%", 1),
    ("\\end{samepage}\n\\filbreak\n\\bigskip\\begin{samepage}\n\\subsection*{{\\color{DarkRed}Prix Italia Digital Factual}}\n%<2118%", 
     "\\end{samepage}\n\\nopagebreak\n\\begin{samepage}\n\\subsection*{{\\color{DarkRed}Prix Italia Digital Factual}}\n%<2118%", 1),
    ("%2125>%", "%2125>%\n\\enlargethispage{2\\baselineskip}", 1),
    ("\\end{samepage}\n\\filbreak\n\\bigskip\\begin{samepage}\n\\subsection*{{\\color{DarkRed}YLAB Prize -- Engineering}}\n%<2162%", 
     "\\end{samepage}\n\\nopagebreak\n\\bigskip\\begin{samepage}\n\\subsection*{{\\color{DarkRed}YLAB Prize -- Engineering}}\n%<2162%", 1),
    ("\\bigskip\\begin{samepage}\n\\section*{2024, Torino", 
     "\\pagebreak\\begin{samepage}\n\\section*{2024, Torino", 1),
 
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
book_broadcasters_txt = tuple()
book_broadcasters_html = (
    # this is because whitespace control in jinja is a nighmare...
    ("|yearsep|", " ", -1), # maybe replace with &nbsp; instead
    ("|compsep|;", ";", -1),
    ("|compsep|.", ".", -1),
    ("|compsep|", " ", -1),
    )
book_broadcasters_tex = tuple()
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

# THE 75GENIUS BOOKLET
genius_book_tex = (
    # fixing overfull boxes
    ("journalist by vocation, a well-travelled",
    "journalist by vocation, a well-trav\\-elled", 1),
    ("proceeded slowly, amidst",
     "proceeded slow\\-ly, amidst", 1),
    # the last portrait is different
    ("\\null\\vfill\n\n% start portrait n 75 %",
     "\\null\\vspace{50pt}\n\n% start portrait n 75 %", 1),
    # just for good looking
    ("end portrait n 59 %\n\n\\bigskip",
     "end portrait n 59 %\n\n\\bigskip\\bigskip", 1),
    ("\\bigskip\n\n% start portrait n 60",
     "\\bigskip\\bigskip\n\n% start portrait n 60", 1),
    )
genius_book_html = tuple()
genius_book_txt = tuple()


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

    ('book broadcasters', 'tex'): book_broadcasters_tex,
    ('book broadcasters', 'html'): book_broadcasters_html,
    ('book broadcasters', 'txt'): book_broadcasters_txt,

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


    ('genius book', 'tex'): genius_book_tex,
    ('genius book', 'html'): genius_book_html,
    ('genius book', 'txt'): genius_book_txt,
}



def do_replace(txt, repl_set, out_type, verbose=True):
    """Custom replacements for tex post-production.
    txt: the raw input text
    repl_set: the replacements set ('silver winners'...)
    out_type: 'txt', 'html', 'tex' 
    verbose: warns when repl. number is different than expected
    """
    replacements = REPLACEMENTS[(repl_set, out_type)]
    no_repl_happened = True
    if replacements:
        for old, new, num in replacements:
            occurrences = txt.count(old)
            txt = txt.replace(old, new)
            if num != -1 and occurrences != num and verbose:
                print(f'Replacement >{old}< {occurrences} found, {num} expected.')
            no_repl_happened = False
    if no_repl_happened:
        print(f'No replacements found for {repl_set} / {out_type}.')
    return txt
