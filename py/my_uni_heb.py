"""
This module exports:
    shunna
    accent_names
    hechar_names
    comma_shunnas
    t_shunna
"""

import unicodedata
import my_hebrew_letters as hl
import my_hebrew_points as hpo
import my_hebrew_accents as ha
import my_str_defs as sd


def shunna(string):
    """ Return a shortened name of the string, if we "know" a shortened name for it. """
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


def hechar_names(string):
    """ Return Hebrew character names. """
    return (_HE_TO_NONHE_DIC[c] for c in string)


def comma_shunnas(string):
    """ Comma-joined shortened unicode names """
    return ','.join(t_shunnas(string))


def t_shunnas(string: str):
    """ Tuple of shortened unicode names """
    assert isinstance(string, str)
    return tuple(map(shunna, string))


def _mk_he_to_nonhe_dic():
    nonhe_set = set()
    for _, nonhe in _HE_AND_NONHE_PAIRS:  # _ is he
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
    (hpo.DAGESH_OM, '·'),
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
    (hpo.XOLAM_XFV, 'ḥḥfv'),
    (hpo.XOLAM, 'o'),  # see "Note on plain holam" below
    (hpo.QUBUTS, 'u'),
)
_HE_AND_NONHE_ACC_PAIRS = (
    (hpo.METEG, '𝓂'),  # we consider it an accent not a point
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
    ('\N{HEBREW ACCENT DEHI}', '(de)'),
    (ha.ZARQA, '~'),  # See: Note on zinor
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

# Note on θ (theta)
# Note on plain holam
# Note on zinor
#
# See my_split_hebrew_mappings.py for all 3 of these notes.
