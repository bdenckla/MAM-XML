"""
This module exports various constants and functions related to identifying
the books of the Hebrew Bible and identifying verses within those books.
"""

# Various programs take a --book39tbn argument.
# This comment explains here, centrally, what values are expected for such an
# argument.
# book39tbn is a book name of the following type:
#    * It names a book in the "1 out of 39 books" sense of the word "book".
#         (This is as opposed to the "1 out of 24 books" sense.)
#    * It names these books using our "tbn" convention. The "tbn" convention
#         is encoded here in the my_tanakh_book_names Python module, in
#         constants like FST_SAMUEL.
# A pithy example of a valid value for book39tbn is 1Samuel.
# The example is pithy since:
#    * It shows that this is a "39 books" name, since we identify a "half"
#         of Samuel.
#    * It shows that this is neither the Sefaria nor the UXLC book naming
#         convention: since those would be I Samuel and Samuel_1 respectively.


def book_is_of_sec(in_section, bkid):
    """ Return whether the given book belongs to the given section. """
    return section(bkid) == in_section


def books_of_sec(in_section):
    """ Return a tuple of all book names in the given section. """
    return tuple(b for b in ALL_BOOK_IDS if book_is_of_sec(in_section, b))


def section(bkid):
    """ Return the section to which the given book belongs. """
    return _bkprop_section(_BOOK_PROPERTIES[bkid])


def book_is_of_bk24(in_bk24id, bkid):
    """ Return whether the given book belongs to the given book24. """
    return _bkprop_bk24id(_BOOK_PROPERTIES[bkid]) == in_bk24id


def bkids_of_bk24(in_bk24id):
    """ Return a tuple of all book names in the given book24. """
    return tuple(b for b in ALL_BOOK_IDS if book_is_of_bk24(in_bk24id, b))


def bk24id(bkid):
    """ Return the book24 to which the given book belongs. """
    return _bkprop_bk24id(_BOOK_PROPERTIES[bkid])


def ordered_short(bkid):  # E.g. 'A1' for GENESIS, 'FD' for SND_CHRONICLES
    """
        Returns the ordered short name (2 alphanumerics) corresponding to the
        given book.
        E.g. A1 for Genesis, BA for 1Samuel.
        The 1st alphanumeric is a letter in the range A to F
        corresponding to the book's section.
        The 2nd alphanumeric is a capital Latin letter or base-10 digit.
        This 2nd alphanumeric identifies and orders the book within its
        section.
        ASCII ordering, in particular digits-before-letters ordering,
        is assumed. E.g. B1 (Joshua) comes before BA (1Samuel).
    """
    return _bkprop_ordered_short(_BOOK_PROPERTIES[bkid])


def ordered_short_sena(sena):  # E.g. 'A' for SEC_TORAH, 'B' for SEC_NEV_RISH
    """
        Returns section code A thru F for section with name sena.
    """
    dic = {
        SEC_TORAH: 'A',
        SEC_NEV_RISH: 'B',
        SEC_NEV_AX: 'C',
        SEC_SIF_EM: 'D',
        SEC_XAM_MEG: 'E',
        SEC_KET_ACH: 'F'
    }
    return dic[sena]


def ordered_short_dash_full(bkid):
    """ Return, for example, A1-Genesis given Genesis """
    return f'{ordered_short(bkid)}-{bkid}'


def ordered_short_dash_full_sena(sena):
    """ Return, for example, A-Torah given Torah """
    return f'{ordered_short_sena(sena)}-{sena}'


def short_bcv(bcv):
    """
       Returns, for example, G2:3 for Genesis chapter 2 verse 3.
       Note that, to minimize string length, there is no space between the
       (short) book name and the chapter.
    """
    return short(bcv[0]) + str(bcv[1]) + ':' + str(bcv[2])


def ordered_short_bcv(bcv):
    """
    Returns, for example, A1G0203 for Genesis 2:3.
    """
    ord_bk = ordered_short(bcv[0])
    sht_bk = short(bcv[0])
    ord_chnu_str = my_zfill(bcv[1], _max_width_for_chnu(bcv[0]))
    ord_vrnu_str = my_zfill(bcv[2], _max_width_for_vrnu(bcv[0], bcv[1]))
    return ord_bk + sht_bk + ord_chnu_str + ord_vrnu_str


def my_zfill(the_int, width):
    """ Call str.zfill, asserting that width is adhered to. """
    out = str(the_int).zfill(width)
    assert len(out) == width
    return out


def short_bcv_of_bcvt(bcvt):
    """ Like short_bcv but on a bcvt. """
    return short_bcv(bcvt_get_bcv_triple(bcvt))


def has_dualcant(bcvtmam):  # bcvt in MAM vtrad
    """ Return whether locale bcvt has dual cantillation """
    assert bcvt_is_tmam(bcvtmam)
    return (
        bcvtmam == _SAGA_OF_REUBEN_BCV or
        bcvtmam in _EXDEC_RANGE or
        bcvtmam in _DEDEC_RANGE)


def is_poetcant(bcvt):
    """ Return whether locale uses poetic (as opposed to prose) cantillation. """
    bkid = bcvt_get_bkid(bcvt)
    return section(bkid) == SEC_SIF_EM and not _is_prose_section_of_job(bcvt)


def nu10(verse_num, vtrad):
    """ Return a bcvt in Numbers chapter 10 """
    cvt = mk_cvt(10, verse_num, vtrad)
    return mk_bcvt(BK_NUMBERS, cvt)


def add_part2_bkids(bkids):
    """
    For each "part 1" bkid included in bkids, add the "part 2" ("next") bkid.
    """
    nexts = tuple(filter(None, map(part2_bkid, bkids)))
    return tuple(set(bkids + tuple(nexts)))


def part2_bkid(bkid):
    """
    If bkid is part 1 of a 2-part book, return the bkid of part 2.
    Otherwise return None.
    """
    the_next_bkid = {  # next book ID
        BK_FST_SAM: BK_SND_SAM,
        BK_FST_KGS: BK_SND_KGS,
        BK_FST_CHR: BK_SND_CHR,
        BK_EZRA: BK_NEXEM,
    }
    return the_next_bkid.get(bkid)


def mk_bcvtmam(bkid, chnu, vrnu):
    """ Return a bcvt with t=VT_MAM """
    return mk_bcvt(bkid, mk_cvtmam(chnu, vrnu))


def mk_bcvtsef(bkid, chnu, vrnu):
    """ Return a bct with t=vtrad Sef """
    return mk_bcvt(bkid, mk_cvtsef(chnu, vrnu))


def mk_bcvtbhs(bkid, chnu, vrnu):
    """ Return a bcvt with t=vtrad BHS """
    return mk_bcvt(bkid, mk_cvtbhs(chnu, vrnu))


def mk_bcvtxxx(bkid, chnu, vrnu, vtrad):
    """ Return a bcvt with t=the given vtrad """
    return mk_bcvt(bkid, mk_cvt(chnu, vrnu, vtrad))


def mk_bcvt(bkid, cvt):
    """ Make a bcvt from a cvt """
    return '_bcvt', bkid, *cvt


def mk_cvtmam(chnu, vrnu):
    """ Return a cv qualified with VT_MAM """
    return chnu, vrnu, VT_MAM


def mk_cvtsef(chnu, vrnu):
    """ Return a cv with vtrad Sef """
    return chnu, vrnu, VT_SEF


def mk_cvtbhs(chnu, vrnu):
    """ Return a cv with vtrad BHS """
    return chnu, vrnu, VT_BHS


def mk_cvt(chnu, vrnu, vtrad):
    """ Return a cv with the given vtrad """
    return chnu, vrnu, vtrad


def bcvt_get_bkid(bcvt):
    """ Return the book ID part of bcvt """
    assert _is_bcvt(bcvt)
    return bcvt[1]


def bcvt_get_cvt(bcvt):
    """ Strip the book name """
    assert _is_bcvt(bcvt)
    return bcvt[2:]


def bcvt_get_chnu(bcvt):
    """ Return the chapter number part of bcvt """
    return cvt_get_chnu(bcvt_get_cvt(bcvt))


def bcvt_get_vrnu(bcvt):
    """ Return the verse number part of bcvt """
    return cvt_get_vrnu(bcvt_get_cvt(bcvt))


def bcvt_get_vtrad(bcvt):
    """ Return the vtrad part of bcvt """
    return cvt_get_vtrad(bcvt_get_cvt(bcvt))


def bcvt_get_bcv_triple(bcvt):
    """ Return the book ID, chapter number, and verse number parts of bcvt """
    return bcvt_get_bkid(bcvt), bcvt_get_chnu(bcvt), bcvt_get_vrnu(bcvt)


def bcvt_is_tmam(bcvt):
    """ Return whether the vtrad is VT_MAM """
    return cvt_is_tmam(bcvt_get_cvt(bcvt))


def cvt_get_chnu(cvt):
    """ Return the chnu part of cvt """
    return cvt[0]


def cvt_get_vrnu(cvt):
    """ Return the vrnu part of cvt """
    return cvt[1]


def cvt_get_vtrad(cvt):
    """ Return the vtrad part of cvt """
    return cvt[2]


def cvt_get_chnu_vrnu(cvt):
    """ Return the chnu and vrnu parts of cvt, as a pair """
    return cvt_get_chnu(cvt), cvt_get_vrnu(cvt)


def cvt_is_tmam(cvt):
    """ Return whether the vtrad is VT_MAM """
    return cvt_get_vtrad(cvt) == VT_MAM


def cvt_is_tsef(cvt):
    """ Return whether the vtrad is vtrad Sef """
    return cvt_get_vtrad(cvt) == VT_SEF


def cvt_strip_vtrad(cvt):
    """ Strip the vtrad """
    return cvt[:-1]


def eq_mod_vtrad(cvt_a, cvt_b):
    """ Return whether these cvts are equal modulo their vtrad. """
    return cvt_strip_vtrad(cvt_a) == cvt_strip_vtrad(cvt_b)


def short(bkid):
    """
        Returns the (unordered) short name (1 or 2 letters) corresponding to
        the given book. E.g. G for Genesis, Er for Ezra.
    """
    return _bkprop_short(_BOOK_PROPERTIES[bkid])


def std_from_short(short_book_name):
    """
        Returns the standard book name given the (unordered) short name
        (1 or 2 letters). E.g. Genesis G, Ezra for Er.
    """
    return _SHORT_TO_STD[short_book_name]


def _is_prose_section_of_job(bcvt):
    if bcvt_get_bkid(bcvt) != BK_JOB:
        return False
    chnu = bcvt_get_chnu(bcvt)
    if chnu in (1, 2):
        return True
    vrnu = bcvt_get_vrnu(bcvt)
    return chnu == 42 and vrnu > 6


def _is_bcvt(obj):
    return (
        obj[0] == '_bcvt' and
        obj[1] in ALL_BOOK_IDS and
        isinstance(obj[2], int) and
        isinstance(obj[3], int) and
        obj[4] in ALL_VTRADS)


def _max_width_for_chnu(bkid):
    if bkid == BK_PSALMS:
        return 3
    if bkid in _BOOKS_WITH_LESS_THAN_10_CHAPS:
        return 1
    return 2


def _max_width_for_vrnu(bkid, chnu):
    if (bkid, chnu) == (BK_PSALMS, 119):
        return 3  # Psalm 119 has 176 verses!
    return 2


def _bkprop_bk24id(bkprop):
    return bkprop[0]


def _bkprop_section(bkprop):
    return bkprop[1]


def _bkprop_short(bkprop):
    return bkprop[2]


def _bkprop_ordered_short(bkprop):
    return bkprop[3]


def _shorts_are_unique():
    unique_shorts = set(map(short, ALL_BOOK_IDS))
    return len(unique_shorts) == len(ALL_BOOK_IDS)


def _mk_verse_range(bcvt, length):
    vrnu_start = bcvt_get_vrnu(bcvt)
    vrange = range(vrnu_start, vrnu_start + length)
    return tuple(_bcvt_setv(bcvt, vrnu) for vrnu in vrange)


def _bcvt_setv(bcvt, new_vrnu):
    bkid, cvt = bcvt_get_bkid(bcvt), bcvt_get_cvt(bcvt)
    new_cvt = _cvt_setv(cvt, new_vrnu)
    return mk_bcvt(bkid, new_cvt)


def _cvt_setv(cvt, new_vrnu):
    chnu, vtrad = cvt_get_chnu(cvt), cvt_get_vtrad(cvt)
    return mk_cvt(chnu, new_vrnu, vtrad)


BK_GENESIS = 'Genesis'
BK_EXODUS = 'Exodus'
BK_LEVIT = 'Levit'
BK_NUMBERS = 'Numbers'
BK_DEUTER = 'Deuter'
BK_JOSHUA = 'Joshua'
BK_JUDGES = 'Judges'
BK_FST_SAM = '1Samuel'
BK_SND_SAM = '2Samuel'
BK_FST_KGS = '1Kings'
BK_SND_KGS = '2Kings'
BK_ISAIAH = 'Isaiah'
BK_JEREM = 'Jeremiah'
BK_EZEKIEL = 'Ezekiel'  # guts to change it to Ezeqiel?
BK_HOSHEA = 'Hosea'  # guts to change it to Hoshea?
BK_JOEL = 'Joel'
BK_AMOS = 'Amos'
BK_OVADIAH = 'Obadiah'  # guts to change it to Ovadiah?
BK_JONAH = 'Jonah'
BK_MIKHAH = 'Micah'  # guts to change it to Mikhah or Miḳah?
BK_NAXUM = 'Nahum'  # guts to change it to Naḥum?
BK_XABA = 'Habakkuk'  # guts to change it to Ḥabakkuk? Ḥabaqquq?
BK_TSEF = 'Tsefaniah'
BK_XAGGAI = 'Haggai'  # guts to change it to Ḥaggai?
BK_ZEKHAR = 'Zechariah'  # guts to change it to Zekhariah or Zeḳariah?
BK_MALAKHI = 'Malachi'  # guts to change it to Malakhi or Malaḳi?
BK_PSALMS = 'Psalms'
BK_PROV = 'Proverbs'
BK_JOB = 'Job'
BK_SONG = 'Song of Songs'
BK_RUTH = 'Ruth'
BK_LAMENT = 'Lamentations'
BK_QOHELET = 'Ecclesiastes'
BK_ESTHER = 'Esther'
BK_DANIEL = 'Daniel'
BK_EZRA = 'Ezra'
BK_NEXEM = 'Nehemiah'  # guts to change it to Neḥemiah?
BK_FST_CHR = '1Chronicles'
BK_SND_CHR = '2Chronicles'

BK24_GENESIS = BK_GENESIS
BK24_EXODUS = BK_EXODUS
BK24_LEVIT = BK_LEVIT
BK24_NUMBERS = BK_NUMBERS
BK24_DEUTER = BK_DEUTER
BK24_JOSHUA = BK_JOSHUA
BK24_JUDGES = BK_JUDGES
BK24_SAMUEL = 'Samuel'
BK24_KINGS = 'Kings'
BK24_ISAIAH = BK_ISAIAH
BK24_JEREM = BK_JEREM
BK24_EZEKIEL = BK_EZEKIEL
BK24_THE_12 = 'The-12-Minor-Prophets'
BK24_PSALMS = BK_PSALMS
BK24_PROV = BK_PROV
BK24_JOB = BK_JOB
BK24_SONG = BK_SONG
BK24_RUTH = BK_RUTH
BK24_LAMENT = BK_LAMENT
BK24_QOHELET = BK_QOHELET
BK24_ESTHER = BK_ESTHER
BK24_DANIEL = BK_DANIEL
BK24_EZ_NE = 'Ezra-Neḥemiah'
BK24_CHRON = 'Chronicles'

SEC_TORAH = 'Torah'
SEC_NEV_RISH = 'NevRish'
SEC_NEV_AX = 'NevAḥ'
SEC_SIF_EM = 'SifEm'
SEC_XAM_MEG = 'ḤamMeg'
SEC_KET_ACH = 'KetAḥ'

VT_MAM = 'vtmam'
VT_SEF = 'vtsef'
VT_BHS = 'vtbhs'
ALL_VTRADS = VT_MAM, VT_SEF, VT_BHS

BKIDS_OF_BOOKS_WITH_DUALCANT = BK_GENESIS, BK_EXODUS, BK_DEUTER

_SH_GENESIS = 'G', 'A1'
_SH_EXODUS = 'E', 'A2'  # E in contrast to Ee, Ec, Es, Er
_SH_LEVIT = 'L', 'A3'  # L in contrast to La
_SH_NUMBERS = 'N', 'A4'  # N in contrast to Ne & Na
_SH_DEUTER = 'D', 'A5'  # D in contrast to Da
_SH_JOSHUA = 'Js', 'B1'  # Jo.*: JsJlJnJb
_SH_JUDGES = 'Ju', 'B2'
_SH_FST_SAM = '1S', 'BA'
_SH_SND_SAM = '2S', 'BB'
_SH_FST_KGS = '1K', 'BC'
_SH_SND_KGS = '2K', 'BD'
_SH_ISAIAH = 'I', 'C1'
_SH_JEREM = 'Je', 'C2'
_SH_EZEKIEL = 'Ee', 'C3'  # Ez.*: EeEr
_SH_HOSEA = 'Ho', 'CA'
_SH_JOEL = 'Jl', 'CB'  # Jo.*: JsJlJnJb
_SH_AMOS = 'A', 'CC'
_SH_OBADIAH = 'O', 'CD'
_SH_JONAH = 'Jn', 'CE'  # Jo.*: JsJlJnJb
_SH_MICAH = 'Mi', 'CF'
_SH_NAXUM = 'Na', 'CG'
_SH_XABA = 'Hb', 'CH'  # Ha.*: HbHg
_SH_TSEF = 'Ts', 'CI'  # was Zp (see note below)
_SH_XAGGAI = 'Hg', 'CJ'  # Ha.*: HbHg
_SH_ZEKHAR = 'Zc', 'CK'  # Zc (see note below)
_SH_MALAKHI = 'Ma', 'CL'
_SH_PSALMS = 'Ps', 'D1'
_SH_PROV = 'Pr', 'D2'
_SH_JOB = 'Jb', 'D3'  # Jo.*: JsJlJnJb
_SH_SONG = 'S', 'E1'
_SH_RUTH = 'R', 'E2'
_SH_LAMENT = 'La', 'E3'
_SH_QOHELET = 'Ec', 'E4'
_SH_ESTHER = 'Es', 'E5'
_SH_DANIEL = 'Da', 'F1'
_SH_EZRA = 'Er', 'FA'  # Ez.*: EeEr
_SH_NEXEM = 'Ne', 'FB'
_SH_FST_CHR = '1C', 'FC'
_SH_SND_CHR = '2C', 'FD'
# Tsefaniah was formerly Zp because (a) it was formerly spelled Zephaniah
# and (b) with this former spelling, Ze would have been ambiguous with
# Zechariah.
# Zechariah is Zc since Ze would have been ambiguous with Tsefaniah when
# Tsefaniah was spelled Zephaniah.


_BOOK_PROPERTIES = {
    BK_GENESIS: (BK24_GENESIS, SEC_TORAH, *_SH_GENESIS),
    BK_EXODUS: (BK24_EXODUS, SEC_TORAH, *_SH_EXODUS),
    BK_LEVIT: (BK24_LEVIT, SEC_TORAH, *_SH_LEVIT),
    BK_NUMBERS: (BK24_NUMBERS, SEC_TORAH, *_SH_NUMBERS),
    BK_DEUTER: (BK24_DEUTER, SEC_TORAH, *_SH_DEUTER),
    BK_JOSHUA: (BK24_JOSHUA, SEC_NEV_RISH, *_SH_JOSHUA),
    BK_JUDGES: (BK24_JUDGES, SEC_NEV_RISH, *_SH_JUDGES),
    BK_FST_SAM: (BK24_SAMUEL, SEC_NEV_RISH, *_SH_FST_SAM),
    BK_SND_SAM: (BK24_SAMUEL, SEC_NEV_RISH, *_SH_SND_SAM),
    BK_FST_KGS: (BK24_KINGS, SEC_NEV_RISH, *_SH_FST_KGS),
    BK_SND_KGS: (BK24_KINGS, SEC_NEV_RISH, *_SH_SND_KGS),
    BK_ISAIAH: (BK24_ISAIAH, SEC_NEV_AX, *_SH_ISAIAH),
    BK_JEREM: (BK24_JEREM, SEC_NEV_AX, *_SH_JEREM),
    BK_EZEKIEL: (BK24_EZEKIEL, SEC_NEV_AX, *_SH_EZEKIEL),
    BK_HOSHEA: (BK24_THE_12, SEC_NEV_AX, *_SH_HOSEA),
    BK_JOEL: (BK24_THE_12, SEC_NEV_AX, *_SH_JOEL),
    BK_AMOS: (BK24_THE_12, SEC_NEV_AX, *_SH_AMOS),
    BK_OVADIAH: (BK24_THE_12, SEC_NEV_AX, *_SH_OBADIAH),
    BK_JONAH: (BK24_THE_12, SEC_NEV_AX, *_SH_JONAH),
    BK_MIKHAH: (BK24_THE_12, SEC_NEV_AX, *_SH_MICAH),
    BK_NAXUM: (BK24_THE_12, SEC_NEV_AX, *_SH_NAXUM),
    BK_XABA: (BK24_THE_12, SEC_NEV_AX, *_SH_XABA),
    BK_TSEF: (BK24_THE_12, SEC_NEV_AX, *_SH_TSEF),
    BK_XAGGAI: (BK24_THE_12, SEC_NEV_AX, *_SH_XAGGAI),
    BK_ZEKHAR: (BK24_THE_12, SEC_NEV_AX, *_SH_ZEKHAR),
    BK_MALAKHI: (BK24_THE_12, SEC_NEV_AX, *_SH_MALAKHI),
    BK_PSALMS: (BK24_PSALMS, SEC_SIF_EM, *_SH_PSALMS),
    BK_PROV: (BK24_PROV, SEC_SIF_EM, *_SH_PROV),
    BK_JOB: (BK24_JOB, SEC_SIF_EM, *_SH_JOB),
    BK_SONG: (BK24_SONG, SEC_XAM_MEG, *_SH_SONG),
    BK_RUTH: (BK24_RUTH, SEC_XAM_MEG, *_SH_RUTH),
    BK_LAMENT: (BK24_LAMENT, SEC_XAM_MEG, *_SH_LAMENT),
    BK_QOHELET: (BK24_QOHELET, SEC_XAM_MEG, *_SH_QOHELET),
    BK_ESTHER: (BK24_ESTHER, SEC_XAM_MEG, *_SH_ESTHER),
    BK_DANIEL: (BK24_DANIEL, SEC_KET_ACH, *_SH_DANIEL),
    BK_EZRA: (BK24_EZ_NE, SEC_KET_ACH, *_SH_EZRA),
    BK_NEXEM: (BK24_EZ_NE, SEC_KET_ACH, *_SH_NEXEM),
    BK_FST_CHR: (BK24_CHRON, SEC_KET_ACH, *_SH_FST_CHR),
    BK_SND_CHR: (BK24_CHRON, SEC_KET_ACH, *_SH_SND_CHR),
}
_BOOKS_WITH_LESS_THAN_10_CHAPS = (
    BK_AMOS,
    BK_XAGGAI,
    BK_XABA,
    BK_LAMENT,
    BK_MALAKHI,
    BK_MIKHAH,
    BK_NAXUM,
    BK_OVADIAH,
    BK_RUTH,
    BK_SONG,
    BK_JOEL,
    BK_JONAH,
    BK_TSEF,
)
ALL_BOOK_IDS = tuple(_BOOK_PROPERTIES.keys())
_ALL_BK24_IDS = {bk24id(bk39id): True for bk39id in ALL_BOOK_IDS}
ALL_BK24_IDS = tuple(_ALL_BK24_IDS.keys())
ALL_SECTION_NAMES = (
    SEC_TORAH, SEC_NEV_RISH, SEC_NEV_AX,
    SEC_SIF_EM, SEC_XAM_MEG, SEC_KET_ACH)
_SHORT_TO_STD = {
    _bkprop_short(prop): std
    for std, prop in _BOOK_PROPERTIES.items()
}
_SAGA_OF_REUBEN_BCV = mk_bcvtmam(BK_GENESIS, 35, 22)
_EXDEC_START = mk_bcvtmam(BK_EXODUS, 20, 2)
_DEDEC_START = mk_bcvtmam(BK_DEUTER, 5, 6)
_EXDEC_RANGE = _mk_verse_range(_EXDEC_START, 12)
_DEDEC_RANGE = _mk_verse_range(_DEDEC_START, 12)

assert _shorts_are_unique()
