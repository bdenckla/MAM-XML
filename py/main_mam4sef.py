""" Exports main """

import xml.etree.ElementTree
import my_utils
import my_osis_book_abbrevs
import my_sef_cmn
import my_tanakh_book_names as my_tbn
import my_mam4sef_handlers
import my_sef_style_write
from my_shrink import shrink


def _handle(etel):  # etel: ElementTree element
    ofc1_raw = []
    ofc2 = {}
    for child in etel:
        output_for_child = _handle(child)
        ofc1_raw.extend(output_for_child)
        ofc2[child] = output_for_child
    ofc1 = shrink(ofc1_raw)
    attr_text = etel.attrib.get('text')
    if attr_text is not None:
        assert not ofc1
        ofc1 = [attr_text]
    tag_and_class = etel.tag, etel.attrib.get('class')
    handler = my_mam4sef_handlers.HANDLERS[tag_and_class]
    return shrink(handler(etel, ofc1, ofc2))


def _read_book_group(bkg_name):
    xml_path = f'../MAM-XML/out/xml-vtrad-sef/{bkg_name}.xml'
    tree = xml.etree.ElementTree.parse(xml_path)
    root = tree.getroot()
    verses_in = root.findall('.//verse')
    book39s_out = {}
    for verse in verses_in:
        osis_id = verse.attrib['osisID']
        bcvt = _get_bcvtsef_from_osis_id(osis_id)
        bkid = my_tbn.bcvt_get_bkid(bcvt)
        verse_out = _handle(verse)
        if bkid not in book39s_out:
            book39s_out[bkid] = []
        book39s_out[bkid].append((bcvt, verse_out))
    return book39s_out


def _get_bcvtsef_from_osis_id(osid_id):
    bkid, chnu, vrnu = my_osis_book_abbrevs.get_bcv_from_osis_id(osid_id)
    return my_tbn.mk_bcvtsef(bkid, chnu, vrnu)


def do_one_book_group(bkg):
    """ Do the book group bkg """
    bkg_name = bkg['bkg-name']
    book39s = _read_book_group(bkg_name)
    variant = {}
    for bkid, verses in book39s.items():
        verses_abd = {
            'cant_alef': [],
            'cant_bet': [],
            'cant_dual': verses,
        }
        sef_eng_bkna = my_sef_cmn.SEF_ENGLISH_BOOK_NAMES[bkid]
        my_sef_style_write.write(variant, sef_eng_bkna, verses_abd)


def _timed_main():
    bkids = my_utils.get_book39_tuple_from_args()
    bkgs = my_osis_book_abbrevs.bk24_bkgs(bkids)
    for bkg in bkgs:
        do_one_book_group(bkg)


def main():
    """ Create the Sefaria MAM from the XML MAM. """
    my_utils.show_time(__file__, _timed_main)


if __name__ == "__main__":
    main()
