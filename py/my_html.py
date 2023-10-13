import xml.etree.ElementTree as ET
import html

import my_open
import my_two_col_css_styles as styles
import my_str_defs as sd


def write_html_to_file(html_el, path):
    """
    Write HTML to file based on two pieces of information:
        * a top-level html element
        * an output path
    """
    my_open.with_tmp_openw(path, {}, _write_callback, html_el)


def write_html_to_file2(body_contents, write_rec):
    """
    Write HTML to file based on two pieces of information:
        * a body contents
        * a "write record" containing:
            * a title
            * an output path
    """
    title = write_rec['wr_title']
    style = write_rec.get('wr_style') or styles.STYLES_STR
    html_el = html_el2(title, body_contents, other={'head_style': style})
    write_html_to_file(html_el, write_rec['wr_out_path'])


def el_to_str(elem):
    if isinstance(elem, str):
        sstt = str.maketrans({  # special space translation table
            '\N{EM SPACE}': '&emsp;',
            sd.THSP: '&thinsp;',
            sd.NBSP: '&nbsp;',
        })
        return html.escape(elem, quote=False).translate(sstt)
    contents_str = ''
    if contents := elem.get('contents'):
        assert isinstance(contents, (tuple, list))
        contents_str = ''.join(map(el_to_str, contents))
    eltag = hel_get_tag(elem)
    fields = {
        'tag_name': eltag,
        'attr': _attr_str(elem.get('attr')),
        'contents': contents_str,
        'close': '' if elem.get('noclose') else f'</{eltag}>',
        'lb1': elem.get('lb1', '\n'),
        'lb2': elem.get('lb2', '\n'),
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


def _write_callback(html_el, out_fp):
    out_fp.write('<!doctype html>\n')
    out_fp.write(el_to_str(html_el))


def _is_text_singleton(array):  # "array": tuple or list
    return len(array) == 1 and isinstance(array[0], str)


def html_el2(title_text, body_contents, css_hrefs=(), other=None):
    other_defaults = {'lang': 'en', 'head_style': None}
    if other is None:
        other = {}
    other = {**other_defaults, **other}
    meta = hel_mk('meta', attr={'charset': 'utf-8'}, noclose=True, lb2='')
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
    return hel_mk('p', attr=attr, contents=contents, lb1='')


def img(contents, attr=None):
    return hel_mk('img', attr=attr, contents=contents, lb1='')


def table_row(contents):
    return hel_mk('tr', contents=contents, lb1='')


def table_data(contents, attr=None):
    return hel_mk('td', attr=attr, contents=contents, lb1='', lb2='')


def table(contents, attr=None):
    return hel_mk('table', attr, contents)


def unordered_list(liconts, attr=None):
    # licont: list item contents
    # liconts: a tuple where each element is a licont
    return hel_mk('ul', attr, tuple(map(_list_item, liconts)))


def heading_level_1(contents, attr=None):
    return hel_mk('h1', attr, contents)


def heading_level_2(contents, attr=None):
    return hel_mk('h2', attr, contents)


def heading_level_3(contents, attr=None):
    return hel_mk('h3', attr, contents)


def anchor(contents, attr=None):
    return hel_mk('a', attr, contents)


def colgroup(contents, attr=None):
    return hel_mk('colgroup', attr, contents)


def col(attr=None):
    return hel_mk('col', attr=attr, noclose=True, lb2='')


def span(contents, attr=None):
    return hel_mk('span', attr=attr, contents=contents, lb1='', lb2='')


def span_c(contents, the_class=None):
    return span(contents, the_class and {'class': the_class})


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
    """
    A <br> that is NOT followed by a newline in the source code.
    (The lb2='' suppresses this newline.)
    """
    return hel_mk('br', attr=attr, lb1='', noclose=True, lb2='')


def line_break2(attr=None):
    """
    A <br> that is followed by a newline in the source code.
    """
    return hel_mk('br', attr=attr, lb1='', noclose=True)


def hel_mk(
        tag,
        attr=None,
        contents=None,
        lb1=None,
        lb2=None,
        noclose=None):
    """ Make an HTML element """
    assert isinstance(tag, str)
    assert isinstance(attr, (type(None), dict))
    contents2 = (contents,) if isinstance(contents, str) else contents
    assert isinstance(contents2, (type(None), tuple, list))
    opts1 = {
        'attr': attr,
        'contents': contents2,
        'lb1': lb1,
        'lb2': lb2,
        'noclose': noclose
    }
    opts2 = {k: v for k, v in opts1.items() if v is not None}
    return {'_hel_tag': tag, **opts2}


def hel_get_tag(hel):
    return hel['_hel_tag']


def _list_item(contents, attr=None):
    return hel_mk('li', attr, contents)


def _link_to_css(css_href):
    link_to_css_attr = {'rel': 'stylesheet', 'href': css_href}
    return hel_mk('link', attr=link_to_css_attr, noclose=True, lb2='')


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
