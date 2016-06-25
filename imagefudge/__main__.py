import argparse
import os, sys
sys.path.append(os.path.abspath('..'))

from collections import namedtuple

from imagefudge.image_fudge import test_many_random
from imagefudge.image_fudge import test_multi_origin

def description():
    """Description For command line interface"""
    return ('',
            '') #TODO: Fill this in

def test_main(args):
    """ """
    parser = argparse.ArgumentParser(description=description())
    parser.add_argument('-f', '--image_file', default='../examples/GodRoss.jpg', type=str, help='The file path of the image to test')
    parser.add_argument('test_name', type=str, help='The name of the test to perform')

    args = parser.parse_args(args)

    try:
        if args.test_name == "test_many_random":
            test_many_random(args.image_file, 5, 5)
        elif args.test_name == "test_multi_origin":
            test_multi_origin(args.image_file, 4)
        else: print("Error: Test function {} doesn't exist".format(args.test_name),
                    file=sys.stderr)
    except OSError:
        print("Error: File: {} doesn't exist".format(args.image_file),
              file=sys.stderr)

def fudge_main(args):
    """ """
    parser = argparse.ArgumentParser(description=description())
    raise NotImplementedError

def main(args=None):
    """ """
    SubCommand = namedtuple('SubCommand', ['command', 'description', 'action'])
    sub_commands = (SubCommand('test', 'run test functions', test_main),
                    SubCommand('fudge', 'Fudge an image', fudge_main))

    if args is None:
        if (sys.argv[1] == "-h") or (sys.argv[1] == "--help"):
            print(description())
            print('USAGE:')
            for subcmd in sub_commands:
                print('{sub} \t -- {descript}'.format(sub=subcmd.command, descript=subcmd.description))
            sys.exit(1)
        args = sys.argv[1:]

    parser = argparse.ArgumentParser(description=description())

    subparsers = []
    subparser = parser.add_subparsers()
    subparser.required = True

    for subcmd in sub_commands:
        subparsers.append(subparser.add_parser(subcmd.command).set_defaults(which=subcmd.command))

    try:
        parsed_arg = parser.parse_args([args[0]])

        found_flag = False
        for subcmd in sub_commands:
            if parsed_arg.which == subcmd.command:
                subcmd.action(args[1:])
                found_flag = True

        if found_flag is False:
            print("First argument: {} doesn't match official commands: {}".format(parsed_arg.which,
                                                                                  ' '.join([subcmd.command for subcmd in sub_commands])),
                  file=sys.stderr)

    except IndexError:
        print("First argument required ({})".format(' '.join([subcmd.command for subcmd in sub_commands])),
              file=sys.stderr)

if __name__ == '__main__':
    main()
