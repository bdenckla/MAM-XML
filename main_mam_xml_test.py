""" Exports read """

import xml.etree.ElementTree
import re
import my_utils
import my_osis_book_abbrevs
import my_sef_cmn
import my_tanakh_book_names as my_tbn
import my_mam_xml_test_handlers as handlers
import my_sef_style_write
from my_shrink import shrink


_HANDLERS = {
    ('verse', None): handlers.verse,
    #
    ('text', None): handlers.text,
    #
    ('good-ending', None): handlers.good_ending,
    ('letter-small', None): handlers.letter_small,
    ('letter-large', None): handlers.letter_large,
    ('letter-hung', None): handlers.letter_hung,
    ('note', None): handlers.note,
    ('kq-k-velo-q', None): handlers.kq_k,
    ('kq-k-velo-q', 'append-maqaf'): handlers.kq_k_append_maqaf,
    ('kq-q-velo-k', None): handlers.kq_q,
    ('kq', None): handlers.ketiv_qere,
    ('kq', 'sep-maqaf'): handlers.ketiv_qere_sep_maqaf,
    ('kq-k', None): handlers.kq_k,
    ('kq-q', None): handlers.kq_q,
    ('kq-trivial', None): handlers.kq_trivial,
    #
    ('spi-samekh2', None): handlers.samekh2_or_3,
    ('spi-samekh3', None): handlers.samekh2_or_3,
    ('spi-samekh3', 'nu10-invnun-neighbor'): handlers.samekh3_nin,
    ('spi-pe2', None): handlers.pe2_or_3,
    ('spi-pe3', None): handlers.pe2_or_3,
    ('spi-invnun', None): handlers.invnun,
    ('spi-invnun', 'including-trailing-space'): handlers.invnun_its,
    ('shirah-space', None): handlers.shirah_space,
    ('lp-legarmeih', None): handlers.legarmeih,
    ('lp-paseq', None): handlers.paseq,
    ('implicit-maqaf', None): handlers.implicit_maqaf,
}


def _handle(etel):  # etel: ElementTree element
    ofc1 = []
    ofc2 = {}
    for child in etel:
        output_for_child = _handle(child)
        ofc1.extend(output_for_child)
        ofc2[child] = output_for_child
    attr_text = etel.attrib.get('text')
    if attr_text is not None:
        assert not ofc1
        ofc1 = [attr_text]
    the_class = etel.attrib.get('class')
    tag_and_class = etel.tag, the_class
    handler = _HANDLERS[tag_and_class]
    return handler(etel, shrink(ofc1), ofc2)


def _read_book_group(bkg_name):
    xml_path = f'../MAM-XML/out/xml/{bkg_name}.xml'
    tree = xml.etree.ElementTree.parse(xml_path)
    root = tree.getroot()
    verses_in = root.findall('.//verse')
    book39s_out = {}
    for verse in verses_in:
        osis_id = verse.attrib['osisID']
        bcvt = _get_bcvt_from_osis_id(osis_id)
        bkid = my_tbn.bcvt_get_bkid(bcvt)
        verse_out = _handle(verse)
        if bkid not in book39s_out:
            book39s_out[bkid] = []
        book39s_out[bkid].append((bcvt, verse_out))
    return book39s_out


def _get_bcvt_from_osis_id(osid_id):
    patt = r'([A-z0-9]*)\.(\d+)\.(\d+)'
    match = re.match(patt, osid_id)
    oba, chnu_str, vrnu_str = match.groups()
    bkid = my_osis_book_abbrevs.BKID_FROM_OBA[oba]
    chnu = int(chnu_str)
    vrnu = int(vrnu_str)
    return my_tbn.mk_bcvtbhs(bkid, chnu, vrnu)


_VARIANT = {
    'variant_mam_for_xxx': 'MAM-XML',
    'variant_path_qual': '-test',
    'variant_write': my_sef_style_write.write_bkg_in_csv_fmt,
}


def do_one_book_group(bkg):
    """ Do one book group (do one bkg) """
    bkg_name = bkg['bkg-name']
    book39s = _read_book_group(bkg_name)
    for bkid, verses in book39s.items():
        verses_abd = {
            'cant_alef': [],
            'cant_bet': [],
            'cant_dual': verses,
        }
        sef_eng_bkna = my_sef_cmn.SEF_ENGLISH_BOOK_NAMES[bkid]
        my_sef_style_write.write_bkg(_VARIANT, sef_eng_bkna, verses_abd)


def _timed_main():
    bkids = my_utils.get_book39_tuple_from_args()
    bkgs = my_osis_book_abbrevs.bk24_bkgs(bkids)
    for bkg in bkgs:
        do_one_book_group(bkg)


def main():
    """
    Test MAM-XML by using it to create something that should match the
    Sefaria output.
    """
    my_utils.show_time(__file__, _timed_main)


if __name__ == "__main__":
    main()
