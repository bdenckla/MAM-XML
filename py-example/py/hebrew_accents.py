""" Exports names for Unicode Hebrew accents """

import py.cantsys as cantsys

ATN = "\N{HEBREW ACCENT ETNAHTA}"
SEG_A = "\N{HEBREW ACCENT SEGOL}"
SHA = "\N{HEBREW ACCENT SHALSHELET}"
ZAQ_Q = "\N{HEBREW ACCENT ZAQEF QATAN}"
ZAQ_G = "\N{HEBREW ACCENT ZAQEF GADOL}"
TIP = "\N{HEBREW ACCENT TIPEHA}"
REV = "\N{HEBREW ACCENT REVIA}"
ZSH_OR_TSIT = "\N{HEBREW ACCENT ZARQA}"
PASH = "\N{HEBREW ACCENT PASHTA}"
YET = "\N{HEBREW ACCENT YETIV}"
TEV = "\N{HEBREW ACCENT TEVIR}"
GER = "\N{HEBREW ACCENT GERESH}"
GER_M = "\N{HEBREW ACCENT GERESH MUQDAM}"
GER_2 = "\N{HEBREW ACCENT GERSHAYIM}"
QAR = "\N{HEBREW ACCENT QARNEY PARA}"
TEL_G = "\N{HEBREW ACCENT TELISHA GEDOLA}"
PAZ = "\N{HEBREW ACCENT PAZER}"
ATN_H = "\N{HEBREW ACCENT ATNAH HAFUKH}"
MUN = "\N{HEBREW ACCENT MUNAH}"
MAH = "\N{HEBREW ACCENT MAHAPAKH}"
MER = "\N{HEBREW ACCENT MERKHA}"
MER_2 = "\N{HEBREW ACCENT MERKHA KEFULA}"
DAR = "\N{HEBREW ACCENT DARGA}"
QOM = "\N{HEBREW ACCENT QADMA}"
TEL_Q = "\N{HEBREW ACCENT TELISHA QETANA}"
YBY = "\N{HEBREW ACCENT YERAH BEN YOMO}"
OLE = "\N{HEBREW ACCENT OLE}"
ILU = "\N{HEBREW ACCENT ILUY}"
DEX = "\N{HEBREW ACCENT DEHI}"
Z_OR_TSOR = "\N{HEBREW ACCENT ZINOR}"

# In SEG_A, the A is for "accent", i.e. distinguishing it from the vowel SEGOL_V.
# In ZSH_OR_TSIT, the ZSH stands for "zarqa stress helper" (!)
# In ZSH_OR_TSIT, the TSIT stands for "tsinnorit" (an accent confied to Sifrei Emet)
# In Z_OR_TSOR, the Z stands for "zarqa"
# In Z_OR_TSOR, the TSOR stands for "tsinnor" (an accent confied to Sifrei Emet)
# In QOM, the Q stands for qadma (aka azla)
# In QOM, the O stands for "or".
# In QOM, the M stands for "metigah".
# Thus, QOM stands for "qadma or metigah".
# YBY is also known as galgal.

# NU: non-Unicode
# Both prose and poetic
NU_SLQ = "nu_slq"
NU_SHA_LEG = "nu_sha_leg"
NU_MUN_LEG = "nu_mun_leg"
# Prose only
NU_Z = "nu_z"
# Poetic only
NU_MAH_LEG = "nu_mah_leg"
NU_AZL_LEG = "nu_azl_leg"
NU_TSOR = "nu_tsor"
NU_TSIT = "nu_tsit"

NON_UNICODE_ACCENTS = {
    NU_SLQ,
    NU_SHA_LEG,
    NU_MUN_LEG,
    NU_Z,
    NU_MAH_LEG,
    NU_AZL_LEG,
    NU_TSOR,
    NU_TSIT,
}

G1_TG = GER + TEL_G
G2_TG = GER_2 + TEL_G

ACCENTS_AND_MTG = "\u0591-\u05ae\u05bd"

_CONJUNCTIVES_BCC_PROSE = [  # See Yeivin ITM #194 (page 167)
    MUN,  # (but munax legarmeih is disjunctive)
    MAH,
    MER,
    DAR,
    QOM,
    TEL_Q,
    YBY,
    MER_2,
    # MAYELA (coded as tipexa; need to distinguish)
]
_CONJUNCTIVES_BCC_POETIC = [  # See Yeivin ITM #358 (page 264) and, for ATN_H only, #361 (page 266)
    MUN,
    MER,  # but as yored (always in oleh-we-yored) is disjunctive
    ILU,
    TIP,  # tarxa
    YBY,
    MAH,  # (but mehuppak legarmeih is disjunctive)
    QOM,  # aka azla (but azla legarmeih is disjunctive)
    SHA,  # shalshelet qeṭannah (but shalshelet gedolah (shalshelet legarmeih) is disjunctive)
    NU_TSIT,  # tsinnorit
    ATN_H,
    # In Yeivin ITM (#361 (page 266)), atnax hafukh is called only "a 'v' shaped sign"
    # and is not listed with the other poetic conjunctives,
    # i.e. is not listed in #358 (page 264).
]
CONJUNCTIVES_BCC = cantsys.mk_cantsys_struct(
    _CONJUNCTIVES_BCC_PROSE, _CONJUNCTIVES_BCC_POETIC
)
