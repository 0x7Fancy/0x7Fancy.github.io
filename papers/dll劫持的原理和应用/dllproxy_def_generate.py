#!/usr/bin/python3
#coding=utf-8

import os
import pefile
import sys

DLL_SOURCE_TEMPLATE = """#include <Windows.h>
#include <stdio.h>

int payload() {
    printf("payload statement execute\\n");
    return 0;
}

BOOL WINAPI DllMain(
    HINSTANCE hinstDLL,  // handle to DLL module
    DWORD fdwReason,     // reason for calling function
    LPVOID lpReserved )  // reserved
{
    // Perform actions based on the reason for calling.
    switch( fdwReason ) 
    { 
        case DLL_PROCESS_ATTACH:
            // Initialize once for each new process.
            // Return FALSE to fail DLL load.
            payload();
            break;

        case DLL_THREAD_ATTACH:
            // Do thread-specific initialization.
            break;

        case DLL_THREAD_DETACH:
            // Do thread-specific cleanup.
            break;

        case DLL_PROCESS_DETACH:
            // Perform any necessary cleanup.
            break;
    }
    return TRUE;  // Successful DLL_PROCESS_ATTACH.
}
"""
DLL_DEF_TEMPLATE = "LIBRARY {}\nEXPORTS\n"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage:")
        print("  python3 dllproxy_def_generate.py [target.dll]")
        exit(0)
    # end if

    dll_path = sys.argv[1]
    print("generate dllproxy for [%s]" % dll_path)

    dll_orig_path = dll_path.rstrip(".dll") + "_origin.dll"
    print("1.rename [%s] to [%s]" % (dll_path, dll_orig_path))
    os.rename(dll_path, dll_orig_path)

    print("2.generate DEF file for dll description")
    dll_orig_name = os.path.basename(dll_orig_path).rstrip(".dll")
    dll_file = os.path.basename(dll_path)
    def_data = DLL_DEF_TEMPLATE.format(dll_file)

    dll = pefile.PE(dll_orig_path)
    count = 0

    for export in dll.DIRECTORY_ENTRY_EXPORT.symbols:
        # entryname[=internal_name|other_module.exported_name] [@ordinal [NONAME] ] [ [PRIVATE] | [DATA] ]

        if export.name == None:
            # NONAME 
            line = "    noname={}.#{} @{} NONAME".format(dll_orig_name, 
                                    export.ordinal, export.ordinal)
        else:
            # NAME
            line = "    {}={}.{} @{}".format(export.name.decode(), dll_orig_name,
                                    export.name.decode(), export.ordinal)
        count += 1
        print(count, line)
        def_data += (line + "\n")
    # end for

    def_file = dll_file.rstrip(".dll") + ".def"
    with open(def_file, "w+") as f:
        f.write(def_data)

    print("3.generate source code for dll")
    def_source = dll_file.rstrip(".dll") + ".c"
    with open(def_source, "w+") as f:
        f.write(DLL_SOURCE_TEMPLATE)

    print("4.compile manually with command\n  gcc -Wall -shared %s %s -o %s" %
            (def_source, def_file, dll_file))
# end main()
