""" Exports various HTMl utilities. """

import xml.etree.ElementTree as ET
from dataclasses import dataclass
import html

import my_open
import my_utils
import my_hebrew_punctuation as hpu
import my_two_col_css_styles as styles
import my_str_defs as sd


def write_html_to_file(html_el, path, add_wbr=False):
    """
    Write HTML to file based on two inputs:
        * a top-level html element
        * an output path
    """
    my_open.with_tmp_openw(path, {}, _write_callback, html_el, add_wbr)


@dataclass
class WriteRec:
    """ Holds info needed to write HTML to a file. """
    title: str
    path: str
    style: str = None
    add_wbr: bool = False



def write_html_to_file2(body_contents, write_rec: WriteRec):
    """
    Write HTML to file based on the following inputs:
        * a body contents
        * a "write record" containing:
            * a title
            * an output path
    """
    style = write_rec.style or styles.STYLES_STR
    other = {'head_style': style}
    html_el = html_el2(write_rec.title, body_contents, other=other)
    write_html_to_file(html_el, write_rec.path, write_rec.add_wbr)


_SSTT = str.maketrans({  # special space translation table
    '\N{EM SPACE}': '&emsp;',
    sd.THSP: '&thinsp;',
    sd.NBSP: '&nbsp;',
})


def el_to_str_no_wbr(html_el):
    """ Call el_to_str with add_wbr=False. """
    return el_to_str(add_wbr=False, html_el=html_el)


def el_to_str(add_wbr, html_el):
    """ Convert an HTML element to a string. """
    if isinstance(html_el, str):
        outstr = html_el
        outstr = html.escape(html_el, quote=False)
        outstr = outstr.translate(_SSTT)
        if add_wbr:
            outstr = outstr.replace(hpu.MAQ, hpu.MAQ + '<wbr>')
        return outstr
    contents_str = ''
    if contents := html_el.get('contents'):
        assert isinstance(contents, (tuple, list))
        contents_str = ''.join(my_utils.sl_map(contents, el_to_str, add_wbr))
    eltag = hel_get_tag(html_el)
    fields = {
        'tag_name': eltag,
        'attr': _attr_str(html_el.get('attr')),
        'contents': contents_str,
        'close': '' if html_el.get('noclose') else f'</{eltag}>',
        'lb1': html_el.get('lb1', '\n'),
        'lb2': html_el.get('lb2', '\n'),
    }
    return '<{tag_name}{attr}>{lb1}{contents}{close}{lb2}'.format(**fields)


def el_to_xml(xml_parent, elem):
    """
        Add our proprietary-format element "elem"
        to the ElementTree-format element xml_parent.
    """
    if isinstance(elem, str):
        ET.SubElement(xml_parent, 'text', {'text': elem})
        return
    attr = elem.get('attr') or {}
    tmp_attr = attr
    if contents := elem.get('contents'):
        assert isinstance(contents, (tuple, list))
        if _is_text_singleton(contents):
            assert 'text' not in attr
            tmp_attr = dict(attr, text=contents[0])
            contents = None
    xml_elem = ET.SubElement(xml_parent, hel_get_tag(elem), tmp_attr)
    if contents:
        for contents_el in contents:
            el_to_xml(xml_elem, contents_el)


def html_el2(title_text, body_contents, css_hrefs=(), other=None):
    """ Make an <html> element. """
    other_defaults = {'lang': 'en', 'head_style': None}
    if other is None:
        other = {}
    other = {**other_defaults, **other}
    meta = hel_mk_nlb2_nc('meta', attr={'charset': 'utf-8'})
    title = hel_mk('title', contents=(title_text,))
    links_to_css = tuple(map(_link_to_css, css_hrefs))
    if other['head_style'] is None:
        style_els = ()
    else:
        style_el = hel_mk('style', contents=(other['head_style'],))
        style_els = (style_el,)
    head_cont = (meta, title) + style_els + links_to_css
    _head = hel_mk('head', contents=head_cont)
    _body = hel_mk('body', contents=body_contents)
    return _html_el1({'lang': other['lang']}, (_head, _body))


def para(contents, attr=None):
    """ Make a <p> element. """
    return hel_mk_nlb1('p', attr=attr, contents=contents)


def img(contents, attr=None):
    """ Make an <img> element. """
    return hel_mk_nlb1('img', attr=attr, contents=contents)


def table_row(contents):
    """ Make a <tr> element. """
    return hel_mk_nlb1('tr', contents=contents)


def table_data(contents, attr=None):
    """ Make a <td> element. """
    return hel_mk_inline('td', attr=attr, contents=contents)


def div(contents, attr=None):
    """ Make a <div> element. """
    return hel_mk('div', attr=attr, contents=contents)


def table(contents, attr=None):
    """ Make a <table> element. """
    return hel_mk('table', attr, contents)


def unordered_list(liconts, attr=None):
    """ Make a <ul> element. """
    # licont: list item contents
    # liconts: a tuple where each element is a licont
    return hel_mk('ul', attr, tuple(map(_list_item, liconts)))


def heading_level_1(contents, attr=None):
    """ Make an <h1> element. """
    return hel_mk('h1', attr, contents)


def heading_level_2(contents, attr=None):
    """ Make an <h2> element. """
    return hel_mk('h2', attr, contents)


def heading_level_3(contents, attr=None):
    """ Make an <h3> element. """
    return hel_mk('h3', attr, contents)


def anchor(contents, attr=None):
    """ Make an <a> element. """
    return hel_mk_inline('a', attr, contents)


def colgroup(contents, attr=None):
    """ Make a <colgroup> element. """
    return hel_mk('colgroup', attr, contents)


def col(attr=None):
    """ Make a <col> element. """
    return hel_mk_nlb2_nc('col', attr=attr)


def span(contents, attr=None):
    """ Make a <span> element. """
    return hel_mk_inline('span', attr=attr, contents=contents)


def span_c(contents, the_class=None):
    """ Make a <span> element, given a value for the "class" attr. """
    return span(contents, the_class and {'class': the_class})


def bold(contents, attr=None):
    """ Make a <bold> element. """
    return hel_mk_inline('b', attr=attr, contents=contents)


def italic(contents, attr=None):
    """ Make a <italic> element. """
    return hel_mk_inline('i', attr=attr, contents=contents)


def small(contents, attr=None):
    """ Make a <small> element. """
    return hel_mk_inline('small', attr=attr, contents=contents)


def big(contents, attr=None):
    """ Make a <big> element. """
    return hel_mk_inline('big', attr=attr, contents=contents)


def sup(contents, attr=None):
    """ Make a <sup> (superscript) element. """
    return hel_mk_inline('sup', attr=attr, contents=contents)


def line_break(attr=None):
    """
    Make a <br> element
    that is NOT followed by a newline in the source code.
    """
    return hel_mk_inline_nc('br', attr=attr)


def line_break2(attr=None):
    """
    Make <br> element
    that is followed by a newline in the source code.
    """
    return hel_mk_nlb1_nc('br', attr=attr)


@dataclass
class HelDetails:
    """ Details about how to make an HTML element. """
    lb1: str = None
    lb2: str = None
    noclose: bool = None


def hel_mk(tag: str, attr=None, contents=None, details=None):
    """ Make an HTML element """
    assert isinstance(tag, str)
    assert isinstance(attr, (type(None), dict))
    contents2 = (contents,) if isinstance(contents, str) else contents
    assert isinstance(contents2, (type(None), tuple, list))
    opts1 = {
        'attr': attr,
        'contents': contents2,
        'lb1': details.lb1 if details else None,
        'lb2': details.lb2 if details else None,
        'noclose': details.noclose if details else None,
    }
    opts2 = {k: v for k, v in opts1.items() if v is not None}
    return {'_hel_tag': tag, **opts2}


def hel_mk_inline(tag: str, attr=None, contents=None):
    """ hel_mk with lb1='', lb2='' """
    details = HelDetails(lb1='', lb2='')
    return hel_mk(tag, attr, contents, details)


def hel_mk_inline_nc(tag: str, attr=None, contents=None):
    """ hel_mk with lb1='', lb2='', noclose=True """
    details = HelDetails(lb1='', lb2='', noclose=True)
    return hel_mk(tag, attr, contents, details)


def hel_mk_nlb1_nc(tag: str, attr=None, contents=None):
    """ hel_mk with lb1='', noclose=True """
    details = HelDetails(lb1='', noclose=True)
    return hel_mk(tag, attr, contents, details)


def hel_mk_nlb1(tag: str, attr=None, contents=None):
    """ hel_mk with lb1='' """
    details = HelDetails(lb1='')
    return hel_mk(tag, attr, contents, details)


def hel_mk_nlb2_nc(tag: str, attr=None, contents=None):
    """ hel_mk with lb2='', noclose=True """
    details = HelDetails(lb2='', noclose=True)
    return hel_mk(tag, attr, contents, details)


def hel_get_tag(html_el):
    """ Get the tag of an HTML element. """
    return html_el['_hel_tag']


###########################################################


def _write_callback(html_el, add_wbr, out_fp):
    out_fp.write('<!doctype html>\n')
    out_fp.write(el_to_str(add_wbr, html_el))


def _is_text_singleton(array):  # "array": tuple or list
    return len(array) == 1 and isinstance(array[0], str)


def _list_item(contents, attr=None):
    return hel_mk('li', attr, contents)


def _link_to_css(css_href):
    link_to_css_attr = {'rel': 'stylesheet', 'href': css_href}
    return hel_mk_nlb2_nc('link', attr=link_to_css_attr)


def _html_el1(attr, contents):
    return hel_mk('html', attr, contents)


def _attr_str(attr_dict):
    if not attr_dict:
        return ''
    return ' ' + ' '.join(map(_kv_str, attr_dict.items()))


def _kv_str(key_and_val):
    key = key_and_val[0]
    value = html.escape(key_and_val[1], quote=True)
    return f'{key}="{value}"'
