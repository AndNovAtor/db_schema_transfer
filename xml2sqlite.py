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

#  ------------------------------
# # File xml2sqlite.py
# import xmlreader #.py
# import dbaccess  #.py
# def main():
#     try:
#         schema = xmlreader.read("file")
#         #...
#         dbaccess.create_schema(schema)
#     except XMLError as e:
#         win.MessageBOx(e)
#         pass
#     except DBError as e:
#         pass
#     except Exception as e:
#         print("CRITICAL error: " + repr(e))
#
# if __name__ == "__main__"
#     main(args)
#
# # -----------------------------------
# #  File xmlreader.py
# class XMLError(Exception):
#     def __init__(self, filename, message):
#         super(XMLError, self).__init__(message)
#         self.filename = filename
#         pass
#     def __str__(self):
#         pass
#
# # interface
# def read(filename)
#     f = None
#     try:
#         f = File.open(filename)
#     except IOError as e:
#         raise XMLReadError()
#
#
# # implementation
# def _parser()
