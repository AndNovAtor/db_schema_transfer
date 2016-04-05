from MSDBD_TO_XML.SQL import *
from Shared.Types import *
# from ddl_classes import *

def create_schema(conn)
    MssqlSchemaToSchema(conn).create_schema()

class MssqlSchemaToSchema:
    def __init__(self, conn, schema_i=None):
        self.connection = conn
        self.cursor = conn.cursor()
        self.schema = schema_i
    
    def create_schema():
        cur = self.cursor
        row = cur.execute("""
                          SELECT
                          TOP(1) TABLE_SCHEMA
                          FROM
                          INFORMATION_SCHEMA.TABLES
                          WHERE TABLE_TYPE = 'BASE TABLE'
                          """).fetchone()
        self.schema = Schema()
        self.schema.name = row[0]
        create_tables()

    def create_tables(self):
        cur = self.cursor
        cur.execute("""
                    SELECT
                        TABLE_NAME
                    FROM
                    INFORMATION_SCHEMA.TABLES
                    WHERE TABLE_TYPE = 'BASE TABLE' AND  not TABLE_NAME = 'sysdiagrams'
                    """)
        row = cur.fetchone()
        while row is not None:
            table = Table()
            table.name = row[0]
            row = cur.fetchone()
            self.schema.tables.append(table)

        cur.close()

        for table in self.schema.tables:
            create_fields(table)
        
        for table in self.schema.tables:
            create_constraints(table)
        
        for table in self.schema.tables:
            create_index(table)

    def create_fields(self, table):
        cur = self.cursor
        cur.execute("""
                    SELECT
                        COLUMN_NAME,
                        DATA_TYPE,
                        CHARACTER_MAXIMUM_LENGTH
                    FROM INFORMATION_SCHEMA.COLUMNS
                    WHERE TABLE_NAME = ?
                    """, (table.name, ))
        row = cur.fetchone()
        while row is not None:
            field = Field()
            domain = Domain()
            field.name = row[0]
            domain.char_length = row[2]
            domain.type = row[1]
            field.domain = domain
            table.append_field(field)
            row = cur.fetchone()
        cur.close()

    def create_constraints(self, table):
        cur = self.cursor
        cur.execute("""
                    SELECT
                        ic.key_ordinal,
                        cl.name
                    FROM sys.key_constraints c
                    join sys.indexes i on c.parent_object_id = i.object_id
                        and c.unique_index_id = i.index_id
                    join sys.index_columns ic on ic.object_id = i.object_id
                        and ic.index_id = i.index_id
                    join sys.columns cl on cl.object_id = i.object_id
                        and ic.column_id = cl.column_id
                    WHERE
                        c.type = 'PK'
                        and 0 = ic.is_included_column
                        and
                        i.object_id = object_id(?)
                    order by ic.key_ordinal
                    """, (table.name, ))
        row = cur.fetchone()
        while row is not None:
            constraint = PrConstraint()
            constraint.item = table.fields_map[row[1]]
            constraint.item_name = row[1]
            table.append_constraint(constraint)
            row = cur.fetchone()

        cur.execute("""
                    SELECT
                        COL_NAME(parent_object_id, parent_column_id) ColumnName,
                        OBJECT_NAME(referenced_object_id) RefTableName,
                        COL_NAME(referenced_object_id, referenced_column_id) RefColumnName

                    FROM
                        sys.foreign_key_columns
                    Where OBJECT_NAME(parent_object_id) = ?;
                    """, (table.name, ))
        row = cur.fetchone()
        while row is not None:
            constraint = ForConstraint()
            constraint.item = table.fields_map[row[0]]
            constraint.item_name = row[0]
            constraint.reference = table.fields_map[row[1]]
            constraint.ref_name = row[1]
            if constraint.kind == 'FOREIGN' and constraint.reference == '':
                raise Exception('No reference table for foreign key')
            if constraint.items == '':
                raise Exception('Items value is empty!')

            table.append_constraint(constraint)
            row = cur.fetchone()
        
        cur.execute("""
                    select definition, COL_NAME(parent_object_id, parent_column_id) col_name
                    from sys.check_constraints
                    Where OBJECT_NAME(parent_object_id) = ?;
                    """, (table.name, ))
        row = cur.fetchone()
        while row is not None:
            constraint = ChConstraint()
            constraint.express = table.fields_map[row[0]]
            constraint.expression = row[0]
            constraint.item = table.fields_map[row[1]]
            constraint.item_name = row[1]
            table.append_constraint(constraint)
            row = cur.fetchone()

    def create_index(conn, table):
        cur = conn.cursor()
        cur.execute("""
                    SELECT ind.name IndexName
                    FROM sys.indexes ind
                    INNER JOIN sys.index_columns ic
                        ON  ind.object_id = ic.object_id and ind.index_id = ic.index_id
                    INNER JOIN sys.columns col
                        ON ic.object_id = col.object_id and ic.column_id = col.column_id
                    INNER JOIN sys.tables t
                        ON ind.object_id = t.object_id
                    WHERE
                        ind.is_primary_key = 0
                        AND ind.is_unique = 0
                        AND ind.is_unique_constraint = 0
                        AND t.is_ms_shipped = 0
                        AND t.name = ?
                    """, (table.name, ))
        row = cur.fetchone()
        while row is not None:
            index = Index()
            index.field_name.append(row[0])
            index.field = table.fields_map[row[0]]
            table.append_index(index)
            row = cur.fetchone()

