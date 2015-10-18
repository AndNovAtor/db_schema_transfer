import ddl_classes

__author__ = 'NovAtor'
# from socket import gethostname
# import xml.dom.minidom
# import xml.dom
import xml.etree.ElementTree as ET
import sqlite3
import xml.etree
# from platform import system


# def less(path):
#     file = open(path)
#     for line in file:
#         print(line, end="")
#     print()
#     file.close()
#     # print("Ok")

# less
#
# if system() == "Linux":
#     dropPath = "/home/novator/Dropbox/"
# else:
#     dropPath = "D:/Dropbox/" if (gethostname() == "NovAtor-ПК") else "C:/Users/NovAtor/Dropbox/"
# xmlPath = dropPath + "Programming/Python/20150221-093102/prjadm.xml"
# dom1 = xml.dom.minidom.parse(xmlPath)
# dom1 = xml.dom.minidom.parse("parme.xml")
# dom1.normalize()

# xmlTree = ET.parse(xmlPath)
xmlTree = ET.parse("parseddl.xml")
xmlRoot = xmlTree.getroot()
# print(xmlRoot.tag)


# def output_tree_dom(node, level=0):
#     if node.nodeType == node.TEXT_NODE:
#         node_name = node.nodeValue.strip()
#         if node_name != "":
#             print("-" * level, node.nodeValue.strip())
#             node_name.upper()
#             """if node_name == "DOMAINS":
#                 node_list"""
#
#     else:  # ELEMENT_NODE или DOCUMENT_NODE
#         atts = node.attributes or {}
#         att_string = ", ".join(
#             ["{}={}".format(k, v) for k, v in atts.items()])
#         print("." * level, node.nodeName, att_string)
#         for child2 in node.childNodes:
#             output_tree_dom(child2, level + 1)


# def print_xml_tree(node, ch='.'):
#      if (ET.iselement(node)):
#
#      print(ch, node.tag)
# output_tree_dom(dom1)
def print_xml_tree(node, level=0):
    print("." * level, node.tag, ": ", node.attrib)
    for tagChild in node.findall("./*"):
        print_xml_tree(tagChild, level + 1)


# print()
# a = {"Domains": 2}
# print(a)
# print(a.items())
# print(dom1.getElementsByTagName("tables").item(0).firstChild.nodeName)
# print(dom1.getElementsByTagName("tables").item(0).nodeName)
# print()
# for child in xmlRoot:
#     print(child.tag, " : ", child.attrib)
#     for childChild in child:
#         print("  ", childChild.tag, " : ", childChild.attrib)

# """Real print - all (create_xml_objs qurcivy)"""
# for chi in xmlRoot.iter():
#     print(chi.tag, " : ", chi.attrib)

print(xmlRoot[0].tag)
for chi1 in xmlRoot.findall("./*"):
    print(chi1.tag)
print(list(xmlRoot))
print_xml_tree(xmlRoot)
# mylist = ["a", "b", "c"]
# mylist.append("z")
# # for el in l:
# #     print(el)
# print(mylist)

domain_lst = []


def parse_domains(root, domains):
    dom_num = 0
    # domains = []
    for domain_dict in root.find("domains"):
        dom_num += 1
        # print(" attr-s:", ["{}={}, ".format(k, v) for k, v in domain.attrib.items()])
        domain = ddl_classes.Domain()

        domain.name = domain_dict.get("name", "")
        # TODO Использование .pop() изменит объект снаружи, однако это уменшит поиск, в теории. Нужно ли заменить?
        domain.description = domain_dict.get("description", "")
        domain.type = domain_dict.get("type", "")
        domain.align = domain_dict.get("align", "")
        domain.width = int(domain_dict.get("width", 0))
        domain.precision = domain_dict.get("precision", 0)
        domain.props = domain_dict.get("props", "")
        domain.char_length = int(domain_dict.get("char_length", 0))

        domains.append(domain)
    return dom_num


def parse_tables(root, in_tables, domains):
    tabl_num = 0
    for table in root.find("tables"):
        tabl_num += 1
        table_obj = ddl_classes.Table()

        table_obj.name = table.get("name", "")
        table_obj.description = table.get("description", "")
        table_obj.props = table.get("props", "")
        table_obj.ht_table_flags = table.get("ht_table_flags", "")
        table_obj.fields = []
        table_obj.pr_constraint = None
        table_obj.fr_constraints = []

        for field_dict in table:
            field = ddl_classes.Field()

            field.name = field_dict.get("name", "")
            field.rname = field_dict.get("rname", "")
            field.domain_name = field_dict.get("domain", "")
            field.description = field_dict.get("description", "")
            field.props = field_dict.get("props", "")
            # TODO: domain = "{}"d for d in domain_list if d.name==self.domain_name]
            for node in domains:
                if node.name == field.domain_name:
                    field.domain = node
                    break

            table_obj.append_field(field)
        in_tables.append(table_obj)
    return tabl_num


# def parse_tables_fields(root, table, domains): #, tables_num):
#     iteration = 0
#     for table in root.find("tables"):
#         for field in table.find("field"):
#             table.append_field(ddl_classes.Field(field.attr, domains))
#         iteration += 1

def parse_tables_other(root, in_tables):
    for table in root.find("tables"):
        for constraint in table.find("constraint"):
            if constraint.get("kind", "") == "PRIMARY":
                la = {}
            else:
                if constraint.get("kind", "") == "FOREIGN":
                    lald = {}
                else:
                    dldld = {}

domain_lst = []
domains_num = parse_domains(xmlRoot, domain_lst)
tables = []
tables_num = parse_tables(xmlRoot, tables, domain_lst)
lala = []
# parse_tables_other(xmlRoot, tables)
# print(xmlRoot[0].tag, xmlRoot[0].attrib, xmlRoot[1].text.strip(), '3')
# print(xmlRoot[1][0].tag, xmlRoot[1][0].attrib, xmlRoot[1][0].text, '3')
# print(domain_lst)
con = sqlite3.connect("temp.db")
cur = con.cursor()
cur.executescript("""
    create table person(
        firstname,
        lastname,
        age
    );

    create table book(
        title,
        author,
        published
    );

    insert into book(title, author, published)
    values (
        'Dirk Gently''s Holistic Detective Agency',
        'Douglas Adams',
        1987
    );
    """)