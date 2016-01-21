import xml.etree.ElementTree as ElTr
import ddl_classes

__author__ = 'NovAtor'


# Next - debug function, but i still keep it
def print_xml_tree(node, level=0):
    print("." * level, node.tag, ": ", node.attrib)
    for tagChild in node.findall("./*"):
        print_xml_tree(tagChild, level + 1)


def xstr(string):
    return str(string) if string is not None else ""


def get_xml_root(file_path):
    try:
        xml_tree_el = ElTr.parse(file_path)
    except ElTr.ParseError:
        print("ParseError occurred.")
        print("Input file is invalid xml or not xml. Taken file path:")
        print(file_path)
        print("Error catched in 'get_xml_root' function")
        return None
    except FileNotFoundError:
        print("File not found")
        print("Taken file path:", file_path)
        print("Error catched in 'get_xml_root' function")
        return None
    xml_root_el = xml_tree_el.getroot()
    return xml_root_el


class XmlSchemaParsing:
    def __init__(self, xml_root_el=None, schema_i=None):
        self.schema = schema_i if schema_i.__class__ == ddl_classes.Schema else ddl_classes.Schema()
        self.xml_root = xml_root_el if xml_root_el.__class__ == ElTr.Element else ElTr.Element("")

    def _xml_parse_schema_data(self):
        if (self.schema.__class__ == ddl_classes.Schema) and (self.xml_root is not None):
            self.schema.name = self.xml_root.get("name", "")

    def _xml_parse_domains(self):
        if self.xml_root is not None and type(self.xml_root) == ElTr.Element:
            for domain_el in self.xml_root.find("domains"):
                domain_obj = ddl_classes.Domain()
                #
#                !!! Bellow use constraint.get("kind", ""), but type of constraint - not dict. It's Element (etree)
#                If want to use constraint["kind"] style, needed constraint.attrib["kind"] or changing loop with .attrib
                domain_obj.name = domain_el.get("name")
                domain_obj.description = domain_el.get("description")
                domain_obj.type = domain_el.get("type")
                domain_obj.align = domain_el.get("align", "L")
                domain_obj.width = domain_el.get("width")
                if domain_obj.width is not None:
                    domain_obj.width = int(domain_obj.width)
                domain_obj.length = domain_el.get("length")
                if domain_obj.length is not None:
                    domain_obj.length = int(domain_obj.length)
                domain_obj.precision = domain_el.get("precision")
                domain_obj.props = domain_el.get("props", "")
                domain_obj.char_length = domain_el.get("char_length")
                if domain_obj.char_length is not None:
                    domain_obj.char_length = int(domain_obj.char_length)
                domain_obj.scale = domain_el.get("scale")
                if domain_obj.scale is not None:
                    domain_obj.scale = int(domain_obj.scale)

                self.schema.domains.append(domain_obj)

    def _xml_parse_tables(self):
        table_num = 0
        for table_el in self.xml_root.find("tables"):
            table_num += 1
            table_obj = ddl_classes.Table()

            table_obj.name = table_el.get("name", "")
            table_obj.description = table_el.get("description", "")
            table_obj.props = table_el.get("props", "")
            table_obj.ht_table_flags = table_el.get("ht_table_flags", "")
            table_obj.temporal_mode = table_el.get("temporal_mode", None)
            table_obj.means = table_el.get("means", None)
            table_obj.fields = {}
            table_obj.pr_constraint = None
            table_obj.fr_constraints = []
            table_obj.indices = []
            self.schema.tables.append(table_obj)

    def _xml_parse_table_fields(self):
        table_ind = 0
        for table_el in self.xml_root.find("tables"):
            table_obj = self.schema.tables[table_ind]
            table_field_pos = 0
            for field_dict in table_el.findall("field"):
                field = ddl_classes.Field()

                table_field_pos += 1

                field.name = field_dict.get("name", "")
                field.rname = field_dict.get("rname", "")
                field.domain_name = field_dict.get("domain", "")
                if field.domain_name == "":
                    un_domain_obj = ddl_classes.Domain()
                    un_domain_obj.name = ""
                    # un_domain_obj.name = field_dict.get("domain.name", "")
                    un_domain_obj.type = field_dict.get("domain.type", "")
                    # un_domain_obj.description = field_dict.get("domain.description", "")
                    un_domain_obj.align = field_dict.get("domain.align", "L")
                    un_domain_obj.width = field_dict.get("domain.width")
                    if un_domain_obj.width is not None:
                        un_domain_obj.width = int(un_domain_obj.width)
                    un_domain_obj.precision = field_dict.get("domain.precision")
                    if un_domain_obj.precision is not None:
                        un_domain_obj.precision = int(un_domain_obj.precision)
                    un_domain_obj.length = field_dict.get("domain.length")
                    if un_domain_obj.length is not None:
                        un_domain_obj.length = int(un_domain_obj.length)
                    un_domain_obj.scale = field_dict.get("domain.scale")
                    if un_domain_obj.scale is not None:
                        un_domain_obj.scale = int(un_domain_obj.scale)
                    un_domain_obj.props = field_dict.get("domain.props", "")
                    un_domain_obj.char_length = field_dict.get("domain.char_length")
                    if un_domain_obj.char_length is not None:
                        un_domain_obj.char_length = int(un_domain_obj.char_length)
                    # if un_domain_obj.name is "":
                    #   un_domain_obj.name = un_domain_obj.type + "[prec='" + xstr(un_domain_obj.precision) + "'len='"\
                    #                 + xstr(un_domain_obj.length) + "'scale='" + xstr(un_domain_obj.scale) + "']"

                    # same_domain = next((item for item in self.schema.un_domains if un_domain_obj.eq(item)), None)
                    # if same_domain is not None:
                    #     field.domain_name = same_domain.name
                    #     field.domain = same_domain
                    # else:
                    self.schema.un_domains.append(un_domain_obj)
                    field.domain_name = un_domain_obj.name
                    field.domain = un_domain_obj
                else:
                    field.domain = next((d for d in self.schema.domains if d.name == field.domain_name), None)
                field.description = field_dict.get("description", "")
                field.props = field_dict.get("props", "")
                field.position = table_field_pos

                table_obj.append_field(field)
            table_ind += 1

    def _xml_parse_tables_cons(self):
        i = 0
        con_num = 0
        for table_el in self.xml_root.find("tables"):
            table_obj = self.schema.tables[i]
            for constraint_el in table_el.findall("./constraint"):
                con_num += 1
                items_field = table_obj.fields[constraint_el.get("items")]
                con_kind = constraint_el.get("kind", "")
                con_name = constraint_el.get("name")
                if con_kind == "PRIMARY":
                    table_obj.pr_constraint = ddl_classes.PrConstraint(items_field, con_name)
                else:
                    con_props = constraint_el.get("props", "")
                    ref_t_name = constraint_el.get("reference")
                    if con_kind == "FOREIGN":
                        ref_table = next((t for t in self.schema.tables if t.name == ref_t_name), None)
                        if ref_table is None:
                            #    !!!  This error situation, so - incorrect xml!!!
                            print("Reference table for last constraint (on the field '", items_field.name,
                                  "', in table '", table_obj.name, "') does not exist (a reference of table '",
                                  ref_t_name, "' does not exist in input xml file).", sep="")
                        else:
                            table_obj.fr_constraints.append(ddl_classes.ForConstraint(items_field, ref_table,
                                                                                      con_props, con_name))
                    else:
                        if con_kind == "CHECK":
                            table_obj.ch_constraint.append(ddl_classes.CheckConstraint(constraint_el.get("reference"),
                                                                                       con_props, con_name),)
                        else:
                            print("Incorrect constraint")
            i += 1
        return con_num

    def _xml_parse_tables_indices(self):
        i = 0
        ind_num = 0
        for table_el in self.xml_root.find("tables"):
            table_obj = self.schema.tables[i]
            for index in table_el.findall("./index"):
                            ind_num += 0
                            table_obj.indices.append(ddl_classes.Index(table_obj.fields[index.get("field")],
                                                                       index.get("props", ""), index.get("expression")))
            i += 1
        return ind_num

    def parse_schema(self):
        if self.schema.__class__ == ddl_classes.Schema:
            self._xml_parse_schema_data()
            self._xml_parse_domains()
            self._xml_parse_tables()
            self._xml_parse_table_fields()
            self.schema.con_num = self._xml_parse_tables_cons()
            self.schema.ind_num = self._xml_parse_tables_indices()
        return self

    def init_xml_root(self, file_path):
        self.xml_root = get_xml_root(file_path)
        if (self.xml_root is None) or (len(self.xml_root) < 1):
            print("Input file path:", file_path)
            print("This xml file has no root tag or has root tag without children")
            print("Stop parsing")
            return False
        return True

    def init_from_xml(self, file_path):
        if self.init_xml_root(file_path):
            self.parse_schema()
            return self
        else:
            return None


class XmlSchemaListParsing:
    def __init__(self, xml_root_el=None, schemas_lst=None):
        self.schemas = [s for s in schemas_lst if s.__class__ == ddl_classes.Schema] if schemas_lst is not None else []
        self.xml_root = xml_root_el if xml_root_el.__class__ == ElTr.Element else ElTr.Element("")

    def get_schemas(self):
        return self.schemas

    def init_xml_root(self, file_path):
        self.xml_root = get_xml_root(file_path)
        if (self.xml_root is None) or (len(self.xml_root) < 1):
            print("Input file path:", file_path)
            print("This xml file has no root tag or has root tag without children")
            print("Stop parsing")
            return False
        vir_xml_root = ElTr.Element("dbd_schemas", {"description": "virtual root"})
        if self.xml_root.tag != "dbd_schemas":
            vir_xml_root.append(self.xml_root)
            self.xml_root = vir_xml_root
        return True

    def parse_schemas(self):
        for schema_root in self.xml_root:
            self.schemas.append(XmlSchemaParsing(schema_root).parse_schema().schema)

    def init_from_xml(self, file_path):
        if self.init_xml_root(file_path):
            self.parse_schemas()
        return self
