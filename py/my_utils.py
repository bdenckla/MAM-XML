"""
    Exports
        szip
        show_time
        show_progress_g
        show_progress_cv
        get_book39_tuple_from_args
"""
import time
import datetime
import os
import argparse

import my_tanakh_book_names as tbn


def first_and_only(seq):
    """ Asserts that this is there is only 1 el of seq, and returns it. """
    assert len(seq) == 1
    return seq[0]


def first_and_only_and_str(seq):
    """ Like first_and_only, but also asserts that result is a string. """
    fao = first_and_only(seq)
    assert isinstance(fao, str)
    return fao


def szip(*seqs):
    """ strong zip (asserts equal length) """
    for seq in seqs[1:]:
        assert _len_for_szip(seq) == _len_for_szip(seqs[0])
    return zip(*seqs)


def show_time(uufileuu, inner_function):
    print(os.path.basename(uufileuu))
    start = time.process_time()
    inner_function()
    end = time.process_time()
    print(datetime.timedelta(seconds=end-start))


def show_progress_g(uufileuu, *rest):
    # label is usually some sort of book name
    bn_uufileuu = os.path.basename(uufileuu)
    bn_and_rest = ' '.join((bn_uufileuu, *rest))
    print(bn_and_rest)


def get_book39_tuple_from_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--book39tbn')  # e.g. 1Samuel not I Samuel
    parser.add_argument('--section6')  # e.g. SifEm
    args = parser.parse_args()
    if args.book39tbn:
        # I think there's a way to tell the argument parser that two arguments
        # are exclusive; if so perhaps I should use that instead of the assert
        # below.
        assert not args.section6
        return (args.book39tbn,)
    if args.section6:
        return tbn.books_of_sec(args.section6)
    return tbn.ALL_BOOK_IDS


def _len_for_szip(obj):
    if not isinstance(obj, (tuple, list)):
        return len(tuple(obj))
    return len(obj)
