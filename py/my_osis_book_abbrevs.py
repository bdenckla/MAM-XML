""" Exports OSIS_BOOK_ABBREVS """

import re
import my_tanakh_book_names as my_tbn
import my_book_group

# From https://wiki.crosswire.org/OSIS_Book_Abbreviations.


def bk24_bkgs(bk39ids):
    """
    Return the bk24 book groups corresponding to the given bk39ids.
    """
    bkg_dic = {}
    for bk39id in bk39ids:
        bk24id = my_tbn.bk24id(bk39id)
        bkids_of_bk24 = my_tbn.bkids_of_bk24(bk24id)
        osis_ids_of_bk24 = map(_osis_id_of_bkid, bkids_of_bk24)
        osis_bk24na = ''.join(osis_ids_of_bk24)
        bkg_dic[osis_bk24na] = bkids_of_bk24
    bkgs = tuple(my_book_group.bkg_make(*item) for item in bkg_dic.items())
    return bkgs


def get_bcv_from_osis_id(osid_id):
    # Get bkid, chnu, & vrnu triple from an osisID.
    patt = r'([A-z0-9]*)\.(\d+)\.(\d+)'
    match = re.match(patt, osid_id)
    oba, chnu_str, vrnu_str = match.groups()
    bkid = BKID_FROM_OBA[oba]
    chnu = int(chnu_str)
    vrnu = int(vrnu_str)
    return bkid, chnu, vrnu


def get_bc_from_osis_id(osid_id):
    # Get bkid & chnu pair from an osisID.
    patt = r'([A-z0-9]*)\.(\d+)'
    match = re.match(patt, osid_id)
    oba, chnu_str = match.groups()
    bkid = BKID_FROM_OBA[oba]
    chnu = int(chnu_str)
    return bkid, chnu


def _osis_id_of_bkid(bkid):
    return OSIS_BOOK_ABBREVS[bkid]


OSIS_BOOK_ABBREVS = {
    my_tbn.BK_GENESIS: 'Gen',
    my_tbn.BK_EXODUS: 'Exod',
    my_tbn.BK_LEVIT: 'Lev',
    my_tbn.BK_NUMBERS: 'Num',
    my_tbn.BK_DEUTER: 'Deut',
    my_tbn.BK_JOSHUA: 'Josh',
    my_tbn.BK_JUDGES: 'Judg',
    my_tbn.BK_RUTH: 'Ruth',
    my_tbn.BK_FST_SAM: '1Sam',
    my_tbn.BK_SND_SAM: '2Sam',
    my_tbn.BK_FST_KGS: '1Kgs',
    my_tbn.BK_SND_KGS: '2Kgs',
    my_tbn.BK_FST_CHR: '1Chr',
    my_tbn.BK_SND_CHR: '2Chr',
    my_tbn.BK_EZRA: 'Ezra',
    my_tbn.BK_NEXEM: 'Neh',
    my_tbn.BK_ESTHER: 'Esth',
    my_tbn.BK_JOB: 'Job',
    my_tbn.BK_PSALMS: 'Ps',
    my_tbn.BK_PROV: 'Prov',
    my_tbn.BK_QOHELET: 'Eccl',
    my_tbn.BK_SONG: 'Song',
    my_tbn.BK_ISAIAH: 'Isa',
    my_tbn.BK_JEREM: 'Jer',
    my_tbn.BK_LAMENT: 'Lam',
    my_tbn.BK_EZEKIEL: 'Ezek',
    my_tbn.BK_DANIEL: 'Dan',
    my_tbn.BK_HOSEA: 'Hos',
    my_tbn.BK_JOEL: 'Joel',
    my_tbn.BK_AMOS: 'Amos',
    my_tbn.BK_OBADIAH: 'Obad',
    my_tbn.BK_JONAH: 'Jonah',
    my_tbn.BK_MICAH: 'Mic',
    my_tbn.BK_NAXUM: 'Nah',
    my_tbn.BK_XABA: 'Hab',
    my_tbn.BK_TSEF: 'Zeph',
    my_tbn.BK_XAGGAI: 'Hag',
    my_tbn.BK_ZEKHAR: 'Zech',
    my_tbn.BK_MALAKHI: 'Mal',
}
BKID_FROM_OBA = {oba: bkid for bkid, oba in OSIS_BOOK_ABBREVS.items()}
