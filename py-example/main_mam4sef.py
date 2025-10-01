""" Exports main """

import pycmn.bib_locales as tbn
import pysefaria.mam4sef_handlers as mam4sef_handlers
import pysefaria.mam4sef_or_ajf as mam4sef_or_ajf


def main():
    """Create the Sefaria MAM from the XML MAM."""
    variant = {
        "variant-vtrad": tbn.VT_SEF,
        "variant-handlers": mam4sef_handlers.HANDLERS,
    }
    mam4sef_or_ajf.main_helper(variant)


if __name__ == "__main__":
    main()
