import argparse
from os.path import isfile

from dbd_object2db_schema import SchemaToSqliteDb
from xml2dbd_object import XmlSchemaParsing


def parse_xml(xml_path):
    if not isfile(xml_path):
        print("Error! Get xml file path:", xml_path)
        print("This file does not exist")
    else:
        schema_parse_obj = XmlSchemaParsing().init_from_xml(xml_path)
        if schema_parse_obj is not None:
            if SchemaToSqliteDb(xml_path, schema_parse_obj.schema).create_schema_db():
                print("All successful")
        else:
            print("Schema was not created")

parser = argparse.ArgumentParser()
parser.add_argument("-x2sq", "--xmltosqlite",
                    help="filepath to db schema xml file that will be parse into sqlite database file "
                         "(currently - into '.db' file) with same location and name", metavar='xml_path')
parser.add_argument("-sq2x", "--sqlitetoxml",
                    help="filepath to db schema in sqlite db-file that will be parse into xml file",
                    metavar='sqlite_db_to_xml_path')
args = parser.parse_args()
if args.xmltosqlite:
    parse_xml(args.xmltosqlite)
if args.sqlitetoxml:
    pass #  parse_sq_db2xml(args.sqlitetoxml)
else:
    print("No arguments")
    parser.print_help()
