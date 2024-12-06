""" Exports main_helper """

import xml.etree.ElementTree as ET
import py.my_utils as my_utils
import py.my_osis_book_abbrevs as my_osis_book_abbrevs
import py.my_sef_cmn as my_sef_cmn
import py.my_locales as tbn
import py.my_write_utils as my_write_utils
import py.my_write_utils_sef_or_ajf as my_write_utils_sef_or_ajf
import py.my_shrink as my_shrink


def main_helper(variant):
    """ Create the Sefaria MAM or AJF MAM from the XML MAM. """
    bkids = my_utils.get_bk39_tuple_from_argparse()
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
    ofc1 = my_shrink.shrink(ofc1_raw)
    attr_text = etel.attrib.get('text')
    if attr_text is not None:
        assert not ofc1
        ofc1 = [attr_text]
    tag_and_class = etel.tag, etel.attrib.get('class')
    handler = handlers[tag_and_class]
    return my_shrink.shrink(handler(etel, ofc1, ofc2))


def _read_book_group(variant, bkg_name):
    vtrad = variant['variant-vtrad']
    xml_vtrad_xxx_dic = {
        tbn.VT_BHS: 'xml-vtrad-bhs',
        tbn.VT_SEF: 'xml-vtrad-sef',
    }
    xml_vtrad_xxx = xml_vtrad_xxx_dic[vtrad]
    xml_path = f'../MAM-XML/out/{xml_vtrad_xxx}/{bkg_name}.xml'
    tree = ET.parse(xml_path)
    return tree.getroot()


XPATH_QUERY_FROM_CANT_DAB = {
    # For cant_dual, we just look for all verses.
    'rv-cant-dual': './/verse',
    # For cant_alef and cant_bet, we look for all verses that have a
    # "cant-all-three" child.
    'rv-cant-alef': './/verse/cant-all-three/..',
    'rv-cant-bet': './/verse/cant-all-three/..',
}


def _process_book_group(variant, root, cant_dab):
    handlers = variant['variant-handlers']
    vtrad = variant['variant-vtrad']
    if tuple(handlers.keys()) == _ALL_3_CANT_DAB_VALUES:
        handlers2 = handlers[cant_dab]
    else:
        handlers2 = handlers
    verses_in = root.findall(XPATH_QUERY_FROM_CANT_DAB[cant_dab])
    bk39s_out = {}
    for verse in verses_in:
        osis_id = verse.attrib['osisID']
        bcvt = _get_bcvt_from_osis_id(vtrad, osis_id)
        bkid = tbn.bcvt_get_bk39id(bcvt)
        verse_out = _handle(handlers2, verse)
        if bkid not in bk39s_out:
            bk39s_out[bkid] = []
        bk39s_out[bkid].append((bcvt, verse_out))
    return bk39s_out


def _get_bcvt_from_osis_id(vtrad, osid_id):
    bkid, chnu, vrnu = my_osis_book_abbrevs.get_bcv_from_osis_id(osid_id)
    return tbn.mk_bcvtxxx(bkid, chnu, vrnu, vtrad)


def _do_for_cant_dab(bkg_out, variant, root, cant_dab):
    bk39s = _process_book_group(variant, root, cant_dab)
    for bkid, verses in bk39s.items():
        if bkid not in bkg_out:
            bkg_out[bkid] = {}
        bkg_out[bkid][cant_dab] = verses


def do_one_book_group(variant, bkg):
    """ Do the book group bkg """
    bkg_name = bkg['bkg-name']
    root = _read_book_group(variant, bkg_name)
    bkg_out = {}
    if variant.get('variant-include-abcants'):
        cant_dabs = _ALL_3_CANT_DAB_VALUES
    else:
        cant_dabs = ('rv-cant-dual',)
    for cant_dab in cant_dabs:
        _do_for_cant_dab(bkg_out, variant, root, cant_dab)
    for bkid, cant_to_verses in bkg_out.items():
        sef_bkna = my_sef_cmn.SEF_BKNA[bkid]
        csv_path = my_write_utils.bkg_path(variant, sef_bkna)
        my_write_utils_sef_or_ajf.write_bkg_in_csv_fmt(
            csv_path, variant, cant_to_verses, cant_dabs)
        my_write_utils.write_bkg_in_un_fmt(
            variant, sef_bkna, cant_to_verses, 'rv-cant-dual')


_ALL_3_CANT_DAB_VALUES = 'rv-cant-dual', 'rv-cant-alef', 'rv-cant-bet'
