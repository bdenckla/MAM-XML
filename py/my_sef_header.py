""" Exports sef_header """

import my_sef_cmn


def sef_header(bkid):
    """ Returns Sefaria header for book with ID bkid. """
    return {
        'Index Title': my_sef_cmn.SEF_BKNA[bkid],
        'Version Title': 'Miqra according to the Masorah',
        'Language': 'he',
        'Version Source': WIKISOURCE_URL_HE,
        'Version Notes': '',
    }


WIKISOURCE_URL_HE = (
    'https://he.wikisource.org/wiki/'
    r'%D7%9E%D7%A9%D7%AA%D7%9E%D7%A9:Dovi/'
    r'%D7%9E%D7%A7%D7%A8%D7%90_'
    r'%D7%A2%D7%9C_'
    r'%D7%A4%D7%99_'
    r'%D7%94%D7%9E%D7%A1%D7%95%D7%A8%D7%94')
