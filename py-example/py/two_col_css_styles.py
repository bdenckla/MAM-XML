def make_css_file_for_mwd(out_path):
    with open(out_path, "w", encoding="utf-8") as out_fp:
        out_fp.write(_MWD_STYLES_STR.lstrip())


def make_css_file_for_authored(out_path):
    with open(out_path, "w", encoding="utf-8") as out_fp:
        out_fp.write(_AUTHORED_STYLES_STR.lstrip())


_AUTHORED_STYLES_STR = """
:root {
  color-scheme: light dark;
}
.element {
  color: light-dark(black, white);
  background-color: light-dark(white, black);
}
body {
    max-width: 40em;
    width: 90%;
    margin-left: auto;
    margin-right: auto;
    font-size: 14pt;
}
*[lang="hbo"] { font-family: "Taamey D WOFF2"; font-size: 140%; }
@font-face { font-family: "Taamey D WOFF2"; src: url("woff2/Taamey_D.woff2"); }
em { font-style: normal; font-weight: bold; }
span.romanized { font-style: italic; }
span.book-title { font-style: italic; }
abbr.small-caps { text-transform: lowercase; font-variant: small-caps; }
p { text-align: justify; }
li { text-align: justify; }
blockquote { text-align: justify; }
*.extra-letter-spacing { letter-spacing: 0.1em; } /* span or bdi */
*.gray { color: gray; }
*.big { font-size: 250%; }
table.border-collapse { border-collapse: collapse; }
table.center { margin-left: auto; margin-right: auto; }
p.center { text-align: center; }
p.center-and-spaced { text-align: center; word-spacing: 1.5em; }
img.width10em { width: 10em; }
img.width5em { width: 5em; }
th, td { padding-right: 0.4em; padding-left: 0.4em; }
img { max-width: 100%; }
"""

_MWD_STYLES_STR = """
body { font-size: 14pt; }
*[lang="hbo"] {
    font-family: "Taamey D WOFF2";
    font-size: 140%;
    font-feature-settings: 'ss01'; /* ss01 = xataf qamats qatan */
}
@font-face {
    font-family: "Taamey D WOFF2";
    src: url("woff2/Taamey_D.woff2");
}
span.mam-dqq-unstressed { font-feature-settings: 'ss01', 'ss02'; }
/* ss01 = xataf qamats qatan */
/* ss02 = qamats qatan with small meteg */
span.mam-letter-small { font-size: 85%; }
span.mam-letter-large { font-size: 125%; }
span.mam-letter-hung { vertical-align: super; }
span.mam-lp-legarmeih { font-weight: bold; }
span.mam-lp-paseq { font-size: 85%; }
span.mam-implicit-maqaf { color: gray; }
span.mam-note-callout { color: red; }
span.mam-doc-callout { color: red; }
span.mam-doc-lemma { color: blue; }
span.mam-doc-target-without-callout { color: blue; }
table.border-collapse { border-collapse: collapse; }
th, td {
    padding-right: 0.4em;
    padding-left: 0.4em;
}
*.bordered { border: 1px solid; }
*.top-n-bot-bordered { border-top: 1px solid; border-bottom: 1px solid; }
*.small { font-size: 85%; }
*.end-aligned { text-align: end; }
"""
