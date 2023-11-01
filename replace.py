# replacements for tex post-production
#-------------------------------------
import os

REPLACEMENTS = {
        # old,   new,   expected replacements
    'silver': (
    # fixing some overfull boxes
        ("Ministry of Rights and Equal Opportunities Sp.~Prize", 
         "Ministry of Rights and Equal Opportunities Sp.~Pr.", 1),
        ("Sp.~Prize ``Programmes That Effect Social Change''", 
         "Sp.~Pr.~``Programmes That Effect Social Change''", 3),
        ("Prix Italia Web, Best Trans-Media for Young Adult Public",
         "Prix Italia Web,\\\\Best Trans-Media for Young Adult Public", 1),
        ("Belgische Radio- en Televisieomroep/ Radio-Télévision Belge",
         "Belgische Radio- en Televisieomroep/\\\\Radio-Télévision Belge", 2),
        ("Canadian Broadcasting Corporation/ Société Radio-Canada",
         "Canadian Broadcasting Corporation/\\\\Société Radio-Canada", 1),
        ("ARTE Groupement Européen d'Intérêt Économique}}2022",
         "ARTE\\\\Groupement Européen d'Intérêt Économique}}2022", 1),
        ("Pasja, czyli misterium Męki Pańskiej w Kalwarii Zebrzydowskiej widziane",
         "Pasja, czyli misterium Męki Pańskiej w Kalwarii Zebrzydow\\-skiej widziane", 1),
        
    # fixing some ugly pagebreaks
        ("A Man of No Importance}\\nopagebreak[2]\\\\ RTF",
         "A Man of No Importance}\\nopagebreak[0]\\\\ RTF", 1),
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
        
        # page "enlargement" (one line more than usually allowed)
        ("Glynn Turman, Ted Ross, Stanley Clay.}", 
         "Glynn Turman, Ted Ross, Stanley Clay.}\\enlargethispage{1\\baselineskip}", 1),
        ("Sten Andersson. Photography: Michael Kinmanson.}",
         "Sten Andersson. Photography: Michael Kinmanson.}\\enlargethispage{1\\baselineskip}", 1),
        ("Joanna Przybyłowska. Sound: Andrzej Brzoska.}",
         "Joanna Przybyłowska. Sound: Andrzej Brzoska.}\\enlargethispage{1\\baselineskip}", 1),

        # mbox to avoid ugly linebreaks
        ("Producer: Bert van der Zouw. Script: J Bernlef", 
         "Producer: Bert van der Zouw. Script: \\mbox{J Bernlef}", 1),
        # these make overfull boxes... whatever
        ("Pertti Saloma, Seppo Partanen, Martti Timonen.}",
         "Pertti Saloma, Seppo Partanen, Martti \\mbox{Timonen}.}", 1),
        ("Sten Holmberg, Jonas Hallqvist.", 
         "Sten Holmberg, Jonas \\mbox{Hallqvist}.", 1),

        # forced linebreaks
        ("Prime Minister Sp.~Prize TV Programme from a Book",
         "Prime Minister Sp.~Prize\\TV Programme from a Book", 1),

    # various fixes
        # not sure about these: maybe use unicode chars instead?
        ("textfrench{VIIIe Station",
         "textfrench{VIII\\textsuperscript{e} Station", 1),
        ("itshape VIIIth Station",
         "itshape VIII\\textsuperscript{th} Station", 1),

              ),

    'book': (
        ('xxx', 'yyy', 0),

             ),
}


def do_replace(repl_set, in_file, verbose=True):
    """Custom replacements for tex post-production.
    repl_set: 'silver', 'book'... 
    in_file: path to origin file
    verbose: warns when repl. number is different than expected
    """
    tex = open(in_file, 'r', encoding='utf8').read()
    for n, (old, new, num) in enumerate(REPLACEMENTS[repl_set]):
        occurrences = tex.count(old)
        tex = tex.replace(old, new)
        if occurrences != num and verbose:
            print(f'Replacement # {n+1}: {occurrences} found, {num} expected.')
    try:
        os.remove(in_file[:-4]+'_replaced'+in_file[-4:])
    except OSError:
        pass
    with open(in_file[:-4]+'_replaced'+in_file[-4:], 'a', encoding='utf8') as f:
        f.write(tex)

