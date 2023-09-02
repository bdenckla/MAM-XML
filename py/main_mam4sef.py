""" Exports main """

import my_utils
import my_tanakh_book_names as tbn
import my_mam4sef_handlers
import my_mam4sef_or_ajf


def _timed_main():
    variant = {
        'variant_vtrad': tbn.VT_SEF,
        'variant_handlers': my_mam4sef_handlers.HANDLERS,
    }
    my_mam4sef_or_ajf.main_helper(variant)


def main():
    """ Create the Sefaria MAM from the XML MAM. """
    my_utils.show_time(__file__, _timed_main)


if __name__ == "__main__":
    main()
