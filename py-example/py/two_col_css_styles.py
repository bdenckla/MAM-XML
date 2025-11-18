from py.two_col_css_styles_m import MWD_STYLES_STR
from py.two_col_css_styles_a import AUTHORED_STYLES_STR


def make_css_file_for_mwd(out_path):
    with open(out_path, "w", encoding="utf-8") as out_fp:
        out_fp.write(MWD_STYLES_STR.lstrip())


def make_css_file_for_authored(out_path):
    with open(out_path, "w", encoding="utf-8") as out_fp:
        out_fp.write(AUTHORED_STYLES_STR.lstrip())


def make_css_file_for_authored_wide(out_path):
    with open(out_path, "w", encoding="utf-8") as out_fp:
        out_fp.write(_AUTHORED_STYLES_STR_WIDE.lstrip())


_AUTHORED_STYLES_STR_WIDE = AUTHORED_STYLES_STR.replace(
    "max-width: 40em;", "max-width: 80em;"
)
assert _AUTHORED_STYLES_STR_WIDE != AUTHORED_STYLES_STR
# The assert above makes sure the replace did something
