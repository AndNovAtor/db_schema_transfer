from os.path import isfile

from dbd_object2db_schema import SchemaToSqliteDb
from xml2dbd_object import XmlSchemaParsing

__author__ = 'NovAtor'


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
