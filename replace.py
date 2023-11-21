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
    ("Sp.~Prixe Expo 2015 - Young Independent Film-Makers", 
     "Sp.~Prixe Expo 2015 - Young Independent\\\\Film-Makers", 1),
    ("Prix Italia Radio Music Attracting a Broader Audience", 
     "Prix Italia Radio Music Attracting\\\\a Broader Audience", 1),
    ("Prix Italia Radio Doc.~and Reportage - Documentary", 
     "Prix Italia Radio Doc.~and Reportage -\\\\Documentary", 1),

    # PART 2 -- page-level fixes
    # ==========================
    # these will force different pagebreaks
    # and are sorted by year
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
        # too, even if they seem to work because there's no full box 
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
    ("\n%873>%", "\\vspace{-2pt}\n%873>%", 1),
    ("\n%877>%", "\\vspace{-2pt}\n%877>%", 1),
    ("\n%880>%", "\\vspace{-2pt}\n%880>%", 1),
    ("\n%883>%", "\\vspace{-2pt}\n%883>%", 1),
    ("\n%887>%", "\\vspace{-2pt}\n%887>%\\enlargethispage{1\\baselineskip}", 1),
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
#    ("Anthony Glennon, Jasmine Callan.}", 
#     "Anthony Glennon, Jasmine Callan.}\\medskip", 1), 
#    ("Jaqueline Cloake, Thomas Wheatley.}", 
#     "Jaqueline Cloake, Thomas Wheatley.}\\medskip", 1), 
#    ("Torben Paaske. Producer: Ulla Kristensen.}", 
#     "Torben Paaske. Producer: Ulla Kristensen.}\\medskip", 1), 
#    ("Mark Burman. Presenter: Alan Dein.}", 
#     "Mark Burman. Presenter: Alan Dein.}\\medskip", 1), 
#    ("David Krügel, Karel Hruska.}", 
#     "David Krügel, Karel Hruska.}\\medskip", 1), 
#    ("Jacek Piotr Bławut, Andrzej Mańkowski.}", 
#     "Jacek Piotr Bławut, Andrzej Mańkowski.}\\medskip", 1), 
#    ("Charles Mnene, Nikki Amuka-Bird.}", 
#     "Charles Mnene, Nikki Amuka-Bird.}\\pagebreak", 1), 
    # -----------------------------------------------------------------
    # 2008 [spread more and force pagebreak]
#    ("Magnus Arvidson. Sound: Fredrik Nilsson.}", 
#     "Magnus Arvidson. Sound: Fredrik Nilsson.}\\medskip", 1), 
#    ("René Dupéré. Commentator: Claus Kleber.}", 
#     "René Dupéré. Commentator: Claus Kleber.}\\medskip", 1), 
#    ("Sound: Jan Palmers, Bjørn Molstad.}", 
#     "Sound: Jan Palmers, Bjørn Molstad.}\\medskip", 1), 
#    ("Jo Øigarden, Bjørn Sundquist.}", 
#     "Jo Øigarden, Bjørn Sundquist.}\\medskip", 1), 
#    ("Sverrir Gudnason, Simon Berger, Ruth Vega Fernandez.}", 
#     "Sverrir Gudnason, Simon Berger, Ruth Vega Fernandez.}\\medskip", 1), 
#    ("footnotesize By: Alison Millar.}", 
#     "footnotesize By: Alison Millar.}\\pagebreak", 1),
#    # -----------------------------------------------------------------
#    # 2011 [add a line to bottom]
#    ("Audrey Ripoull, Raphaëlle Mantoux.}", 
#     "Audrey Ripoull, Raphaëlle Mantoux.}\\enlargethispage{1\\baselineskip}", 1), 
#    # -----------------------------------------------------------------
#    # 2012 / 1 [spread more and force pagebreak]
#    ("Paul Malinowski. Music: Sebastian Rivas.}", 
#     "Paul Malinowski. Music: Sebastian Rivas.}\\medskip", 1), 
#    ("Florence Loiret Caille, Christophe Brault.}", 
#     "Florence Loiret Caille, Christophe Brault.}\\medskip", 1), 
#    ("Hanneke Hendrix. Sound: Frans de Rond.}", 
#     "Hanneke Hendrix. Sound: Frans de Rond.}\\medskip", 1), 
#    ("Lasse Nederhoed. Editor: Kåre Johan Lund.}", 
#     "Lasse Nederhoed. Editor: Kåre Johan Lund.}\\medskip", 1), 
#    ("Jarvis Cocker. Sound: Vic Kent.}", 
#     "Jarvis Cocker. Sound: Vic Kent.}\\medskip", 1), 
#    ("André Rigaut. Editor: Toni Froschhammer.}", 
#     "André Rigaut. Editor: Toni Froschhammer.}\\pagebreak", 1), 
#    # -----------------------------------------------------------------
#    # 2012 / 2 [spread more and force pagebreak]
#    ("Boris Gerrets. Producer: Thomas Den Drijver.}", 
#     "Boris Gerrets. Producer: Thomas Den Drijver.}\\medskip", 1), 
#    ("Heide Simon, Natascha Paulick.}", 
#     "Heide Simon, Natascha Paulick.}\\medskip", 1), 
#    ("Katarzyna Maciąg, Teresa Budzisz-Krzyżanowska.}", 
#     "Katarzyna Maciąg, Teresa Budzisz-Krzyżanowska.}\\medskip", 1), 
#    ("footnotesize By: Maria Kuhlbergs.}", 
#     "footnotesize By: Maria Kuhlbergs.}\\medskip", 1), 
#    ("footnotesize By: Fernand Melgar.}", 
#     "footnotesize By: Fernand Melgar.}\\medskip", 1), 
#    ("Hugues Sweeney. Director: Pascal Brouard.}", 
#     "Hugues Sweeney. Director: Pascal Brouard.}\\pagebreak", 1), 
#    # -----------------------------------------------------------------
#    # 2014 [spread more, just for good looking - no pagebreak at the end]
#    ("Kunuk Nykjær, Christian Planck.}",
#     "Kunuk Nykjær, Christian Planck.}\\medskip", 1), 
#    ("Arno Lafontaine, Julia Revault.}",
#     "Arno Lafontaine, Julia Revault.}\\medskip", 1),
#    ("Programmers: Maxime Quintard, Yves Diffre.}",
#     "Programmers: Maxime Quintard, Yves Diffre.}\\medskip", 1),
#    ("Jehane Noujaim. Producer: Mette Heide.}",
#     "Jehane Noujaim. Producer: Mette Heide.}\\medskip", 1),
#    ("footnotesize By: Juan Francisco Scassa.}",
#     "footnotesize By: Juan Francisco Scassa.}\\medskip", 1),
#    # -----------------------------------------------------------------
#    # 2015 [spread more and force pagebreak]
#    ("Yves Diffre, Maxime Gravouil.}", 
#     "Yves Diffre, Maxime Gravouil.}\\medskip", 1), 
#    ("Denis Delestrac, Sandrine Feydel.}", 
#     "Denis Delestrac, Sandrine Feydel.}\\medskip", 1), 
#    ("By: Leonardo Ferrari Carissimi.}", 
#     "By: Leonardo Ferrari Carissimi.}\\medskip", 1), 
#    ("Mitra Kaboli, Shira Bannerman, Shani Aviram.}", 
#     "Mitra Kaboli, Shira Bannerman, Shani Aviram.}\\medskip", 1), 
#    ("Fabrice Estève, Christian Popp.}", 
#     "Fabrice Estève, Christian Popp.}\\medskip", 1), 
#    ("Elisabeth Stratka. Technician: Martin Todt.}", 
#     "Elisabeth Stratka. Technician: Martin Todt.}\\pagebreak", 1), 
#    # -----------------------------------------------------------------
#    # 2017 [add a line to bottom]
#    ("Saša Dobrohotov, Nataša Vujnović.}", 
#     "Saša Dobrohotov, Nataša Vujnović.}\\enlargethispage{1\\baselineskip}", 1),
#    # -----------------------------------------------------------------
#    # 2018 [spread more and force pagebreak]
#    ("Riikka Talvitie. Sound: Heidi Soidinsalo.}", 
#     "Riikka Talvitie. Sound: Heidi Soidinsalo.}\\medskip", 1), 
#    ("Silvain Gire. Music, Editor: Arnaud Forest.}", 
#     "Silvain Gire. Music, Editor: Arnaud Forest.}\\medskip", 1),
#    ("Daria Corrias, Fabiana Carobolante.}", 
#     "Daria Corrias, Fabiana Carobolante.}\\medskip", 1),
#    ("Rutger Lemm. Actor: Etgar Keret.}", 
#     "Rutger Lemm. Actor: Etgar Keret.}\\medskip", 1),
#    ("Lesley Sharp, Paul Kaye.}", 
#     "Lesley Sharp, Paul Kaye.}\\medskip", 1),
#    ("Jesper Ankarfeldt. Editor: Sander Vos.}", 
#      "Jesper Ankarfeldt. Editor: Sander Vos.}\\pagebreak", 1),
#    # -----------------------------------------------------------------
#    # 2023 [add a line to bottom]
#    ("Daria Hensemberger, Sara Polese.}", 
#     "Daria Hensemberger, Sara Polese.}\\enlargethispage{1\\baselineskip}", 1), 
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
