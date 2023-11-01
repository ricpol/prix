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
              ),

    'book': (
        ('xxx', 'yyy'),

             ),
}


def do_replace(repl_set, in_file, verbose=True):
    """Custom replacements for tex post-production.
    repl_set: 'silver', 'book'... 
    in_file: path to origin file
    verbose: prints when 0 or >1 replacements occurred
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

