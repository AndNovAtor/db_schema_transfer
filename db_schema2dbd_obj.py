import sqlite3

import ddl_classes


def _load_db(cursor):
    results = []
    if cursor.__class__ != sqlite3.Cursor:
        return []
    results.append(cursor.execute("""
                                   select
                                     dbd$domains.id,
                                     dbd$domains.name,
                                     dbd$domains.description,
                                     dbd$data_types.type_id,
                                     dbd$domains.length,
                                     dbd$domains.char_length,
                                     dbd$domains.width,
                                     dbd$domains.align,
                                     dbd$domains.precision,
                                     dbd$domains.scale,
                                     dbd$domains.summable,
                                     dbd$domains.show_null,
                                     dbd$domains.show_lead_nulls,
                                     dbd$domains.thousands_separator,
                                     dbd$domains.case_sensitive "case_sensitive"
                                   from dbd$domains
                                     inner join dbd$data_types on dbd$domains.data_type_id = dbd$data_types.id
                                   order by dbd$domains.id
                                   """).fetchall())
    results.append(cursor.execute("""
                                   select
                                     dbd$tables.id
                                     dbd$tables.name
                                     dbd$tables.description
                                     dbd$data_types.type_id
                                     dbd$tables.length
                                     dbd$tables.char_length
                                     dbd$tables.precision
                                     dbd$tables.scale
                                     dbd$tables.width
                                     dbd$tables.align
                                     dbd$tables.show_null
                                     dbd$tables.show_lead_nulls
                                     dbd$tables.thousands_separator
                                     dbd$tables.summable
                                     dbd$tables.case_sensitive
                                   from dbd$tables
                                     inner join dbd$data_types on dbd$tables.data_type_id = dbd$data_types.type_id
                                   """).fetchall())
    results.append()
    results.append()
    results.append()


def _get_domains(cursor, domains, un_domains, domains_map_dict):
    if cursor.__class__ != sqlite3.Cursor:
        return
    domains_tuples_tuple = cursor.execute("""
                                          select
                                            dbd$domains.id,
                                            dbd$domains.name,
                                            dbd$domains.description,
                                            dbd$data_types.type_id,
                                            dbd$domains.length,
                                            dbd$domains.char_length,
                                            dbd$domains.width,
                                            dbd$domains.align,
                                            dbd$domains.precision,
                                            dbd$domains.scale,
                                            dbd$domains.summable,
                                            dbd$domains.show_null,
                                            dbd$domains.show_lead_nulls,
                                            dbd$domains.thousands_separator,
                                            dbd$domains.case_sensitive "case_sensitive"
                                          from dbd$domains
                                            inner join dbd$data_types on dbd$domains.data_type_id = dbd$data_types.id
                                          order by dbd$domains.id
                                          """).fetchall()
    for domain_row in domains_tuples_tuple: 
        domain = ddl_classes.Domain()
        domain.name = domain_row[1]
        domain.description = domain_row[2]
        domain.type = domain_row[3]
        if domain_row[4] is not None:
            domain.length = int(domain_row[4])
        if domain_row[5] is not None:
            domain.char_length = int(domain_row[5])
        if domain_row[6] is not None:
            domain.width = int(domain_row[6])
        domain.align = domain_row[7]
        if domain_row[8] is not None:
            domain.precision = int(domain_row[8])
        if domain_row[9] is not None:
            domain.scale = int(domain_row[9])
        props_lst = []
        if (domain_row[10] is not None) and (domain_row[10] == 1):
            props_lst.append("summable")
        if (domain_row[11] is not None) and (domain_row[11] == 1):
            props_lst.append("show_null")
        if (domain_row[12] is not None) and (domain_row[12] == 1):
            props_lst.append("show_lead_nulls")
        if (domain_row[13] is not None) and (domain_row[13] == 1):
            props_lst.append("thousands_separator")
        if (domain_row[14] is not None) and (domain_row[14] == 1):
            props_lst.append("case_sensitive")
        domain.props = ", ".join(props_lst)
        if domain_row[1] is not None:
            domains.append(domain)
        else:
            un_domains.append(domain)
        domains_map_dict[domain_row[0]] = domain


def _get_tables(cursor, tables, tables_map_dict):
    if cursor.__class__ != sqlite3.Cursor:
        return ""
    tables_tuples_tuple = cursor.execute("""
                                         select
                                           dbd$tables.id,
                                           dbd$schemas.name "schema_name",
                                           dbd$tables.name "table_name",
                                           dbd$tables.description,
                                           dbd$tables.means,
                                           dbd$tables.can_add,
                                           dbd$tables.can_edit,
                                           dbd$tables.can_delete,
                                           dbd$tables.temporal_mode
                                         from dbd$tables
                                           inner join dbd$schemas on dbd$tables.schema_id = dbd$schemas.id
                                         order by dbd$tables.id
                                         """).fetchall()
    for table_row in tables_tuples_tuple:
        table = ddl_classes.Table()
        table.name = table_row[2]
        table.description = table_row[3]
        table.means = table_row[4]
        props_lst = []
        if (table_row[5] is not None) and (table_row[5] == 1):
            props_lst.append("add")
        if (table_row[6] is not None) and (table_row[6] == 1):
            props_lst.append("edit")
        if (table_row[7] is not None) and (table_row[7] == 1):
            props_lst.append("delete")
        table.props = ", ".join(props_lst)
        # table.temporal_mode = table_row[8]
        tables.append(table)
        tables_map_dict[table_row[0]] = table
    return tables_tuples_tuple[0][1]  # Return schema name


def _get_fields(cursor, tables_map_dict, domains_map_dict, fields_map_dict):
    if cursor.__class__ != sqlite3.Cursor:
        return
    fields_tuples_tuple = cursor.execute("""
                                         select
                                           dbd$fields.id
                                           dbd$fields.table_id
                                           dbd$fields.position
                                           dbd$fields.name
                                           dbd$fields.russian_short_name
                                           dbd$fields.description
                                           dbd$fields.domain_id
                                           dbd$fields.can_input
                                           dbd$fields.can_edit
                                           dbd$fields.show_in_grid
                                           dbd$fields.show_in_details
                                           dbd$fields.is_mean
                                           dbd$fields.autocalculated
                                           dbd$fields.required
                                         from dbd$fields
                                         order by dbd$fields.position
                                         """).fetchall()
    for field_row in fields_tuples_tuple:
        field = ddl_classes.Field()
        field.name = field_row[3]
        field.rname = field_row[4]
        field.description = field_row[5]
        props_lst = []
        if (field_row[7] is not None) and (field_row[7] == 1):
            props_lst.append("input")
        if (field_row[8] is not None) and (field_row[8] == 1):
            props_lst.append("edit")
        if (field_row[9] is not None) and (field_row[9] == 1):
            props_lst.append("delete")
        if (field_row[10] is not None) and (field_row[10] == 1):
            props_lst.append("show_in_grid")
        if (field_row[11] is not None) and (field_row[11] == 1):
            props_lst.append("show_in_details")
        if (field_row[12] is not None) and (field_row[12] == 1):
            props_lst.append("is_mean")
        if (field_row[13] is not None) and (field_row[13] == 1):
            props_lst.append("autocalculated")
        if (field_row[14] is not None) and (field_row[14] == 1):
            props_lst.append("required")
        field.props = ", ".join(props_lst)
        field.set_domain(domains_map_dict[field_row[6]])
        fields_map_dict[field_row[0]] = field
        tables_map_dict[field_row[1]].append_field(field)


def _get_constraints(cursor, tables_map_dict, constraints_map_dict):
    if cursor.__class__ != sqlite3.Cursor:
        return
    fields_tuples_tuple = cursor.execute("""
                                         select
                                           constraints_t.id "constraint_id",
                                           constraints_t.constraint_type "constraint_type",
                                           dbd$constraint_details.position "position",
                                           dbd$constraint_details.field_id,
                                           dbd$tables.name "table_name",
                                           dbd$fields.name "field_name"
                                         from
                                           dbd$constraints constraints_t
                                           inner join dbd$constraints const_ref
                                             on constraints_t.unique_key_id = const_ref.id
                                           inner join dbd$constraint_details
                                             on dbd$constraint_details.constraint_id = constraints_t.id
                                           inner join dbd$tables on constraints_t.table_id = dbd$tables.id
                                           left join dbd$fields on dbd$constraint_details.field_id = dbd$fields.id
                                         order by
                                           position
                                         """).fetchall()
    for field_row in fields_tuples_tuple:
        field = ddl_classes.Field()
        field.name = field_row[3]
        field.rname = field_row[4]
        field.description = field_row[5]
        props_lst = []
        if (field_row[7] is not None) and (field_row[7] == 1):
            props_lst.append("input")
        if (field_row[8] is not None) and (field_row[8] == 1):
            props_lst.append("edit")
        if (field_row[9] is not None) and (field_row[9] == 1):
            props_lst.append("delete")
        if (field_row[10] is not None) and (field_row[10] == 1):
            props_lst.append("show_in_grid")
        if (field_row[11] is not None) and (field_row[11] == 1):
            props_lst.append("show_in_details")
        if (field_row[12] is not None) and (field_row[12] == 1):
            props_lst.append("is_mean")
        if (field_row[13] is not None) and (field_row[13] == 1):
            props_lst.append("autocalculated")
        if (field_row[14] is not None) and (field_row[14] == 1):
            props_lst.append("required")
        field.props = ", ".join(props_lst)
        field.set_domain(domains_map_dict[field_row[6]])
        fields_map_dict[field_row[0]] = field
        tables_map_dict[field_row[1]].append_field(field)


def _get_indices(cursor, indices, indices_map_dict):
    if cursor.__class__ != sqlite3.Cursor:
        return


def get_db_schema(file_path):
    con = sqlite3.connect(file_path)
    cur = con.cursor()
    domains_lst = []
    un_domains_lst = []
    # fields_lst = []
    tables_lst = []
    constraints_lst = []
    indices_lst = []
    schemas_lst = []
    domains_map = {}
    fields_map = {}
    tables_map = {}
    constraints_map = {}
    indices_map = {}
    _get_domains(cur, domains_lst, un_domains_lst, domains_map)
    schema_name = _get_tables(cur, tables_lst, tables_map)
    _get_fields(cur, tables_map, domains_map, fields_map)


