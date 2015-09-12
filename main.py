import ddl_classes

__author__ = 'NovAtor'
# from socket import gethostname
# import xml.dom.minidom
# import xml.dom
import xml.etree.ElementTree as ET
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


def parse_domains(root):
    dom_num = 0
    domains = []
    for domain in root.find("domains"):
        dom_num += 1
        # print(" attr-s:", ["{}={}, ".format(k, v) for k, v in domain.attrib.items()])
        domains.append(ddl_classes.Domain(domain.attrib))
    return domains


def parse_tables(root):
    tables_num = 0

domain_lst = parse_domains(xmlRoot)
print(xmlRoot[0].tag, xmlRoot[0].attrib, xmlRoot[1].text.strip(), '3')
print(xmlRoot[1][0].tag, xmlRoot[1][0].attrib, xmlRoot[1][0].text, '3')
print(domain_lst)
