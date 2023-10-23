# glossary and repertoire
#----------------------------------------------------------------------

ROLES_SINGULAR = ['', '_null', 
    # authors
    'Adapted by', 'Adapted from', 'Author', 'By','Content Author', 'Chief Editor', 
    'Content Manager', 'Format', 'Poems', 'Project Manager', 'Script', 
    'Subject', 
    # directors
    'Assistant Director', 'Director', 
    # photography, editing
    'Editor', 'Filmmaker', 'Photography', 'Video', 
    # music, dance
    'Ballet', 'Choreography', 'Conductor', 'Dancer', 'Instrumentalist', 
    'Lyrics', 'Music arrangement', 'Music', 'Musician', 'Vocals', 
    # actors, performes
    'Actor', 'Commentator', 'Correspondent', 'Narrator', 'Participant', 
    'Performer', 'Presenter', 'Reporter', 
    # technicians
    'Animation', 'Art Director', 'Costumes', 'Designer', 'Developer', 
    'Drawings', 'Effects', 'Electronics', 'Foley', 'Graphics', 
    'Interactivity', 'Mixing','Photos', 'Recording', 'Scenography', 
    'Social Editor' , 'Sound', 'Technician', 'Teleplay', 'Transmedia', 
    'Web Artist', 'Web Designer', 'Web Editor', 'Web Master', 'Web Programmer',
    # producers, bosses
    'Commissioner', 'Coordination', 'Coproducer', 'Executive Producer', 
    'Head of Programme', 'Producer', 'Programmer', 'Stage Direction', 
    'Studio Manager', 'Supervising Editor', 'Technical Project Manager',
    # others
    'Archive', 'Research', 
    ]
ROLES_SINGULAR.sort()

# in alphabetical order
ROLES_PLURAL = ['', 
    'Actors', 'Adapted by', 'Adapted from', 'Animation', 'Archive', 'Art Directors', 
    'Assistant Directors', 'Authors', 
    'Ballet', 'By', 
    'Chief Editors', 'Choreography', 'Commentators', 'Commissioners', 'Conductors', 
    'Content Authors', 'Content Managers', 'Coordination', 'Coproducers', 'Correspondents', 
    'Costumes', 
    'Dancers', 'Designers', 'Developers', 'Directors', 'Drawings', 
    'Editors', 'Effects', 'Electronics', 'Executive Producers', 
    'Filmmakers', 'Foley', 'Format', 
    'Graphics', 
    'Head of Programme', 
    'Instrumentalists', 'Interactivity', 
    'Lyrics', 
    'Mixing', 'Music arrangement', 'Music', 'Musicians', 
    'Narrators', 
    'Participants', 'Performers', 'Photography', 'Photos', 'Poems', 'Presenters', 
    'Producers', 'Programmers', 'Project Managers', 
    'Recording', 'Reporters', 'Research', 
    'Scenography', 'Script', 'Social Editors', 'Sound', 'Stage Direction', 
    'Studio Managers', 'Subject', 'Supervising Editors', 
    'Technical Project Managers', 'Technicians', 'Teleplay', 'Transmedia', 
    'Video', 'Vocals', 
    'Web Artists', 'Web Designers', 'Web Editors', 'Web Masters', 'Web Programmers', 
    '_null', ]

ROLES = ROLES_SINGULAR + ROLES_PLURAL
assert len(ROLES_SINGULAR) == len(ROLES_PLURAL)



COMMON_PUNCTUATION = ' .,:;…#%°"/()?!+-«»–&_@' + "'" 

OR_TITLE_PUNCTUATION = COMMON_PUNCTUATION + '「」〜（）！〈〉、・' + '\u3000'

CREDIT_PUNCTUATION = " :,.'-_&()"  # the ONLY allowed in credits! ("_" is for "_null")


# the dash madness!
# do not use:
# — (em dash)          -> – (en dash)
# ～ (Fullwidth Tilde) -> 〜 (Wave Dash)
# ‐ (hyphen)           -> - (hypen-minus)
#
#
# - (U+002D) -> hyphen-minus
# ‐ (U+2010) -> Hyphen
# – (U+2013) -> En Dash
# — (U+2014) -> Em Dash
#



