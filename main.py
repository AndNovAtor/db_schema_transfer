from os.path import splitext
import uuid
import xml.etree.ElementTree as ElTr
import errno
import ddl_classes
from dbd_const import SQL_DBD_Init
import sqlite3
from os import remove

__author__ = 'NovAtor'
# from platform import system

#
# if system() == "Linux":
#     dropPath = "/home/novator/Dropbox/"
# else:
#     dropPath = "D:/Dropbox/" if (gethostname() == "NovAtor-ПК") else "C:/Users/NovAtor/Dropbox/"
# xmlPath = dropPath + "Programming/Python/20150221-093102/prjadm.xml"
xml_path = "parsedbd.xml"
xmlTree = ElTr.parse(xml_path)
xmlRoot = xmlTree.getroot()


# Next - debug function, but i still keep it
def print_xml_tree(node, level=0):
    print("." * level, node.tag, ": ", node.attrib)
    for tagChild in node.findall("./*"):
        print_xml_tree(tagChild, level + 1)


def parse_domains(root, domains, types=None):
    dom_num = 0
    # domains = []
    for domain_el in root.find("domains"):
        dom_num += 1
        # print(" attr-s:", ["{}={}, ".format(k, v) for k, v in domain.attrib.items()])
        domain_obj = ddl_classes.Domain()
        #
        #       !!! Bellow use constraint.get("kind", ""), but type of constraint - not dict. It's Element (etree)
        #       If want to use constraint["kind"] style, needed constraint.attrib["kind"] or changing loop with .attrib
        #
        domain_obj.name = domain_el.get("name")
        # TODO Использование .pop() изменит объект снаружи, однако это уменшит поиск, в теории. Нужно ли заменить?
        domain_obj.description = domain_el.get("description")
        domain_obj.type = domain_el.get("type")
        if types.__class__.__name__ == "dict":
            if domain_obj.type is not None:
                    types.setdefault(domain_obj.type)
        domain_obj.align = domain_el.get("align", "L")
        domain_obj.width = domain_el.get("width")
        if domain_obj.width is not None:
            domain_obj.width = int(domain_obj.width)
        domain_obj.precision = domain_el.get("precision")
        domain_obj.props = domain_el.get("props", "")
        domain_obj.char_length = domain_el.get("char_length")
        if domain_obj.char_length is not None:
            domain_obj.char_length = int(domain_obj.char_length)
        domain_obj.length = domain_el.get("length")
        if domain_obj.length is not None:
            domain_obj.length = int(domain_el.get("length"))
        domain_obj.scale = domain_el.get("scale")
        if domain_obj.scale is not None:
            domain_obj.scale = int(domain_el.get("scale"))

        domains.append(domain_obj)
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
        table_obj.temporal_mode = table.get("temporal_mode", None)
        table_obj.means = table.get("means", None)
        table_obj.fields = {}
        table_obj.pr_constraint = None
        table_obj.fr_constraints = []
        table_obj.indexes = []

        for field_dict in table.findall("field"):
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


def parse_tables_other(root, in_tables):
    i = 0
    for table in root.find("tables"):
        table_obj = in_tables[i]
        for constraint in table.findall("constraint"):
            items_field = table_obj.fields[constraint.get("items")]
            if constraint.get("kind", "") == "PRIMARY":
                table_obj.pr_constraint = ddl_classes.PrConstraint(items_field)
            else:
                if constraint.get("kind", "") == "FOREIGN":
                    ref_table = next((t for t in in_tables if t.name == constraint.get("reference")), None)
                    if ref_table is None:
                        # !!!!!!!!!!!!!!!!!!!!!!!!!!!! ERROR HERE !!!!!!!!!!!!!!!
                        table_obj.fr_constraints.append(ddl_classes.ForConstraint(items_field, None,
                                                                                  constraint.get("props", "")))
                    else:
                        table_obj.fr_constraints.append(ddl_classes.ForConstraint(items_field, ref_table,
                                                                                  constraint.get("props", "")))
                        # else:
                        #     print("Incorrect constraint")
        for index in table.findall("index"):
            table_obj.indexes.append(ddl_classes.Index(table_obj.fields[index.get("field")], index.get("props")))
        # ++i
        i += 1


domain_lst = []
# types_dict = {}
domains_num = parse_domains(xmlRoot, domain_lst)
tables_lst = []
tables_num = parse_tables(xmlRoot, tables_lst, domain_lst)
parse_tables_other(xmlRoot, tables_lst)


def silentrem(filename):
    try:
        remove(filename)
    except OSError as e:  # this would be "except OSError, e:" before Python 2.6
        if e.errno != errno.ENOENT:  # errno.ENOENT = no such file or directory
            raise  # re-raise exception if a different error occurred

db_path = splitext(xml_path)[0]+".db"
silentrem(db_path)
con = sqlite3.connect(db_path)
cur = con.cursor()
cur.executescript(SQL_DBD_Init)
print("Empty db-file was successfully created.")
cur.execute("create temporary table domains_tmp (b,c,t_name,e,f,g,h,i,j,k,l,m,n,o,p);")
for domain in domain_lst:
    d_name = domain.name
    d_description = domain.description
    d_type_name = domain.type
    d_length = domain.length
    d_char_length = domain.char_length
    d_precision = domain.precision
    d_scale = domain.scale
    d_width = domain.width
    d_align = domain.align
    d_show_null = ("show_null" in domain.props)
    d_show_lead_nulls = ("show_lead_nulls" in domain.props)
    d_thousands_separator = ("thousands_separator" in domain.props)
    d_summable = ("summable" in domain.props)
    d_case_sensitive = ("case_sensitive" in domain.props)
    d_uuid = uuid.uuid4().hex
    cur.execute("insert into domains_tmp values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (d_name, d_description,
                d_type_name, d_length, d_char_length, d_precision, d_scale, d_width, d_align, d_show_null,
                d_show_lead_nulls, d_thousands_separator, d_summable, d_case_sensitive, d_uuid))
cur.executescript("""insert into dbd$domains select null, d.b, d.c, t.id, d.e, d.f, d.g,
                  d.h, d.i, d.j, d.k, d.l, d.m, d.n, d.o, d.p
                  from domains_tmp d inner join dbd$data_types t on d.t_name = t.type_id;

                  DROP TABLE domains_tmp;""")
con.commit()
#   Next not supported in sqlite3 (update... set.. FROM)
# cur.execute("update dbd$domains "
#             "set data_type_id = t.id "
#             "from dbd$domains d "
#             "inner join dbd$data_types t "
#             "on d.type_name = t.id ")
#   So...
# cur.execute("""replace into dbd$domains
#             (id, name, description, data_type_id, length, char_length,precision, scale, width, align, show_null,
#             show_lead_nulls, thousands_separator, summable, case_sensitive, uuid, type_name)
#             select d.id, d.name, d.description, t.id, d.length, d.char_length, d.precision,
#             d.scale, d.width, d.align, d.show_null, d.show_lead_nulls, d.thousands_separator,
#             d.summable boolean, d.case_sensitive, d.uuid, d.type_name
#             from dbd$domains d inner join dbd$data_types t on d.type_name = t.id;""")
# cur.execute("ALTER TABLE dbd$domains DROP COLUMN type_name;")
con.commit()
for table in tables_lst:
    t_name = table.name
    t_description = table.description
    t_can_add = ("add" in table.props)
    t_can_edit = ("edit" in table.props)
    t_can_delete = ("delete" in table.props)
    # t_r = ("r" in table.ht_table_flags)
    t_temporal_mode = table.temporal_mode
    t_means = table.means
    t_uuid = uuid.uuid4().hex
    cur.execute("insert into dbd$tables values (Null,Null,?,?,?,?,?,?,?,?);", (t_name, t_description,
                t_can_add, t_can_edit, t_can_delete, t_temporal_mode, t_means, t_uuid,))
con.commit()
# cur.execute("create temporary constraints_tmp table fields_tmp (t_name,a,b,c,d,d_name,f,g,h,i,j,k,l,m);")
# cur.execute("create temporary con_details_tmp table fields_tmp (t_name,a,b,c,d,d_name,f,g,h,i,j,k,l,m);")
# cur.execute("create temporary indices table fields_tmp (t_name,a,b,c,d,d_name,f,g,h,i,j,k,l,m);")
# cur.execute("create temporary ind_details_tmp table fields_tmp (t_name,a,b,c,d,d_name,f,g,h,i,j,k,l,m);")
cur.execute("create table fields_tmp (t_name,a,b,c,d,d_name,g,h,i,j,k,l,m,n);")
for table in tables_lst:
    f_pos = 0
    for fld_name, field in table.fields.items():
        f_pos += 1
        f_name = fld_name
        f_rname = field.rname
        f_description = field.description
        f_d_name = field.domain_name
        f_can_input = ("input" in field.props)
        f_can_edit = ("edit" in field.props)
        f_sh_in_grid = ("show_in_grid" in field.props)
        f_sh_in_det = ("show_in_details" in field.props)
        f_is_mean = ("is_mean" in field.props)
        f_au_calc = ("autocalculated" in field.props)
        f_required = ("required" in field.props)
        f_uuid = uuid.uuid4().hex
        cur.execute("insert into fields_tmp values (?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (t_name, f_pos, f_name, f_rname,
                    f_description, f_d_name, f_can_input, f_can_edit, f_sh_in_grid, f_sh_in_det, f_is_mean,
                    f_au_calc, f_required, f_uuid))
cur.executescript("""insert into dbd$fields select null, t.id, f.a, f.b, f.c,
                  f.d, d.id, f.g, f.h, f.i, f.j, f.k, f.l, f.m, f.n
                  from (fields_tmp f inner join dbd$tables t on f.t_name = t.name)
                  inner join dbd$domains d on f.d_name = d.name;

                  DROP TABLE fields_tmp;""")
con.commit()
# TODO: Сделать разрешение проблемы id для constraint'ов и indexes'ов
# for table in tables_lst:
#     f_pos = 0
#     for field in table.fields:

print("Db-file update code executed successfully.")

