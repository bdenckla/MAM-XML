"""
Exports:
    write_bkg_in_un_fmt
    bkg_path
"""

import my_html
import my_open
import my_uni_heb as uh
import my_verse_and_friends as vaf
import my_tanakh_book_names as tbn
import my_str_defs as sd


def write_bkg_in_un_fmt(variant, bkg_name, verses, rv_cant_that_covers):
    """ Write book group in "Unicode names" format. """
    do_quick_test_of_get_pre_lines()
    path = bkg_path(variant, bkg_name, fmt_is_unicode_names=True)
    title = f'unicode_names {bkg_name}'
    verses_dicts = {
        roca: dict(list_of_pairs)
        for roca, list_of_pairs in verses.items()
    }
    my_open.with_tmp_openw(
        path, {},
        _write_callback, verses, rv_cant_that_covers, title, verses_dicts)


def bkg_path(variant, bkg_name, fmt_is_unicode_names=False):
    """ Return path based on book group name bkg_name. """
    if fmt_is_unicode_names:
        fmt = 'unicode_names'
    else:
        fmt = variant.get('variant_file_format') or 'csv'
    path_qual = variant.get('variant_path_qual') or ''
    # vpq examples include '' (the empty string) and '-ajf'
    folders = {
        'unicode_names': f'unicode-names{path_qual}',
        'csv': f'csv{path_qual}',
        'xml': f'xml{path_qual}',
    }
    exts = {
        'unicode_names': '.txt',
        'csv': '.csv',
        'xml': '.xml',
    }
    mam_for_xxx = variant.get('variant_mam_for_xxx') or 'MAM-for-Sefaria'
    parent = f'../{mam_for_xxx}/out'
    path = f'{parent}/{folders[fmt]}/{bkg_name}{exts[fmt]}'
    return path


def _write_callback(verses, rv_cant_that_covers, title, verses_dicts, out_fp):
    out_fp.write(f'{title}\n')
    for bcvt, _verse_body in verses[rv_cant_that_covers]:
        multiverse = {
            roca: verses_dicts[roca].get(bcvt)
            for roca in verses.keys()
            if verses_dicts[roca].get(bcvt) is not None
        }
        _write_verse_un(out_fp, bcvt, multiverse)


def _write_verse_un(out_fp, bcvt, multiverse):
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


def _write_segments(out_fp, some_kind_of_verse, cant_dab=None, indent=''):
    if isinstance(some_kind_of_verse, (list, tuple)):
        html_els = some_kind_of_verse
        _write_segments_from_html_els(
            out_fp, html_els, cant_dab, indent)
        return
    if isinstance(some_kind_of_verse, vaf.VerseAndFriends):
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
                line = uh.comma_shunnas(pre_line)
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


def do_quick_test_of_get_pre_lines():
    """ Do a quick test. """
    lines1 = _get_pre_lines(' ', ' '+'אבג')
    lines2 = _get_pre_lines(' ', 'דהו'+' ')
    lines3 = _get_pre_lines(' ', ' '+'זחט'+' ')
    assert lines1 == [' ', 'אבג']
    assert lines2 == ['דהו', ' ']
    assert lines3 == [' ', 'זחט', ' ']


