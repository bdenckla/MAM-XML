""" Exports sef_header """

import my_sef_cmn


def sef_header(bkid):
    """ Returns Sefaria header for book with ID bkid. """
    return {
        'Index Title': my_sef_cmn.SEF_ENGLISH_BOOK_NAMES[bkid],
        'Version Title': 'Miqra according to the Masorah',
        'Language': 'he',
        'Version Source': '/'.join((
            'https://en.wikisource.org', 'wiki', 'User:Dovi',
            'Miqra_according_to_the_Masorah')),
        'Version Notes': '',
    }
