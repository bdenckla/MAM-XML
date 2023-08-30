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


def write_bkg_in_csv_fmt(path, variant, verses, cant_dabs):
    """ Write Sefaria-style file in CSV format """
    book_out = {}
    bkid = None
    verses_dicts = {
        cant_dab: dict(list_of_pairs)
        for cant_dab, list_of_pairs in verses.items()
    }
    for bcvt, _html_els in verses['rv-cant-dual']:
        if bkid is None:
            bkid = my_tbn.bcvt_get_bkid(bcvt)
        else:
            assert bkid == my_tbn.bcvt_get_bkid(bcvt)
        book_out[bcvt] = tuple(
            _html_str(_maybe_get(verses_dicts, cant_dab, bcvt))
            for cant_dab in cant_dabs
        )

    def _write_callback(file_handle):
        _write_bkg_in_csv_fmt2(variant, bkid, book_out, file_handle)

    my_open.with_tmp_openw(path, _write_callback, newline='')


def _maybe_get(verses_dicts, cant_dab, bcvt):
    vd_cd = verses_dicts.get(cant_dab) or {}
    return vd_cd.get(bcvt)


def _html_str(html_els):
    return ''.join(map(my_html.el_to_str, html_els)) if html_els else ''


def _write_bkg_in_csv_fmt2(variant, bkid, contents, file_handle):
    writer = csv.writer(file_handle)
    exclude_header = variant.get('variant_exclude_header_from_csv')
    if not exclude_header:
        header = my_sef_header.sef_header(bkid)
        for hkey, hval in header.items():
            writer.writerow((hkey, hval))
    sef_bkna = my_sef_cmn.SEF_BKNA[bkid]
    for bcvt, verse in contents.items():
        chnu = my_tbn.bcvt_get_chnu(bcvt)
        vrnu = my_tbn.bcvt_get_vrnu(bcvt)
        bcv_str = f'{sef_bkna} {chnu}:{vrnu}'
        writer.writerow((bcv_str, *verse))
