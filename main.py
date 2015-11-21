from os.path import splitext
import uuid
import xml.etree.ElementTree as ElTr
import errno
import ddl_classes
from dbd_const import SQL_DBD_Init
import sqlite3
from os import remove

__author__ = 'NovAtor'


xml_path = "D:/parsedbd.xml"


xmlTree = ElTr.parse(xml_path)
xmlroot = xmlTree.getroot()


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
        domain_obj.description = domain_el.get("description")
        domain_obj.type = domain_el.get("type")
        # if types.__class__.__name__ == "dict":
        #     if domain_obj.type is not None:
        #             types.setdefault(domain_obj.type)
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

        domains.append(domain_obj)
    return dom_num


def xstr(string):
    return str(string) if string is not None else ""


def parse_tables(root, in_tables, domains, unnamed_domains, t_schema=None):
    table_num = 0
    for table_el in root.find("tables"):
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

        for field_dict in table_el.findall("field"):
            field = ddl_classes.Field()

            field.name = field_dict.get("name", "")
            field.rname = field_dict.get("rname", "")
            field.domain_name = field_dict.get("domain", "")
            if field.domain_name == "":
                un_domain_obj = ddl_classes.Domain()
                un_domain_obj.name = field_dict.get("domain.name", "")
                un_domain_obj.type = field_dict.get("domain.type", "")
                un_domain_obj.description = field_dict.get("domain.description", "")
                un_domain_obj.align = field_dict.get("domain.align", "L")
                un_domain_obj.width = field_dict.get("domain.width")
                if un_domain_obj.width is not None:
                    un_domain_obj.width = int(un_domain_obj.width )
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
                if un_domain_obj.name is None:
                    un_domain_obj.name = un_domain_obj.type + "[prec='" + xstr(un_domain_obj.precision) + "'len='"\
                                + xstr(un_domain_obj.length) + "'scale='" + xstr(un_domain_obj.scale) + "']"
                same_domain = next((item for item in unnamed_domains if un_domain_obj.eq(item)), None)
                if same_domain is not None:
                    field.domain_name = same_domain.name
                    field.domain = same_domain
                else:
                    unnamed_domains.append(un_domain_obj)
                    field.domain_name = un_domain_obj.name
                    field.domain = un_domain_obj
            else:
                field.domain = next((d for d in domains if d.name == field.domain_name), None)
            field.description = field_dict.get("description", "")
            field.props = field_dict.get("props", "")

            table_obj.append_field(field)
        in_tables.append(table_obj)
    return table_num


def parse_tables_other(root, in_tables):
    i = 0
    con_num = 0
    ind_num = 0
    for table_el in root.find("tables"):
        table_obj = in_tables[i]
        for constraint_el in table_el.findall("constraint"):
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
                    ref_table = next((t for t in in_tables if t.name == ref_t_name), None)
                    if ref_table is None:
                        #    !!!  This error situation, so - incorrect xml!!!
                        print("Reference table for last constraint (on the field '", items_field.name, "', in table '",
                              table_obj.name, "') does not exist (a reference of table '", ref_t_name,
                              "' does not exist in input xml file).", sep="")
                        # table_obj.fr_constraints.append(ddl_classes.ForConstraint(items_field, None,
                        #                                                          con_props, con_name))
                    else:
                        table_obj.fr_constraints.append(ddl_classes.ForConstraint(items_field, ref_table,
                                                                                  con_props, con_name))
                else:
                    if con_kind == "CHECK":
                        table_obj.ch_constraint.append(ddl_classes.CheckConstraint(constraint_el.get("reference"),
                                                                                   con_props, con_name),)
                    else:
                        print("Incorrect constraint")
        for index in table_el.findall("index"):
            ind_num += 0
            table_obj.indices.append(ddl_classes.Index(table_obj.fields[index.get("field")], index.get("props", ""),
                                                       index.get("expression")))
        # ++i
        i += 1
    return [con_num, ind_num]


domain_lst = []
unnamed_domains_lst = []
domains_num = parse_domains(xmlroot, domain_lst)
tables_lst = []
tables_num = parse_tables(xmlroot, tables_lst, domain_lst, unnamed_domains_lst)
con_ind_num = parse_tables_other(xmlroot, tables_lst)


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
# con.isolation_level = "IMMEDIATE"
cur.executescript(SQL_DBD_Init)
print("Empty db-file was successfully created.")
cur.execute("""create temporary table domains_tmp (do_n,do_d,ty_name,do_l,do_c_l,do_pr,
                 do_sc,do_w,do_al,do_sn,do_sln,do_ts,do_sum,do_cs,do_uuid);""")
for domain in domain_lst+unnamed_domains_lst:
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
cur.executescript("""BEGIN;
                  insert into dbd$domains select null, d.do_n, d.do_d, t.id, d.do_l, d.do_c_l, d.do_pr,
                  d.do_sc, d.do_w, d.do_al, d.do_sn, d.do_sln, d.do_ts, d.do_sum, d.do_cs, d.do_uuid
                  from domains_tmp d inner join dbd$data_types t on d.ty_name = t.type_id;

                  DROP table domains_tmp;
                  COMMIT;""")
con.commit()
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
cur.executescript("""create temporary table fields_tmp (t_name, fi_pos, fi_n, fi_rn, fi_d,d_name, fi_ci, fi_ce, fi_sig,
                       fi_sid, fi_im, fi_ac, fi_req, fi_uuid);
                     create temporary table constraints_tmp (c_id,c_t_name,c_n,c_t,c_ref_t_n, c_hve,c_cd,c_exp,c_uuid);
                     create temporary table con_details_tmp (cd_c_id, cd_pos, f_name);
                     create temporary table indices_tmp (ind_id, ind_t_name, ind_name, ind_loc, ind_kind, ind_uuid);
                     create temporary table ind_details_tmp (ind_d_ind_id, ind_d_pos, ind_d_f_name,
                       ind_d_expr,ind_d_desc);""")
c_id = cur.execute("SELECT seq from sqlite_sequence where name = 'dbd$constraints'").fetchone()
cur.execute("UPDATE sqlite_sequence set seq = seq + ? where name = 'dbd$constraints'", (con_ind_num[0],)).fetchone()
con.commit()
in_id = cur.execute("SELECT seq from sqlite_sequence where name = 'dbd$indices'").fetchone()
cur.execute("UPDATE sqlite_sequence set seq = seq + ? where name = 'dbd$indices'", (con_ind_num[1],)).fetchone()
con.commit()


def init_id_from_seq(seq_result):
    if seq_result is not None:
        return seq_result[0]
    else:
        return 0

c_id = init_id_from_seq(c_id)
in_id = init_id_from_seq(in_id)

cur.execute("BEGIN;")
for table in tables_lst:
    f_pos = 0
    con_pos = 0
    ind_pos = 0
    t_name = table.name
    for fld_name, fld_obj in table.fields.items():
        f_pos += 1
        f_name = fld_name
        f_rname = fld_obj.rname
        f_description = fld_obj.description
        f_d_name = fld_obj.domain_name
        f_can_input = ("input" in fld_obj.props)
        f_can_edit = ("edit" in fld_obj.props)
        f_sh_in_grid = ("show_in_grid" in fld_obj.props)
        f_sh_in_det = ("show_in_details" in fld_obj.props)
        f_is_mean = ("is_mean" in fld_obj.props)
        f_au_calc = ("autocalculated" in fld_obj.props)
        f_required = ("required" in fld_obj.props)
        f_uuid = uuid.uuid4().hex
        cur.execute("insert into fields_tmp values (?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (t_name, f_pos, f_name, f_rname,
                    f_description, f_d_name, f_can_input, f_can_edit, f_sh_in_grid, f_sh_in_det, f_is_mean,
                    f_au_calc, f_required, f_uuid))

    t_constraints = [table.pr_constraint] + table.fr_constraints + [table.ch_constraint]
    for t_constraint in t_constraints:
        if t_constraint is not None:
            c_id += 1
            c_name = t_constraint.name
            c_type = t_constraint.const_type
            c_ref_t_n = getattr(t_constraint, "ref_name", None)
            c_has_v_ed = ("has_value_edit" in getattr(t_constraint, "props", ""))
            if c_type == "FOREIGN":
                c_cas_del = ("cascading_delete" in t_constraint.props)
            else:
                c_cas_del = None
            c_expr = getattr(t_constraint, "expression", None)
            c_uuid = uuid.uuid4().hex
            cur.execute("insert into constraints_tmp values (?,?,?,?,?,?,?,?,?);", (c_id, t_name, c_name, c_type,
                        c_ref_t_n, c_has_v_ed, c_cas_del, c_expr, c_uuid))
            con_pos += 1
            con_f_name = t_constraint.item_name
            cur.execute("insert into con_details_tmp values (?,?,?);", (c_id, con_pos, con_f_name))
    t_indices = table.indices
    for t_index in t_indices:
        in_id += 1
        in_name = t_index.name
        in_loc = ("local" in t_index.props)
        in_kind = next((x for x in ("uniqueness", " fulltext", " simple") if x in t_index.props.lower()), "simple")
        in_uuid = uuid.uuid4().hex
        cur.execute("insert into indices_tmp values (?,?,?,?,?,?);", (in_id, t_name, in_name, in_loc, in_kind, in_uuid))
        ind_pos += 1
        in_f_name = t_index.field_name
        in_expr = t_index.expression
        in_desc = ("descend" in t_index.props)
        cur.execute("insert into ind_details_tmp values (?,?,?,?,?);", (in_id, ind_pos, in_f_name, in_expr, in_desc))

cur.executescript("""BEGIN;
                     insert into dbd$fields select null, t.id, fi_pos, fi_n, fi_rn,
                     fi_d, d.id, fi_ci, fi_ce, fi_sig, fi_sid, fi_im, fi_ac, fi_req, fi_uuid
                     from (fields_tmp f inner join dbd$tables t on f.t_name = t.name)
                     inner join dbd$domains d on f.d_name = d.name;

                     insert into dbd$constraints select con.c_id, t.id, con.c_n, con.c_t, ca.c_id, con.c_hve,
                       con.c_cd, con.c_exp, con.c_uuid
                       from (constraints_tmp con inner join (select c_id,c_t_name from constraints_tmp
                       where c_t="PRIMARY") ca on con.c_ref_t_n=ca.c_t_name)
                       inner join dbd$tables t on con.c_t_name=t.name;

                     insert into dbd$constraint_details select null, cd.cd_c_id, cd.cd_pos, f.id
                       from con_details_tmp cd inner join dbd$fields f on cd.f_name = f.name;

                     insert into dbd$indices select i.ind_id, t.name, i.ind_name, i.ind_loc, i.ind_kind, i.ind_uuid
                       from indices_tmp i inner join dbd$tables t on i.ind_t_name=t.name;

                     insert into dbd$index_details select null, id.ind_d_ind_id, id.ind_d_pos, f.id,
                       id.ind_d_expr, id.ind_d_desc
                       from ind_details_tmp id inner join dbd$fields f on id.ind_d_f_name = f.name;

                     DROP TABLE fields_tmp;
                     DROP TABLE constraints_tmp;
                     DROP TABLE con_details_tmp;
                     DROP TABLE indices_tmp;
                     DROP TABLE ind_details_tmp;

                     COMMIT;""")
con.commit()

print("Db-file update code executed successfully.")
