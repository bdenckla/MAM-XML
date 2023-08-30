""" Exports some constants commonly needed for Sefaria-related work. """

import my_tanakh_book_names as my_tbn


_SEF_BOOK_PROPERTIES = {
    my_tbn.BK_GENESIS: ('Genesis',),
    my_tbn.BK_EXODUS: ('Exodus',),
    my_tbn.BK_LEVIT: ('Leviticus',),
    my_tbn.BK_NUMBERS: ('Numbers',),
    my_tbn.BK_DEUTER: ('Deuteronomy',),
    my_tbn.BK_JOSHUA: ('Joshua',),
    my_tbn.BK_JUDGES: ('Judges',),
    my_tbn.BK_FST_SAM: ('I Samuel',),
    my_tbn.BK_SND_SAM: ('II Samuel',),
    my_tbn.BK_FST_KGS: ('I Kings',),
    my_tbn.BK_SND_KGS: ('II Kings',),
    my_tbn.BK_ISAIAH: ('Isaiah',),
    my_tbn.BK_JEREM: ('Jeremiah',),
    my_tbn.BK_EZEKIEL: ('Ezekiel',),
    my_tbn.BK_HOSEA: ('Hosea',),
    my_tbn.BK_JOEL: ('Joel',),
    my_tbn.BK_AMOS: ('Amos',),
    my_tbn.BK_OBADIAH: ('Obadiah',),
    my_tbn.BK_JONAH: ('Jonah',),
    my_tbn.BK_MICAH: ('Micah',),
    my_tbn.BK_NAXUM: ('Nahum',),
    my_tbn.BK_XABA: ('Habakkuk',),
    my_tbn.BK_TSEF: ('Zephaniah',),
    my_tbn.BK_XAGGAI: ('Haggai',),
    my_tbn.BK_ZEKHAR: ('Zechariah',),
    my_tbn.BK_MALAKHI: ('Malachi',),
    my_tbn.BK_PSALMS: ('Psalms',),
    my_tbn.BK_PROV: ('Proverbs',),
    my_tbn.BK_JOB: ('Job',),
    my_tbn.BK_SONG: ('Song of Songs',),
    my_tbn.BK_RUTH: ('Ruth',),
    my_tbn.BK_LAMENT: ('Lamentations',),
    my_tbn.BK_QOHELET: ('Ecclesiastes',),
    my_tbn.BK_ESTHER: ('Esther',),
    my_tbn.BK_DANIEL: ('Daniel',),
    my_tbn.BK_EZRA: ('Ezra',),
    my_tbn.BK_NEXEM: ('Nehemiah',),
    my_tbn.BK_FST_CHR: ('I Chronicles',),
    my_tbn.BK_SND_CHR: ('II Chronicles',),
}

SEF_BKNA = {bkid: p[0] for bkid, p in _SEF_BOOK_PROPERTIES.items()}
