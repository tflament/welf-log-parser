#!/bin/python3

import sys
import getopt

VERBOSE = False

def verbose(*arg):
    if VERBOSE:
        print(" ".join(arg))

def build_index_dict(wanted_keys):
    toreturn = {}
    i = 0
    for wanted in wanted_keys:
        toreturn[wanted] = i
        i += 1

    return toreturn

def print_wanted_keys(wanted_keys, index_dict, parts, format):
    toprint = [""] * len(wanted_keys)
    
    for part in parts:
        splitted = part.split("=")

        token = splitted[0]
        value = "=".join(splitted[1:])

        if token in wanted_keys:
            if format == "original":
                toprint[index_dict[token]] = "%s=%s" % (token, value)
            else:
                toprint[index_dict[token]] = value

    if format == "original":
        print(" ".join(toprint))
    else:
        print(",".join(toprint))

def extract_line_part(line):
    line = line.strip()
    splitted = line.split()

    final = []
    i = 0
    while i < len(splitted):
        if "=" in splitted[i] and "\"" not in splitted[i]:
            final.append(splitted[i])
            
            verbose("#1", splitted[i])
        elif "=" in splitted[i] and "\"" in splitted[i] and splitted[i].count("\"") % 2 == 0:
            final.append(splitted[i])

            verbose("#2", splitted[i])
        elif "=" in splitted[i] and "\"" in splitted[i]:
            verbose("#3", splitted[i])

            full_part = splitted[i]

            j = i + 1
            while j < len(splitted) and "\"" not in splitted[j]:
                full_part += " "
                full_part += splitted[j]
                j += 1
            full_part += " "
            full_part += splitted[j]

            verbose("#3 next:", full_part)

            final.append(full_part)

            # we move directly to next interesting position, this is why we also need to "continue"
            i = j+1
            continue
        elif splitted[i] == "":
            pass
        else:
            print("Invalid format")
            print("Array:", splitted)
            print("Value at index %d has no '=' char" % i)
            exit()

        i += 1

    return final

def usage():
    print("%s [options] logfile columns" % sys.argv[0])
    print("cat file.log|%s [options] columns" % sys.argv[0])

def main():
    global VERBOSE

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'vhf:', ['help', 'format='])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err)  # will print something like "option -a not recognized"
        # usage()
        sys.exit(2)

    format = "original"
    for o, a in opts:
        if o == "-v":
            VERBOSE = True
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-f", "--format"):
            if a not in ["original", "csv"]:
                print("Invalid format")
                exit()
            format = a
    
    if len(args) < 1 or len(args) > 2:
        usage()
        sys.exit()

    if len(args) == 1:
        wanted_keys = args[0].split(",")
    elif len(args) == 2:
        wanted_keys = args[1].split(",")
    
    index_dict = build_index_dict(wanted_keys)

    if len(args) == 1:
        for line in sys.stdin:
            parts = extract_line_part(line)
            print_wanted_keys(wanted_keys, index_dict, parts, format)
    elif len(args) == 2:
        with open(args[0]) as file:
            for line in file:
                parts = extract_line_part(line)
                print_wanted_keys(wanted_keys, index_dict, parts, format)

if __name__ == "__main__":
    main()