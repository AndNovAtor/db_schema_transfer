import argparse

from xml2sqlite import parse_xml

parser = argparse.ArgumentParser()
parser.add_argument("-x2sq", "--xmltosqlite",
                    help="filepath to db schema xml file that will be parse into sqlite database file "
                         "(currently - into '.db' file) with same location and name", metavar='xml_path')
args = parser.parse_args()
if args.xmltosqlite:
    parse_xml(args.xmltosqlite)
else:
    print("No arguments")
    parser.print_help()
