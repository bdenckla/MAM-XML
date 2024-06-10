"""
Exports:
    write_bkg_in_csv_fmt
"""

import csv
import my_html
import my_open
import my_utils
import my_sef_header
import my_sef_cmn
import my_tanakh_book_names as tbn


def write_bkg_in_csv_fmt(path, variant, verses, cant_dabs):
    """ Write Sefaria-style file in CSV format """
    book_out = {}
    bkid = None
    verses_dicts = my_utils.dv_map(dict, verses)
    for bcvt, _html_els in verses['rv-cant-dual']:
        if bkid is None:
            bkid = tbn.bcvt_get_bkid(bcvt)
        else:
            assert bkid == tbn.bcvt_get_bkid(bcvt)
        book_out[bcvt] = tuple(
            _html_str(_maybe_get(verses_dicts, cant_dab, bcvt))
            for cant_dab in cant_dabs
        )
    my_open.with_tmp_openw(
        path, {'newline': ''}, _write_bkg_in_csv_fmt2, variant, bkid, book_out)


def _maybe_get(verses_dicts, cant_dab, bcvt):
    vd_cd = verses_dicts.get(cant_dab) or {}
    return vd_cd.get(bcvt)


def _html_str(html_els):
    return ''.join(map(my_html.el_to_str_no_wbr, html_els)) if html_els else ''


def _write_bkg_in_csv_fmt2(variant, bkid, contents, file_handle):
    writer = csv.writer(file_handle)
    exclude_header = variant.get('variant-exclude-header-from-csv')
    if not exclude_header:
        header = my_sef_header.sef_header(bkid)
        for hkey, hval in header.items():
            writer.writerow((hkey, hval))
    sef_bkna = my_sef_cmn.SEF_BKNA[bkid]
    for bcvt, verse in contents.items():
        chnu = tbn.bcvt_get_chnu(bcvt)
        vrnu = tbn.bcvt_get_vrnu(bcvt)
        bcv_str = f'{sef_bkna} {chnu}:{vrnu}'
        writer.writerow((bcv_str, *verse))
