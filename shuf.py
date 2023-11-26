#!/usr/bin/python


import random, sys, argparse

class randline:
    def __init__(self, lines):
        self.lines = lines

    def chooseline(self):
        return random.choice(self.lines)

    def print_random_lines(self, head_count, eon, repeat):
        copy_lines = self.lines
        if eon is False and repeat is False:
            for i in range(head_count):
                curr_line = random.choice(copy_lines)
                sys.stdout.write(curr_line)
        if eon is True and repeat is False:
            for i in range(head_count):
                curr_line = random.choice(copy_lines)
                print(curr_line)
                copy_lines.remove(curr_line)
        if eon is False and repeat is True:
            for i in range(head_count):
                curr_line = random.choice(copy_lines)
                sys.stdout.write(curr_line)
        if eon is True and repeat is True:
            for i in range(head_count):
                curr_line = random.choice(copy_lines)
                print(curr_line)

def main():
    usage_msg = """shuf[OPTION]...

Output randomly selected lines from LINE(S) or a FILE specified by -n. If -n is not specified, print all lines."""

    parser = argparse.ArgumentParser(
                          usage=usage_msg,
                          formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-e","--echo",action="store_true",help="treat each arg as an input line")
    parser.add_argument("-n", "--head-count",
                      action="store", dest="head_count", default=None,
                      help="output head_count lines")
    parser.add_argument("input",metavar="INPUT",nargs="*",help="input line(s) or input file(s)")
    parser.add_argument("-r","--repeat",action="store_true",help="output lines can be repeated")
    parser.add_argument("-i","--input-range",action="store",dest="input_range",help="treat each number LO through HI as an input line")
    args = parser.parse_args()

    if args.input_range is not None and (args.echo or args.input):
        print("shuf:cannot combine -e and -i options")
        sys.exit(1) 

    eon = False
    if args.echo:
        input_lines = args.input
        eon = True
        if not input_lines:
            parser.error("no input specified")
    else:
        input_lines = []

    if args.input_range:
        eon = True
        try:
            lo, hi = map(int, args.input_range.split('-'))
            if lo <= hi:
                input_lines.extend(map(str, range(lo, hi + 1)))
            else:
                parser.error("invalid input range: {0}".format(args.input_range))
        except ValueError:
            parser.error("invalid input range format: {0}".format(args.input_range))

    if not args.echo and not args.input_range and args.input:
        for item in args.input:
            if item == '<' or item == "-" or item == '- <':
                continue
            try:
                with open(item, 'r') as file:
                    input_lines.extend(file.readlines())
            except FileNotFoundError:
                parser.error("file not found: {0}".format(item))

    if args.head_count is not None:
        try:
            head_count = int(args.head_count)
            if head_count > len(input_lines):
                parser.error("head_count is greater than the number of input lines")
        except ValueError:
            parser.error("invalid HEAD_COUNT: {0}".
                         format(args.head_count))
        if head_count < 0:
            parser.error("negative count: {0}".
                         format(head_count))
    else:
        if args.echo and not args.input:
            parser.error("no input specified")

    repeat = True
    if not args.repeat:
        repeat = False

    try:
        if args.head_count is not None:
            generator = randline(input_lines)
        else:
            head_count = len(input_lines)
            generator = randline(input_lines)
        generator.print_random_lines(head_count, eon, repeat)
    except IOError as e:
        parser.error("I/O error({0}): {1}".
                     format(e.errno, e.strerror))

if __name__ == "__main__":
    main()



