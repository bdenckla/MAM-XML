"""
Exports:
    with_tmp_openw
    std_json_dump_to_file_path
    dump_json_lines
"""

import os
import pathlib
import json


def with_tmp_openw(path, kwargs_dic, write_fun, *write_fun_args):
    """ Open path for writing, but through a temporary file """
    tpath = _tmp_path(path)
    with _openw(tpath, **kwargs_dic) as outfp:
        retval = write_fun(*write_fun_args, outfp)
    os.replace(tpath, path)
    return retval


def std_json_dump_to_file_path(dumpable, path, indent=0):
    """ Dump JSON to a file path """
    with_tmp_openw(path, {}, _write_callback1, dumpable, indent)


def dump_json_lines(path, outlines):
    """ Dump JSON lines to a file path """
    with_tmp_openw(path, {}, _write_callback2, outlines)


def _write_callback1(dumpable, indent, out_fp):
    _std_json_dump_to_file_pointer(dumpable, out_fp, indent)


def _write_callback2(outlines, out_fp):
    out_fp.write('[\n')
    for outline in outlines[:-1]:
        out_fp.write(outline + ',\n')
    if outlines:
        out_fp.write(outlines[-1] + '\n')
    out_fp.write(']\n')


def _openw(path, **kwargs):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return open(path, 'w', encoding='utf-8', **kwargs)


def _tmp_path(path):
    pathobj = pathlib.Path(path)
    # e.g. from /dfoo/dbar/stem.ext return /dfoo/dbar/stem.tmp.ext
    # where suffix = .ext
    return pathobj.parent / (str(pathobj.stem) + '.tmp' + pathobj.suffix)


def _std_json_dump_to_file_pointer(
    dumpable,
    out_fp,
    indent=0
):
    json.dump(
        dumpable,
        out_fp,
        ensure_ascii=False,
        indent=indent)
    out_fp.write('\n')
