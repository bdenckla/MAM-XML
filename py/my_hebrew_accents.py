""" Exports names for Unicode Hebrew accents """

TEL_G = '\N{HEBREW ACCENT TELISHA GEDOLA}'
TEL_Q = '\N{HEBREW ACCENT TELISHA QETANA}'
GER = '\N{HEBREW ACCENT GERESH}'
GER_2 = '\N{HEBREW ACCENT GERSHAYIM}'
GER_M = '\N{HEBREW ACCENT GERESH MUQDAM}'
REV = '\N{HEBREW ACCENT REVIA}'
MER = '\N{HEBREW ACCENT MERKHA}'
MUN = '\N{HEBREW ACCENT MUNAH}'
OLE = '\N{HEBREW ACCENT OLE}'
YBY = '\N{HEBREW ACCENT YERAH BEN YOMO}'  # aka galgal
ATN_H = '\N{HEBREW ACCENT ATNAH HAFUKH}'
ATN = '\N{HEBREW ACCENT ETNAHTA}'
TIP = '\N{HEBREW ACCENT TIPEHA}'
PASH = '\N{HEBREW ACCENT PASHTA}'
SEG_A = '\N{HEBREW ACCENT SEGOL}'  # A for accent (not vowel)
ZARQA_SH = '\N{HEBREW ACCENT ZARQA}'  # SH: stress helper (!); tsinorit in Sifrei Emet
ZARQA = '\N{HEBREW ACCENT ZINOR}'  # tsinor in Sifrei Emet


G1_TG = GER + TEL_G
G2_TG = GER_2 + TEL_G

ACCENT_RANGE = '\u0591-\u05ae\u05bd'
# Above includes meteg even though Unicode calls meteg a point not an accent.
