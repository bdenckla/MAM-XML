"""
    Exports
        szip
        show_progress_g
        show_progress_cv
        get_book39_tuple_from_args
"""
import os
import argparse

import my_tanakh_book_names as tbn


def init(dic, key, val):
    """ If key is fresh in dic, set its value to val. Other assert. """
    assert key not in dic
    dic[key] = val


def maybe_init(dic, key, val):
    """ If key is fresh in dic, set its value to val. Otherwise whiff. """
    if key not in dic:
        dic[key] = val


def first_and_only(seq):
    """ Assert that this is there is only 1 el of seq, and returns it. """
    assert len(seq) == 1
    return seq[0]


def first_and_only_and_str(seq):
    """ Like first_and_only, but also asserts that result is a string. """
    fao = first_and_only(seq)
    assert isinstance(fao, str)
    return fao


def szip(*seqs):
    """ Strongly zip (zip, asserting equal length) """
    for seq in seqs[1:]:
        assert _len_for_szip(seq) == _len_for_szip(seqs[0])
    return zip(*seqs)


def l_szip(*seqs):
    """ Force output of szip to be a list. """
    return list(szip(*seqs))


def intersperse(sep, seq):
    """ Intersperse a separator between the elements of a sequence. """
    seps = (sep,) * len(seq)
    tmp = sum(szip(seq, seps), tuple())
    return tmp[:-1]  # rm final sep, e.g. final None


def dv_map(foc, the_dic):
    """
    "Dictionary value map"
    Return a dict with the same keys but with values mapped.
    {k: v} becomes {k: f(v)}
    """
    assert isinstance(the_dic, dict)
    if isinstance(foc, tuple):
        return {k: foc[0](*foc[1:], v) for k, v in the_dic.items()}
    return {k: foc(v) for k, v in the_dic.items()}


def dkv_map(foc, the_dic):
    """
    "Dictionary key and value map"
    Return a dict with the same keys but with values mapped.
    {k: v} becomes {k: f(k, v)}
    """
    assert isinstance(the_dic, dict)
    if isinstance(foc, tuple):
        return {k: foc[0](*foc[1:], k, v) for k, v in the_dic.items()}
    return {k: foc(k, v) for k, v in the_dic.items()}


def ll_map(fun, the_list):
    """
    Map the given function over the given list.
    (The "ll" means "list in, list out".)
    """
    assert isinstance(the_list, list)
    # Sure, we could just implement ll_map using sl_map.
    # But that increases the stack depth, making debugging
    # a little more awkward.
    # So we just repeat ourselves.
    if isinstance(fun, tuple):
        return [fun[0](*fun[1:], elem) for elem in the_list]
    return list(map(fun, the_list))


def tt_map(fun, the_tuple):
    """
    Map the given function over the given tuple.
    (The "tt" means "tuple in, tuple out".)
    """
    assert isinstance(the_tuple, tuple)
    return st_map(fun, the_tuple)


def sl_map(fun, the_sequence):
    """
    Map the given function over the given sequence (e.g. list or tuple).
    (The "sl" means "[any] sequence in, list out".)
    """
    if isinstance(fun, tuple):
        return [fun[0](*fun[1:], elem) for elem in the_sequence]
    return list(map(fun, the_sequence))


def st_map(fun, the_sequence):
    """
    Map the given function over the given sequence (e.g. list or tuple).
    (The "st" means "[any] sequence in, tuple out".)
    """
    if isinstance(fun, tuple):
        return tuple(fun[0](*fun[1:], elem) for elem in the_sequence)
    return tuple(map(fun, the_sequence))


def ss_map(fun, the_sequence):
    """
    Map the given function over the given sequence (e.g. list or tuple).
    (The "ss" means "[any] sequence in, [any] sequence out".)
    """
    type_of_seq = type(the_sequence)  # presumably list or tuple
    if isinstance(fun, tuple):
        return type_of_seq(fun[0](*fun[1:], elem) for elem in the_sequence)
    return type_of_seq(map(fun, the_sequence))


def dv_dispatch(fn_table, dic, *extra_args):
    """
    Transform the value at each key using a table of functions.
    {k: v} becomes {k: f[k](v)}
    """
    return {key: fn_table[key](*extra_args, val) for key, val in dic.items()}


def sum_of_lists(seq_of_lists):
    """ Return the sum of a sequence of lists. """
    accum = []
    for the_list in seq_of_lists:
        accum.extend(the_list)
    return accum


def sum_of_tuples(seq_of_tuples):
    """ Return the sum of a sequence of tuples. """
    accum = tuple()
    for the_tuple in seq_of_tuples:
        accum += the_tuple
    return accum


def show_progress_g(uufileuu, *rest):
    # label is usually some sort of book name
    bn_uufileuu = os.path.basename(uufileuu)
    bn_and_rest = ' '.join((bn_uufileuu, *rest))
    print(bn_and_rest)


def get_book39_tuple_from_argparse():
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
