#!/bin/env python

import sys
from os import path

def generate_line(cmdfile):
    complete_line, space = '', ''
    for line in open(cmdfile, "r"):
        line = line.strip()
        if line and line[-1] == '\\':
            complete_line += space + line[:-1].rstrip()
            space = ' '
            continue
        
        if line:
            complete_line += space + line
        yield complete_line
        complete_line, space = '', ''

def parse_file(cmdfile):
    files = set()
    for line in generate_line(cmdfile):
        if line.startswith('source_'):
            src = line.split(':=')[1].strip()
            files.add(src)
            continue
        if line.startswith('deps_'):
            if len(files) == 0:
                break
            deps = line.split(':=')[1].strip()
            deps = deps.replace('$(wildcard', '')
            deps = deps.replace(')', '')
            for d in deps.split():
                if '..' in d:
                    d = path.realpath(d)
                files.add(d)
            break
    return files

def main():
    allfiles = set()
    for path in open(sys.argv[1], "r"): 
        path = path.strip()
        files = parse_file(path)
        allfiles.update(files)

    for f in sorted(allfiles):
        print f

if __name__ == '__main__':
        main()
