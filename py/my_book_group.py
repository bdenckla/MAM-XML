""" exports bkg_make """


def bkg_make(name, bkids):
    """ Make a "book group" structure. """
    return {
        'bkg-name': name,
        'bkg-bkids': bkids,
    }
