# replacements for tex post-production
#-------------------------------------
import os
from texify import (PRIZE_NAMES_TEX, PRIZE_NAMES_ABBR_TEX, 
                    BROADCASTER_ACRONYMS_TEX, BROADCASTER_NAMES_TEX, 
                    COUNTRY_NAMES_TEX, COUNTRY_NAMES_ABBR_TEX)

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
    # LEAVE THIS FIRST
    # it's hard to keep spaces/dashes straight... I put non-breaking spaces
    # whenever possible in the templates, but db strings don't have those.
    # So, let's do a sweeping replace first:
    ('  ', ' ', -1), 
    ('~ ', '~', -1), 
    (' --', '~--', -1), 
    ('~~', '~', -1),
    ('Ukrayinsʹke radio', "Ukrayins'ke radio", 1), # missing char... :-(
    ('Czech Rep..', 'Czech Rep.', -1),
    ('Shortlist reasoning:', '{\\color{DarkRed}\\textit{Shortlist reasoning:}}', -1),
    ('Noa (Achinoam Nin) (Israel)', 'Noa (Achinoam Nin), Israel', 2),
    ("{mention}}~CNN by CNN, United States.", "{mention}}~CNN (United States).", 1),
    ('Mediastorm by Mediastorm', 'Mediastorm', 1),
    # fixing some overfull boxes
    # --------------------------
    ("Ministry of Rights and Equal Opportunities Sp.~Prize", 
     "Ministry of Rights and Equal Opportunities Sp.~Pr.", 1),
    ("Prix~Italia Web, Best Trans-Media for Young Adult Public",
     "Prix~Italia Web,\\\\Best Trans-Media for Young Adult Public", 1),
    ("Pasja, czyli misterium Męki Pańskiej w Kalwarii Zebrzydowskiej widziane",
     "Pasja, czyli misterium Męki Pańskiej w Kalwarii Zebrzydow\\-skiej widziane", 1),
    ("salvaguardia dell'agricoltura",
     "salvaguardia dell'agri\\-coltura", 1),
    # sometimes it's hard to keep dashes together with cjk characters
    ("~-- {\\itshape Sleepless Waits a Lonely Wife", " {\\itshape Sleepless Waits a Lonely Wife", 1), 
    # various fixes
    # -------------
    # not sure about these: maybe use unicode chars instead?
    ("textfrench{VIIIe Station",
     "textfrench{VIII\\textsuperscript{e} Station", 1),
    ("itshape VIIIth Station",
     "itshape VIII Station", 1),
    # the golden medal 1983: we use the "Prodi" layout below
    ("%<2169%\nHenrik Hahr (Sweden)", 
     "%<2169%\n{\\large Henrik Hahr}\\\\ Sweden", 1),
    # prix galileo 1988-1990: we use the "Prodi" layout below
    ("%<2170%\nEckhart Stein (Germany)", 
     "%<2170%\n{\\large Eckhart Stein}\\\\ Germany", 1),
    ("%<2171%\nLiz Forgan (United Kingdom)", 
     "%<2171%\n{\\large Liz Forgan}\\\\ United Kingdom", 1),
    ("%<2172%\nAngelo Guglielmi (Italy)",
     "%<2172%\n{\\large Angelo Guglielmi}\\\\ Italy", 1), 
    # these are because the Euro Prize was awarded to a Country, 
    # not a programme
    ("%<609%\nItaly (Italy)", 
     "%<609%\n{\\large Italy}", 1),
    ("%<610%\nAustria (Austria)", 
     "%<610%\n{\\large Austria}", 1),
    ("%<611%\nUnited Kingdom (United Kingdom)", 
     "%<611%\n{\\large United Kingdom}", 1),
    # the same, in the participant list
    ("\\\\*Austria (Austria). Italy (Italy). Jeremy Isaacs (United Kingdom). United Kingdom (United Kingdom).",
     "\\\\*Austria. Italy. United Kingdom. Jeremy Isaacs (United Kingdom).", 1), 
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
    ("%<2168%\nJeremy Isaacs (United Kingdom)",
     "%<2168%\n{\\large Jeremy Isaacs}\\\\ United Kingdom", 1),
    # This is for the Euro Prize (honorary) 2000
    # should be smaller (see 1991 and 1998 above) 
    # but it would be odd-looking in the page context
    ("%<2154%\nRomano Prodi (Italy)", 
     "%<2154%\n{\\large Romano Prodi}\\\\ Italy", 1),
    # This is for the sp. prize web 2000
    ("%<651%\nKataweb (Italy)", 
     "%<651%\n{\\large Kataweb}\\\\ Italy", 1),
    # This is a fix for the latex parser in Cardine 2001
    #("\n%691>%\n\\\\ \\\\\n", "\n\\\\ \\\\\n", 1),
    # This is for the multimedia section prize 2012
    ("%<1276%\n{\\large\\textitalian{Il~Post}}\\\\* Il~Post (Italy)", 
     "%<1276%\n{\\large\\textitalian{Il~Post}}\\\\* Italy", 1),
    # This is for the multimedia section prize 2013
    ("%<1342%\n{\\large\\textitalian{Piccolo Teatro Milano}}\\\\* Piccolo Teatro Milano (Italy)", 
     "%<1342%\n{\\large\\textitalian{Piccolo Teatro Milano}}\\\\* Italy", 1),
    # 2015, expo: do not repeat name in credits...
    ("\\\\* {\\footnotesize By: Valentina Landenna.~}", "", 1),
    ("\\\\* {\\footnotesize By: Leonardo Ferrari Carissimi.~}", "", 1),
    # the short names here are just too long...
    ("La~Sept~-- Société européenne de~programmes de~télévision (France)",
     "La~Sept (France)", 3),
    ("ARTE Groupement Européen d'Intérêt Économique (France)",
     "ARTE GEIE (France)", 1),
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
    ("사이렌", "\\mbox{사이렌}", 1),
    # these make overfull boxes... whatever
    ("Pertti Saloma, Seppo Partanen, Martti Timonen.~}",
     "Pertti Saloma, Seppo Partanen, Martti \\mbox{Timonen}.~}", 1),
    ("Sten Holmberg, Jonas Hallqvist.", 
     "Sten Holmberg, Jonas \\mbox{Hallqvist}.", 1),
    ("``This is Europe? I thought it'd be''.", "\\mbox{``This is Europe? I thought it'd be''.}", 1),
    # forced linebreaks
    # -----------------
    ("Prime Minister Sp.~Prize TV Programme from a Book",
     "Prime Minister Sp.~Prize\\\\TV Programme from a Book", 1),
    ("Best TV Campaign, Non-Euro Country",
     "Best TV Campaign,\\\\Non-Euro Country", 1),
    ("Prix~Italia Radio Doc.~Cultural and General Interest",
     "Prix~Italia Radio Doc.\\\\Cultural and General Interest", 4),
    ("Prix~Italia TV Doc.~Cultural and General Interest",
     "Prix~Italia TV Doc.\\\\Cultural and General Interest", 14),
    ("Archives Web Site / Le site Web des archives",
     "Archives Web Site/\\\\Le site Web des archives", 1),
    ("フィリピン・ムスリムの兄と妹", 
     "フィリピン・\\\\ムスリムの兄と妹", 1),
    ("Students' Jury Sp.~Prize TV Drama Serials and Series", 
     "Students' Jury Sp.~Prize\\\\TV Drama Serials and Series", 4),
    ("Students' Jury Sp.~Prize TV Movies and Mini-Series", 
     "Students' Jury Sp.~Prize\\\\TV Movies and Mini-Series", 4),
    ("Students' Jury Sp.~Prize TV Doc.~Cultural and General Interest", 
     "Students' Jury Sp.~Prize\\\\TV Doc.~Cultural and General Interest", 1),
    ("Sp.~Prize Outstanding Innovative/Creative Web Project", 
     "Sp.~Prize Outstanding Innovative/Creative\\\\Web Project", 2),
    ("Sp.~Prixe Expo 2015~-- Young Independent Film-Makers", 
     "Sp.~Prixe Expo 2015~-- Young Independent\\\\Film-Makers", 1),
    ("Prix~Italia Radio Music Attracting a Broader Audience", 
     "Prix~Italia Radio Music Attracting\\\\a Broader Audience", 1),
    ("Prix~Italia Radio Doc.~and Reportage~-- Documentary", 
     "Prix~Italia Radio Doc.~and Reportage~--\\\\Documentary", 1),
    ("Peaky Blinders: Rambert",
     "Peaky Blinders:\\\\Rambert", 1),
    # forced no-indents
    ("%<2156%\nChris Dunkley (United Kingdom)", "%<2156%\n\\noindent Chris Dunkley (United Kingdom)", 1),
    ("%<2160%\nLennart Ehrenborg (Sweden)", "%<2160%\n\\noindent Lennart Ehrenborg (Sweden)", 1),
    ("%<2159%\nMaria Teresa Miscovich (Argentina)", "%<2159%\n\\noindent Maria Teresa Miscovich (Argentina)", 1),
    ("%<2158%\nDiana Palma (Italy)", "%<2158%\n\\noindent Diana Palma (Italy)", 1),
    ("%<2155%\nLord~George Thomson of~Monifieth (United Kingdom)", "%<2155%\n\\noindent Lord~George Thomson of~Monifieth (United Kingdom)", 1),
    ("%<2161%\nUrsula von~Zallinger (Austria)", "%<2161%\n\\noindent Ursula von~Zallinger (Austria)", 1),
    # some ex-aequos, must be in the same "samepage" context
    ("%18>%\n%18>%\n", "\n\\bigskip\n\\noindent", 1),
    ("%26>%\n%26>%\n", "\n\\bigskip\n\\noindent", 1),
    ("%691>%\n%691>%\n", "\n\\bigskip\n\\noindent", 1),
    ("%1402>%\n%1402>%\n", "\n\\bigskip\n\\noindent", 1),
    ("%460>%\n%460>%\n", "\n\\bigskip\n\\noindent ", 1), # the CNN case need one more space
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
     "\\vspace{20pt}\n\\fancyhead[R]{\\scshape The Winners}", 1),
    # for the same reason, we reduce the gap between 1949 and 1950
    ("%9>%\n\\end{samepage}\n\\bigskip", "%9>%\n\\end{samepage}\n\\medskip", 1), 
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
    ("\\end{samepage}\n\\filbreak\n\\bigskip\\begin{samepage}\n\\subsection*{{\\color{DarkRed}Honorary Prix~Italia}}\n%<2246%", 
     "\\end{samepage}\n\\nopagebreak\n\\bigskip\\begin{samepage}\n\\subsection*{{\\color{DarkRed}Honorary Prix~Italia}}\n%<2246%", 1),
    ("\\bigskip\\begin{samepage}\n\\section*{2003, Catania/Siracusa", 
     "\\pagebreak\\begin{samepage}\n\\section*{2003, Catania/Siracusa", 1),
    # 2003
    ("\\end{samepage}\n\\filbreak\n\\bigskip\\begin{samepage}\n\\subsection*{{\\color{DarkRed}Signis~Award}}\n%<782%", 
     "\\end{samepage}\n\\nopagebreak\n\\bigskip\\begin{samepage}\n\\subsection*{{\\color{DarkRed}Signis~Award}}\n%<782%", 1),
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
    ("\\end{samepage}\n\\filbreak\n\\bigskip\\begin{samepage}\n\\subsection*{{\\color{DarkRed}Signis~Award}}\n%<1017%", 
     "\\end{samepage}\n\\nopagebreak\n\\bigskip\\begin{samepage}\n\\subsection*{{\\color{DarkRed}Signis~Award}}\n%<1017%", 1),
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
    ("%2176>%\n\\end{samepage}\n\\filbreak", "%2176>%\n\\end{samepage}\n\\nopagebreak", 1),
    ("\\bigskip\\begin{samepage}\n\\section*{2014, Torino", 
     "\\pagebreak\\begin{samepage}\n\\section*{2014, Torino", 1),
    # 2014
    ("%1343>%\n\\end{samepage}\n\\filbreak", "%1343>%\n\\end{samepage}\n\\nopagebreak", 1),
    ("\\bigskip\\begin{samepage}\n\\section*{2015, Torino", 
     "\\pagebreak\\begin{samepage}\n\\section*{2015, Torino", 1),
    # 2017
    ("%1599>%\n\\end{samepage}\n\\filbreak\n\\bigskip\\begin{samepage}\n\\subsection*{{\\color{DarkRed}Prix~Italia Radio Doc", 
     "%1599>%\n\\end{samepage}\n\\nopagebreak\n\\medskip\\begin{samepage}\n\\subsection*{{\\color{DarkRed}Prix~Italia Radio Doc", 1),
    ("%1424>%", "%1424>%\n\\enlargethispage{1\\baselineskip}", 1),
    ("%1434>%\n\\end{samepage}\n\\filbreak\n\\bigskip", 
     "%1434>%\n\\end{samepage}\n\\nopagebreak\n\\smallskip", 1),
    ("%1435>%", "%1435>%\n\\enlargethispage{1\\baselineskip}", 1),
    ("\\bigskip\\begin{samepage}\n\\section*{2018, Capri", 
     "\\begin{samepage}\n\\section*{2018, Capri", 1),
    # 2018
    ("%1675>%\n\\end{samepage}\n\\filbreak\n\\bigskip", 
     "%1675>%\n\\end{samepage}\n\\nopagebreak\n", 1),
    ("%1445>%", "%1445>%\n\\enlargethispage{1\\baselineskip}", 1),
    # 2019
    ("%1471>%\n\\end{samepage}\n\\filbreak", "%1471>%\n\\end{samepage}\n\\nopagebreak", 1),
    ("%1470>%\n\\end{samepage}\n\\filbreak\n\\bigskip", 
     "%1470>%\n\\end{samepage}\n\\nopagebreak\n\\bigskip\n", 1),

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
    ("\\end{samepage}\n\\filbreak\n\\bigskip\\begin{samepage}\n\\subsection*{{\\color{DarkRed}YLAB Prize~-- Communication}}\n%<2167%", 
     "\\end{samepage}\n\\nopagebreak\n\\bigskip\\begin{samepage}\n\\subsection*{{\\color{DarkRed}YLAB Prize~-- Communication}}\n%<2167%", 1),
    ("\\bigskip\\begin{samepage}\n\\section*{2023, Bari", 
     "\\pagebreak\\begin{samepage}\n\\section*{2023, Bari", 1),
    # 2023 - this is pretty tortured because the digital interactive motivation is sooo long
    ("\\end{samepage}\n\\filbreak\n\\bigskip\\begin{samepage}\n\\subsection*{{\\color{DarkRed}Prix~Italia Radio \\& Podcast Doc.~and Reportage}}\n%<2090%", 
     "\\end{samepage}\n\\nopagebreak\n\\begin{samepage}\n\\subsection*{{\\color{DarkRed}Prix~Italia Radio \\& Podcast Doc.~and Reportage}}\n%<2090%", 1),
    ("\\end{samepage}\n\\filbreak\n\\bigskip\\begin{samepage}\n\\subsection*{{\\color{DarkRed}Prix~Italia Digital Fiction}}\n%<2125%", 
     "\\end{samepage}\n\\nopagebreak\n\\begin{samepage}\n\\subsection*{{\\color{DarkRed}Prix~Italia Digital Fiction}}\n%<2125%", 1),
    ("\\end{samepage}\n\\filbreak\n\\bigskip\\begin{samepage}\n\\subsection*{{\\color{DarkRed}Prix~Italia Digital Factual}}\n%<2118%", 
     "\\end{samepage}\n\\nopagebreak\n\\begin{samepage}\n\\subsection*{{\\color{DarkRed}Prix~Italia Digital Factual}}\n%<2118%", 1),
    ("%2125>%", "%2125>%\n\\enlargethispage{2\\baselineskip}", 1),
    ("\\end{samepage}\n\\filbreak\n\\bigskip\\begin{samepage}\n\\subsection*{{\\color{DarkRed}YLAB~Prize~-- Engineering}}\n%<2162%", 
     "\\end{samepage}\n\\nopagebreak\n\\bigskip\\begin{samepage}\n\\subsection*{{\\color{DarkRed}YLAB~Prize~-- Engineering}}\n%<2162%", 1),
    ("\\bigskip\\begin{samepage}\n\\section*{2024, Torino", 
     "\\pagebreak\\begin{samepage}\n\\section*{2024, Torino", 1),

    # PART 3 -- more tweaks just for good looking
    # we add more space before some year sections
    ("\\begin{samepage}\n\\section*{1955, Perugia}", 
     "\\bigskip\\begin{samepage}\n\\section*{1955, Perugia}", 1),
    ("\\begin{samepage}\n\\section*{1956, Rimini}", 
     "\\bigskip\\begin{samepage}\n\\section*{1956, Rimini}", 1),
    ("\\begin{samepage}\n\\section*{1980, Riva del Garda}", 
     "\\bigskip\\begin{samepage}\n\\section*{1980, Riva del Garda}", 1),
    ("\\begin{samepage}\n\\section*{1984, Trieste}", 
     "\\bigskip\\begin{samepage}\n\\section*{1984, Trieste}", 1),
    ("\\begin{samepage}\n\\section*{1985, Cagliari}", 
     "\\bigskip\\begin{samepage}\n\\section*{1985, Cagliari}", 1),
    ("\\begin{samepage}\n\\section*{1991, Urbino/Pesaro}", 
     "\\bigskip\\begin{samepage}\n\\section*{1991, Urbino/Pesaro}", 1),
    ("\\begin{samepage}\n\\section*{1997, Ravenna}", 
     "\\bigskip\\begin{samepage}\n\\section*{1997, Ravenna}", 1),
    ("\\begin{samepage}\n\\section*{2010, Torino}", 
     "\\bigskip\\begin{samepage}\n\\section*{2010, Torino}", 1),
#    ("\\begin{samepage}\n\\section*{2015, Torino}", 
#     "\\bigskip\\begin{samepage}\n\\section*{2015, Torino}", 1),
#    ("\\begin{samepage}\n\\section*{2019, Roma}", 
#     "\\bigskip\\begin{samepage}\n\\section*{2019, Roma}", 1),
    # only starting from 2000 (because it's already too much of a pain...)
    # we also add more space between prizes, if needed
    # 1985 - ok this one is too ugly to not fix
    ("%366>%\n\\end{samepage}\n\\filbreak\n\\bigskip", 
     "%366>%\n\\end{samepage}\n\\filbreak\n\\bigskip\\bigskip", 1),
    ("%367>%\n\\end{samepage}\n\\filbreak\n\\bigskip", 
     "%367>%\n\\end{samepage}\n\\filbreak\n\\bigskip\\bigskip", 1),
    ("%368>%\n\\end{samepage}\n\\filbreak\n\\bigskip", 
     "%368>%\n\\end{samepage}\n\\filbreak\n\\bigskip\\bigskip", 1),
    # 2000
    ("%617>%\n\\end{samepage}\n\\filbreak\n\\bigskip", 
     "%617>%\n\\end{samepage}\n\\filbreak\n\\bigskip\\bigskip", 1),
    ("%632>%\n\\end{samepage}\n\\filbreak\n\\bigskip",
     "%632>%\n\\end{samepage}\n\\filbreak\n\\bigskip\\bigskip\\bigskip", 1), 
    # 2001
    ("%661>%\n\\end{samepage}\n\\filbreak", 
     "%661>%\n\\end{samepage}\n\\filbreak\\bigskip", 1),    
    ("%664>%\n\\end{samepage}\n\\filbreak\n\\bigskip",
     "%664>%\n\\end{samepage}\n\\filbreak\n\\bigskip\\bigskip", 1),
    ("%678>%\n\\end{samepage}\n\\filbreak\n\\bigskip",
     "%678>%\n\\end{samepage}\n\\filbreak\n\\bigskip\\bigskip", 1),
    ("%685>%\n\\end{samepage}\n\\filbreak", 
     "%685>%\n\\end{samepage}\n\\filbreak\\bigskip", 1),
    ("%1844>%\n\\end{samepage}\n\\filbreak\n\\bigskip",
     "%1844>%\n\\end{samepage}\n\\filbreak\n\\bigskip\\bigskip", 1),
    # 2002
    ("%707>%\n\\end{samepage}\n\\filbreak\n\\bigskip",
     "%707>%\n\\end{samepage}\n\\filbreak\n\\bigskip\\bigskip", 1),
    ("%712>%\n\\end{samepage}\n\\filbreak\n\\bigskip",
     "%712>%\n\\end{samepage}\n\\filbreak\n\\bigskip\\bigskip", 1),
    ("%715>%\n\\end{samepage}\n\\filbreak\n\\bigskip",
     "%715>%\n\\end{samepage}\n\\filbreak\n\\bigskip\\bigskip", 1),
    ("%1041>%\n\\end{samepage}\n\\filbreak\n\\bigskip",
     "%1041>%\n\\end{samepage}\n\\filbreak\n\\bigskip\\bigskip", 1),
    ("%746>%\n\\end{samepage}\n\\nopagebreak\n\\bigskip",
     "%746>%\n\\end{samepage}\n\\nopagebreak\n\\bigskip\\bigskip", 1),
    # 2003
    ("%763>%\n\\end{samepage}\n\\filbreak\n\\bigskip",
     "%763>%\n\\end{samepage}\n\\filbreak\n\\bigskip\\bigskip", 1),
    ("%1841>%\n\\end{samepage}\n\\filbreak\n\\bigskip",
     "%1841>%\n\\end{samepage}\n\\filbreak\n\\bigskip\\bigskip", 1),
    ("%1697>%\n\\end{samepage}\n\\nopagebreak\n\\bigskip",
     "%1697>%\n\\end{samepage}\n\\nopagebreak\n\\bigskip\\bigskip", 1),
    # 2004
    ("%1033>%\n\\end{samepage}\n\\filbreak\n\\bigskip",
     "%1033>%\n\\end{samepage}\n\\filbreak\n\\bigskip\\bigskip", 1),
    ("%797>%\n\\end{samepage}\n\\filbreak\n\\bigskip",
     "%797>%\n\\end{samepage}\n\\filbreak\n\\bigskip\\bigskip", 1),
    ("%813>%\n\\end{samepage}\n\\filbreak\n\\bigskip",
     "%813>%\n\\end{samepage}\n\\filbreak\n\\bigskip\\bigskip", 1),
    ("%814>%\n\\end{samepage}\n\\filbreak\n\\bigskip",
     "%814>%\n\\end{samepage}\n\\filbreak\n\\bigskip\\bigskip", 1),
    # 2005
    ("%1047>%\n\\end{samepage}\n\\filbreak\n\\bigskip",
     "%1047>%\n\\end{samepage}\n\\filbreak\n\\bigskip\\bigskip", 1),
    ("%1049>%\n\\end{samepage}\n\\filbreak\n\\bigskip",
     "%1049>%\n\\end{samepage}\n\\filbreak\n\\bigskip\\bigskip", 1),
    ("%852>%\n\\end{samepage}\n\\filbreak\n\\bigskip",
     "%852>%\n\\end{samepage}\n\\filbreak\n\\bigskip\\bigskip", 1),
    ("%868>%\n\\end{samepage}\n\\filbreak\n\\bigskip",
     "%868>%\n\\end{samepage}\n\\filbreak\n\\bigskip\\bigskip", 1),
    # 2006
    ("%879>%\n\\end{samepage}\n\\filbreak\n\\bigskip",
     "%879>%\n\\end{samepage}\n\\filbreak\n\\bigskip\\bigskip", 1),
    ("%906>%\n\\end{samepage}\n\\filbreak\n\\bigskip",
     "%906>%\n\\end{samepage}\n\\filbreak\n\\bigskip\\bigskip", 1),
    ("%909>%\n\\end{samepage}\n\\filbreak\n\\bigskip",
     "%909>%\n\\end{samepage}\n\\filbreak\n\\bigskip\\bigskip", 1),
    ("%913>%\n\\end{samepage}\n\\filbreak\n\\bigskip",
     "%913>%\n\\end{samepage}\n\\filbreak\n\\bigskip\\bigskip", 1),
    ("%922>%\n\\end{samepage}\n\\nopagebreak\n\\bigskip",   # \nopagebreak introduced earlier
     "%922>%\n\\end{samepage}\n\\nopagebreak\n\\bigskip\\bigskip", 1),
    # 2007
    ("%926>%\n\\end{samepage}\n\\filbreak\n\\bigskip",
     "%926>%\n\\end{samepage}\n\\filbreak\n\\bigskip\\bigskip", 1),
    ("%933>%\n\\end{samepage}\n\\filbreak\n\\bigskip",
     "%933>%\n\\end{samepage}\n\\filbreak\n\\bigskip\\bigskip", 1),
    ("%960>%\n\\end{samepage}\n\\filbreak\n\\bigskip",
     "%960>%\n\\end{samepage}\n\\filbreak\n\\bigskip\\bigskip", 1),
    ("%964>%\n\\end{samepage}\n\\filbreak\n\\bigskip",
     "%964>%\n\\end{samepage}\n\\filbreak\n\\bigskip\\bigskip", 1),
    ("%965>%\n\\end{samepage}\n\\nopagebreak\n\\bigskip",   # \nopagebreak introduced earlier
     "%965>%\n\\end{samepage}\n\\nopagebreak\n\\bigskip\\bigskip", 1),
    # 2008
    ("%971>%\n\\end{samepage}\n\\filbreak\n\\bigskip",
     "%971>%\n\\end{samepage}\n\\filbreak\n\\bigskip\\bigskip", 1),
    ("%977>%\n\\end{samepage}\n\\filbreak\n\\bigskip",
     "%977>%\n\\end{samepage}\n\\filbreak\n\\bigskip\\bigskip", 1),
    ("%983>%\n\\end{samepage}\n\\filbreak\n\\bigskip",
     "%983>%\n\\end{samepage}\n\\filbreak\n\\bigskip\\bigskip", 1),
    ("%998>%\n\\end{samepage}\n\\filbreak\n\\bigskip",
     "%998>%\n\\end{samepage}\n\\filbreak\n\\bigskip\\bigskip", 1),
    ("%1010>%\n\\end{samepage}\n\\filbreak\n\\bigskip",
     "%1010>%\n\\end{samepage}\n\\filbreak\n\\bigskip\\bigskip", 1),
    # 2009
    ("%1080>%\n\\end{samepage}\n\\filbreak\n\\bigskip",
     "%1080>%\n\\end{samepage}\n\\filbreak\n\\bigskip\\bigskip", 1),
    ("%1088>%\n\\end{samepage}\n\\filbreak\n\\bigskip",
     "%1088>%\n\\end{samepage}\n\\filbreak\n\\bigskip\\bigskip", 1),
    ("%1093>%\n\\end{samepage}\n\\filbreak\n\\bigskip",
     "%1093>%\n\\end{samepage}\n\\filbreak\n\\bigskip\\bigskip", 1),
    ("%1099>%\n\\end{samepage}\n\\filbreak\n\\bigskip",
     "%1099>%\n\\end{samepage}\n\\filbreak\n\\bigskip\\bigskip", 1),
    # 2010
    ("%1132>%\n\\end{samepage}\n\\filbreak\n\\bigskip",
     "%1132>%\n\\end{samepage}\n\\filbreak\n\\bigskip\\bigskip", 1),
    ("%1142>%\n\\end{samepage}\n\\filbreak\n\\bigskip",
     "%1142>%\n\\end{samepage}\n\\filbreak\n\\bigskip\\bigskip", 1),
    ("%1148>%\n\\end{samepage}\n\\filbreak\n\\bigskip",
     "%1148>%\n\\end{samepage}\n\\filbreak\n\\bigskip\\bigskip", 1),
    ("%1851>%\n\\end{samepage}\n\\filbreak\n\\bigskip",
     "%1851>%\n\\end{samepage}\n\\filbreak\n\\bigskip\\bigskip", 1),
    # 2011
    ("%1174>%\n\\end{samepage}\n\\filbreak\n\\bigskip",
     "%1174>%\n\\end{samepage}\n\\filbreak\n\\bigskip\\bigskip", 1),
    ("%1179>%\n\\end{samepage}\n\\filbreak\n\\bigskip",
     "%1179>%\n\\end{samepage}\n\\filbreak\n\\bigskip\\bigskip", 1),
    ("%1187>%\n\\end{samepage}\n\\filbreak\n\\bigskip",
     "%1187>%\n\\end{samepage}\n\\filbreak\n\\bigskip\\bigskip", 1),
    ("%1198>%\n\\end{samepage}\n\\filbreak\n\\bigskip",
     "%1198>%\n\\end{samepage}\n\\filbreak\n\\bigskip\\bigskip", 1),
    ("%1215>%\n\\end{samepage}\n\\filbreak\n\\bigskip",
     "%1215>%\n\\end{samepage}\n\\filbreak\n\\bigskip\\bigskip", 1),
    ("%1218>%\n\\end{samepage}\n\\filbreak\n\\bigskip",
     "%1218>%\n\\end{samepage}\n\\filbreak\n\\bigskip\\bigskip", 1),
    # 2012
    ("%1261>%\n\\end{samepage}\n\\filbreak\n\\bigskip",
     "%1261>%\n\\end{samepage}\n\\filbreak\n\\bigskip\\bigskip", 1),
    ("%1272>%\n\\end{samepage}\n\\filbreak\n\\bigskip",
     "%1272>%\n\\end{samepage}\n\\filbreak\n\\bigskip\\bigskip", 1),
    ("%1274>%\n\\end{samepage}\n\\filbreak\n\\bigskip",
     "%1274>%\n\\end{samepage}\n\\filbreak\n\\bigskip\\bigskip", 1),
    ("%1279>%\n\\end{samepage}\n\\filbreak\n\\bigskip",
     "%1279>%\n\\end{samepage}\n\\filbreak\n\\bigskip\\bigskip", 1),
    # 2013
    ("%1288>%\n\\end{samepage}\n\\filbreak\n\\bigskip",
     "%1288>%\n\\end{samepage}\n\\filbreak\n\\bigskip\\bigskip", 1),
    ("%1295>%\n\\end{samepage}\n\\filbreak\n\\bigskip",
     "%1295>%\n\\end{samepage}\n\\filbreak\n\\bigskip\\bigskip", 1),
    ("%1301>%\n\\end{samepage}\n\\filbreak\n\\bigskip",
     "%1301>%\n\\end{samepage}\n\\filbreak\n\\bigskip\\bigskip", 1),
    ("%1303>%\n\\end{samepage}\n\\filbreak\n\\bigskip",
     "%1303>%\n\\end{samepage}\n\\filbreak\n\\bigskip\\bigskip", 1),
    ("%1308>%\n\\end{samepage}\n\\filbreak\n\\bigskip",
     "%1308>%\n\\end{samepage}\n\\filbreak\n\\bigskip\\bigskip", 1),
    ("%1323>%\n\\end{samepage}\n\\filbreak\n\\bigskip",
     "%1323>%\n\\end{samepage}\n\\filbreak\n\\bigskip\\bigskip", 1),
    # 2014
    ("%2266>%\n\\end{samepage}\n\\filbreak\n\\bigskip",
     "%2266>%\n\\end{samepage}\n\\filbreak\n\\bigskip\\bigskip", 1),
    # 2015
    ("%1558>%\n\\end{samepage}\n\\filbreak\n\\bigskip",
     "%1558>%\n\\end{samepage}\n\\filbreak\n\\bigskip\\bigskip", 1),
    ("%1403>%\n\\end{samepage}\n\\filbreak\n\\bigskip",
     "%1403>%\n\\end{samepage}\n\\filbreak\n\\bigskip\\bigskip", 1),
    # 2016
    ("%1582>%\n\\end{samepage}\n\\filbreak\n\\bigskip",
     "%1582>%\n\\end{samepage}\n\\filbreak\n\\bigskip\\bigskip", 1),
    # 2018
    ("%1639>%\n\\end{samepage}\n\\filbreak\n\\bigskip",
     "%1639>%\n\\end{samepage}\n\\filbreak\n\\bigskip\\bigskip", 1),
    ("%1650>%\n\\end{samepage}\n\\filbreak\n\\bigskip",
     "%1650>%\n\\end{samepage}\n\\filbreak\n\\bigskip\\bigskip", 1),
    ("%1672>%\n\\end{samepage}\n\\filbreak\n\\bigskip",
     "%1672>%\n\\end{samepage}\n\\filbreak\n\\bigskip\\bigskip", 1),
    # 2019
    ("%2012>%\n\\end{samepage}\n\\filbreak\n\\bigskip",
     "%2012>%\n\\end{samepage}\n\\filbreak\n\\bigskip\\bigskip", 1),
    ("%2024>%\n\\end{samepage}\n\\filbreak\n\\bigskip",
     "%2024>%\n\\end{samepage}\n\\filbreak\n\\bigskip\\bigskip", 1),
    ("%2036>%\n\\end{samepage}\n\\filbreak\n\\bigskip",
     "%2036>%\n\\end{samepage}\n\\filbreak\n\\bigskip\\bigskip", 1),
    ("%2044>%\n\\end{samepage}\n\\filbreak\n\\bigskip",
     "%2044>%\n\\end{samepage}\n\\filbreak\n\\bigskip\\bigskip", 1),
    # 2020
    ("%1964>%\n\\end{samepage}\n\\filbreak\n\\bigskip",
     "%1964>%\n\\end{samepage}\n\\filbreak\n\\bigskip\\bigskip", 1),
    ("%1986>%\n\\end{samepage}\n\\filbreak\n\\bigskip",
     "%1986>%\n\\end{samepage}\n\\filbreak\n\\bigskip\\bigskip", 1),
    ("%1978>%\n\\end{samepage}\n\\filbreak\n\\bigskip",
     "%1978>%\n\\end{samepage}\n\\filbreak\n\\bigskip\\bigskip", 1),
    # 2021
    ("%1927>%\n\\end{samepage}\n\\filbreak\n\\bigskip",
     "%1927>%\n\\end{samepage}\n\\filbreak\n\\bigskip\\bigskip", 1),
    ("%1935>%\n\\end{samepage}\n\\filbreak\n\\bigskip",
     "%1935>%\n\\end{samepage}\n\\filbreak\n\\bigskip\\bigskip", 1),
    ("%1944>%\n\\end{samepage}\n\\filbreak\n\\bigskip",
     "%1944>%\n\\end{samepage}\n\\filbreak\n\\bigskip\\bigskip", 1),
    ("%1957>%\n\\end{samepage}\n\\filbreak\n\\bigskip",
     "%1957>%\n\\end{samepage}\n\\filbreak\n\\bigskip\\bigskip", 1),
    ("%1517>%\n\\end{samepage}\n\\nopagebreak\n\\bigskip",   # \nopagebreak introduced earlier
     "%1517>%\n\\end{samepage}\n\\nopagebreak\n\\bigskip\\bigskip", 1),
    # 2022
    ("%1870>%\n\\end{samepage}\n\\filbreak\n\\bigskip",
     "%1870>%\n\\end{samepage}\n\\filbreak\n\\bigskip\\bigskip", 1),
    ("%1889>%\n\\end{samepage}\n\\filbreak\n\\bigskip",
     "%1889>%\n\\end{samepage}\n\\filbreak\n\\bigskip\\bigskip", 1),
    ("%1901>%\n\\end{samepage}\n\\filbreak\n\\bigskip",
     "%1901>%\n\\end{samepage}\n\\filbreak\n\\bigskip\\bigskip", 1),
    ("%1913>%\n\\end{samepage}\n\\filbreak\n\\bigskip",
     "%1913>%\n\\end{samepage}\n\\filbreak\n\\bigskip\\bigskip", 1),
    ("%1544>%\n\\end{samepage}\n\\filbreak\n\\bigskip",
     "%1544>%\n\\end{samepage}\n\\filbreak\n\\bigskip\\bigskip", 1),
    ("%2166>%\n\\end{samepage}\n\\nopagebreak\n\\bigskip",   # \nopagebreak introduced earlier
     "%2166>%\n\\end{samepage}\n\\nopagebreak\n\\bigskip\\bigskip", 1),
    # 2023
    ("%2103>%\n\\end{samepage}\n\\filbreak\n\\bigskip",
     "%2103>%\n\\end{samepage}\n\\filbreak\n\\bigskip\\bigskip", 1),
    ("%2153>%\n\\end{samepage}\n\\filbreak\n\\bigskip",
     "%2153>%\n\\end{samepage}\n\\filbreak\n\\bigskip\\bigskip", 1),
    ("%2164>%\n\\end{samepage}\n\\nopagebreak\n\\bigskip",   # \nopagebreak introduced earlier
     "%2164>%\n\\end{samepage}\n\\nopagebreak\n\\bigskip\\bigskip", 1),
    )
silver_broadcasters_txt = tuple()
silver_broadcasters_html = tuple()
silver_broadcasters_tex = (
    # forced linebreaks (to avoid overfull boxes)
    ("Belgische Radio-~en~Televisieomroep/ Radio-Télévision Belge",
     "Belgische Radio-~en~Televisieomroep/\\\\Radio-Télévision Belge", 2),
    ("Canadian Broadcasting Corporation/ Société Radio-Canada",
     "Canadian Broadcasting Corporation/\\\\Société Radio-Canada", 1),
    ("ARTE Groupement Européen d'Intérêt Économique}}{\\itshape 2019",
     "ARTE\\\\Groupement Européen d'Intérêt Économique}}{\\itshape 2019", 1),
    # forced linebreaks and other tricks (aesthetics only)
    ("Établissement Public de~Télévision/ Télévision Algérienne",
      "Établissement Public de~Télévision/\\\\Télévision Algérienne", 1),
    ("Balgarska Natsionalna Televizia/ Bulgarian National Television",
     "Balgarska Natsionalna Televizia/\\\\Bulgarian National Television", 1),
    ("Bǎlgarsko Nacionalno Radio/ Bulgarian National Radio",
     "Bǎlgarsko Nacionalno Radio/\\\\Bulgarian National Radio", 1),
    ("Cameroon Radio Television/ Radiodiffusion-télévision du~Cameroun",
     "Cameroon Radio Television/\\\\Radiodiffusion-télévision du~Cameroun", 1),
    ("section*{Czech~Rep.}", "section*{Czech~Republic}", 1),
    ("Société européenne de~programmes de~télévision}}1989", 
     "Société européenne de~programmes\\\\de~télévision}}1989", 1),
    ("al-Mis'ri/ Egyptian Radio and Television Union",
     "al-Mis'ri/\\\\Egyptian Radio and Television Union", 1),
    ("mauts'q'ebeli/ Georgian Public Broadcasting",
     "mauts'q'ebeli/\\\\Georgian Public Broadcasting", 1),
    ("Ríkisútvarpið/ The~Icelandic National Broadcasting Service",
     "Ríkisútvarpið/\\\\The~Icelandic National Broadcasting Service", 1),
    ("National Association of~Commercial Broadcasters in~Japan", 
     "National Association of~Commercial Broadcasters\\\\in~Japan", 1),
    ("al'urduniyi/ Jordan Radio", 
     "al'urduniyi/\\\\Jordan Radio", 1),
    ("Bangsong Gongsa/ Korean Broadcasting",
     "Bangsong Gongsa/\\\\Korean Broadcasting", 1), 
    ("Munhwa Bangsong/ Munhwa Broadcasting",
     "Munhwa Bangsong/\\\\Munhwa Broadcasting", 1), 
    ("Radio~Televizioni i~Kosovës/ Radio Television of~Kosovo",
     "Radio~Televizioni i~Kosovës/ Radio Television of~Kosovo~", 1),
    ("voor~de~Radio-omroep/ Institut National de~Radiodiffusion", 
     "voor~de~Radio-omroep/\\\\Institut National de~Radiodiffusion", 1),
    ("al-Filasṭīniyya/ Palestinian Broadcasting Corporation", 
     "al-Filasṭīniyya/\\\\Palestinian Broadcasting Corporation", 1), 
    ("Golos Rossii/ Voice of~Russia", "Golos Rossii/\\\\Voice of~Russia", 1), 
    ("Elektronskih Medija/ Association of~Independent Electronic Media",
     "Elektronskih Medija/\\\\Association of~Independent Electronic Media", 3), 
    ("Thai Public Broadcasting Service", "Thai Public Broadcasting Service~", 1), 
    ("radio/ National Radio Company of~Ukraine", 
     "radio/\\\\National Radio Company of~Ukraine", 1),
    ("Television Authority/ Independent Television", 
     "Television Authority/\\\\Independent Television", 1), 
    ("Broadcasting Authority/ Independent Television", 
     "Broadcasting Authority/\\\\Independent Television", 1), 
                          )
silver_other_participants_txt = tuple()
silver_other_participants_html = tuple()
silver_other_participants_tex = tuple()
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

    ('silver participants', 'txt'): silver_other_participants_txt,
    ('silver participants', 'html'): silver_other_participants_html,
    ('silver participants', 'tex'): silver_other_participants_tex,

    ('silver milestones', 'txt'): silver_milestones_txt,
    ('silver milestones', 'html'): silver_milestones_html,
    ('silver milestones', 'tex'): silver_milestones_tex,

    ('silver book', 'txt'): (silver_intro_txt + silver_winners_txt 
                             + silver_broadcasters_txt + silver_other_participants_txt 
                             + silver_milestones_txt),
    ('silver book', 'html'): (silver_intro_html + silver_winners_html 
                              + silver_broadcasters_html+ silver_other_participants_html 
                              + silver_milestones_html),
    ('silver book', 'tex'): (silver_intro_tex + silver_winners_tex 
                             + silver_broadcasters_tex + silver_other_participants_tex 
                             + silver_milestones_tex),


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
    if out_type == 'tex':
        replacements = PRIZE_NAMES_TEX + PRIZE_NAMES_ABBR_TEX + \
            BROADCASTER_NAMES_TEX + BROADCASTER_ACRONYMS_TEX + \
            COUNTRY_NAMES_TEX + COUNTRY_NAMES_ABBR_TEX + replacements
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
