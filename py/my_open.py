"""
Exports:
    with_tmp_openw
    std_json_dump_to_file_path
    dump_json_lines
"""

import os
import pathlib
import json


def with_tmp_openw(path, callback, **kwargs):
    """ Open path for writing, but through a temporary file """
    tpath = _tmp_path(path)
    with _openw(tpath, **kwargs) as outfp:
        retval = callback(outfp)
    os.replace(tpath, path)
    return retval


def std_json_dump_to_file_path(dumpable, path, indent=0, sort_keys=False):
    """ dump JSON to file path """
    def _write_callback(out_fp):
        _std_json_dump_to_file_pointer(dumpable, out_fp, indent, sort_keys)
    with_tmp_openw(path, _write_callback)


def dump_json_lines(path, outlines):
    """ dump JSON lines to path """
    def _write_callback(out_fp):
        out_fp.write('[\n')
        for outline in outlines[:-1]:
            out_fp.write(outline + ',\n')
        if outlines:
            out_fp.write(outlines[-1] + '\n')
        out_fp.write(']\n')
    with_tmp_openw(path, _write_callback)


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
    indent=0,
    sort_keys=False
):
    json.dump(
        dumpable,
        out_fp,
        ensure_ascii=False,
        indent=indent,
        sort_keys=sort_keys)
    out_fp.write('\n')
