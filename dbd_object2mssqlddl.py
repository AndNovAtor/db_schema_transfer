from ddl_classes import *


class SchemaToMssqlDDL:
    def __init__(self, ddl_path_i="", schema_i=None):
        self.ddl_path = ddl_path_i
        self.schema = schema_i
        
    def make_schema(self):
        ddl_string = self.parse_domains()
        ddl_string += self.parse_tables()
        ddl_string += self.parse_for_cons()
        ddl_string += self.parse_check_cons()
        if self.ddl_path:
            with open(self.ddl_path, 'w', encoding='utf-8') as file:
                file.write(ddl_string)
        return ddl_string

    def parse_domains(self):
        ddl_string = ''
        for domain in self.schema.domains:
            ddl_string += "CREATE DOMAIN \"{0}\" as {1};\n".format(
                domain.name,
                self._get_mssql_domain_type(domain)
            )
        return ddl_string

    def _get_mssql_domain_type(self, domain):
        d_type = self._replace_domain(domain.type)
        if domain.char_length != '':
            if type != 'bytea' and type != 'text':
                return "{0}({1})".format(d_type, domain.char_length)
            else:
                return d_type

        else:
            return self._replace_domain(d_type)

    def _replace_domain(self, domain_type):
        return {
            "byte": "smallint",
            "word": "integer",
            "largeint": "bigint",
            "string": "varchar",
            "float": "real",
            "memo": "text",
            "code": "real",
            "blob": "bytea",
            "nvarchar": "varchar",
            "ntext": "text",
            "image": "bytea",
            "datetime": "timestamp",
            "bit": "boolean"
        }.get(domain_type.lower(), domain_type)

    def parse_tables(self):
        ddl_string = ''
        for table in self.schema.tables:
            ddl_string += "CREATE TABLE \"{0}\" ({1}\n);\n{2}\n\n".format(
                table.name,
                self._parse_field(table),
                self._parse_index(table)
            )
        return ddl_string

    def _parse_field(self, table):
        fields_ddl_list = []
        for field in table.fields:
            if field.domain_name is not None:
                fields_ddl_list.append("\n    {0} \"{1}\"".format(
                    field.name,
                    field.domain_name
                ))
            else:
                fields_ddl_list.append("\n    {0} {1}".format(
                    field.name,
                    self._get_mssql_domain_type(field.domain)
                ))
        primary_key_ddl = self._parse_primary_key(table)
        if primary_key_ddl != '':
            fields_ddl_list.append(primary_key_ddl)
        return ", ".join(fields_ddl_list)

    def _parse_primary_key(self, table):
        cons_ddl_lst = []
        for constraint in table.pr_constraints:
            cons_ddl_lst.append(constraint.item_name)
        return '' if len(cons_ddl_lst) == 0 else '\n    PRIMARY KEY({0})'.format(', '.join(cons_ddl_lst))

    def _parse_index(self, table):
        ind_ddl_lst = ''
        for index in table.indices:
            ind_ddl_lst += "CREATE INDEX ON \"{0}\" ({1});\n".format(
                table.name,
                ', '.join(index.field)
            )
        return '' if len(ind_ddl_lst) == 0 else ind_ddl_lst

    def parse_for_cons(self):
        ddl_string = ''
        for table in self.schema.tables:
            for constraint in table.fr_constraints:
                ddl_string += "ALTER TABLE \"{0}\" ADD FOREIGN KEY ({1}) REFERENCES \"{2}\" {3};\n".format(
                    table.name,
                    constraint.item_name,
                    constraint.ref_name,
                    "ON DELETE CASCADE" if "cascading_delete" in constraint.props else ''
                )
        return ddl_string
        
    def parse_check_cons(self):
        ddl_string = ''
        for table in self.schema.tables:
            for constraint in table.ch_constraints:
                ddl_string += "ALTER TABLE \"{0}\" ADD CHECK {1};\n".format(
                    table.name,
                    constraint.expression
                )
        return ddl_string
