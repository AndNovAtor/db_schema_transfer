import pypyodbc
import psycopg2


class DbdobjToPslDate:
    def __init__(self, tables_i, ddl_file="tmp.sql", ms_server_name="(localdb)\\v11.0", database_name='Northwind', postgresql_user="postgres",
                 postgresql_password='1', is_sql_expr_con=True):
        self.tables = tables_i
        self.ms_driver_str = '{SQL Server Native Client 11.0}' if is_sql_expr_con else '{SQL Server}'
        self.connect_msdbd = pypyodbc.connect(
            driver=self.ms_driver_str,
            server=ms_server_name,
            database=database_name,
            trusted_Connection='yes'
        )
        tmp_curs = psycopg2.connect("dbname='postgres' user='{0}' password='{1}'".format(
            postgresql_user,
            postgresql_password
        )).cursor()
        tmp_curs.execute("DROP DATABASE IF EXISTS '{0}'".format(database_name))
        tmp_curs.execute("Create DATABASE IF NOT EXISTS '{0}'".format(database_name))
        self.connect_postgres = psycopg2.connect("dbname='{0}' user='{1}' password='{2}'".format(
            database_name,
            postgresql_user,
            postgresql_password
        ))
        with self.connect_postgres.cursor() as cursor:
            cursor.execute(open(ddl_file, "r").read())

    def transfer(self):
        for table in self.tables:
            self.transfer_table(table.name)

    def transfer_table(self, table):
        table_name = table.name
        fields = [field.name for field in table.fields]
        param = self.get_param(len(fields))
        fields = ", ".join(fields)
        cur = self.connect_msdbd.cursor()
        cur.execute("Select {0} from \"{1}\";".format(fields, table_name))
        cur_2 = self.connect_postgres.cursor()
        cur_2.execute("BEGIN;")
        cur_2.execute("ALTER TABLE \"{0}\" DISABLE TRIGGER ALL;".format(table_name))
        row = cur.fetchone()
        while row is not None:
            cur_2.execute("Insert into \"{0}\" ({1}) VALUES({2});".format(table_name, fields, param), row)
            row = cur.fetchone()
        cur.close()
        cur_2.execute("ALTER TABLE \"{0}\" ENABLE TRIGGER ALL;".format(table_name))
        cur_2.execute("COMMIT;")
        cur_2.close()

    def get_param(self, count):
        ret = "%s," * count
        return ret[:-1]
