""" Exports some constants commonly needed for Sefaria-related work. """

import my_tanakh_book_names as my_tbn


SEF_BOOK_PROPERTIES = {
    my_tbn.BK_GENESIS: ('Genesis', 'בראשית', 'Torah'),
    my_tbn.BK_EXODUS: ('Exodus', 'שמות', 'Torah'),
    my_tbn.BK_LEVITICUS: ('Leviticus', 'ויקרא', 'Torah'),
    my_tbn.BK_NUMBERS: ('Numbers', 'במדבר', 'Torah'),
    my_tbn.BK_DEUTER: ('Deuteronomy', 'דברים', 'Torah'),
    my_tbn.BK_JOSHUA: ('Joshua', 'יהושע', 'Prophets'),
    my_tbn.BK_JUDGES: ('Judges', 'שופטים', 'Prophets'),
    my_tbn.BK_FST_SAMUEL: ('I Samuel', 'שמואל א', 'Prophets'),
    my_tbn.BK_SND_SAMUEL: ('II Samuel', 'שמואל ב', 'Prophets'),
    my_tbn.BK_FST_KINGS: ('I Kings', 'מלכים א', 'Prophets'),
    my_tbn.BK_SND_KINGS: ('II Kings', 'מלכים ב', 'Prophets'),
    my_tbn.BK_ISAIAH: ('Isaiah', 'ישעיהו', 'Prophets'),
    my_tbn.BK_JEREMIAH: ('Jeremiah', 'ירמיהו', 'Prophets'),
    my_tbn.BK_EZEKIEL: ('Ezekiel', 'יחזקאל', 'Prophets'),
    my_tbn.BK_HOSEA: ('Hosea', 'הושע', 'Prophets'),
    my_tbn.BK_JOEL: ('Joel', 'יואל', 'Prophets'),
    my_tbn.BK_AMOS: ('Amos', 'עמוס', 'Prophets'),
    my_tbn.BK_OBADIAH: ('Obadiah', 'עובדיה', 'Prophets'),
    my_tbn.BK_JONAH: ('Jonah', 'יונה', 'Prophets'),
    my_tbn.BK_MICAH: ('Micah', 'מיכה', 'Prophets'),
    my_tbn.BK_NAXUM: ('Nahum', 'נחום', 'Prophets'),
    my_tbn.BK_XABAKKUK: ('Habakkuk', 'חבקוק', 'Prophets'),
    my_tbn.BK_TSEFANIAH: ('Zephaniah', 'צפניה', 'Prophets'),
    my_tbn.BK_XAGGAI: ('Haggai', 'חגי', 'Prophets'),
    my_tbn.BK_ZEKHARIAH: ('Zechariah', 'זכריה', 'Prophets'),
    my_tbn.BK_MALAKHI: ('Malachi', 'מלאכי', 'Prophets'),
    my_tbn.BK_PSALMS: ('Psalms', 'תהילים', 'Writings'),
    my_tbn.BK_PROVERBS: ('Proverbs', 'משלי', 'Writings'),
    my_tbn.BK_JOB: ('Job', 'איוב', 'Writings'),
    my_tbn.BK_SONG_OF_SONGS: ('Song of Songs', 'שיר השירים', 'Writings'),
    my_tbn.BK_RUTH: ('Ruth', 'רות', 'Writings'),
    my_tbn.BK_LAMENTATIONS: ('Lamentations', 'איכה', 'Writings'),
    my_tbn.BK_ECCLESIASTES: ('Ecclesiastes', 'קהלת', 'Writings'),
    my_tbn.BK_ESTHER: ('Esther', 'אסתר', 'Writings'),
    my_tbn.BK_DANIEL: ('Daniel', 'דניאל', 'Writings'),
    my_tbn.BK_EZRA: ('Ezra', 'עזרא', 'Writings'),
    my_tbn.BK_NEXEMIAH: ('Nehemiah', 'נחמיה', 'Writings'),
    my_tbn.BK_FST_CHRONICLES: ('I Chronicles', 'דברי הימים א', 'Writings'),
    my_tbn.BK_SND_CHRONICLES: ('II Chronicles', 'דברי הימים ב', 'Writings'),
}

SEF_ENGLISH_BOOK_NAMES = {b: p[0] for b, p in SEF_BOOK_PROPERTIES.items()}
SEF_HEBREW_BOOK_NAMES = {b: p[1] for b, p in SEF_BOOK_PROPERTIES.items()}
SEF_TANAKH_SUBCATEGORIES = {b: p[2] for b, p in SEF_BOOK_PROPERTIES.items()}
BKID_FR_SEBN = {p[0]: b for b, p in SEF_BOOK_PROPERTIES.items()}
