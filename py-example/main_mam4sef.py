"""Create the Sefaria MAM variant from the XML MAM."""

from pycmn import bib_locales as tbn
from pysefaria import mam4sef_handlers
from pysefaria import mam4sef_or_ajf


def almost_main():
    """Create the Sefaria MAM from the XML MAM."""
    variant = {
        "variant-vtrad": tbn.VT_SEF,
        "variant-handlers": mam4sef_handlers.HANDLERS,
    }
    mam4sef_or_ajf.main_helper(variant)


def main():
    """Create the Sefaria MAM from the XML MAM."""
    almost_main()


if __name__ == "__main__":
    main()
