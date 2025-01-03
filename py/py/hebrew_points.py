""" Exports names for Unicode Hebrew points """

import py.my_str_defs as sd

MTGOSLQ = "\N{HEBREW POINT METEG}"
VARIKA = "\N{HEBREW POINT JUDEO-SPANISH VARIKA}"
DAGOMOSD = "\N{HEBREW POINT DAGESH OR MAPIQ}"  # dagesh or mapiq or shuruq dot
RAFE = "\N{HEBREW POINT RAFE}"
SHIND = "\N{HEBREW POINT SHIN DOT}"
SIND = "\N{HEBREW POINT SIN DOT}"
SHEVA = "\N{HEBREW POINT SHEVA}"
XSEGOL = "\N{HEBREW POINT HATAF SEGOL}"
XPATAX = "\N{HEBREW POINT HATAF PATAH}"
XQAMATS = "\N{HEBREW POINT HATAF QAMATS}"
XIRIQ = "\N{HEBREW POINT HIRIQ}"
TSERE = "\N{HEBREW POINT TSERE}"
SEGOL_V = "\N{HEBREW POINT SEGOL}"  # V for vowel (not accent)
PATAX = "\N{HEBREW POINT PATAH}"
QAMATS = "\N{HEBREW POINT QAMATS}"
QAMATS_Q = "\N{HEBREW POINT QAMATS QATAN}"
XOLAM_XFV = "\N{HEBREW POINT HOLAM HASER FOR VAV}"
XOLAM = "\N{HEBREW POINT HOLAM}"
QUBUTS = "\N{HEBREW POINT QUBUTS}"

DROP_VARIKA = str.maketrans({VARIKA: None})

RECC_APCV = "\u0591-\u05c7" + sd.CGJ + VARIKA
RECC_HEBR = "\u0591-\u05f4" + sd.CGJ + VARIKA
# RECC: Regular Expression Class Contents
# Accents, Points, CGJ, & Varika
RE_APCV_STAR = f"[{RECC_APCV}]*"
RE_YES_HEBREW = f"[{RECC_HEBR}]"
RE_NOT_HEBREW = f"[^{RECC_HEBR}]"