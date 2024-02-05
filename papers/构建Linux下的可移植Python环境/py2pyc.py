#!/usr/bin/python3
#!coding=utf-8

"""
Filename: py2pyc.py
Description:
Author: xx
Time: 2019.07.05
"""

import os
import sys
import shutil


result_folder = "pyc/"


def organize_pyc(lib_path):
    print("[*] start organize pyc folder")

    #
    if not os.path.exists(result_folder):
        os.mkdir(result_folder)

    #
    for path, dirnames, filenames in os.walk(lib_path):
        for name in filenames:
            if not name.endswith(".pyc"):
                continue
            src = os.path.join(path, name)

            # delete the "__pychache"
            dst_path = path.replace("__pycache__", "")
            # delete the version info. eg:
            # base64_codec.cpython-37.pyc => base64_codec.pyc 
            array = name.split(".")
            dst_name = array[0] + "." + array[2]

            dst = os.path.join(result_folder, dst_path)
            if not os.path.exists(dst):
                os.makedirs(dst)
            dst = os.path.join(dst, dst_name)

            print("[*] processing [%s]" % src)
            shutil.copy(src, dst)
        # end for
    # end for


def do_compile(lib_path):
    print("[*] start compile libs [%s]" % lib_path)

    import compileall
    compileall.compile_dir(lib_path, force=True)


def main():
    print("[*] Compile *.py to *.pyc")
    if len(sys.argv) < 2:
        print("Usage:\n  python %s [lib_path]" % sys.argv[0])
        return

    lib_path = sys.argv[1]
    if not os.path.exists(lib_path):
        print("the lib [%s] not found" % lib_path)
        return

    #
    do_compile(lib_path)
    #
    organize_pyc(lib_path)
    print("\n[*] in [%s], Build success" % result_folder)


if __name__ == "__main__":
    main()
