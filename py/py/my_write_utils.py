"""
Exports:
    write_bkg_in_un_fmt
    bkg_path
"""

import py.my_html as my_html
import py.my_open as my_open
import py.my_utils as my_utils
import py.my_uni_heb as uh
import py.my_verse_and_friends as vaf
import py.my_locales as tbn
import py.my_str_defs as sd


def write_bkg_in_un_fmt(variant, bkg_name, verses, rv_cant_that_covers):
    """ Write book group in "Unicode names" format. """
    do_quick_test_of_get_pre_lines()
    path = bkg_path(variant, bkg_name, fmt_is_unicode_names=True)
    title = f'unicode_names {bkg_name}'
    verses_dicts = my_utils.dv_map(dict, verses)
    my_open.with_tmp_openw(
        path, {},
        _write_callback, verses, rv_cant_that_covers, title, verses_dicts)
    

# Yes we could programmatically generate these but I want them to be
# discoverable by search.
_FOLDERS = {
    '': {
        'vff-unicode-names': 'unicode-names',
        'vff-csv': 'csv',
        'vff-xml': 'xml',
    },
    'vpq-vtrad-bhs': {
        'vff-unicode-names': 'unicode-names-vtrad-bhs',
        'vff-csv': 'csv-vtrad-bhs',
        'vff-xml': 'xml-vtrad-bhs',
    },
    'vpq-vtrad-sef': {
        'vff-unicode-names': 'unicode-names-vtrad-sef',
        'vff-csv': 'csv-vtrad-sef',
        'vff-xml': 'xml-vtrad-sef',
    },
    'vpq-vtrad-mam': {
        'vff-unicode-names': 'unicode-names-vtrad-mam',
        'vff-csv': 'csv-vtrad-mam',
        'vff-xml': 'xml-vtrad-mam',
    },
    'vpq-ajf': {
        'vff-unicode-names': 'unicode-names-ajf',
        'vff-csv': 'csv-ajf',
        'vff-xml': 'xml-ajf',
    },
}
_EXTENSIONS = {
    'vff-unicode-names': '.txt',
    'vff-csv': '.csv',
    'vff-xml': '.xml',
}


def bkg_path(variant, bkg_name, fmt_is_unicode_names=False):
    """ Return path based on book group name bkg_name. """
    if fmt_is_unicode_names:
        fmt = 'vff-unicode-names'
    else:
        fmt = variant.get('variant-file-format') or 'vff-csv'
    path_qual = variant.get('variant-path-qual') or ''
    # path_qual examples include '' (the empty string) and 'vpq-ajf'
    folders = _FOLDERS[path_qual]
    mam_for_xxx = variant.get('variant-mam-for-xxx') or 'MAM-for-Sefaria'
    parent = f'../{mam_for_xxx}/out'
    path = f'{parent}/{folders[fmt]}/{bkg_name}{_EXTENSIONS[fmt]}'
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
    if isinstance(some_kind_of_verse, (tuple, list)):
        html_els = some_kind_of_verse
        _write_segments_from_html_els(
            out_fp, html_els, cant_dab, indent)
        return
    if isinstance(some_kind_of_verse, vaf.VerseAndFriends):
        veraf = some_kind_of_verse
        for html_els in (veraf.verse, veraf.vaf_next_cp, veraf.good_ending):
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
                line = uh.join_shunnas(pre_line)
                out_fp.write(indent + line + '\n')
            continue
        if isinstance(html_el, dict):
            segtag = my_html.htel_get_tag(html_el)  # e.g. 'span'
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


