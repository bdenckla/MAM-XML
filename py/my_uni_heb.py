"""
This module exports:
    do_quick_test
    shortened_unicode_name
    accent_names
    hechar_names
    write_verse_un
    comma_shunna
    t_shunna
"""

import unicodedata
import my_html
import my_tanakh_book_names as tbn
import my_hebrew_letters as hl
import my_hebrew_points as hpo
import my_hebrew_accents as ha
import my_str_defs as sd
import my_render_wikitext as rwt


def do_quick_test():
    """ Do a quick test. """
    lines1 = _get_pre_lines(' ', ' '+'אבג')
    lines2 = _get_pre_lines(' ', 'דהו'+' ')
    lines3 = _get_pre_lines(' ', ' '+'זחט'+' ')
    assert lines1 == [' ', 'אבג']
    assert lines2 == ['דהו', ' ']
    assert lines3 == [' ', 'זחט', ' ']


def shunna(string):
    """ Return a shortened name of the string,
    if we "know" a shortened name for it
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


def hechar_names(string):
    """ Return Hebrew character names. """
    return (_HE_TO_NONHE_DIC[c] for c in string)


def write_verse_un(out_fp, bcvt, multiverse):
    """ Write verse in "unicode names" format """
    bkid, chnu, vrnu = tbn.bcvt_get_bcv_triple(bcvt)
    vtrad = tbn.bcvt_get_vtrad(bcvt)
    out_fp.write(f'{bkid} {chnu}:{vrnu} in vtrad {vtrad}\n')
    for rv_cant, body in multiverse.items():
        if len(multiverse) > 1:
            _write_segments(out_fp, body, rv_cant)
        else:
            _write_segments(out_fp, body, None)
    out_fp.write('\n')


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


def _write_segments(out_fp, some_kind_of_verse, cant_dab=None, indent=''):
    if isinstance(some_kind_of_verse, (list, tuple)):
        html_els = some_kind_of_verse
        _write_segments_from_html_els(
            out_fp, html_els, cant_dab, indent)
        return
    if isinstance(some_kind_of_verse, rwt.VerseAndFriends):
        veraf = some_kind_of_verse
        for html_els in (veraf.verse, veraf.next_cp, veraf.good_ending):
            _write_segments_from_html_els(
                out_fp, html_els, cant_dab, indent)
        return
    assert False, some_kind_of_verse


def _write_segments_from_html_els(out_fp, html_els, cant_dab=None, indent=''):
    if cant_dab:
        out_fp.write(f'{cant_dab}\n')
        indent = '    '
    for html_el in html_els:
        if isinstance(html_el, str):
            pre_lines = [html_el]
            for sep in ' ', sd.NBSP:
                list_of_lists = [_get_pre_lines(sep, pl) for pl in pre_lines]
                pre_lines = sum(list_of_lists, [])
            for pre_line in pre_lines:
                line = comma_shunnas(pre_line)
                out_fp.write(indent + line + '\n')
            continue
        if isinstance(html_el, dict):
            segtag = my_html.hel_get_tag(html_el)  # e.g. 'span'
            attr = html_el.get('attr')
            kev_strs = _key_eq_val_strs(attr or {})
            if contents := html_el.get('contents'):
                out_fp.write(indent + _stasto('START', segtag, kev_strs))
                _write_segments(out_fp, contents, None, indent)
                out_fp.write(indent + _stasto('STOP', segtag, kev_strs))
            else:
                out_fp.write(indent + _stasto('START/STOP', segtag, kev_strs))
            continue
        assert False, 'instance of unexpected type'


def _key_eq_val_strs(dic):
    return tuple(f'{key}={val}' for key, val in dic.items())


def _stasto(stasto, segtag, kev_strs):
    return ' '.join((stasto, segtag, *kev_strs)) + '\n'


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
    (hpo.SEGOL, '∵'),  # ∵ aka BECAUSE
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
    ('\N{HEBREW ACCENT SEGOL}', '∴'),  # ∴ aka THEREFORE
    ('\N{HEBREW ACCENT SHALSHELET}', '(sh)'),
    ('\N{HEBREW ACCENT ZAQEF QATAN}', 'ƶ'),
    ('\N{HEBREW ACCENT ZAQEF GADOL}', 'Ƶ'),
    (ha.TIP, '(ti)'),
    (ha.REV, '◆'),  # ◆ aka BLACK DIAMOND
    ('\N{HEBREW ACCENT ZARQA}', '≁'),  # See: Note on zinor
    ('\N{HEBREW ACCENT PASHTA}', '(p)'),
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
    ('\N{HEBREW ACCENT TELISHA QETANA}', '(tq)'),
    (ha.YBY, '(yy)'),
    (ha.OLE, '(ol)'),
    ('\N{HEBREW ACCENT ILUY}', '(il)'),
    ('\N{HEBREW ACCENT DEHI}', '(de)'),
    ('\N{HEBREW ACCENT ZINOR}', '~'),  # See: Note on zinor
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

# Note on θ
# Note on plain holam
# Note on zinor
#
# See my_split_hebrew_mappings.py for all 3 of these notes.
