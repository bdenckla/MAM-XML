""" Exports sef_header """

import my_sef_cmn


def sef_header(bkid):
    """ Returns Sefaria header for book with ID bkid. """
    sefmet = _sef_metadata(bkid)
    return {
        'Index Title': sefmet['title'],
        'Version Title': sefmet['versionTitle'],
        'Language': sefmet['language'],
        'Version Source': sefmet['versionSource'],
        'Version Notes': '',
    }


# Previous values for versionSource:
#
#  '/'.join((
#     'https://docs.google.com/spreadsheets/d',
#     '1mkQyj6by1AtBUabpbaxaZq9Z2X3pX8ZpwG91ZCSOEYs',
#     'edit?usp=sharing'))
#
# (
#     # משתמש:Dovi/מקרא_על_פי_המסורה#ראש
#     'https://he.wikisource.org/wiki/' +
#     r'%D7%9E%D7%A9%D7%AA%D7%9E%D7%A9:Dovi/' +  # משתמש:Dovi/
#     r'%D7%9E%D7%A7%D7%A8%D7%90_' +  # מקרא_
#     r'%D7%A2%D7%9C_' +  # על_
#     r'%D7%A4%D7%99_' +  # פי_
#     r'%D7%94%D7%9E%D7%A1%D7%95%D7%A8%D7%94#' +  # המסורה#
#     r'%D7%A8%D7%90%D7%A9'  # ראש
# )

_VERSION_SOURCE = \
    'https://en.wikisource.org/wiki/User:Dovi/Miqra_according_to_the_Masorah'


def _sef_metadata(bkid):
    # The order of keys seems arbitrary,
    # but this is how they downloaded from Sefaria.
    # So, to facilitate comparison, we use that order here.
    dic = dict(
        priority=None,  # std text has 1.0 (a number not a string)
        versionTitleInHebrew='מקרא על פי המסורה',
        # std text has 'תנ״ך מלווה בטעמי מקרא'
        title=my_sef_cmn.SEF_ENGLISH_BOOK_NAMES[bkid],  # e.g. 'Deuteronomy'
        language='he',
        license='CC-BY-SA 3.0',  # std text has "Public Domain"
        status=None,  # std text has "locked"
        versionSource=_VERSION_SOURCE,
        # std text has "http://www.tanach.us/Tanach.xml"
        versionTitle='Miqra according to the Masorah',
        # std text has "Tanach with Ta'amei Hamikra"
        licenseVetted=None,  # std text has true (a boolean not a string)
        heTitle=my_sef_cmn.SEF_HEBREW_BOOK_NAMES[bkid],  # e.g. 'דברים'
        categories=['Tanakh', my_sef_cmn.SEF_TANAKH_SUBCATEGORIES[bkid]],
    )
    return dic
