""" Exports HANDLERS """

import my_html
from my_str_defs import MAQ, PAS, NUN_HAF, NBSP, OCTO_NBSP, THSP
from my_shrink import shrink

# etel: ElementTree element
# ofc1: output for all children, summed together
# ofc2: output for all children, per child


def _verse(etel, ofc1, _ofc2):
    return ofc1 + _maybe_sampe(etel)


def _text(etel, _ofc1, _ofc2):
    return [etel.attrib['text']]


def _samekh2_or_3(_etel, _ofc1, _ofc2):
    span = my_html.span_c(('{ס}',), 'mam-spi-samekh')
    return [NBSP, span, OCTO_NBSP]


def _pe2_or_3(_etel, _ofc1, _ofc2):
    span = my_html.span_c(('{פ}',), 'mam-spi-pe')
    return [NBSP, span, my_html.line_break()]


def _samekh3_nin(_etel, _ofc1, _ofc2):
    """ Handle a samekh3 element with class "nu10-invnun-neighbor" """
    return [NBSP]


def _invnun(etel, _ofc1, _ofc2):
    """
    Handle either of the following two types of invnun elements:

        Type 1: a default (i.e., no trailing space) invnun element.
        These are the two Numbers 10 invnuns,
        at the start of verse 35 and the end of verse 36.

        Type 2: an invnun element with class "including-trailing-space"
        These are the 7 Psalm 107 invnuns,
        at the start of verses 23-28 and 40.
    """
    maybe_nbsp_dic = {'including-trailing-space': [NBSP], None: []}
    maybe_nbsp = maybe_nbsp_dic[etel.attrib.get('class')]
    span = my_html.span_c((NUN_HAF,), 'mam-spi-invnun')
    return [span, *maybe_nbsp]


def _legarmeih(_etel, _ofc1, _ofc2):
    return [THSP, my_html.bold((PAS,))]


def _paseq(_etel, _ofc1, _ofc2):
    return [THSP, my_html.small((PAS,)), THSP]


def _empty(_etel, _ofc1, _ofc2):
    return []


def _pass_thru(_etel, ofc1, _ofc2):
    return ofc1


def _letter_small(_etel, ofc1, _ofc2):
    return [my_html.small(ofc1)]


def _letter_large(_etel, ofc1, _ofc2):
    return [my_html.big(ofc1)]


def _letter_hung(_etel, ofc1, _ofc2):
    return [my_html.sup(ofc1)]


def _kq_trivial(_etel, ofc1, _ofc2):
    """ Handle a trivial ketiv/qere element """
    return [my_html.span_c(ofc1, 'mam-kq-trivial')]


def _ketiv_qere(etel, _ofc1, ofc2):
    assert len(ofc2) == 2
    sep_dic = {'sep-maqaf': MAQ, None: ' '}
    separator = sep_dic[etel.attrib.get('class')]
    kq_or_qk = tuple(ofc2.values())
    inside = [*kq_or_qk[0], separator, *kq_or_qk[1]]
    return [my_html.span_c(inside, 'mam-kq')]


def _ketiv(etel, ofc1, _ofc2):
    """
    Handle a ketiv element that is:
       * the ketiv part of a ketiv ve qere (common)
       * a ketiv velo qere (rare)
    """
    maybe_maqaf_dic = {'append-maqaf': MAQ, None: ''}
    maybe_maqaf = maybe_maqaf_dic[etel.attrib.get('class')]
    return _ketiv_or_qere_helper('mam-kq-k', '()', ofc1, maybe_maqaf)


def _qere(_etel, ofc1, _ofc2):
    """
    Handle a qere element that is:
       * the qere part of a ketiv ve qere (common)
       * a qere velo ketiv (rare)
    """
    return _ketiv_or_qere_helper('mam-kq-q', '[]', ofc1)


def _scrdfftar(_etel, _ofc1, ofc2):
    target, note, starpos = [
        {'ofc2_key': k, 'ofc2_value': v} for k, v in ofc2.items()]
    maybe_note_0 = _star(starpos, note, 'sdt-starpos-before-word')
    maybe_note_1 = _star(starpos, note, 'sdt-starpos-after-word')
    return maybe_note_0 + target['ofc2_value'] + maybe_note_1


def _star(starpos, note, pos):
    tag = starpos['ofc2_key'].tag
    assert tag in ('sdt-starpos-before-word', 'sdt-starpos-after-word')
    assert pos in ('sdt-starpos-before-word', 'sdt-starpos-after-word')
    return note['ofc2_value'] if tag == pos else []


def _scrdfftar_target(_etel, ofc1, _ofc2):
    return ofc1


def _scrdfftar_note(_etel, ofc1, _ofc2):
    """ Handle a scroll difference note element """
    paren_ofc1 = _paren(ofc1)
    el_sup = my_html.sup(['*'], {'class': 'footnote-marker'})
    el_italic = my_html.italic(paren_ofc1, {'class': 'footnote'})
    return [el_sup, el_italic]


def _shirah_space(_etel, _ofc1, _ofc2):
    return [OCTO_NBSP]


def _implicit_maqaf(_etel, _ofc1, _ofc2):
    return [my_html.span_c([MAQ], 'mam-implicit-maqaf')]


#######################################################################
#######################################################################


def _paren(lst: list):
    return shrink(['('] + lst + [')'])


def _ketiv_or_qere_helper(the_class, brackets, ofc1, maybe_maqaf=''):
    brac_ofc1_m = [brackets[0], *ofc1, brackets[1] + maybe_maqaf]
    return [my_html.span(shrink(brac_ofc1_m), {'class': the_class})]


def _maybe_sampe(etel):
    ews = etel.attrib.get('ends-with-sampe')
    if ews is None:
        return []
    sampe_fn_dic = {
        'samekh2': _samekh2_or_3,
        'samekh3': _samekh2_or_3,
        'pe2': _pe2_or_3,
        'pe3': _pe2_or_3,
    }
    sampe_fn = sampe_fn_dic[ews]
    return sampe_fn(None, None, None)


HANDLERS = {
    ('verse', None): _verse,
    ('text', None): _text,
    #
    ('good-ending', None): _empty,
    ('letter-small', None): _letter_small,
    ('letter-large', None): _letter_large,
    ('letter-hung', None): _letter_hung,
    #
    ('kq-k-velo-q', None): _ketiv,
    ('kq-k-velo-q', 'append-maqaf'): _ketiv,
    ('kq-q-velo-k', None): _qere,
    ('kq', None): _ketiv_qere,
    ('kq', 'sep-maqaf'): _ketiv_qere,
    ('kq-k', None): _ketiv,
    ('kq-q', None): _qere,
    ('kq-trivial', None): _kq_trivial,
    #
    ('cant-dual', None): _pass_thru,
    ('cant-alef', None): _empty,
    ('cant-bet', None): _empty,
    ('cant-all-three', None): _pass_thru,
    #
    ('spi-samekh2', None): _samekh2_or_3,
    ('spi-samekh3', None): _samekh2_or_3,
    ('spi-samekh3', 'nu10-invnun-neighbor'): _samekh3_nin,
    ('spi-pe2', None): _pe2_or_3,
    ('spi-pe3', None): _pe2_or_3,
    ('spi-invnun', None): _invnun,
    ('spi-invnun', 'including-trailing-space'): _invnun,
    ('shirah-space', None): _shirah_space,
    ('lp-legarmeih', None): _legarmeih,
    ('lp-paseq', None): _paseq,
    ('implicit-maqaf', None): _implicit_maqaf,
    #
    ('scrdfftar', None): _scrdfftar,
    ('sdt-target', None): _scrdfftar_target,
    ('sdt-note', None): _scrdfftar_note,
    ('sdt-starpos-before-word', None): _empty,
    ('sdt-starpos-after-word', None): _empty,
    #
    ('slh-word', None): _pass_thru,
    ('slhw-targ', None): _pass_thru,
    ('slhw-desc-0', None): _empty,
    ('slhw-desc-1', None): _empty,
    ('slhw-desc-2', None): _empty,
    ('slhw-desc-3', None): _empty,
}
