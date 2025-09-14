""" Exports various HTML utilities """

import xml.etree.ElementTree as ET
import html
from dataclasses import dataclass
from typing import Union

import pycmn.file_io as file_io
import pycmn.hebrew_punctuation as hpu
import py.two_col_css_styles as styles
import pycmn.str_defs as sd
import py.my_html_get_lines as hgl
from pycmn.my_utils import st_map
from pycmn.my_utils import sl_map
from pycmn.my_utils import sum_of_map


@dataclass
class WriteCtx:
    """Holds info needed to write HTML to a file."""

    title: str
    path: str
    style: Union[str, None] = None
    add_wbr: bool = False


def write_html_to_file(body_contents, write_ctx: WriteCtx):
    """
    Write HTML to file based on the following inputs:
        * a body contents
        * a "write context" structure containing:
            * a title
            * an output path
    """
    style = write_ctx.style or styles.STYLES_STR
    html_el = html_el2(write_ctx.title, body_contents, other={"head_style": style})
    file_io.with_tmp_openw(
        write_ctx.path, {}, _write_callback, html_el, write_ctx.add_wbr
    )


_SSTT = str.maketrans(
    {  # special space translation table
        "\N{EM SPACE}": "&emsp;",
        sd.THSP: "&thinsp;",
        sd.NBSP: "&nbsp;",
    }
)


def el_to_str_for_sef(html_el):
    lines = hgl.get_lines_from_html_el(False, -1, html_el)
    assert len(lines) == 1
    return lines[0]


def simplify_if_htel_span(obj):
    # This is for dumping to JSON
    if not _is_htel(obj):
        return obj
    if not obj["_htel_tag"] == "span":
        return obj
    if list(obj["attr"].keys()) != ["class"]:
        return obj
    rest = dict(obj)
    del rest["_htel_tag"]
    del rest["attr"]
    del rest["contents"]
    attr_class = obj["attr"]["class"]
    contents = _simplify_if_singleton(obj["contents"])
    return {attr_class: contents, **rest}


def _simplify_if_singleton(lis_obj):
    if len(lis_obj) == 1 and isinstance(lis_obj[0], str):
        return lis_obj[0]
    return lis_obj


def add_htel_to_etxml(etxml_parent, htel):
    """
    Add our proprietary-format HTML/XML element "htel"
    to the ElementTree-format element xml_parent.
    """
    if isinstance(htel, str):
        ET.SubElement(etxml_parent, "text", {"text": htel})
        return
    attr = htel.get("attr") or {}
    tmp_attr = attr
    if contents := htel.get("contents"):
        assert isinstance(contents, (tuple, list))
        if _is_text_singleton(contents):
            assert "text" not in attr
            tmp_attr = dict(attr, text=contents[0])
            contents = None
    xml_elem = ET.SubElement(etxml_parent, htel_get_tag(htel), tmp_attr)
    if contents:
        for contents_el in contents:
            add_htel_to_etxml(xml_elem, contents_el)


def html_el2(title_text, body_contents, css_hrefs=(), other=None):
    """Make an <html> element."""
    other_defaults = {"lang": "en", "head_style": None}
    if other is None:
        other = {}
    other = {**other_defaults, **other}
    meta = htel_mk_nlb2_nc("meta", attr={"charset": "utf-8"})
    title = htel_mk("title", flex_contents=(title_text,))
    links_to_css = st_map(_link_to_css, css_hrefs)
    if other["head_style"] is None:
        style_els = ()
    else:
        style_el = htel_mk("style", flex_contents=(other["head_style"],))
        style_els = (style_el,)
    head_cont = (meta, title) + style_els + links_to_css
    _head = htel_mk("head", flex_contents=head_cont)
    _body = htel_mk("body", flex_contents=body_contents)
    return _html_el1({"lang": other["lang"]}, (_head, _body))


def para(contents, attr=None):
    """Make a <p> element."""
    return htel_mk_nlb1("p", attr=attr, contents=contents)


def img(contents, attr=None):
    """Make an <img> element."""
    return htel_mk_nlb1("img", attr=attr, contents=contents)


def caption(contents):
    """Make a <caption> element."""
    return htel_mk_nlb1("caption", contents=contents)


def table_row(contents):
    """Make a <tr> element."""
    return htel_mk_nlb1("tr", contents=contents)


def table_row_of_data(tdconts, tdattrs=None):
    """Make a <tr> element containing <td> elements."""
    # tdcont: table datum contents
    # tdconts: a sequence where each element is a tdcont
    if tdattrs is None:
        tdattrs = (None,) * len(tdconts)
    return table_row(st_map(table_datum2, zip(tdconts, tdattrs)))


def table_row_of_headers(thconts):
    """Make a <tr> element containing <th> elements."""
    # thcont: table header contents
    # thconts: a sequence where each element is a thcont
    return table_row(st_map(table_header, thconts))


def table_datum2(contents_and_attr):
    return table_datum(*contents_and_attr)


def table_datum(contents, attr=None):
    """Make a <td> (table datum cell) element."""
    return htel_mk_inline("td", attr, contents)


def table_header(contents, attr=None):
    """Make a <th> (table header cell) element."""
    return htel_mk_inline("th", attr, contents)


def div(contents, attr=None):
    """Make a <div> element."""
    return htel_mk("div", attr=attr, flex_contents=contents)


def table(contents, attr=None):
    """Make a <table> element."""
    return htel_mk("table", attr, contents)


def unordered_list(liconts, attr=None):
    """Make a <ul> element."""
    # licont: list item contents
    # liconts: a tuple where each element is a licont
    return htel_mk("ul", attr, st_map(_list_item, liconts))


def heading_level_1(contents, attr=None):
    """Make an <h1> element."""
    return htel_mk("h1", attr, contents)


def heading_level_2(contents, attr=None):
    """Make an <h2> element."""
    return htel_mk("h2", attr, contents)


def heading_level_3(contents, attr=None):
    """Make an <h3> element."""
    return htel_mk("h3", attr, contents)


def anchor(contents, attr=None):
    """Make an <a> element."""
    return htel_mk_inline("a", attr, contents)


def colgroup(contents, attr=None):
    """Make a <colgroup> element."""
    return htel_mk("colgroup", attr, contents)


def col(attr=None):
    """Make a <col> element."""
    return htel_mk_nlb2_nc("col", attr=attr)


def span(contents, attr=None):
    """Make a <span> element."""
    return htel_mk_inline("span", attr=attr, contents=contents)


def span_c(contents, the_class=None):
    """Make a <span> element, given a value for the "class" attr."""
    return span(contents, the_class and {"class": the_class})


def bold(contents, attr=None):
    """Make a <bold> element."""
    return htel_mk_inline("b", attr=attr, contents=contents)


def italic(contents, attr=None):
    """Make a <italic> element."""
    return htel_mk_inline("i", attr=attr, contents=contents)


def small(contents, attr=None):
    """Make a <small> element."""
    return htel_mk_inline("small", attr=attr, contents=contents)


def big(contents, attr=None):
    """Make a <big> element."""
    return htel_mk_inline("big", attr=attr, contents=contents)


def sup(contents, attr=None):
    """Make a <sup> (superscript) element."""
    return htel_mk_inline("sup", attr=attr, contents=contents)


def horizontal_rule(attr=None):
    """
    Make a <hr> element
    """
    return htel_mk_nlb1_nc("hr", attr=attr)


def line_break(attr=None):
    """
    Make a <br> element
    that is NOT followed by a newline in the source code.
    """
    return htel_mk_inline_nc("br", attr=attr)


def line_break2(attr=None):
    """
    Make <br> element
    that is followed by a newline in the source code.
    """
    return htel_mk_nlb1_nc("br", attr=attr)


def flatten(flex_contents):
    if _is_str_or_htel(flex_contents):
        return [flex_contents]
    if isinstance(flex_contents, (tuple, list)):
        return sum_of_map(flatten, flex_contents)
    assert flex_contents is None, flex_contents
    return None



def htel_mk(tag: str, attr=None, flex_contents=None, details=None):
    """Make an HTML element"""
    assert isinstance(tag, str)
    assert isinstance(attr, (type(None), dict))
    flat_contents = flatten(flex_contents)
    if isinstance(flat_contents, (tuple, list)):
        for seq_el in flat_contents:
            assert _is_str_or_htel(seq_el)
    else:
        assert flat_contents is None
    opts1 = {
        "attr": attr,
        "contents": flat_contents,
    }
    opts2 = {k: v for k, v in opts1.items() if v is not None}
    return {"_htel_tag": tag, **opts2}


def htel_mk_inline(tag: str, attr=None, contents=None):
    return htel_mk(tag, attr, contents)


def htel_mk_inline_nc(tag: str, attr=None, contents=None):
    return htel_mk(tag, attr, contents)


def htel_mk_nlb1_nc(tag: str, attr=None, contents=None):
    return htel_mk(tag, attr, contents)


def htel_mk_nlb1(tag: str, attr=None, contents=None):
    return htel_mk(tag, attr, contents)


def htel_mk_nlb2_nc(tag: str, attr=None, contents=None):
    return htel_mk(tag, attr, contents)


def htel_get_tag(html_el):
    """Get the tag of an HTML element."""
    return html_el["_htel_tag"]


def htel_get_class_attr(html_el):
    """Get the class attribute of an HTML element."""
    return html_el["attr"]["class"]


###########################################################


def _is_str_or_htel(obj):
    return isinstance(obj, str) or _is_htel(obj)


def _is_htel(obj):
    return isinstance(obj, dict) and "_htel_tag" in obj


def _write_callback(html_el, add_wbr, out_fp):
    out_fp.write("<!doctype html>\n")
    lines = hgl.get_lines_from_html_el(add_wbr, 100, html_el)
    out_fp.write("\n".join(lines))


def _is_text_singleton(array):  # "array": tuple or list
    return len(array) == 1 and isinstance(array[0], str)


def _list_item(contents, attr=None):
    return htel_mk("li", attr, contents)


def _link_to_css(css_href):
    link_to_css_attr = {"rel": "stylesheet", "href": css_href}
    return htel_mk_nlb2_nc("link", attr=link_to_css_attr)


def _html_el1(attr, contents):
    return htel_mk("html", attr, contents)


def _attr_str(attr_dict):
    if not attr_dict:
        return ""
    return " " + " ".join(map(_kv_str, attr_dict.items()))


def _kv_str(key_and_val):
    key = key_and_val[0]
    value = html.escape(key_and_val[1], quote=True)
    return f'{key}="{value}"'
