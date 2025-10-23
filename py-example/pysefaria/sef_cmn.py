""" Exports SEF_BKNA """

from pycmn import bib_locales as tbn


_SEF_BOOK_PROPERTIES = {
    tbn.BK_GENESIS: ("Genesis",),
    tbn.BK_EXODUS: ("Exodus",),
    tbn.BK_LEVIT: ("Leviticus",),
    tbn.BK_NUMBERS: ("Numbers",),
    tbn.BK_DEUTER: ("Deuteronomy",),
    tbn.BK_JOSHUA: ("Joshua",),
    tbn.BK_JUDGES: ("Judges",),
    tbn.BK_FST_SAM: ("I Samuel",),
    tbn.BK_SND_SAM: ("II Samuel",),
    tbn.BK_FST_KGS: ("I Kings",),
    tbn.BK_SND_KGS: ("II Kings",),
    tbn.BK_ISAIAH: ("Isaiah",),
    tbn.BK_JEREM: ("Jeremiah",),
    tbn.BK_EZEKIEL: ("Ezekiel",),
    tbn.BK_HOSHEA: ("Hosea",),
    tbn.BK_JOEL: ("Joel",),
    tbn.BK_AMOS: ("Amos",),
    tbn.BK_OVADIAH: ("Obadiah",),
    tbn.BK_JONAH: ("Jonah",),
    tbn.BK_MIKHAH: ("Micah",),
    tbn.BK_NAXUM: ("Nahum",),
    tbn.BK_XABA: ("Habakkuk",),
    tbn.BK_TSEF: ("Zephaniah",),
    tbn.BK_XAGGAI: ("Haggai",),
    tbn.BK_ZEKHAR: ("Zechariah",),
    tbn.BK_MALAKHI: ("Malachi",),
    tbn.BK_PSALMS: ("Psalms",),
    tbn.BK_PROV: ("Proverbs",),
    tbn.BK_JOB: ("Job",),
    tbn.BK_SONG: ("Song of Songs",),
    tbn.BK_RUTH: ("Ruth",),
    tbn.BK_LAMENT: ("Lamentations",),
    tbn.BK_QOHELET: ("Ecclesiastes",),
    tbn.BK_ESTHER: ("Esther",),
    tbn.BK_DANIEL: ("Daniel",),
    tbn.BK_EZRA: ("Ezra",),
    tbn.BK_NEXEM: ("Nehemiah",),
    tbn.BK_FST_CHR: ("I Chronicles",),
    tbn.BK_SND_CHR: ("II Chronicles",),
}

SEF_BKNA = {bkid: p[0] for bkid, p in _SEF_BOOK_PROPERTIES.items()}
