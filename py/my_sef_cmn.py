""" Exports some constants commonly needed for Sefaria-related work. """

import my_tanakh_book_names as my_tbn


_SEF_BOOK_PROPERTIES = {
    my_tbn.BK_GENESIS: ('Genesis',),
    my_tbn.BK_EXODUS: ('Exodus',),
    my_tbn.BK_LEVITICUS: ('Leviticus',),
    my_tbn.BK_NUMBERS: ('Numbers',),
    my_tbn.BK_DEUTER: ('Deuteronomy',),
    my_tbn.BK_JOSHUA: ('Joshua',),
    my_tbn.BK_JUDGES: ('Judges',),
    my_tbn.BK_FST_SAMUEL: ('I Samuel',),
    my_tbn.BK_SND_SAMUEL: ('II Samuel',),
    my_tbn.BK_FST_KINGS: ('I Kings',),
    my_tbn.BK_SND_KINGS: ('II Kings',),
    my_tbn.BK_ISAIAH: ('Isaiah',),
    my_tbn.BK_JEREMIAH: ('Jeremiah',),
    my_tbn.BK_EZEKIEL: ('Ezekiel',),
    my_tbn.BK_HOSEA: ('Hosea',),
    my_tbn.BK_JOEL: ('Joel',),
    my_tbn.BK_AMOS: ('Amos',),
    my_tbn.BK_OBADIAH: ('Obadiah',),
    my_tbn.BK_JONAH: ('Jonah',),
    my_tbn.BK_MICAH: ('Micah',),
    my_tbn.BK_NAXUM: ('Nahum',),
    my_tbn.BK_XABAKKUK: ('Habakkuk',),
    my_tbn.BK_TSEFANIAH: ('Zephaniah',),
    my_tbn.BK_XAGGAI: ('Haggai',),
    my_tbn.BK_ZEKHARIAH: ('Zechariah',),
    my_tbn.BK_MALAKHI: ('Malachi',),
    my_tbn.BK_PSALMS: ('Psalms',),
    my_tbn.BK_PROVERBS: ('Proverbs',),
    my_tbn.BK_JOB: ('Job',),
    my_tbn.BK_SONG_OF_SONGS: ('Song of Songs',),
    my_tbn.BK_RUTH: ('Ruth',),
    my_tbn.BK_LAMENTATIONS: ('Lamentations',),
    my_tbn.BK_ECCLESIASTES: ('Ecclesiastes',),
    my_tbn.BK_ESTHER: ('Esther',),
    my_tbn.BK_DANIEL: ('Daniel',),
    my_tbn.BK_EZRA: ('Ezra',),
    my_tbn.BK_NEXEMIAH: ('Nehemiah',),
    my_tbn.BK_FST_CHRONICLES: ('I Chronicles',),
    my_tbn.BK_SND_CHRONICLES: ('II Chronicles',),
}

SEF_ENGLISH_BOOK_NAMES = {bkid: p[0] for bkid, p in _SEF_BOOK_PROPERTIES.items()}
BKID_FR_SEBN = {p[0]: bkid for bkid, p in _SEF_BOOK_PROPERTIES.items()}
