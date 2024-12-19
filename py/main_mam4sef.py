""" Exports main """

import py.my_locales as tbn
import py.my_mam4sef_handlers as my_mam4sef_handlers
import py.my_mam4sef_or_ajf as my_mam4sef_or_ajf


def main():
    """Create the Sefaria MAM from the XML MAM."""
    variant = {
        "variant-vtrad": tbn.VT_SEF,
        "variant-handlers": my_mam4sef_handlers.HANDLERS,
    }
    my_mam4sef_or_ajf.main_helper(variant)


if __name__ == "__main__":
    main()
