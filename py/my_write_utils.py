"""
Exports:
    write_bkg_in_un_fmt
    bkg_path
"""

import my_uni_heb
import my_open


def write_bkg_in_un_fmt(variant, bkg_name, verses, rv_cant_that_covers):
    """ Write book group in "Unicode names" format. """
    my_uni_heb.do_quick_test()
    path = bkg_path(variant, bkg_name, fmt_is_unicode_names=True)
    title = f'unicode_names {bkg_name}'
    verses_dicts = {
        roca: dict(list_of_pairs)
        for roca, list_of_pairs in verses.items()
    }

    def _write_callback(out_fp):
        out_fp.write(f'{title}\n')
        for bcvt, _verse_body in verses[rv_cant_that_covers]:
            multiverse = {
                roca: verses_dicts[roca].get(bcvt)
                for roca in verses.keys()
                if verses_dicts[roca].get(bcvt) is not None
            }
            my_uni_heb.write_verse_un(out_fp, bcvt, multiverse)

    my_open.with_tmp_openw(path, _write_callback)


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
