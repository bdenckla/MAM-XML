"""
Exports:
    write_bkg_in_csv_fmt
"""

import csv
import py.my_html as my_html
import pycmn.file_io as file_io
import pycmn.my_utils as my_utils
import pysefaria.sef_header as sef_header
import pysefaria.sef_cmn as sef_cmn
import pycmn.bib_locales as tbn


def write_bkg_in_csv_fmt(out_path, variant, verses, cant_dabs):
    """Write Sefaria-style file in CSV format"""
    book_out = {}
    bkid = None
    verses_dicts = my_utils.dv_map(dict, verses)
    for bcvt, _html_els in verses["rv-cant-combined"]:
        if bkid is None:
            bkid = tbn.bcvt_get_bk39id(bcvt)
        else:
            assert bkid == tbn.bcvt_get_bk39id(bcvt)
        book_out[bcvt] = tuple(
            _html_str(_maybe_get(verses_dicts, cant_dab, bcvt))
            for cant_dab in cant_dabs
        )
    file_io.with_tmp_openw(
        out_path, {"newline": ""}, _write_callback, variant, bkid, book_out
    )


def _maybe_get(verses_dicts, cant_dab, bcvt):
    vd_cd = verses_dicts.get(cant_dab) or {}
    return vd_cd.get(bcvt)


def _html_str(html_els):
    return "".join(map(my_html.el_to_str_for_sef, html_els)) if html_els else ""


def _write_callback(variant, bkid, contents, file_handle):
    writer = csv.writer(file_handle)
    exclude_header = variant.get("variant-exclude-header-from-csv")
    if not exclude_header:
        header = sef_header.sef_header(bkid)
        for hkey, hval in header.items():
            writer.writerow((hkey, hval))
    sef_bkna = sef_cmn.SEF_BKNA[bkid]
    for bcvt, verse in contents.items():
        chnu = tbn.bcvt_get_chnu(bcvt)
        vrnu = tbn.bcvt_get_vrnu(bcvt)
        bcv_str = f"{sef_bkna} {chnu}:{vrnu}"
        writer.writerow((bcv_str, *verse))
