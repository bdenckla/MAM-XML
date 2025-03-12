"""
This module exports:
    shunna
    accent_names
    he_char_name
    join_shunnas
    t_shunnas
"""

import unicodedata
import py.hebrew_letters as hl
import py.hebrew_points as hpo
import py.hebrew_punctuation as hpu
import py.hebrew_accents as ha
import py.str_defs as sd


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
    return sfpp + " " + " ".join(fullname_words[2:])


def accent_names(string):
    """Return accent names."""
    return list(filter(None, (_HE_TO_NONHE_ACC_DIC.get(c) for c in string)))


def rm_mtgoslq(string):
    return string.replace(hpo.MTGOSLQ, "")


def he_char_name(unicode_str_of_len_1):
    """Return Hebrew character name."""
    return _HE_TO_NONHE_DIC[unicode_str_of_len_1]


def join_shunnas(string, sep=","):
    """
    Join the short unicode names of the chars of a string.
    Join with the given separator, or comma by default.
    """
    return sep.join(t_shunnas(string))


def t_shunnas(string: str):
    """Tuple of short unicode names"""
    assert isinstance(string, str)
    return tuple(map(shunna, string))


def _mk_he_to_nonhe_dic():
    nonhe_set = set()
    for _he, nonhe in _HE_AND_NONHE_PAIRS:
        assert nonhe not in nonhe_set
        nonhe_set.add(nonhe)
    return dict(_HE_AND_NONHE_PAIRS)


def _shorten_fullname_prefix(word1, word2):
    return _SHORTEN_DIC.get((word1, word2)) or word1 + " " + word2


_SHORTEN_DIC = {
    ("HEBREW", "LETTER"): "HLE",
    ("HEBREW", "POINT"): "HPO",
    ("HEBREW", "ACCENT"): "HAC",
    ("HEBREW", "PUNCTUATION"): "HPU",
    ("HEBREW", "MARK"): "HMA",
}

_HE_AND_NONHE_LETT_PAIRS = (
    (hl.ALEF, "α"),  # Greek alpha
    (hl.BET, "v"),  # v not b
    (hl.GIMEL, "g"),
    (hl.DALET, "d"),
    (hl.HE, "h"),
    (hl.VAV, "w"),
    (hl.ZAYIN, "z"),
    (hl.XET, "x"),
    (hl.TET, "θ"),  # See note on θ (theta)
    (hl.YOD, "y"),
    (hl.FKAF, "k."),
    (hl.KAF, "k"),
    (hl.LAMED, "l"),
    (hl.FMEM, "m."),
    (hl.MEM, "m"),
    (hl.FNUN, "n."),
    (hl.NUN, "n"),
    (hl.SAMEKH, "σ"),  # Greek sigma
    (hl.AYIN, "ʕ"),  # PHARYNGEAL VOICED FRICATIVE
    (hl.FPE, "f."),  # f. not p.
    (hl.PE, "f"),  # f not p
    (hl.FTSADI, "ц."),
    (hl.TSADI, "ц"),  # Cyrillic small letter tse
    (hl.QOF, "q"),
    (hl.RESH, "r"),
    (hl.SHIN, "$"),
    (hl.TAV, "τ"),  # Greek tau
)
_HE_AND_NONHE_POINT_PAIRS = (
    (hpo.VARIKA, "varika"),
    (hpo.DAGOMOSD, "·"),
    (hpo.RAFE, "‾"),  # r̄ was another candidate
    (hpo.SHIND, "·sh"),
    (hpo.SIND, "·si"),
    (hpo.SHEVA, ":"),  # ambiguous, could be na or nax
    (hpo.XSEGOL, ":∵"),  # ∵ aka BECAUSE
    (hpo.XPATAX, ":_"),
    (hpo.XQAMATS, ":a"),
    (hpo.XIRIQ, "i"),
    (hpo.TSERE, "‥"),
    (hpo.SEGOL_V, "∵"),  # ∵ aka BECAUSE
    (hpo.PATAX, "_"),
    (hpo.QAMATS, "a"),  # ambiguous, could be gadol or qatan
    (hpo.QAMATS_Q, "oa"),
    (hpo.XOLAM_XFV, "xxfv"),
    (hpo.XOLAM, "o"),
    (hpo.QUBUTS, "u"),
)
_HE_AND_NONHE_ACC_PAIRS = (
    (ha.Z_OR_TSOR, "~"),  # zarqa or tsinnor; see: Note on zinor
    (ha.ZSH_OR_TSIT, "≁"),  # zarqa stress helper or tsinnorit; see: Note on zinor
    (hpo.MTGOSLQ, "(mos)"),  # meteg or silluq; we consider it an accent not a point
    (ha.ATN, "(atn)"),
    (ha.SEG_A, "(seg_a)"),
    (ha.SHA, "(sha)"),
    (ha.ZAQ_Q, "(zaq_q)"),
    (ha.ZAQ_G, "(zaq_g)"),
    (ha.TIP, "(tip)"),
    (ha.REV, "(rev)"),
    (ha.PASH, "(pash)"),
    (ha.YET, "(yet)"),
    (ha.TEV, "(tev)"),
    (ha.GER, "(ger)"),
    (ha.GER_M, "(ger_m)"),
    (ha.GER_2, "(ger_2)"),
    (ha.QAR, "(qar)"),
    (ha.TEL_G, "(tel_g)"),
    (ha.PAZ, "(paz)"),
    (ha.ATN_H, "(atn_h)"),
    (ha.MUN, "(mun)"),
    (ha.MAH, "(mah)"),
    (ha.MER, "(mer)"),
    (ha.MER_2, "(mer_2)"),
    (ha.DAR, "(dar)"),
    (ha.QOM, "(qom)"),  # qadma or metigah
    (ha.TEL_Q, "(tel_q)"),
    (ha.YBY, "(yby)"),
    (ha.OLE, "(ole)"),
    (ha.ILU, "(ilu)"),
    (ha.DEX, "(dex)"),
)
_HE_AND_NONHE_PUNC_PAIRS = (
    (hpu.MAQ, "-"),
    (hpu.PASOLEG, "|"),
    (hpu.SOPA, "(sopa)"),  # sof pasuq
    (hpu.MCIRC, "ḿ"),  # U+1E3F: LATIN SMALL LETTER M WITH ACUTE
)
_MISC_UNI_NAME_SHORTENINGS = ((sd.CGJ, "CGJ"),)
_HE_AND_NONHE_PAIRS = (
    _MISC_UNI_NAME_SHORTENINGS
    + _HE_AND_NONHE_LETT_PAIRS
    + _HE_AND_NONHE_POINT_PAIRS
    + _HE_AND_NONHE_PUNC_PAIRS
    + _HE_AND_NONHE_ACC_PAIRS
)
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
