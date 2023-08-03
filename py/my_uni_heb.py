"""
This module exports:
    do_quick_test
    shortened_unicode_name
    accent_names
    hechar_names
    write_verse_un
"""

import unicodedata
import my_html
import my_tanakh_book_names as my_tbn
import my_hebrew_letters as hl
import my_hebrew_points as hp
from my_str_defs import CGJ, NBSP


def do_quick_test():
    lines1 = _get_pre_lines(' ', ' '+'אבג')
    lines2 = _get_pre_lines(' ', 'דהו'+' ')
    lines3 = _get_pre_lines(' ', ' '+'זחט'+' ')
    assert lines1 == [' ', 'אבג']
    assert lines2 == ['דהו', ' ']
    assert lines3 == [' ', 'זחט', ' ']


def shortened_unicode_name(string):
    """ return a shortened name of the string,
    if we "know" a shortened name for it
    """
    if nonhe := _HE_TO_NONHE_DIC.get(string):
        return nonhe
    if muns := _MISC_UNI_NAME_SHORTENINGS.get(string):
        return muns
    fullname = unicodedata.name(string)
    fullname_words = fullname.split()
    if len(fullname_words) < 3:
        return fullname
    sfpp = _shorten_fullname_prefix(fullname_words[0], fullname_words[1])
    return sfpp + ' ' + ' '.join(fullname_words[2:])


def accent_names(string):
    return filter(None, (_HE_TO_NONHE_ACC_DIC.get(c) for c in string))


def hechar_names(string):
    return (_HE_TO_NONHE_DIC[c] for c in string)


def write_verse_un(out_fp, bcvt, multiverse):
    """ Write verse in "unicode names" format """
    bkid, chnu, vrnu = my_tbn.bcvt_get_bcv_triple(bcvt)
    vtrad = my_tbn.bcvt_get_vtrad(bcvt)
    out_fp.write(f'{bkid} {chnu}:{vrnu} in vtrad {vtrad}\n')
    dual = multiverse['cant_dual']
    alef = multiverse['cant_alef']
    bet = multiverse['cant_bet']
    if alef or bet:
        assert alef and bet
        _write_segments(out_fp, dual, 'cant_dual')
        _write_segments(out_fp, alef, 'cant_alef')
        _write_segments(out_fp, bet, 'cant_bet')
    else:
        _write_segments(out_fp, dual, None)
    out_fp.write('\n')


def _mk_he_to_nonhe_dic():
    nonhe_set = set()
    for _, nonhe in _HE_AND_NONHE_PAIRS:  # _ is he
        assert nonhe not in nonhe_set
        nonhe_set.add(nonhe)
    return dict(_HE_AND_NONHE_PAIRS)


def _shorten_fullname_prefix(word1, word2):
    return _SHORTEN_DIC.get((word1, word2)) or word1 + ' ' + word2


def _write_segments(out_fp, segments, cant_dab=None, indent=''):
    if cant_dab:
        out_fp.write(f'{cant_dab}\n')
        indent = '    '
    for segment in segments:
        if isinstance(segment, str):
            pre_lines = [segment]
            for sep in ' ', NBSP:
                list_of_lists = [_get_pre_lines(sep, pl) for pl in pre_lines]
                pre_lines = sum(list_of_lists, [])
            for pre_line in pre_lines:
                line = comma_shunna(pre_line)
                out_fp.write(indent + line + '\n')
            continue
        if isinstance(segment, dict):
            segtag = my_html.hel_get_tag(segment)  # e.g. 'span'
            attr = segment.get('attr')
            kev = _key_eq_val_str(attr or {})
            out_fp.write(indent + f'START {segtag} {kev}\n')
            if contents := segment.get('contents'):
                _write_segments(out_fp, contents, None, indent)
                out_fp.write(indent + f'STOP {segtag} {kev}\n')
            continue
        assert False, 'instance of unexpected type'


def _key_eq_val_str(dic):
    return ' '.join((f'{key}={val}' for key, val in dic.items()))


def _get_pre_lines(sep, segment):
    pre_lines = []
    nsruns = segment.split(sep)  # nsrun: non-sep run
    for nsrun in nsruns[:-1]:
        if nsrun:
            pre_lines.append(nsrun)
        pre_lines.append(sep)
    if nsruns[-1]:
        pre_lines.append(nsruns[-1])
    return pre_lines


def comma_shunna(string):
    """ Comma-joined shortened unicode names """
    return ','.join(shunna(string))


def shunna(string: str):
    """ Tuple of shortened unicode names """
    assert isinstance(string, str)
    return tuple(map(shortened_unicode_name, string))


_SHORTEN_DIC = {
    ('HEBREW', 'LETTER'): 'HLE',
    ('HEBREW', 'POINT'): 'HPO',
    ('HEBREW', 'ACCENT'): 'HAC',
    ('HEBREW', 'PUNCTUATION'): 'HPU',
    ('HEBREW', 'MARK'): 'HMA',
}

_HE_AND_NONHE_LET_PAIRS = (
    (hl.ALEF, 'α'),  # Greek alpha
    (hl.BET, 'v'),  # v not b
    (hl.GIMEL, 'g'),
    (hl.DALET, 'd'),
    (hl.HE, 'h'),
    (hl.VAV, 'w'),
    (hl.ZAYIN, 'z'),
    (hl.XET, 'x'),
    (hl.TET, 'θ'),  # See note on θ
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
    (hp.JSVARIKA, 'varika'),
    (hp.DAGESH_OM, '·'),
    (hp.RAFE, '‾'),  # r̄ was another candidate
    (hp.SHIND, '·sh'),
    (hp.SIND, '·si'),
    (hp.SHEVA, ':'),  # ambiguous, could be na or nach
    (hp.XSEGOL, ':∵'),  # ∵ aka BECAUSE
    (hp.XPATAX, ':_'),
    (hp.XQAMATS, ':a'),
    (hp.XIRIQ, 'i'),
    (hp.TSERE, '‥'),
    (hp.SEGOL, '∵'),  # ∵ aka BECAUSE
    (hp.PATAX, '_'),
    (hp.QAMATS, 'a'),  # ambiguous, could be gadol or qatan
    (hp.QAMATS_Q, 'oa'),
    (hp.XOLAM_XFV, 'ḥḥfv'),
    (hp.XOLAM, 'o'),  # see "Note on plain holam" below
    (hp.QUBUTS, 'u'),
)
_HE_AND_NONHE_ACC_PAIRS = (
    ('\N{HEBREW POINT METEG}', '𝓂'),  # we consider it an accent not a point
    ('\N{HEBREW ACCENT ETNAHTA}', '⅄'),
    ('\N{HEBREW ACCENT SEGOL}', '∴'),  # ∴ aka THEREFORE
    ('\N{HEBREW ACCENT SHALSHELET}', '(sh)'),
    ('\N{HEBREW ACCENT ZAQEF QATAN}', 'ƶ'),
    ('\N{HEBREW ACCENT ZAQEF GADOL}', 'Ƶ'),
    ('\N{HEBREW ACCENT TIPEHA}', '(ti)'),
    ('\N{HEBREW ACCENT REVIA}', '◆'),  # ◆ aka BLACK DIAMOND
    ('\N{HEBREW ACCENT ZARQA}', '≁'),  # See: Note on zinor
    ('\N{HEBREW ACCENT PASHTA}', '(p)'),
    ('\N{HEBREW ACCENT YETIV}', '(ye)'),
    ('\N{HEBREW ACCENT TEVIR}', '⟓'),
    ('\N{HEBREW ACCENT GERESH}', '(ge)'),
    ('\N{HEBREW ACCENT GERESH MUQDAM}', 'γ'),  # Greek small gamma
    ('\N{HEBREW ACCENT GERSHAYIM}', '(G)'),
    ('\N{HEBREW ACCENT QARNEY PARA}', '(qp)'),
    ('\N{HEBREW ACCENT TELISHA GEDOLA}', '⌕'),  # aka TELEPHONE RECORDER
    ('\N{HEBREW ACCENT PAZER}', 'μ'),  # Greek small mu
    ('\N{HEBREW ACCENT ATNAH HAFUKH}', '(ah)'),
    ('\N{HEBREW ACCENT MUNAH}', '⅃'),
    ('\N{HEBREW ACCENT MAHAPAKH}', '<'),
    ('\N{HEBREW ACCENT MERKHA}', '(me)'),
    ('\N{HEBREW ACCENT MERKHA KEFULA}', '(mk)'),
    ('\N{HEBREW ACCENT DARGA}', '(da)'),
    ('\N{HEBREW ACCENT QADMA}', '(qa)'),
    ('\N{HEBREW ACCENT TELISHA QETANA}', '(tq)'),
    ('\N{HEBREW ACCENT YERAH BEN YOMO}', '(yy)'),
    ('\N{HEBREW ACCENT OLE}', '(ol)'),
    ('\N{HEBREW ACCENT ILUY}', '(il)'),
    ('\N{HEBREW ACCENT DEHI}', '(de)'),
    ('\N{HEBREW ACCENT ZINOR}', '~'),  # See: Note on zinor
)
_HE_AND_NONHE_PUNC_PAIRS = (
    ('\N{HEBREW PUNCTUATION MAQAF}', '-'),
    ('\N{HEBREW PUNCTUATION PASEQ}', '|'),
    ('\N{HEBREW PUNCTUATION SOF PASUQ}', '.'),  # ‡ would be another option
)
_MISC_UNI_NAME_SHORTENINGS = {
    CGJ: 'CGJ',
}
_HE_AND_NONHE_PAIRS = (
    _HE_AND_NONHE_LET_PAIRS +
    _HE_AND_NONHE_POINT_PAIRS +
    _HE_AND_NONHE_PUNC_PAIRS +
    _HE_AND_NONHE_ACC_PAIRS)
_HE_TO_NONHE_DIC = _mk_he_to_nonhe_dic()
_HE_TO_NONHE_ACC_DIC = dict(_HE_AND_NONHE_ACC_PAIRS)

# Note on θ
# Note on plain holam
# Note on zinor
#
# See my_split_hebrew_mappings.py for all 3 of these notes.
