"""
Exports:
    with_tmp_openw
    json_dump_to_file_path
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


def json_dump_to_file_path(dumpable, path):
    """ Dump JSON to a file path """
    with_tmp_openw(path, {}, _json_dump_to_file_pointer, dumpable)


def _json_lines_dump_to_file_pointer(outlines, out_fp):
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


def _json_dump_to_file_pointer(dumpable, out_fp):
    json.dump(
        dumpable,
        out_fp,
        ensure_ascii=False,
        indent=2)
    out_fp.write('\n')
