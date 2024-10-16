"""
This module exports:
    shunna
    accent_names
    he_char_names
    join_shunnas
    t_shunnas
"""

import unicodedata
import my_hebrew_letters as hl
import my_hebrew_points as hpo
import my_hebrew_punctuation as hpu
import my_hebrew_accents as ha
import my_str_defs as sd


def shunna(string):
    """
    Return the short name for the Unicode code point in the given (length-1) string,
    if we "know" a short name for it.
    Otherwise give the standard Unicode name.
    """
    if nonhe := _HE_TO_NONHE_DIC.get(string):
        return nonhe
    fullname = unicodedata.name(string)
    fullname_words = fullname.split()
    if len(fullname_words) < 3:
        return fullname
    sfpp = _shorten_fullname_prefix(fullname_words[0], fullname_words[1])
    return sfpp + ' ' + ' '.join(fullname_words[2:])


def accent_names(string):
    """ Return accent names. """
    return filter(None, (_HE_TO_NONHE_ACC_DIC.get(c) for c in string))


def he_char_names(string):
    """ Return Hebrew character names. """
    return (_HE_TO_NONHE_DIC[c] for c in string)


def join_shunnas(string, sep=','):
    """
    Join the short unicode names of the chars of a string.
    Join with the given separator, or comma by default.
    """
    return sep.join(t_shunnas(string))


def t_shunnas(string: str):
    """ Tuple of short unicode names """
    assert isinstance(string, str)
    return tuple(map(shunna, string))


def _mk_he_to_nonhe_dic():
    nonhe_set = set()
    for _he, nonhe in _HE_AND_NONHE_PAIRS:
        assert nonhe not in nonhe_set
        nonhe_set.add(nonhe)
    return dict(_HE_AND_NONHE_PAIRS)


def _shorten_fullname_prefix(word1, word2):
    return _SHORTEN_DIC.get((word1, word2)) or word1 + ' ' + word2


_SHORTEN_DIC = {
    ('HEBREW', 'LETTER'): 'HLE',
    ('HEBREW', 'POINT'): 'HPO',
    ('HEBREW', 'ACCENT'): 'HAC',
    ('HEBREW', 'PUNCTUATION'): 'HPU',
    ('HEBREW', 'MARK'): 'HMA',
}

_HE_AND_NONHE_LETT_PAIRS = (
    (hl.ALEF, 'α'),  # Greek alpha
    (hl.BET, 'v'),  # v not b
    (hl.GIMEL, 'g'),
    (hl.DALET, 'd'),
    (hl.HE, 'h'),
    (hl.VAV, 'w'),
    (hl.ZAYIN, 'z'),
    (hl.XET, 'x'),
    (hl.TET, 'θ'),  # See note on θ (theta)
    (hl.YOD, 'y'),
    (hl.FKAF, 'k.'),
    (hl.KAF, 'k'),
    (hl.LAMED, 'l'),
    (hl.FMEM, 'm.'),
    (hl.MEM, 'm'),
    (hl.FNUN, 'n.'),
    (hl.NUN, 'n'),
    (hl.SAMEKH, 'σ'),  # Greek sigma
    (hl.AYIN, 'ʕ'),  # PHARYNGEAL VOICED FRICATIVE
    (hl.FPE, 'f.'),  # f. not p.
    (hl.PE, 'f'),  # f not p
    (hl.FTSADI, 'ц.'),
    (hl.TSADI, 'ц'),  # Cyrillic small letter tse
    (hl.QOF, 'q'),
    (hl.RESH, 'r'),
    (hl.SHIN, '$'),
    (hl.TAV, 'τ'),  # Greek tau
)
_HE_AND_NONHE_POINT_PAIRS = (
    (hpo.JSVARIKA, 'varika'),
    (hpo.DAGOMOSD, '·'),
    (hpo.RAFE, '‾'),  # r̄ was another candidate
    (hpo.SHIND, '·sh'),
    (hpo.SIND, '·si'),
    (hpo.SHEVA, ':'),  # ambiguous, could be na or nach
    (hpo.XSEGOL, ':∵'),  # ∵ aka BECAUSE
    (hpo.XPATAX, ':_'),
    (hpo.XQAMATS, ':a'),
    (hpo.XIRIQ, 'i'),
    (hpo.TSERE, '‥'),
    (hpo.SEGOL_V, '∵'),  # ∵ aka BECAUSE
    (hpo.PATAX, '_'),
    (hpo.QAMATS, 'a'),  # ambiguous, could be gadol or qatan
    (hpo.QAMATS_Q, 'oa'),
    (hpo.XOLAM_XFV, 'ḥḥfv'),
    (hpo.XOLAM, 'o'),
    (hpo.QUBUTS, 'u'),
)
_HE_AND_NONHE_ACC_PAIRS = (
    (hpo.MTGOSLQ, '𝓂'),  # we consider it an accent not a point
    (ha.ATN, '⅄'),
    (ha.SEG_A, '∴'),  # ∴ aka THEREFORE
    ('\N{HEBREW ACCENT SHALSHELET}', '(sh)'),
    ('\N{HEBREW ACCENT ZAQEF QATAN}', 'ƶ'),
    ('\N{HEBREW ACCENT ZAQEF GADOL}', 'Ƶ'),
    (ha.TIP, '(ti)'),
    (ha.REV, '◆'),  # ◆ aka BLACK DIAMOND
    (ha.ZARQA_SH, '≁'),  # See: Note on zinor
    (ha.PASH, '(p)'),
    ('\N{HEBREW ACCENT YETIV}', '(ye)'),
    ('\N{HEBREW ACCENT TEVIR}', '⟓'),
    (ha.GER, '(ge)'),
    (ha.GER_M, 'γ'),  # Greek small gamma
    (ha.GER_2, '(G)'),
    ('\N{HEBREW ACCENT QARNEY PARA}', '(qp)'),
    (ha.TEL_G, '⌕'),  # aka TELEPHONE RECORDER
    ('\N{HEBREW ACCENT PAZER}', 'μ'),  # Greek small mu
    (ha.ATN_H, '(ah)'),
    (ha.MUN, '⅃'),
    ('\N{HEBREW ACCENT MAHAPAKH}', '<'),
    (ha.MER, '(me)'),
    ('\N{HEBREW ACCENT MERKHA KEFULA}', '(mk)'),
    ('\N{HEBREW ACCENT DARGA}', '(da)'),
    ('\N{HEBREW ACCENT QADMA}', '(qa)'),
    (ha.TEL_Q, '(tq)'),
    (ha.YBY, '(yy)'),
    (ha.OLE, '(ol)'),
    ('\N{HEBREW ACCENT ILUY}', '(il)'),
    (ha.DEX, '(de)'),
    (ha.Z_OR_TSOR, '~'),  # See: Note on zinor
)
_HE_AND_NONHE_PUNC_PAIRS = (
    ('\N{HEBREW PUNCTUATION MAQAF}', '-'),
    ('\N{HEBREW PUNCTUATION PASEQ}', '|'),
    ('\N{HEBREW PUNCTUATION SOF PASUQ}', '.'),  # ‡ would be another option
)
_MISC_UNI_NAME_SHORTENINGS = (
    (sd.CGJ, 'CGJ'),
)
_HE_AND_NONHE_PAIRS = (
    _MISC_UNI_NAME_SHORTENINGS +
    _HE_AND_NONHE_LETT_PAIRS +
    _HE_AND_NONHE_POINT_PAIRS +
    _HE_AND_NONHE_PUNC_PAIRS +
    _HE_AND_NONHE_ACC_PAIRS)
_HE_TO_NONHE_DIC = _mk_he_to_nonhe_dic()
_HE_TO_NONHE_ACC_DIC = dict(_HE_AND_NONHE_ACC_PAIRS)

#######################################
# Note on θ (theta)
#
# Is θ (theta) a bad choice for tet since θ is IPA for tav?
# Relatedly, there is a (mostly historic) transliteration of tav
# as "th". A notable example is the English word "Sabbath"!
# We chose theta for tet because its name reminded us of tet.
# Similarly we chose tau for tav because of its name reminded us of tav.
#######################################
# Note on zinor
#
# Really the accent called ZINOR in Unicode
# should be called TSINOR or TSINOR/ZARQA.
# So its name is not great, but not terrible.
#
# More messed up is this related situation:
# Really the accent called ZARQA in Unicode
# should be called TSINORIT or TSINORIT/ZARQA STRESS HELPER.
