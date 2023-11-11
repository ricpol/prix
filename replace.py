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
    # fixing some overfull boxes
    # ==========================
    ("Ministry of Rights and Equal Opportunities Sp.~Prize", 
     "Ministry of Rights and Equal Opportunities Sp.~Pr.", 1),
    ("Sp.~Prize ``Programmes That Effect Social Change''", 
     "Sp.~Pr.~``Programmes That Effect Social Change''", 3),
    ("Prix Italia Web, Best Trans-Media for Young Adult Public",
     "Prix Italia Web,\\\\Best Trans-Media for Young Adult Public", 1),
    ("Pasja, czyli misterium Męki Pańskiej w Kalwarii Zebrzydowskiej widziane",
     "Pasja, czyli misterium Męki Pańskiej w Kalwarii Zebrzydow\\-skiej widziane", 1),

    # various fixes  === THESE GO FIRST!
    # ==================================
    # not sure about these: maybe use unicode chars instead?
    ("textfrench{VIIIe Station",
     "textfrench{VIII\\textsuperscript{e} Station", 1),
    ("itshape VIIIth Station",
     "itshape VIII\\textsuperscript{th} Station", 1),
    # this is to avoid the correct but ugly blank line
    # in the 1991 Presidents' Prize
    ("United Kingdom)\n \\\\ \\\\\n CNN",
     "United Kingdom)\n\\\\\nCNN", 1),
    # these are because the Euro Prize was awarded to a Country, 
    # not a programme
    ("Italy (Italy)", 
     "{\\large Italy}", 1),
    ("Austria (Austria)", 
     "{\\large Austria}", 1),
    ("United Kingdom (United Kingdom)", 
     "{\\large United Kingdom}", 1),
    # This is for the sp. prize web 2000
    ("Kataweb (Italy)", 
     "{\\large Kataweb}\\\\ Italy", 1),
    # This is for the multimedia section prize 2012
    ("Il Post (Italy)", 
     "Italy", 1),
    # This is for the multimedia section prize 2013
    ("Piccolo Teatro Milano (Italy)", 
     "Italy", 1),

    # ugly pagebreaks: spread and break sooner
    # ========================================
    ("A Man of No Importance}\\nopagebreak[2]\\\\ RTF",
     "A Man of No Importance}\\nopagebreak[0]\\\\ RTF", 1),
    # the following 6 are a group -------------------------------------
    # the only time I attempted to shrink the page adding negative space
    ("Inoue Yasushi. Music: Hayashi Hikaru.}", 
     "Inoue Yasushi. Music: Hayashi Hikaru.}\\vspace{-2pt}", 1), 
    ("Ennio Mastrostefano. Sound: Goffredo Palazzesi.}", 
     "Ennio Mastrostefano. Sound: Goffredo Palazzesi.}\\vspace{-2pt}", 1),
    ("Jean-Marie Coldefy. Choreography: Georges Skibine.}", 
     "Jean-Marie Coldefy. Choreography: Georges Skibine.}\\vspace{-2pt}", 1),
    ("Karl Wittlinger. Director: Rainer Erler.}", 
     "Karl Wittlinger. Director: Rainer Erler.}\\vspace{-2pt}", 1),
    ("Michael Colomb. Narrator: Michael Flanders.}", 
     "Michael Colomb. Narrator: Michael Flanders.}\\vspace{-2pt}", 1),
    ("A RNE programme submitted by DGRT.}}", 
     "A RNE programme submitted by DGRT.}}\\vspace{-2pt}", 1),
    # -----------------------------------------------------------------
    # the following 6 are a group -------------------------------------
    ("Music: Luboš Fišer. Director: Petr Weigl.}", 
     "Music: Luboš Fišer. Director: Petr Weigl.}\\smallskip", 1),
    ("Director, Script: Maurice Cazeneuve.}",
     "Director, Script: Maurice Cazeneuve.}\\smallskip", 1),
    ("Photography: Niko Timbergen. Presenter: Christopher Parsons.}",
     "Photography: Niko Timbergen. Presenter: Christopher Parsons.}\\smallskip", 1),
    ("Script: Claude Ollier. Director: Georges Peyrou.}", 
     "Script: Claude Ollier. Director: Georges Peyrou.}\\smallskip", 1),
    ("footnotesize By: Bob Uschi.}",
     "footnotesize By: Bob Uschi.}\\smallskip", 1),
    ("\\section*{1970, Firenze}",
     "\\pagebreak \\section*{1970, Firenze}", 1),
    # -----------------------------------------------------------------
    # the following 7 are a group -------------------------------------
    ("Script: Hoshikawa Seiji. Director: Segi Hiroyasu.}",
     "Script: Hoshikawa Seiji. Director: Segi Hiroyasu.}\\medskip", 1),
    ("Photography: Mike Dodds. Editor: Mike Taylor.}",
     "Photography: Mike Dodds. Editor: Mike Taylor.}\\medskip", 1),
    ("Producer: Maeda Naozumi. Script: Kimura Yoshinaga.}",
     "Producer: Maeda Naozumi. Script: Kimura Yoshinaga.}\\medskip", 1),
    ("By: Severo Sarduy. Director: René Jentet.}",
     "By: Severo Sarduy. Director: René Jentet.}\\medskip", 1),
    ("footnotesize By: Jacek Stwora.}",
     "footnotesize By: Jacek Stwora.}\\medskip", 1),
    ("Bernhard Kulbach. Sound: H J Müller.}",
     "Bernhard Kulbach. Sound: H J Müller.}\\medskip", 1),
    ("\\section*{1973, Venezia}",
     "\\pagebreak \\section*{1973, Venezia}", 1),
    # -----------------------------------------------------------------
    # the following 7 are a group -------------------------------------
    ("Stuart Weiss. Choreography: Pat Birch.}", 
     "Stuart Weiss. Choreography: Pat Birch.}\\medskip", 1),
    ("Sylvain Copans, Nicolas Parodi.}",
     "Sylvain Copans, Nicolas Parodi.}\\medskip", 1),
    ("Anrijs Krenbergs. Coproducer: Veronyca Bodnarec.}",
     "Anrijs Krenbergs. Coproducer: Veronyca Bodnarec.}\\medskip", 1),
    ("Ernstalbrecht Stiebler. Music: Walter Zimmermann.}",
     "Ernstalbrecht Stiebler. Music: Walter Zimmermann.}\\medskip", 1),
    ("Actors: Jane Friedmann, Aino Taube.}",
     "Actors: Jane Friedmann, Aino Taube.}\\medskip", 1),
    ("Mads Baastrup. Sound: Jesper Tholl.}",
     "Mads Baastrup. Sound: Jesper Tholl.}\\medskip", 1),
    ("William Sargent. Choreography: Andrea Francalanci.}",
     "William Sargent. Choreography: Andrea Francalanci.}\\pagebreak", 1),
    # -----------------------------------------------------------------
    # the following 9 are a group -------------------------------------
    ("Jacek Petrycki. Editor: Stefan Ronowicz.}", 
     "Jacek Petrycki. Editor: Stefan Ronowicz.}\\medskip", 1),
    ("CNN}\\nopagebreak[2]\\\\ CNN  \n (United States)", 
     "CNN}\\nopagebreak[2]\\\\ CNN  \n (United States)\\medskip", 1),
    ("BBC News}\\nopagebreak[2]\\\\ BBC  \n (United Kingdom)", 
     "BBC News}\\nopagebreak[2]\\\\ BBC  \n (United Kingdom)\\medskip", 1),
    ("Mosquito}}\\nopagebreak[2]\\\\ SVT  \n (Sweden)", 
     "Mosquito}}\\nopagebreak[2]\\\\ SVT  \n (Sweden)\\medskip", 1),
    ("CBC for Kids}\\nopagebreak[2]\\\\ CBC/SRC  \n (Canada)", 
     "CBC for Kids}\\nopagebreak[2]\\\\ CBC/SRC  \n (Canada)\\medskip", 1),
    ("{\\large Italy}",                        # 
     "{\\large Italy}\\medskip", 1),           # note: these 3 are the
    ("{\\large Austria}",                      # already-replaced
     "{\\large Austria}\\medskip", 1),         # 1999 Euro Prizes
    ("{\\large United Kingdom}",               #
     "{\\large United Kingdom}\\medskip", 1),  #
    ("Actors: Roland Magdane, Jo Stevens.}", 
     "Actors: Roland Magdane, Jo Stevens.}\\pagebreak", 1),
    # -----------------------------------------------------------------
    # the following 7 are a group -------------------------------------
    ("Shimizu Hiroyuki. Narrator: David Attenborough.}", 
     "Shimizu Hiroyuki. Narrator: David Attenborough.}\\medskip", 1),
    ("Sanna Salmenkallio. Sound: Martti Turunen.}", 
     "Sanna Salmenkallio. Sound: Martti Turunen.}\\medskip", 1),
    ("Josef Kjaersgaard, Tommy Renard.}", 
     "Josef Kjaersgaard, Tommy Renard.}\\medskip", 1),
    ("Felix Mabait. Sound: Katano Masami.}", 
     "Felix Mabait. Sound: Katano Masami.}\\medskip", 1),
    ("\\subsection*{{\\color{DarkRed}Quirinale Sp.~Prize}}{\\large Sex Traffic", 
     "\\medskip\\subsection*{{\\color{DarkRed}Quirinale Sp.~Prize}}{\\large Sex Traffic", 1),
    ("\\subsection*{{\\color{DarkRed}Signis Award}}{\\large\\textspanish{Centroamérica", 
     "\\pagebreak\\subsection*{{\\color{DarkRed}Signis Award}}{\\large\\textspanish{Centroamérica", 1),
    # -----------------------------------------------------------------
    # the following 6 are a group -------------------------------------
    ("Magnus Arvidson. Producer: Håkan Enström.}", 
     "Magnus Arvidson. Producer: Håkan Enström.}\\medskip", 1),
    ("Ria Marks, Titus Tiel Groenestege.}", 
     "Ria Marks, Titus Tiel Groenestege.}\\medskip", 1),
    ("Yeon Woon-Kyung, Jung Chan, Jin Koo.}", 
     "Yeon Woon-Kyung, Jung Chan, Jin Koo.}\\medskip", 1),
    ("Pegah Ferydoni, Emil Reinke.}", 
     "Pegah Ferydoni, Emil Reinke.}\\medskip", 1),
    ("footnotesize Director: Thomas Jonhson.}", 
     "footnotesize Director: Thomas Jonhson.}\\medskip", 1),
    ("Richard Ranken. Sound: Andrei Budylin.}", 
     "Richard Ranken. Sound: Andrei Budylin.}\\pagebreak", 1),
    # -----------------------------------------------------------------
    # the following 7 are a group -------------------------------------
    ("Anthony Glennon, Jasmine Callan.}", 
     "Anthony Glennon, Jasmine Callan.}\\medskip", 1), 
    ("Jaqueline Cloake, Thomas Wheatley.}", 
     "Jaqueline Cloake, Thomas Wheatley.}\\medskip", 1), 
    ("Torben Paaske. Producer: Ulla Kristensen.}", 
     "Torben Paaske. Producer: Ulla Kristensen.}\\medskip", 1), 
    ("Mark Burman. Presenter: Alan Dein.}", 
     "Mark Burman. Presenter: Alan Dein.}\\medskip", 1), 
    ("David Krügel, Karel Hruska.}", 
     "David Krügel, Karel Hruska.}\\medskip", 1), 
    ("Jacek Piotr Bławut, Andrzej Mańkowski.}", 
     "Jacek Piotr Bławut, Andrzej Mańkowski.}\\medskip", 1), 
    ("Charles Mnene, Nikki Amuka-Bird.}", 
     "Charles Mnene, Nikki Amuka-Bird.}\\pagebreak", 1), 
    # -----------------------------------------------------------------
    # the following 6 are a group -------------------------------------
    ("Magnus Arvidson. Sound: Fredrik Nilsson.}", 
     "Magnus Arvidson. Sound: Fredrik Nilsson.}\\medskip", 1), 
    ("René Dupéré. Commentator: Claus Kleber.}", 
     "René Dupéré. Commentator: Claus Kleber.}\\medskip", 1), 
    ("Sound: Jan Palmers, Bjørn Molstad.}", 
     "Sound: Jan Palmers, Bjørn Molstad.}\\medskip", 1), 
    ("Jo Øigarden, Bjørn Sundquist.}", 
     "Jo Øigarden, Bjørn Sundquist.}\\medskip", 1), 
    ("Sverrir Gudnason, Simon Berger, Ruth Vega Fernandez.}", 
     "Sverrir Gudnason, Simon Berger, Ruth Vega Fernandez.}\\medskip", 1), 
    ("footnotesize By: Alison Millar.}", 
     "footnotesize By: Alison Millar.}\\pagebreak", 1), 
    # -----------------------------------------------------------------
    # the following 6 are a group -------------------------------------
    ("Paul Malinowski. Music: Sebastian Rivas.}", 
     "Paul Malinowski. Music: Sebastian Rivas.}\\medskip", 1), 
    ("Florence Loiret Caille, Christophe Brault.}", 
     "Florence Loiret Caille, Christophe Brault.}\\medskip", 1), 
    ("Hanneke Hendrix. Sound: Frans de Rond.}", 
     "Hanneke Hendrix. Sound: Frans de Rond.}\\medskip", 1), 
    ("Lasse Nederhoed. Editor: Kåre Johan Lund.}", 
     "Lasse Nederhoed. Editor: Kåre Johan Lund.}\\medskip", 1), 
    ("Jarvis Cocker. Sound: Vic Kent.}", 
     "Jarvis Cocker. Sound: Vic Kent.}\\medskip", 1), 
    ("André Rigaut. Editor: Toni Froschhammer.}", 
     "André Rigaut. Editor: Toni Froschhammer.}\\pagebreak", 1), 
    # -----------------------------------------------------------------
    # the following 6 are a group -------------------------------------
    ("Boris Gerrets. Producer: Thomas Den Drijver.}", 
     "Boris Gerrets. Producer: Thomas Den Drijver.}\\medskip", 1), 
    ("Heide Simon, Natascha Paulick.}", 
     "Heide Simon, Natascha Paulick.}\\medskip", 1), 
    ("Katarzyna Maciąg, Teresa Budzisz-Krzyżanowska.}", 
     "Katarzyna Maciąg, Teresa Budzisz-Krzyżanowska.}\\medskip", 1), 
    ("footnotesize By: Maria Kuhlbergs.}", 
     "footnotesize By: Maria Kuhlbergs.}\\medskip", 1), 
    ("footnotesize By: Fernand Melgar.}", 
     "footnotesize By: Fernand Melgar.}\\medskip", 1), 
    ("Hugues Sweeney. Director: Pascal Brouard.}", 
     "Hugues Sweeney. Director: Pascal Brouard.}\\pagebreak", 1), 
    # -----------------------------------------------------------------
    # the following 5 are a group -------------------------------------
    # (this is just for good looking - no forced pagebreak at the end)
    ("Kunuk Nykjær, Christian Planck.}",
     "Kunuk Nykjær, Christian Planck.}\\medskip", 1), 
    ("Arno Lafontaine, Julia Revault.}",
     "Arno Lafontaine, Julia Revault.}\\medskip", 1),
    ("Programmers: Maxime Quintard, Yves Diffre.}",
     "Programmers: Maxime Quintard, Yves Diffre.}\\medskip", 1),
    ("Jehane Noujaim. Producer: Mette Heide.}",
     "Jehane Noujaim. Producer: Mette Heide.}\\medskip", 1),
    ("footnotesize By: Juan Francisco Scassa.}",
     "footnotesize By: Juan Francisco Scassa.}\\medskip", 1),
    # -----------------------------------------------------------------
    # the following 6 are a group -------------------------------------
    ("Yves Diffre, Maxime Gravouil.}", 
     "Yves Diffre, Maxime Gravouil.}\\medskip", 1), 
    ("Denis Delestrac, Sandrine Feydel.}", 
     "Denis Delestrac, Sandrine Feydel.}\\medskip", 1), 
    ("By: Leonardo Ferrari Carissimi.}", 
     "By: Leonardo Ferrari Carissimi.}\\medskip", 1), 
    ("Mitra Kaboli, Shira Bannerman, Shani Aviram.}", 
     "Mitra Kaboli, Shira Bannerman, Shani Aviram.}\\medskip", 1), 
    ("Fabrice Estève, Christian Popp.}", 
     "Fabrice Estève, Christian Popp.}\\medskip", 1), 
    ("Elisabeth Stratka. Technician: Martin Todt.}", 
     "Elisabeth Stratka. Technician: Martin Todt.}\\pagebreak", 1), 
    # -----------------------------------------------------------------
    # the following 6 are a group -------------------------------------
    ("Riikka Talvitie. Sound: Heidi Soidinsalo.}", 
     "Riikka Talvitie. Sound: Heidi Soidinsalo.}\\medskip", 1), 
    ("Silvain Gire. Music, Editor: Arnaud Forest.}", 
     "Silvain Gire. Music, Editor: Arnaud Forest.}\\medskip", 1),
    ("Daria Corrias, Fabiana Carobolante.}", 
     "Daria Corrias, Fabiana Carobolante.}\\medskip", 1),
    ("Rutger Lemm. Actor: Etgar Keret.}", 
     "Rutger Lemm. Actor: Etgar Keret.}\\medskip", 1),
    ("Lesley Sharp, Paul Kaye.}", 
     "Lesley Sharp, Paul Kaye.}\\medskip", 1),
    ("Jesper Ankarfeldt. Editor: Sander Vos.}", 
      "Jesper Ankarfeldt. Editor: Sander Vos.}\\pagebreak", 1),
     # -----------------------------------------------------------------
     
    # ugly pagebreaks: enlarge page (one line more than usually allowed)
    # ==================================================================
    ("Glynn Turman, Ted Ross, Stanley Clay.}", 
     "Glynn Turman, Ted Ross, Stanley Clay.}\\enlargethispage{1\\baselineskip}", 1),
    ("Sten Andersson. Photography: Michael Kinmanson.}",
     "Sten Andersson. Photography: Michael Kinmanson.}\\enlargethispage{1\\baselineskip}", 1),
    ("Joanna Przybyłowska. Sound: Andrzej Brzoska.}",
     "Joanna Przybyłowska. Sound: Andrzej Brzoska.}\\enlargethispage{1\\baselineskip}", 1),
    ("Luc Ferrari. Producer: José Iges.}",
     "Luc Ferrari. Producer: José Iges.}\\enlargethispage{1\\baselineskip}", 1),
    ("Actors: Tina Kellegher, Colm Meaney.}",
     "Actors: Tina Kellegher, Colm Meaney.}\\enlargethispage{1\\baselineskip}", 1),
    ("Ida Rapaičová, Anna Javorková.}",
     "Ida Rapaičová, Anna Javorková.}\\enlargethispage{1\\baselineskip}", 1),
    ("Marek Leščák, Odrej Šulaj.}",
     "Marek Leščák, Odrej Šulaj.}\\enlargethispage{1\\baselineskip}", 1),
    ("Actors: Gail Gilmore, Eric Gould.}",
     "Actors: Gail Gilmore, Eric Gould.}\\enlargethispage{1\\baselineskip}", 1),
    ("Kanno Yoshihiro. Sound: Itobayashi Kaoru.}", 
     "Kanno Yoshihiro. Sound: Itobayashi Kaoru.}\\enlargethispage{1\\baselineskip}", 1),
    ("Audrey Ripoull, Raphaëlle Mantoux.}", 
     "Audrey Ripoull, Raphaëlle Mantoux.}\\enlargethispage{1\\baselineskip}", 1),
    ("Saša Dobrohotov, Nataša Vujnović.}", 
     "Saša Dobrohotov, Nataša Vujnović.}\\enlargethispage{1\\baselineskip}", 1),
    ("Daria Hensemberger, Sara Polese.}", 
     "Daria Hensemberger, Sara Polese.}\\enlargethispage{1\\baselineskip}", 1),

    # spread more this page, there is too much space left at the end
    # ==============================================================
    # the following 7 are a group -------------------------------------
    ("Mária Prechovská, Vladimír Müller.}", 
     "Mária Prechovská, Vladimír Müller.}\\medskip", 1),
    ("Jeoffrey Whitehead, John Jacobs. Sound: John Jacobs.}", 
     "Jeoffrey Whitehead, John Jacobs. Sound: John Jacobs.}\\medskip", 1),
    ("Sp.~Prize Radio Title Sequences}}Not awarded.", 
     "Sp.~Prize Radio Title Sequences}}Not awarded.\\medskip", 1),
    ("Sp.~Prize TV Music and Arts}}Not awarded.", 
     "Sp.~Prize TV Music and Arts}}Not awarded.\\medskip", 1),
    ("Antero Takala. Sound: Antero Honkanen.}", 
     "Antero Takala. Sound: Antero Honkanen.}\\medskip", 1),
    ("Christine Pireaux. Sound: Yvan Geeraert.}", 
     "Christine Pireaux. Sound: Yvan Geeraert.}\\medskip", 1),
    ("\\section*{1993, Roma}", 
     "\\medskip\\section*{1993, Roma}", 1),
    # -----------------------------------------------------------------

    # ugly linebreaks: avoid with mbox
    # ================================
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
    # =================
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
