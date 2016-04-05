import argparse
from os.path import isfile

from dbd_object2sqlite_schema import SchemaToSqliteDb
from xml2dbd_object import XmlSchemaParsing
from sqlite_schema2dbd_obj import SqliteDbToSchema
from dbd_obj2xml import DbdSchemaToXml


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


def parse_sq_schema(db_path):
    if not isfile(db_path):
        print("Error! Get db file path:", db_path)
        print("This file does not exist")
    else:
        schema_parse_obj = SqliteDbToSchema().get_db_schema(db_path)
        if schema_parse_obj is not None:
            if DbdSchemaToXml(schema_parse_obj.schema, db_path).write_schema():
                print("All successful")
            else:
                print("Xml was not created")
        else:
            print("Schema object was not created was not created")

parser = argparse.ArgumentParser()
parser.add_argument("-x2sq", "--xmltosqlite",
                    help="filepath to db schema xml file that will be parse into sqlite database file "
                         "(currently - into '.db' file) with same location and name", metavar='xml_path')
parser.add_argument("-sq2x", "--sqlitetoxml",
                    help="filepath to db schema in sqlite db-file that will be parse into xml file",
                    metavar='sqlite_db_to_xml_path')
args = parser.parse_args()
was_no_arguments = True
if args.xmltosqlite:
    parse_xml(args.xmltosqlite)
    was_no_arguments = False
if args.sqlitetoxml:
    parse_sq_schema(args.sqlitetoxml)
    was_no_arguments = False
if was_no_arguments:
    print("No arguments")
    parser.print_help()
