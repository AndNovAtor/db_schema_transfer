import sqlite3

import ddl_classes


class SqliteDbToSchema:
    def __init__(self, db_connection=None, schema_i=None):
        if db_connection.__class__ == sqlite3.Connection:
            self.connection = db_connection
            self.cursor = db_connection.cursor
        else:
            self.connection = None
            self.cursor = None
        self.schema = schema_i

    def init_db_con(self, db_path):
        con = sqlite3.connect(db_path)
        if con.__class__ == sqlite3.Connection:
            self.connection = con
            self.cursor = con.cursor()

    def _load_db(self):
        results = []
        if self.cursor.__class__ != sqlite3.Cursor:
            return []
        results.append(self.cursor.execute("""
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
        results.append(self.cursor.execute("""
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

    def _get_domains(self, domains, un_domains, domains_map_dict):
        if self.cursor.__class__ != sqlite3.Cursor:
            return
        domains_tuples_tuple = self.cursor.execute("""
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

    def _get_tables(self, tables, tables_map_dict):
        if self.cursor.__class__ != sqlite3.Cursor:
            return ""
        tables_tuples_tuple = self.cursor.execute("""
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

    def _get_fields(self, tables_map_dict, domains_map_dict, fields_map_dict):
        if self.cursor.__class__ != sqlite3.Cursor:
            return
        fields_tuples_tuple = self.cursor.execute("""
                                                  select
                                                    dbd$fields.id,
                                                    dbd$fields.table_id,
                                                    dbd$fields.position,
                                                    dbd$fields.name,
                                                    dbd$fields.russian_short_name,
                                                    dbd$fields.description,
                                                    dbd$fields.domain_id,
                                                    dbd$fields.can_input,
                                                    dbd$fields.can_edit,
                                                    dbd$fields.show_in_grid,
                                                    dbd$fields.show_in_details,
                                                    dbd$fields.is_mean,
                                                    dbd$fields.autocalculated,
                                                    dbd$fields.required
                                                  from dbd$fields
                                                  order by dbd$fields.table_id, dbd$fields.position
                                                  """).fetchall()
        for field_row in fields_tuples_tuple:
            field = ddl_classes.Field()
            field.position = field_row
            field.name = field_row[3]
            field.rname = field_row[4]
            field.description = field_row[5]
            props_lst = []
            if (field_row[7] is not None) and (field_row[7] == 1):
                props_lst.append("input")
            if (field_row[8] is not None) and (field_row[8] == 1):
                props_lst.append("edit")
            if (field_row[9] is not None) and (field_row[9] == 1):
                props_lst.append("show_in_grid")
            if (field_row[10] is not None) and (field_row[10] == 1):
                props_lst.append("show_in_details")
            if (field_row[11] is not None) and (field_row[11] == 1):
                props_lst.append("is_mean")
            if (field_row[12] is not None) and (field_row[12] == 1):
                props_lst.append("autocalculated")
            if (field_row[13] is not None) and (field_row[13] == 1):
                props_lst.append("required")
            field.props = ", ".join(props_lst)
            field.set_domain(domains_map_dict[field_row[6]])
            fields_map_dict[field_row[0]] = field
            tables_map_dict[field_row[1]].append_field(field)

    def _get_constraints(self, tables_map_dict, fields_map_dict):
        if self.cursor.__class__ != sqlite3.Cursor:
            return
        constr_tuples_tuple = self.cursor.execute("""
                                                  select
                                                    constraints_t.id "constraint_id",
                                                    constraints_t.name,
                                                    constraints_t.constraint_type "constraint_type",
                                                    dbd$constraint_details.position "position",
                                                    dbd$tables.id "table_id",
                                                    dbd$fields.id "field_id",
                                                    dbd$fields.name "field_name",
                                                    const_ref.table_id "ref_table_id",
                                                    constraints_t.has_value_edit,
                                                    constraints_t.cascading_delete,
                                                    constraints_t.expression
                                                  from
                                                    dbd$constraints constraints_t
                                                    left join dbd$constraint_details
                                                      on dbd$constraint_details.constraint_id = constraints_t.id
                                                    inner join dbd$tables
                                                      on constraints_t.table_id = dbd$tables.id
                                                    left join dbd$fields
                                                      on dbd$constraint_details.field_id=dbd$fields.id
                                                    left join dbd$constraints const_ref
                                                      on constraints_t.unique_key_id = const_ref.id
                                                  order by
                                                    table_id, position
                                                  """).fetchall()
        for constr_row in constr_tuples_tuple:
            constr = None
            if constr_row[2] == "PRIMARY":
                constr = ddl_classes.PrConstraint()
            else:
                if constr_row[2] == "FOREIGN":
                    constr = ddl_classes.ForConstraint()
                    props_lst = []
                    if constr_row[8] == 1:
                        props_lst.append("has_value_edit")
                    if constr_row[9] == 1:
                        props_lst.append("cascading_delete")
                    if props_lst:
                        constr.props = ", ".join(props_lst)
                    constr.reference = fields_map_dict[constr_row[7]]
                    constr.ref_name = constr.reference.name
                else:
                    constr = ddl_classes.CheckConstraint(constr_row[11],)
            constr.name = constr_row[1]
            # if constr_row[2] != "CHECK":
            constr.item = fields_map_dict[constr_row[5]]
            constr.item_name = constr_row[6]
            #
            constr.expression = constr_row[10]
            tables_map_dict[constr_row[4]].append_constraint(constr)
        return len(constr_tuples_tuple)

    def _get_indices(self, tables_map_dict, fields_map_dict):
        if self.cursor.__class__ != sqlite3.Cursor:
            return
        ind_tuples_tuple = self.cursor.execute("""
                                               select
                                                 dbd$indices.id index_id,
                                                 dbd$indices.name index_name,
                                                 dbd$indices.table_id,
                                                 dbd$index_details.position,
                                                 dbd$index_details.field_id,
                                                 dbd$fields.name field_name,
                                                 dbd$indices.kind,
                                                 dbd$indices.local,
                                                 dbd$index_details.descend,
                                                 dbd$index_details.expression
                                               from
                                                 dbd$indices
                                                 inner join dbd$index_details
                                                   on dbd$index_details.index_id = dbd$indices.id
                                                 inner join dbd$tables
                                                   on dbd$indices.table_id = dbd$tables.id
                                                 left join dbd$fields
                                                   on dbd$index_details.field_id = dbd$fields.id
                                               order by
                                                 dbd$tables.name, dbd$index_details.position
                                               """).fetchall()
        for index_row in ind_tuples_tuple:
            index = ddl_classes.Index(None, "", index_row[9], index_row[1])
            props_lst = []
            index.name = index_row[1]
            index.field = fields_map_dict[index_row[4]]
            index.field_name = index_row[5]
            if str.lower(index_row[6]) != "simple":
                props_lst.append("has_value_edit")
            if index_row[7] == 1:
                props_lst.append("local")
            if index_row[8] == 1:
                props_lst.append("descend")
            if props_lst:
                index.props = ", ".join(props_lst)
            index.expression = index_row[9] if index_row[9] is not None else ''
            tables_map_dict[index_row[2]].append_index(index)
        return len(ind_tuples_tuple)

    def get_db_schema(self, file_path):
        self.init_db_con(file_path)
        domains_lst = []
        un_domains_lst = []
        # fields_lst = []
        tables_lst = []
        # schemas_lst = []
        domains_map = {}
        fields_map = {}
        tables_map = {}
        self._get_domains(domains_lst, un_domains_lst, domains_map)
        schema_name = self._get_tables(tables_lst, tables_map)
        self._get_fields(tables_map, domains_map, fields_map)
        constraints_num = self._get_constraints(tables_map, fields_map)
        indices_num = self._get_indices(tables_map, fields_map)
        if domains_lst and tables_lst:
            self.schema = ddl_classes.Schema(domains_lst, un_domains_lst, tables_lst,
                                             constraints_num, indices_num, schema_name)
            return self
        else:
            return None
