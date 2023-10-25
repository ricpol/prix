# replacements for tex post-production
#-------------------------------------
import os

REPLACEMENTS = {
        # old,   new
    'silver': (
        ('xxx', 'yyy'),

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
    for n, (old, new) in enumerate(REPLACEMENTS[repl_set]):
        occurrences = tex.count(old)
        tex = tex.replace(old, new)
        if occurrences != 1 and verbose:
            print(f'Replacement # {n}: found {occurences} occurrences.')
    try:
        os.remove('replaced_'+in_file)
    except OSError:
        pass
    with open('replaced_'+in_file, 'a', encoding='utf8') as f:
        f.write(tex)

