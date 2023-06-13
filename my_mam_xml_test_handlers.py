""" Exports misc. handlers for MAM-XML test """

import my_html
from my_str_defs import MAQ, NBSP, NUN_HAF, OCTO_NBSP, PAS, THSP
from my_shrink import shrink

# etel: ElementTree element
# ofc1: output for all children, summed together
# ofc2: output for all children, per child


def verse(etel, ofc1, _ofc2):
    """ Handle a verse element """
    return ofc1 + _maybe_sampe(etel)


def text(etel, _ofc1, _ofc2):
    """ Handle a text element """
    return [etel.attrib['text']]


def samekh2_or_3(_etel, _ofc1, _ofc2):
    """ Handle a samekh2 or samekh3 element """
    span = my_html.span(('{ס}',), {'class': 'mam-spi-samekh'})
    return [NBSP, span, OCTO_NBSP]


def pe2_or_3(_etel, _ofc1, _ofc2):
    """ Handle a pe2 or pe3 element """
    span = my_html.span(('{פ}',), {'class': 'mam-spi-pe'})
    return [NBSP, span, my_html.line_break()]


def samekh3_nin(_etel, _ofc1, _ofc2):
    """ Handle a samekh3 element with class "nu10-invnun-neighbor" """
    return [NBSP]


def invnun(_etel, _ofc1, _ofc2):
    """ Handle a default (i.e., no trailing space) invnun element """
    return _invnun_helper()


def invnun_its(_etel, _ofc1, _ofc2):
    """ Handle an invnun element with class "including-trailing-space" """
    return _invnun_helper(NBSP)


def legarmeih(_etel, _ofc1, _ofc2):
    """ Handle a legarmeih element """
    return [THSP, my_html.bold((PAS,))]


def paseq(_etel, _ofc1, _ofc2):
    """ Handle a paseq element """
    return [THSP, my_html.small((PAS,)), THSP]


def good_ending(_etel, ofc1, _ofc2):
    """ Handle a "good ending" element """
    return [my_html.line_break(), my_html.small(ofc1)]


def letter_small(_etel, ofc1, _ofc2):
    """ Handle a letter-small element """
    return [my_html.small(ofc1)]


def letter_large(_etel, ofc1, _ofc2):
    """ Handle a letter-large element """
    return [my_html.big(ofc1)]


def letter_hung(_etel, ofc1, _ofc2):
    """ Handle a letter-hung element """
    return [my_html.sup(ofc1)]


def kq_trivial(_etel, ofc1, _ofc2):
    """ Handle a kq-trivial element """
    return [my_html.span(ofc1, {'class': 'mam-kq-trivial'})]


def ketiv_qere(_etel, _ofc1, ofc2):
    """ Handle a default (i.e. space-separated) kq element """
    return _ketiv_qere_helper(ofc2)


def ketiv_qere_sep_maqaf(_etel, _ofc1, ofc2):
    """
    Handle a kq element with class "sep-maqaf",
    i.e. a maqaf-separated kq element
    """
    return _ketiv_qere_helper(ofc2, MAQ)


def kq_k(_etel, ofc1, _ofc2):
    """ Handle a kq-k element """
    return _ketiv_or_qere_helper('mam-kq-k', '()', ofc1)


def kq_k_append_maqaf(_etel, ofc1, _ofc2):
    """ Handle a kq-k element with class "append-maqaf" """
    return _ketiv_or_qere_helper('mam-kq-k', '()', ofc1, MAQ)


def kq_q(_etel, ofc1, _ofc2):
    """ Handle a kq-q element """
    return _ketiv_or_qere_helper('mam-kq-q', '[]', ofc1)


def note(_etel, ofc1, _ofc2):
    """ Handle a note (scroll difference note) element """
    return [my_html.sup(['*']), my_html.italic(ofc1, {'class': 'footnote'})]


def shirah_space(_etel, _ofc1, _ofc2):
    """ Handle a shirah-space element """
    return [OCTO_NBSP]


def implicit_maqaf(_etel, _ofc1, _ofc2):
    """ Handle an implicit-maqaf element """
    return [my_html.span([MAQ], {'class': 'mam-implicit-maqaf'})]


#######################################################################
#######################################################################


def _ketiv_qere_helper(ofc2, separator=' '):
    """ Handle a kq element """
    kq_or_qk = tuple(ofc2.values())
    inside = kq_or_qk[0] + [separator] + kq_or_qk[1]
    return [my_html.span(inside, {'class': 'mam-kq'})]


def _ketiv_or_qere_helper(the_class, brackets, ofc1, maybe_maqaf=''):
    brac_ofc1 = [brackets[0]] + ofc1 + [brackets[1]]
    brac_ofc1_m = brac_ofc1 + [maybe_maqaf]
    return [my_html.span(shrink(brac_ofc1_m), {'class': the_class})]


def _invnun_helper(maybe_trailing=''):
    """ Handle a default (i.e., no trailing space) invnun element """
    span = my_html.span((NUN_HAF,), {'class': 'mam-spi-invnun'})
    return shrink([span] + [maybe_trailing])


def _maybe_sampe(etel):
    ews = etel.attrib.get('ends-with-sampe')
    if ews is None:
        return []
    sampe_fn_dic = {
        'samekh2': samekh2_or_3,
        'samekh3': samekh2_or_3,
        'pe2': pe2_or_3,
        'pe3': pe2_or_3,
    }
    sampe_fn = sampe_fn_dic[ews]
    return sampe_fn(None, None, None)
