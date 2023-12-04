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
    ("\n%691>%\n\\\\ \\\\\n", "\n\\\\ \\\\\n", 1),
    # This is for the multimedia section prize 2012
    ("Il Post (Italy)", 
     "Italy", 1),
    # This is for the multimedia section prize 2013
    ("Piccolo Teatro Milano (Italy)", 
     "Italy", 1),
    # 2015, expo: do not repeat name in credits...
    ("\n\\\\* {\\footnotesize By: Valentina Landenna.}", "", 1),
    ("\n\\\\* {\\footnotesize By: Leonardo Ferrari Carissimi.}", "", 1),
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
    # 1960 [just for good looking] [spread more]
    ("\n%70>%", "\\smallskip\n%70>%", 1),
    ("\n%71>%", "\\smallskip\n%71>%", 1),
    ("\n%72>%", "\\smallskip\n%72>%", 1),
    ("\n%73>%", "\\smallskip\n%73>%", 1),
    ("\n%74>%", "\\smallskip\n%74>%", 1),
    ("\n%75>%", "\\smallskip\n%75>%", 1),
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
    # 1963 [just for good looking] [spread more]
    ("\n%100>%", "\\smallskip\n%100>%", 1),
    ("\n%101>%", "\\smallskip\n%101>%", 1),
    ("\n%102>%", "\\smallskip\n%102>%", 1),
    ("\n%103>%", "\\smallskip\n%103>%", 1),
    ("\n%104>%", "\\smallskip\n%104>%", 1),
    ("\n%105>%", "\\smallskip\n%105>%", 1),
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
    # 1970 / [just for good looking] [spread more]
    ("\n%173>%", "\\smallskip\n%173>%", 1),
    ("\n%174>%", "\\smallskip\n%174>%", 1),
    ("\n%175>%", "\\smallskip\n%175>%", 1),
    ("\n%176>%", "\\smallskip\n%176>%", 1),
    ("\n%177>%", "\\smallskip\n%177>%", 1),
    ("\n%178>%", "\\smallskip\n%178>%", 1),
    # -----------------------------------------------------------------
    # 1971 / [just for good looking] [spread more]
    ("\n%180>%", "\\smallskip\n%180>%", 1),
    ("\n%181>%", "\\smallskip\n%181>%", 1),
    ("\n%182>%", "\\smallskip\n%182>%", 1),
    ("\n%183>%", "\\smallskip\n%183>%", 1),
    ("\n%184>%", "\\smallskip\n%184>%", 1),
    ("\n%185>%", "\\smallskip\n%185>%", 1),
    ("\n%186>%", "\\smallskip\n%186>%", 1),
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
    # 1975 [just for good looking] [spread more]
    ("\n%226>%", "\\smallskip\n%219>%", 1),
    ("\n%227>%", "\\smallskip\n%219>%", 1),
    ("\n%228>%", "\\smallskip\n%219>%", 1),
    ("\n%229>%", "\\smallskip\n%219>%", 1),
    ("\n%230>%", "\\smallskip\n%219>%", 1),
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
    # 2003 [just for good looking] [spread more]
    ("\n%749>%", "\\smallskip\n%749>%", 1),
    ("\n%747>%", "\\smallskip\n%747>%", 1),
    ("\n%753>%", "\\smallskip\n%753>%", 1),
    ("\n%754>%", "\\smallskip\n%754>%", 1),
    ("\n%758>%", "\\smallskip\n%758>%", 1),
    ("\n%761>%", "\\smallskip\n%761>%", 1),
    # -----------------------------------------------------------------
    # 2004 [just for good looking] [spread more]
    ("\n%508>%", "\\smallskip\n%508>%", 1),
    ("\n%804>%", "\\smallskip\n%804>%", 1),
    ("\n%808>%", "\\smallskip\n%808>%", 1),
    ("\n%811>%", "\\smallskip\n%811>%", 1),
    ("\n%509>%", "\\smallskip\n%509>%", 1),
    ("\n%815>%", "\\smallskip\n%815>%", 1),
    




    # -----------------------------------------------------------------
    # 2005 / 1 [spread more, the pagebreak will happen "naturally"]
    ("\n%833>%", "\\medskip\n%833>%", 1),
    ("\n%836>%", "\\medskip\n%836>%", 1),
    ("\n%839>%", "\\medskip\n%839>%", 1),
    ("\n%510>%", "\\medskip\n%510>%", 1),
    ("\n%844>%", "\\medskip\n%844>%", 1),
    ("\n%842>%", "\\medskip\n%842>%", 1),
    # -----------------------------------------------------------------
    # 2005 / 2 [spread more, the pagebreak will happen "naturally"]
    ("\n%851>%", "\\medskip\n%851>%", 1),
    ("\n%854>%", "\\medskip\n%854>%", 1),
    ("\n%857>%", "\\medskip\n%857>%", 1),
    ("\n%860>%", "\\medskip\n%860>%", 1),
    ("\n%862>%", "\\medskip\n%862>%", 1),
    ("\n%865>%", "\\medskip\n%865>%", 1),
    # -----------------------------------------------------------------
    # 2006 / 1 [shrink the page adding negative space, add a line to bottom]
    ("\n%869>%", "\\vspace{-2pt}\n%869>%", 1),
    ("\n%1853>%", "\\vspace{-2pt}\n%1853>%", 1),
    ("\n%1852>%", "\\vspace{-2pt}\n%1852>%", 1),
    ("\n%873>%", "\\vspace{-10pt}\n%873>%", 1),
    ("\n%877>%", "\\vspace{-2pt}\n%877>%", 1),
    ("\n%880>%", "\\vspace{-2pt}\n%880>%", 1),
    ("%<883%\n", "%<883%\n\\enlargethispage{1\\baselineskip}", 1),
    # -----------------------------------------------------------------
    # 2006 / 2 [spread more, pagebreak will happen "naturally"]
    ("\n%887>%", "\\medskip\n%887>%", 1),
    ("\n%890>%", "\\medskip\n%890>%", 1),
    ("\n%893>%", "\\medskip\n%893>%", 1),
    ("\n%896>%", "\\medskip\n%896>%", 1),
    ("\n%899>%", "\\medskip\n%899>%", 1),
    ("\n%901>%", "\\medskip\n%901>%", 1),
    # -----------------------------------------------------------------
    # 2006 / 3 [spread more and force pagebreak]
    ("\n%907>%", "\\bigskip\n%907>%", 1),
    ("\n%910>%", "\\bigskip\n%910>%", 1),
    ("\n%914>%", "\\bigskip\n%914>%", 1),
    ("\n%915>%", "\\bigskip\n%915>%", 1),
    ("\n%922>%", "\\bigskip\n%922>%", 1),
    ("%919>%", "%919>%\n\\pagebreak", 1),
    # -----------------------------------------------------------------
    # 2008 / 1 [just for good looking] [spread more]
    ("\n%966>%", "\\smallskip\n%966>%", 1),
    ("\n%965>%", "\\smallskip\n%965>%", 1),
    ("\n%967>%", "\\smallskip\n%967>%", 1),
    ("\n%968>%", "\\smallskip\n%968>%", 1),
    ("\n%972>%", "\\smallskip\n%972>%", 1),
    # -----------------------------------------------------------------
    # 2008 / 2 [spread more and force pagebreak]
    ("\n%978>%", "\\bigskip\n%978>%", 1),
    ("\n%982>%", "\\bigskip\n%982>%", 1),
    ("\n%986>%", "\\bigskip\n%986>%", 1),
    ("\n%988>%", "\\bigskip\n%988>%", 1),
    ("\n%991>%", "\\bigskip\n%991>%", 1),
    ("%994>%", "%994>%\n\\pagebreak", 1),
    # -----------------------------------------------------------------
    # 2009 [spread more and force pagebreak]
    ("\n%1094>%", "\\bigskip\n%1094>%", 1),
    ("\n%1097>%", "\\bigskip\n%1097>%", 1),
    ("\n%517>%", "\\bigskip\n%517>%", 1),
    ("\n%1102>%", "\\bigskip\n%1102>%", 1),
    ("\n%1105>%", "\\bigskip\n%1105>%", 1),
    ("\n%1108>%", "\\bigskip\n%1108>%", 1),
    ("%1109>%", "%1109>%\n\\pagebreak", 1),
    # -----------------------------------------------------------------
    # 2010 / 1 [just for good looking] [spread more]
    ("\n%1112>%", "\\smallskip\n%1112>%", 1),
    ("\n%1116>%", "\\smallskip\n%1116>%", 1),
    ("\n%1118>%", "\\smallskip\n%1118>%", 1),
    ("\n%1121>%", "\\smallskip\n%1121>%", 1),
    ("\n%1124>%", "\\smallskip\n%1124>%", 1),
    # -----------------------------------------------------------------
    # 2010 / 2[just for good looking] [spread more]
    ("\n%1150>%", "\\smallskip\n%1150>%", 1),
    ("\n%1151>%", "\\smallskip\n%1151>%", 1),
    ("\n%1156>%", "\\smallskip\n%1156>%", 1),
    ("\n%1160>%", "\\smallskip\n%1160>%", 1),
    ("\n%1161>%", "\\smallskip\n%1161>%", 1),
    ("\n%1159>%", "\\smallskip\n%1159>%", 1),
    # -----------------------------------------------------------------
    # 2011 / 1 [add a line to bottom]
    ("%<1197%\n", "%<1197%\n\\enlargethispage{1\\baselineskip}", 1),
    # -----------------------------------------------------------------
    # 2011 / 2 [spread more and force pagebreak]
    ("\n%1201>%", "\\bigskip\n%1201>%", 1),
    ("\n%1199>%", "\\bigskip\n%1199>%", 1),
    ("\n%1203>%", "\\bigskip\n%1203>%", 1),
    ("\n%1206>%", "\\bigskip\n%1206>%", 1),
    ("\n%1209>%", "\\bigskip\n%1209>%", 1),
    ("%1212>%", "%1212>%\n\\pagebreak", 1),
    # -----------------------------------------------------------------
    # 2011 / 3 [just for good looking] [spread more]
    ("\n%1216>%", "\\smallskip\n%1206>%", 1),
    ("\n%1219>%", "\\smallskip\n%1206>%", 1),
    ("\n%1223>%", "\\smallskip\n%1206>%", 1),
    ("\n%1226>%", "\\smallskip\n%1206>%", 1),
    ("\n%1229>%", "\\smallskip\n%1206>%", 1),
    # -----------------------------------------------------------------
    # 2013 / 1 [just for good looking] [spread more]
    ("\n%1292>%", "\\bigskip\n%1292>%", 1),
    ("\n%520>%", "\\bigskip\n%520>%", 1),
    ("\n%1299>%", "\\bigskip\n%1299>%", 1),
    ("\n%519>%", "\\bigskip\n%519>%", 1),
    ("\n%1304>%", "\\bigskip\n%1304>%", 1),
    ("\n%1306>%", "\\bigskip\n%1306>%", 1),
    # -----------------------------------------------------------------
    # 2013 / 2 [spread more and force pagebreak]
    ("\n%1335>%", "\\bigskip\n%1335>%", 1),
    ("\n%1338>%", "\\bigskip\n%1338>%", 1),
    ("\n%1341>%", "\\bigskip\n%1341>%", 1),
    ("\n%1342>%", "\\bigskip\n%1342>%", 1),
    ("\n%1343>%", "\\bigskip\n%1343>%", 1),
    ("%1344>%", "%1344>%\n\\pagebreak", 1),
    # -----------------------------------------------------------------
    # 2014 / 1 [shrink the page adding negative space, add a line to bottom]
    ("\n%1349>%", "\\vspace{-2pt}\n%1349>%", 1),
    ("\n%1350>%", "\\vspace{-2pt}\n%1350>%", 1),
    ("\n%1345>%", "\\vspace{-2pt}\n%1345>%", 1),
    ("\n%1346>%", "\\vspace{-2pt}\n%1346>%", 1),
    ("\n%1354>%", "\\vspace{-2pt}\n%1354>%", 1),
    ("\n%1355>%", "\\vspace{-2pt}\n%1355>%", 1),
    ("%<1351%\n", "%<1351%\n\\enlargethispage{1\\baselineskip}", 1),
    # -----------------------------------------------------------------
    # 2014 / 2 [shrink the page adding negative space, add a line to bottom]
    ("\n%1363>%", "\\vspace{-2pt}\n%1363>%", 1),
    ("\n%1369>%", "\\vspace{-2pt}\n%1369>%", 1),
    ("\n%1370>%", "\\vspace{-2pt}\n%1370>%", 1),
    ("\n%1371>%", "\\vspace{-2pt}\n%1371>%", 1),
    ("\n%1372>%", "\\vspace{-10pt}\n%1372>%", 1),
    ("\n%1373>%", "\\vspace{-2pt}\n%1373>%", 1),
    ("%<1374%\n", "%<1374%\n\\enlargethispage{1\\baselineskip}", 1),
    # -----------------------------------------------------------------
    # 2015 [add a line to bottom]
    ("%<1402%\n", "%<1402%\n\\enlargethispage{1\\baselineskip}", 1),
    # -----------------------------------------------------------------
    # 2018 [just for good looking] [spread more]
    ("\n%1434>%", "\\medskip\n%1434>%", 1), 
    ("\n%1435>%", "\\medskip\n%1435>%", 1), 
    ("\n%1437>%", "\\medskip\n%1437>%", 1), 
    ("\n%1438>%", "\\medskip\n%1438>%", 1), 
    ("\n%1440>%", "\\medskip\n%1440>%", 1), 
    # -----------------------------------------------------------------
    # 2019 [just for good looking] [spread more]
    ("\n%1453>%", "\\smallskip\n%1453>%", 1), 
    ("\n%1455>%", "\\smallskip\n%1455>%", 1), 
    ("\n%1457>%", "\\smallskip\n%1457>%", 1), 
    ("\n%1458>%", "\\smallskip\n%1458>%", 1), 
    ("\n%1460>%", "\\smallskip\n%1460>%", 1), 
    ("\n%1462>%", "\\smallskip\n%1462>%", 1), 
    # -----------------------------------------------------------------
    # 2022 [shrink the page adding negative space, add a line to bottom]
    ("\n%1516>%", "\\vspace{-2pt}\n%1516>%", 1),
    ("\n%1518>%", "\\vspace{-10pt}\n%1518>%", 1),
    ("\n%1519>%", "\\vspace{-2pt}\n%1519>%", 1),
    ("\n%1521>%", "\\vspace{-2pt}\n%1521>%", 1),
    ("\n%1523>%", "\\vspace{-2pt}\n%1523>%", 1),
    ("\n%1525>%", "\\vspace{-2pt}\n%1525>%", 1),
    ("%<1527%\n", "%<1527%\n\\enlargethispage{1\\baselineskip}", 1),
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
