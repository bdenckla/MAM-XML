""" Exports main_helper """

import xml.etree.ElementTree
import my_utils
import my_osis_book_abbrevs
import my_sef_cmn
import my_tanakh_book_names as my_tbn
import my_sef_style_write
from my_shrink import shrink


def main_helper(variant):
    """ Create the Sefaria MAM or AJF MAM from the XML MAM. """
    bkids = my_utils.get_book39_tuple_from_args()
    bkgs = my_osis_book_abbrevs.bk24_bkgs(bkids)
    for bkg in bkgs:
        do_one_book_group(variant, bkg)


def _handle(handlers, etel):  # etel: ElementTree element
    ofc1_raw = []  # output for all children, summed together
    ofc2 = {}  # output for all children, per child
    for child in etel:
        output_for_child = _handle(handlers, child)
        ofc1_raw.extend(output_for_child)
        ofc2[child] = output_for_child
    ofc1 = shrink(ofc1_raw)
    attr_text = etel.attrib.get('text')
    if attr_text is not None:
        assert not ofc1
        ofc1 = [attr_text]
    tag_and_class = etel.tag, etel.attrib.get('class')
    handler = handlers[tag_and_class]
    return shrink(handler(etel, ofc1, ofc2))


def _read_book_group(variant, bkg_name):
    vtrad = variant['variant_vtrad']
    xml_vtrad_xxx_dic = {
        my_tbn.VT_BHS: 'xml-vtrad-bhs',
        my_tbn.VT_SEF: 'xml-vtrad-sef',
    }
    xml_vtrad_xxx = xml_vtrad_xxx_dic[vtrad]
    xml_path = f'../MAM-XML/out/{xml_vtrad_xxx}/{bkg_name}.xml'
    tree = xml.etree.ElementTree.parse(xml_path)
    return tree.getroot()


def _process_book_group(variant, root):
    handlers = variant['variant_handlers']
    vtrad = variant['variant_vtrad']
    verses_in = root.findall('.//verse')
    book39s_out = {}
    for verse in verses_in:
        osis_id = verse.attrib['osisID']
        bcvt = _get_bcvt_from_osis_id(vtrad, osis_id)
        bkid = my_tbn.bcvt_get_bkid(bcvt)
        verse_out = _handle(handlers, verse)
        if bkid not in book39s_out:
            book39s_out[bkid] = []
        book39s_out[bkid].append((bcvt, verse_out))
    return book39s_out


def _get_bcvt_from_osis_id(vtrad, osid_id):
    bkid, chnu, vrnu = my_osis_book_abbrevs.get_bcv_from_osis_id(osid_id)
    return my_tbn.mk_bcvtxxx(bkid, chnu, vrnu, vtrad)


def do_one_book_group(variant, bkg):
    """ Do the book group bkg """
    bkg_name = bkg['bkg-name']
    root = _read_book_group(variant, bkg_name)
    book39s = _process_book_group(variant, root)
    for bkid, verses in book39s.items():
        verses_abd = {
            'cant_alef': [],
            'cant_bet': [],
            'cant_dual': verses,
        }
        sef_eng_bkna = my_sef_cmn.SEF_ENGLISH_BOOK_NAMES[bkid]
        my_sef_style_write.write(variant, sef_eng_bkna, verses_abd)
