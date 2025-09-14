import html
import pycmn.hebrew_punctuation as hpu
import pycmn.str_defs as sd
from pycmn.my_utils import sum_of_map


def get_lines_from_html_el(add_wbr, max_line_len, html_el):
    io_paragraphs = [[""]]
    _el_to_paragraphs(add_wbr, io_paragraphs, html_el)
    return sum_of_map((_get_lines_from_words, max_line_len), io_paragraphs)


def _el_to_paragraphs(add_wbr, io_paragraphs, html_el):
    """Convert an HTML element to a string."""
    if isinstance(html_el, str):
        _add_str(io_paragraphs[-1], _finalize_string(add_wbr, html_el))
        return
    eltag = html_el["_htel_tag"]
    # hts: htel string
    hts_attr = _attr_str(html_el.get("attr"))
    _add_word(io_paragraphs[-1], f"<{eltag}{hts_attr}>")
    _maybe_start_new_paragraph(io_paragraphs, _LB1.get(eltag, "\n"))
    if contents := html_el.get("contents"):
        assert isinstance(contents, (tuple, list))
        for seq_el in contents:
            if eltag == "style":
                _add_word(io_paragraphs[-1], seq_el)
            else:
                _el_to_paragraphs(add_wbr, io_paragraphs, seq_el)
    if eltag not in _NOCLOSE_SET:
        _add_word(io_paragraphs[-1], f"</{eltag}>")
    _maybe_start_new_paragraph(io_paragraphs, _hts_lb2(eltag))


def _finalize_string(add_wbr, string):
    outstr = string
    outstr = html.escape(outstr, quote=False)
    outstr = outstr.translate(_SSTT)
    if add_wbr:
        outstr = outstr.replace(hpu.MAQ, hpu.MAQ + "<wbr>")
    return outstr


def _add_str(io_paragraph, string: str):
    assert "\n" not in string
    words = string.split(" ")
    _add_word(io_paragraph, words[0])
    io_paragraph.extend(words[1:])


def _add_word(io_paragraph, new_word: str):
    io_paragraph[-1] += new_word


def _maybe_start_new_paragraph(io_paragraphs, hts_lbn):
    if hts_lbn == "\n":
        io_paragraphs.append([""])
    else:
        assert hts_lbn == ""


def _get_lines_from_words(max_line_len, words):
    out_lines = [words[0]]
    for word in words[1:]:
        new_last_line = out_lines[-1] + " " + word
        if max_line_len == -1 or len(new_last_line) <= max_line_len:
            out_lines[-1] = new_last_line
        else:
            out_lines.append(word)
    return out_lines


def _hts_lb2(eltag):
    hts_lb2 = _LB2.get(eltag)
    if hts_lb2 is None:
        hts_lb2 = "" if eltag in _NOCLOSE_SET else None
    if hts_lb2 is None:
        hts_lb2 = "\n"
    return hts_lb2


def _attr_str(attr_dic):
    if not attr_dic:
        return ""
    return " " + " ".join(map(_kv_str, attr_dic.items()))


def _kv_str(key_and_val):
    key = key_and_val[0]
    value = html.escape(key_and_val[1], quote=True)
    return f'{key}="{value}"'


_SSTT = str.maketrans(
    {  # special space translation table
        "\N{EM SPACE}": "&emsp;",
        sd.THSP: "&thinsp;",
        sd.NBSP: "&nbsp;",
    }
)
_NOCLOSE_SET = {"br", "hr", "meta", "link", "col"}
_LB2 = {
    "bdi": "",
    "a": "",
    "span": "",
    "abbr": "",
    "em": "",
    "sup": "",
    "big": "",
    "small": "",
    "b": "",
}
_LB1 = {
    **_LB2,
    "td": "",
    "th": "",
    "h1": "",
    "h2": "",
    "h3": "",
    "blockquote": "",
    "hr": "",
    "li": "",
    "br": "",
    "caption": "",
    "p": "",
}
