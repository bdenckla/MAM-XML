"""
Exports:
    write_bkg_in_csv_fmt
"""

import csv
import my_html
import my_sef_header
import my_open
import my_sef_cmn
import my_tanakh_book_names as my_tbn


def write_bkg_in_csv_fmt(path, variant, verses):
    """ Write Sefaria-style file in CSV format """
    book_out = {}
    bkid = None
    dic_alef = dict(verses.get('cant_alef') or [])
    dic_bet = dict(verses.get('cant_bet') or [])
    for bcvt, html_els in verses['cant_dual']:
        if bkid is None:
            bkid = my_tbn.bcvt_get_bkid(bcvt)
        else:
            assert bkid == my_tbn.bcvt_get_bkid(bcvt)
        dual = _html_str(html_els)
        if variant.get('variant_include_abcants'):
            alef = _html_str(dic_alef.get(bcvt))
            bet = _html_str(dic_bet.get(bcvt))
            book_out[bcvt] = dual, alef, bet
        else:
            book_out[bcvt] = (dual,)

    def _write_callback(file_handle):
        _write_bkg_in_csv_fmt2(variant, bkid, book_out, file_handle)

    my_open.with_tmp_openw(path, _write_callback, newline='')


def _html_str(html_els):
    return ''.join(map(my_html.el_to_str, html_els)) if html_els else ''


def _write_bkg_in_csv_fmt2(variant, bkid, contents, file_handle):
    writer = csv.writer(file_handle)
    exclude_header = variant.get('variant_exclude_header_from_csv')
    if not exclude_header:
        header = my_sef_header.sef_header(bkid)
        for hkey, hval in header.items():
            writer.writerow((hkey, hval))
    sef_bkna = my_sef_cmn.SEF_ENGLISH_BOOK_NAMES[bkid]
    for bcvt, verse in contents.items():
        chnu = my_tbn.bcvt_get_chnu(bcvt)
        vrnu = my_tbn.bcvt_get_vrnu(bcvt)
        bcv_str = f'{sef_bkna} {chnu}:{vrnu}'
        writer.writerow((bcv_str, *verse))
