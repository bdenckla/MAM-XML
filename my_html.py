import xml.etree.ElementTree as ET
import html

import my_open
from my_str_defs import NBSP, THSP


def write_html_to_file(html_el, path):
    def _write_callback(out_fp):
        out_fp.write('<!doctype html>\n')
        out_fp.write(el_to_str(html_el))
    my_open.with_tmp_openw(path, _write_callback)


def el_to_str(elem):
    if isinstance(elem, str):
        sstt = str.maketrans({  # special space translation table
            '\N{EM SPACE}': '&emsp;',
            THSP: '&thinsp;',
            NBSP: '&nbsp;',
        })
        return html.escape(elem, quote=False).translate(sstt)
    contents_str = ''
    contents = elem.get('contents')
    if contents:
        assert isinstance(contents, (tuple, list))
        contents_str = ''.join(map(el_to_str, contents))
    lb2 = elem.get('lb2', '\n')
    noclose = elem.get('noclose')
    eltag = hel_get_tag(elem)
    fields = dict(
        tag_name=eltag,
        attr=_attr_str(elem.get('attr')),
        contents=contents_str,
        close='' if noclose else f'</{eltag}>{lb2}',
        lb1=elem.get('lb1', '\n'),
    )
    return '<{tag_name}{attr}>{lb1}{contents}{close}'.format(**fields)


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
    contents = elem.get('contents')
    if contents:
        assert isinstance(contents, (tuple, list))
        if _is_text_singleton(contents):
            assert 'text' not in attr
            tmp_attr = dict(attr, text=contents[0])
            contents = None
    xml_elem = ET.SubElement(xml_parent, hel_get_tag(elem), tmp_attr)
    if contents:
        for contents_el in contents:
            el_to_xml(xml_elem, contents_el)


def _is_text_singleton(array):  # "array": tuple or list
    return len(array) == 1 and isinstance(array[0], str)


def html_el2(title_text, body_contents, css_hrefs=(), other=None):
    other_defaults = dict(lang='en', head_style=None)
    if other is None:
        other = {}
    other = {**other_defaults, **other}
    meta = hel_mk('meta', attr=dict(charset='utf-8'), noclose=True)
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
    return _html_el1(dict(lang=other['lang']), (_head, _body))


def para(contents, attr=None):
    return hel_mk('p', attr=attr, contents=contents, lb1='')


def table_row(contents):
    return hel_mk('tr', contents=contents, lb1='')


def table_data(contents, attr=None):
    return hel_mk('td', attr=attr, contents=contents, lb1='', lb2='')


def table(contents, attr=None):
    return hel_mk('table', attr=attr, contents=contents)


def unordered_list(contents, attr=None):
    return hel_mk('ul', attr=attr, contents=contents)


def list_item(contents, attr=None):
    return hel_mk('li', attr=attr, contents=contents)


def anchor(contents, attr=None):
    return hel_mk('a', attr=attr, contents=contents)


def colgroup(contents, attr=None):
    return hel_mk('colgroup', attr=attr, contents=contents)


def col(attr=None):
    return hel_mk('col', attr=attr, noclose=True)


def span(contents, attr=None):
    return hel_mk('span', attr=attr, contents=contents, lb1='', lb2='')


def bold(contents, attr=None):
    return hel_mk('b', attr=attr, contents=contents, lb1='', lb2='')


def italic(contents, attr=None):
    return hel_mk('i', attr=attr, contents=contents, lb1='', lb2='')


def small(contents, attr=None):
    return hel_mk('small', attr=attr, contents=contents, lb1='', lb2='')


def big(contents, attr=None):
    return hel_mk('big', attr=attr, contents=contents, lb1='', lb2='')


def sup(contents, attr=None):
    return hel_mk('sup', attr=attr, contents=contents, lb1='', lb2='')


def line_break(attr=None):
    return hel_mk('br', attr=attr, lb1='', noclose=True)


def hel_mk(tag, **rest):
    return {'_hel_tag': tag, **rest}


def hel_get_tag(hel):
    return hel['_hel_tag']


def _link_to_css(css_href):
    link_to_css_attr = dict(rel='stylesheet', href=css_href)
    return hel_mk('link', attr=link_to_css_attr, noclose=True)


def _html_el1(attr, contents):
    return hel_mk('html', attr=attr, contents=contents)


def _attr_str(attr_dict):
    if not attr_dict:
        return ''
    return ' ' + ' '.join(map(_kv_str, attr_dict.items()))


def _kv_str(key_and_val):
    key = key_and_val[0]
    value = html.escape(key_and_val[1], quote=True)
    return f'{key}="{value}"'
