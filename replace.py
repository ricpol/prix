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
    ("\n%691>%\n\\\\ \\\\\n", "\n\\\\ \\\\\n", 1),
    # This is for the multimedia section prize 2012
    ("Il Post (Italy)", 
     "Italy", 1),
    # This is for the multimedia section prize 2013
    ("Piccolo Teatro Milano (Italy)", 
     "Italy", 1),
    # the short names here are just too long...
    ("La Sept -- Société européenne de programmes de télévision (France)",
     "La Sept (France)", 3),
    ("ARTE Groupement Européen d'Intérêt Économique (France)",
     "ARTE GEIE (France", 1),
    # a programme title...
    ("Annie M. G.", "Annie M.~G.", 1),
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
    # 1954 [just for good looking] [spread more]
    ("\n%33>%", "\\medskip\n%33>%", 1),
    ("\n%34>%", "\\medskip\n%34>%", 1),
    ("\n%35>%", "\\medskip\n%35>%", 1),
    ("\n%36>%", "\\medskip\n%36>%", 1),
    ("\n%37>%", "\\medskip\n%37>%", 1),
    ("\n%38>%", "\\medskip\n%38>%", 1),
    # -----------------------------------------------------------------
    # 1957 [just for good looking] [spread more]
    ("\n%48>%", "\\bigskip\n%48>%", 1),
    ("\n%49>%", "\\bigskip\n%49>%", 1),
    ("\n%50>%", "\\bigskip\n%50>%", 1),
    ("\n%51>%", "\\bigskip\n%51>%", 1),
    ("\n%52>%", "\\bigskip\n%52>%", 1),
    ("\n%53>%", "\\bigskip\n%53>%", 1),
    # -----------------------------------------------------------------
    # 1958 [just for good looking] [spread more]
    ("\n%55>%", "\\medskip\n%55>%", 1),
    ("\n%56>%", "\\medskip\n%56>%", 1),
    ("\n%57>%", "\\medskip\n%57>%", 1),
    ("\n%58>%", "\\medskip\n%58>%", 1),
    ("\n%59>%", "\\medskip\n%59>%", 1),
    ("\n%60>%", "\\medskip\n%60>%", 1),
    # -----------------------------------------------------------------
    # 1961 [just for good looking] [shrink the space above the section]
    ("\n%79>%", "\\vspace{-4pt}\n%79>%", 1),
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
    # 1964 / 1 [just for good looking] [spread more]
    ("\n%107>%", "\\smallskip\n%107>%", 1),
    ("\n%108>%", "\\smallskip\n%108>%", 1),
    ("\n%109>%", "\\smallskip\n%109>%", 1),
    ("\n%110>%", "\\smallskip\n%110>%", 1),
    ("\n%111>%", "\\smallskip\n%111>%", 1),
    ("\n%112>%", "\\smallskip\n%112>%", 1),
    # -----------------------------------------------------------------
    # 1964 / 2 [just for good looking] [spread more]
    ("\n%114>%", "\\medskip\n%114>%", 1),
    ("\n%115>%", "\\medskip\n%115>%", 1),
    ("\n%116>%", "\\medskip\n%116>%", 1),
    ("\n%117>%", "\\medskip\n%117>%", 1),
    ("\n%118>%", "\\medskip\n%118>%", 1),
    ("\n%119>%", "\\medskip\n%119>%", 1),
    ("\n%120>%", "\\medskip\n%120>%", 1),
    # -----------------------------------------------------------------
    # 1966 [just for good looking] [spread more]
    ("\n%130>%", "\\smallskip\n%130>%", 1),
    ("\n%131>%", "\\smallskip\n%131>%", 1),
    ("\n%132>%", "\\smallskip\n%132>%", 1),
    ("\n%133>%", "\\smallskip\n%133>%", 1),
    ("\n%134>%", "\\smallskip\n%134>%", 1),
    ("\n%135>%", "\\smallskip\n%135>%", 1),
    # -----------------------------------------------------------------
    # 1969 / 1 [just for good looking] [spread more]
    ("\n%160>%", "\\smallskip\n%160>%", 1),
    ("\n%161>%", "\\smallskip\n%161>%", 1),
    ("\n%162>%", "\\smallskip\n%162>%", 1),
    ("\n%2074>%", "\\smallskip\n%2074>%", 1),
    ("\n%163>%", "\\smallskip\n%163>%", 1),
    ("\n%164>%", "\\smallskip\n%164>%", 1),
    # -----------------------------------------------------------------
    # 1969 / 2 [spread more and force pagebreak]
    ("\n%166>%", "\\bigskip\n%166>%", 1),
    ("\n%167>%", "\\bigskip\n%167>%", 1),
    ("\n%168>%", "\\bigskip\n%168>%", 1),
    ("\n%169>%", "\\bigskip\n%169>%", 1),
    ("\n%170>%", "\\bigskip\n%170>%", 1),
    ("\n%171>%", "\\bigskip\n%171>%", 1),
    ("%172>%", "%172>%\n\\pagebreak", 1),
    # -----------------------------------------------------------------
    # 1972 [spread more and force pagebreak]
    ("\n%196>%", "\\bigskip\n%196>%", 1),
    ("\n%197>%", "\\bigskip\n%197>%", 1),
    ("\n%198>%", "\\bigskip\n%198>%", 1),
    ("\n%199>%", "\\bigskip\n%199>%", 1),
    ("\n%200>%", "\\bigskip\n%200>%", 1),
    ("\n%201>%", "\\bigskip\n%201>%", 1),
    ("%202>%", "%202>%\n\\pagebreak", 1),
    # -----------------------------------------------------------------
    # 1974 / 1 [just for good looking] [spread more]
    ("\n%211>%", "\\medskip\n%211>%", 1),
    ("\n%212>%", "\\medskip\n%212>%", 1),
    ("\n%213>%", "\\medskip\n%213>%", 1),
    ("\n\n%214>%", "\\medskip\n%214>%", 1), # a little different...
    ("\n%215>%", "\\medskip\n%215>%", 1),
    ("\n%216>%", "\\medskip\n%216>%", 1),
    ("\n\n%217>%", "\\medskip\n%217>%", 1), # a little different...
    # -----------------------------------------------------------------
    # 1974 / 2 [just for good looking] [spread more]
    ("\n%219>%", "\\bigskip\n%219>%", 1),
    ("\n%220>%", "\\bigskip\n%220>%", 1),
    ("\n%221>%", "\\bigskip\n%221>%", 1),
    ("\n%222>%", "\\bigskip\n%222>%", 1),
    ("\n%223>%", "\\bigskip\n%223>%", 1),
    ("\n%224>%", "\\bigskip\n%224>%", 1),
    # -----------------------------------------------------------------
    # 1977 / 1 [just for good looking] [spread more]
    ("\n%246>%", "\\medskip\n%246>%", 1),
    ("\n%247>%", "\\medskip\n%247>%", 1),
    ("\n%248>%", "\\medskip\n%248>%", 1),
    ("\n%249>%", "\\medskip\n%249>%", 1),
    ("\n%250>%", "\\medskip\n%250>%", 1),
    # -----------------------------------------------------------------
    # 1977 / 2 [just for good looking] [spread more]
    ("\n%252>%", "\\medskip\n%252>%", 1),
    ("\n%253>%", "\\medskip\n%253>%", 1),
    ("\n%254>%", "\\medskip\n%254>%", 1),
    ("\n%255>%", "\\medskip\n%255>%", 1),
    ("\n%256>%", "\\medskip\n%256>%", 1),
    ("\n%257>%", "\\medskip\n%257>%", 1),
    # -----------------------------------------------------------------
    # 1978 [add a line to bottom]
        # NOTE: this is the "right" place to add the command
        # on the same line of \subsection. Strangely enough, if we 
        # add the command on a single line, *and* there is a box full 
        # to the limit, latex will add extra space here.
        # So, the *wrong* way is
        # "%previous#>%", "%previous#>%\n\\enlarge..."
        # and the "*right* way is
        # "%<next#%\n", "%<next#%\n\\enlarge..."
    ("%<273%\n", "%<273%\n\\enlargethispage{1\\baselineskip}", 1),
    # -----------------------------------------------------------------
    # 1981 [just for good looking] [spread more]
    ("\n%303>%", "\\smallskip\n%303>%", 1),
    ("\n%304>%", "\\smallskip\n%304>%", 1),
    ("\n%305>%", "\\smallskip\n%305>%", 1),
    ("\n%306>%", "\\smallskip\n%306>%", 1),
    ("\n%307>%", "\\smallskip\n%307>%", 1),
    ("\n%308>%", "\\smallskip\n%308>%", 1),
    # -----------------------------------------------------------------
    # 1983 [just for good looking] [spread more]
    ("\n%322>%", "\\smallskip\n%322>%", 1),
    ("\n%326>%", "\\smallskip\n%326>%", 1),
    ("\n%330>%", "\\smallskip\n%330>%", 1),
    ("\n%331>%", "\\smallskip\n%331>%", 1),
    ("\n%332>%", "\\smallskip\n%332>%", 1),
    ("\n%333>%", "\\smallskip\n%333>%", 1),
    # -----------------------------------------------------------------
    # 1984 [add a line to bottom]
    ("%<357%\n", "%<357%\n\\enlargethispage{1\\baselineskip}", 1),
    # -----------------------------------------------------------------
    # 1986 [just for good looking] [spread more]
    ("\n%372>%", "\\medskip\n%372>%", 1),
    ("\n%373>%", "\\medskip\n%373>%", 1),
    ("\n\n%374>%", "\\medskip\n%374>%", 1), # a little different
    ("\n%375>%", "\\medskip\n%375>%", 1),
    ("\n%376>%", "\\medskip\n%376>%", 1),
    ("\n%377>%", "\\medskip\n%377>%", 1),
    ("\n%378>%", "\\medskip\n%378>%", 1),
    # -----------------------------------------------------------------
    # 1988 / 1 [just for good looking] [spread more]
    ("\n%395>%", "\\medskip\n%395>%", 1),
    ("\n%396>%", "\\medskip\n%396>%", 1),
    ("\n%397>%", "\\medskip\n%397>%", 1),
    ("\n%398>%", "\\medskip\n%398>%", 1),
    ("\n%399>%", "\\medskip\n%399>%", 1),
    ("\n%401>%", "\\medskip\n%401>%", 1),
    ("\n%403>%", "\\medskip\n%403>%", 1),
    # -----------------------------------------------------------------
    # 1988 / 2 [just for good looking] [spread more]
    ("\n%409>%", "\\medskip\n%409>%", 1),
    ("\n%411>%", "\\medskip\n%411>%", 1),
    ("\n%400>%", "\\medskip\n%400>%", 1),
    ("\n%402>%", "\\medskip\n%402>%", 1),
    ("\n%405>%", "\\medskip\n%405>%", 1),
    ("\n%408>%", "\\medskip\n%408>%", 1),
    ("\n%410>%", "\\medskip\n%410>%", 1),
    # -----------------------------------------------------------------
    # 1989 / 1 [add a line to bottom]
    ("%<419%\n", "%<419%\n\\enlargethispage{1\\baselineskip}", 1),
    # -----------------------------------------------------------------
    # 1989 / 2 [just for good looking] [spread more]
    ("\n%422>%", "\\medskip\n%422>%", 1),
    ("\n%424>%", "\\medskip\n%424>%", 1),
    ("\n%426>%", "\\medskip\n%426>%", 1),
    ("\n%416>%", "\\medskip\n%416>%", 1),
    ("\n%418>%", "\\medskip\n%418>%", 1),
    ("\n%420>%", "\\medskip\n%420>%", 1),
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
    ("%<447%\n", "%<447%\n\\enlargethispage{1\\baselineskip}", 1),
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
    # 1993 [just for good looking] [spread more]
    ("\n%480>%", "\\smallskip\n%480>%", 1),
    ("\n%482>%", "\\smallskip\n%482>%", 1),
    ("\n%484>%", "\\smallskip\n%484>%", 1),
    ("\n%486>%", "\\smallskip\n%486>%", 1),
    ("\n%488>%", "\\smallskip\n%488>%", 1),
    ("\n%479>%", "\\smallskip\n%479>%", 1),
    # -----------------------------------------------------------------
    # 1994 / 1 [add a line to bottom, shrink space before section]
    ("\n%1860>%", "\\vspace{-4pt}\n%1860>%", 1),
    ("%<537%\n", "%<537%\n\\enlargethispage{1\\baselineskip}", 1),
    # -----------------------------------------------------------------
    # 1994 / 2 [add a line to bottom]
    ("%<1861%\n", "%<1861%\n\\enlargethispage{1\\baselineskip}", 1),
    # -----------------------------------------------------------------
    # 1995 [add a line to bottom, shrink space before section]
    ("\n%1862>%", "\\vspace{-4pt}\n%1862>%", 1),
    ("%<548%\n", "%<548%\n\\enlargethispage{1\\baselineskip}", 1),
    # -----------------------------------------------------------------
    # 1996 [add a line to bottom]
    ("%<555%\n", "%<555%\n\\enlargethispage{1\\baselineskip}", 1),
    # -----------------------------------------------------------------
    # 1997 [just for good looking] [spread more]
    ("\n%494>%", "\\smallskip\n%494>%", 1),
    ("\n%558>%", "\\smallskip\n%558>%", 1),
    ("\n%560>%", "\\smallskip\n%560>%", 1),
    ("\n%495>%", "\\smallskip\n%495>%", 1),
    ("\n%562>%", "\\smallskip\n%562>%", 1),
    ("\n%563>%", "\\smallskip\n%563>%", 1),
    # -----------------------------------------------------------------
    # 1999 [just for good looking] [spread more]
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
    ("\n%615>%", "\\vspace{-2pt}\n%615>%", 1),
    ("\n%616>%", "\\vspace{-2pt}\n%615>%", 1),
    ("\n%619>%", "\\vspace{-2pt}\n%615>%", 1),
    ("\n%622>%", "\\vspace{-2pt}\n%615>%", 1),
    ("\n%623>%", "\\vspace{-2pt}\n%615>%", 1),
    ("\n\n%626>%", "\\vspace{-2pt}\n%615>%", 1), # a little different...
    ("%<627%\n", "%<627%\n\\enlargethispage{1\\baselineskip}", 1),
    # -----------------------------------------------------------------
    # 2002 / [spread more, the pagebreak will happen "naturally"]
    ("\n%692>%", "\\medskip\n%692>%", 1),
    ("\n%697>%", "\\medskip\n%697>%", 1),
    ("\n%698>%", "\\medskip\n%698>%", 1),
    ("\n%702>%", "\\medskip\n%702>%", 1),
    ("\n%699>%", "\\medskip\n%699>%", 1),
    ("\n%705>%", "\\medskip\n%705>%", 1),
    # -----------------------------------------------------------------
    # 2002 / 2 [shrink the page adding negative space, add a line to bottom]
    # this is a little too dense maybe?
    ("\n%708>%", "\\vspace{-4pt}\n%708>%", 1),
    ("\n%711>%", "\\vspace{-4pt}\n%708>%", 1),
    ("\n%714>%", "\\vspace{-4pt}\n%708>%", 1),
    ("\n\n%717>%", "\\vspace{-4pt}\n%708>%", 1), # a little different...
    ("\n%720>%", "\\vspace{-4pt}\n%708>%", 1),
    ("\n%723>%", "\\vspace{-4pt}\n%708>%", 1),
    ("\n%726>%", "\\vspace{-4pt}\n%708>%", 1),
    ("%<729%\n", "%<729%\n\\enlargethispage{2\\baselineskip}", 1),
    # -----------------------------------------------------------------
    # 2004 [just for good looking] [spread more]
    ("\n%508>%", "\\smallskip\n%508>%", 1),
    ("\n%804>%", "\\smallskip\n%804>%", 1),
    ("\n%808>%", "\\smallskip\n%808>%", 1),
    ("\n%811>%", "\\smallskip\n%811>%", 1),
    ("\n%509>%", "\\smallskip\n%509>%", 1),
    ("\n%815>%", "\\smallskip\n%815>%", 1),
    # -----------------------------------------------------------------
    # 2005 [spread more, the pagebreak will happen "naturally"]
    ("\n%839>%", "\\medskip\n%839>%", 1),
    ("\n%510>%", "\\medskip\n%510>%", 1),
    ("\n%844>%", "\\medskip\n%844>%", 1),
    ("\n%842>%", "\\medskip\n%842>%", 1),
    ("\n%848>%", "\\medskip\n%848>%", 1),
    ("\n%851>%", "\\medskip\n%851>%", 1),
    # -----------------------------------------------------------------
    # 2006 / 1 [shrink the page adding negative space, add a line to bottom]
    ("\n%1852>%", "\\vspace{-2pt}\n%1852>%", 1),
    ("\n%873>%", "\\vspace{-10pt}\n%873>%", 1),
    ("\n%877>%", "\\vspace{-2pt}\n%877>%", 1),
    ("\n%880>%", "\\vspace{-2pt}\n%880>%", 1),
    ("\n%883>%", "\\vspace{-2pt}\n%883>%", 1),
    ("\n%887>%", "\\vspace{-2pt}\n%887>%", 1),
    ("%<890%\n", "%<890%\n\\enlargethispage{1\\baselineskip}", 1),
    # -----------------------------------------------------------------
    # 2006 / 2 [spread more, pagebreak will happen "naturally"]
    ("\n%893>%", "\\medskip\n%893>%", 1),
    ("\n%896>%", "\\medskip\n%896>%", 1),
    ("\n%899>%", "\\medskip\n%899>%", 1),
    ("\n%901>%", "\\medskip\n%901>%", 1),
    ("\n%904>%", "\\medskip\n%904>%", 1),
    ("\n%907>%", "\\medskip\n%907>%", 1),
    ("\n%910>%", "\\medskip\n%910>%", 1),
    # -----------------------------------------------------------------
    # 2007 [spread more and force pagebreak]
    ("\n%511>%", "\\medskip\n%511>%", 1),
    ("\n%512>%", "\\medskip\n%512>%", 1),
    ("\n%941>%", "\\medskip\n%941>%", 1),
    ("\n%513>%", "\\medskip\n%513>%", 1),
    ("\n%945>%", "\\medskip\n%945>%", 1),
    ("\n%947>%", "\\medskip\n%947>%", 1),
    ("%514>%", "%514>%\n\\pagebreak", 1),
    # -----------------------------------------------------------------
    # 2008 / 1 [just for good looking] [spread more]
    ("\n%967>%", "\\smallskip\n%967>%", 1),
    ("\n%968>%", "\\smallskip\n%968>%", 1),
    ("\n%972>%", "\\smallskip\n%972>%", 1),
    ("\n%975>%", "\\smallskip\n%975>%", 1),
    ("\n%978>%", "\\smallskip\n%978>%", 1),
    # -----------------------------------------------------------------
    # 2008 / 2 [spread more and force pagebreak]
    ("\n%986>%", "\\bigskip\n%986>%", 1),
    ("\n%988>%", "\\bigskip\n%988>%", 1),
    ("\n%991>%", "\\bigskip\n%991>%", 1),
    ("\n%994>%", "\\bigskip\n%994>%", 1),
    ("\n%997>%", "\\bigskip\n%997>%", 1),
    ("%999>%", "%999>%\n\\pagebreak", 1),
    # -----------------------------------------------------------------
    # 2011 / 1 [just for good looking] [spread more]
    ("\n%1161>%", "\\medskip\n%978>%", 1),
    ("\n%1159>%", "\\medskip\n%978>%", 1),
    ("\n%1162>%", "\\medskip\n%978>%", 1),
    ("\n%1165>%", "\\medskip\n%978>%", 1),
    ("\n%1167>%", "\\medskip\n%978>%", 1),
    # -----------------------------------------------------------------
    # 2011 / 2 [add a line to bottom]
    ("%<1223%\n", "%<1223%\n\\enlargethispage{1\\baselineskip}", 1),
    # -----------------------------------------------------------------
    # 2012 / 1 [shrink the page adding negative space, add a line to bottom]
    ("\n%1229>%", "\\vspace{-2pt}\n%1229>%", 1),
    ("\n%1232>%", "\\vspace{-2pt}\n%1232>%", 1),
    ("\n%1235>%", "\\vspace{-2pt}\n%1235>%", 1),
    ("\n%1238>%", "\\vspace{-2pt}\n%1238>%", 1),
    ("\n%1241>%", "\\vspace{-2pt}\n%1241>%", 1),
    ("\n%518>%", "\\vspace{-2pt}\n%518>%", 1),
    ("\n%1246>%", "\\vspace{-2pt}\n%1246>%", 1),
    ("%<1249%\n", "%<1249%\n\\enlargethispage{1\\baselineskip}", 1),
    # -----------------------------------------------------------------
    # 2012 / 2 [spread more, pagebreak will happen "naturally"]
    ("\n%1253>%", "\\bigskip\n%1253>%", 1),
    ("\n%1256>%", "\\bigskip\n%1256>%", 1),
    ("\n%1259>%", "\\bigskip\n%1259>%", 1),
    ("\n%1262>%", "\\bigskip\n%1262>%", 1),
    ("\n%1269>%", "\\bigskip\n%1269>%", 1),
    # -----------------------------------------------------------------
    # 2012 / 3 [just for good looking] [spread more]
    ("\n%1273>%", "\\medskip\n%1273>%", 1),
    ("\n\n%1276>%", "\\medskip\n%1276>%", 1), # a little different...
    ("\n%1277>%", "\\medskip\n%1277>%", 1),
    ("\n%1280>%", "\\medskip\n%1280>%", 1),
    ("\n%1283>%", "\\medskip\n%1283>%", 1),
    # -----------------------------------------------------------------
    # 2014 [just for good looking] [spread more]
    ("\n%1362>%", "\\smallskip\n%1362>%", 1),
    ("\n%1366>%", "\\smallskip\n%1366>%", 1),
    ("\n%1363>%", "\\smallskip\n%1363>%", 1),
    ("\n%1369>%", "\\smallskip\n%1369>%", 1),
    ("\n%1370>%", "\\smallskip\n%1370>%", 1),
    # -----------------------------------------------------------------
    # 2015 / 1 [just for good looking] [spread more]
    ("\n%1373>%", "\\medskip\n%1373>%", 1),
    ("\n%1374>%", "\\medskip\n%1374>%", 1),
    ("\n%1376>%", "\\medskip\n%1376>%", 1),
    ("\n\n%1377>%", "\\medskip\n%1377>%", 1), # a little different...
    ("\n%1378>%", "\\medskip\n%1378>%", 1),
    ("\n\n%1379>%", "\\medskip\n%1379>%", 1), # a little different...
    # -----------------------------------------------------------------
    # 2015 / 2 [spread more and force pagebreak]
    ("\n%1391>%", "\\medskip\n%1391>%", 1),
    ("\n%1399>%", "\\medskip\n%1399>%", 1),
    ("\n%1402>%", "\\medskip\n%1402>%", 1),
    ("\n%1403>%", "\\medskip\n%1403>%", 1),
    ("\n%1404>%", "\\medskip\n%1404>%", 1),
    ("\n%1405>%", "\\medskip\n%1405>%", 1),
    ("%1407>%", "%1407>%\n\\pagebreak", 1),
    # -----------------------------------------------------------------
    # 2016 [just for good looking] [spread more]
    ("\n%1408>%", "\\medskip\n%1408>%", 1),
    ("\n%1411>%", "\\medskip\n%1411>%", 1),
    ("\n%1412>%", "\\medskip\n%1412>%", 1),
    ("\n%1414>%", "\\medskip\n%1414>%", 1),
    ("\n%1415>%", "\\medskip\n%1415>%", 1),
    # -----------------------------------------------------------------
    # 2017 / 1 [add a line to bottom]
    ("%<1422%\n", "%<1422%\n\\enlargethispage{1\\baselineskip}", 1),
    # -----------------------------------------------------------------
    # 2017 / 2 [just for good looking] [spread more]
    ("\n%1425>%", "\\medskip\n%1415>%", 1),
    ("\n%1426>%", "\\medskip\n%1415>%", 1),
    ("\n%1428>%", "\\medskip\n%1415>%", 1),
    ("\n%1430>%", "\\medskip\n%1415>%", 1),
    ("\n%1432>%", "\\medskip\n%1415>%", 1),
    ("\n%1434>%", "\\medskip\n%1415>%", 1),
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
    ("\n%2090>%", "\\vspace{-2pt}\n%2090>%", 1),
    ("%<2097%\n", "%<2097%\n\\enlargethispage{1\\baselineskip}", 1),
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
