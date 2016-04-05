import ddl_classes
import xml.dom.minidom as MiniDom
from os.path import splitext


class DbdSchemaToXml:
    def __init__(self, schema_i=None, db_path_i=None):
        self.schema = schema_i
        self.xml_path = splitext(db_path_i)[0]+".xml" if db_path_i is not None else ""
        self.root_node = None
        self.xml_root = MiniDom.Document()

    def set_xml_path(self, db_path):
        self.xml_path = splitext(db_path)[0] + ".xml" if db_path is not None else ""

    def _set_schema(self):
        self.root_node = self.xml_root.createElement("dbd_schema")
        self.root_node.setAttribute("fulltext_engine", "ORACLE TEXT")
        self.root_node.setAttribute("version", "1.2")
        if self.schema.__class__ == ddl_classes.Schema:
            self.root_node.setAttribute("name", self.schema.name)
        self.xml_root.appendChild(self.root_node)

    def _add_domains(self):
        if self.root_node.__class__ == MiniDom.Element:
            domains_tag = self.xml_root.createElement("domains")
            for domain_obj in self.schema.domains:
                domain_tag = self.xml_root.createElement("domains")
                domain_tag.setAttribute("name", domain_obj.name)
                if domain_obj.description:
                    domain_tag.setAttribute("description", domain_obj.description)
                domain_tag.setAttribute("type", domain_obj.description)
                if domain_obj.align:
                    domain_tag.setAttribute("align", domain_obj.align)
                if domain_obj.length:
                    domain_tag.setAttribute("length", str(domain_obj.length))
                if domain_obj.width:
                    domain_tag.setAttribute("width", str(domain_obj.width))
                if domain_obj.precision:
                    domain_tag.setAttribute("precision", str(domain_obj.precision))
                if domain_obj.props:
                    domain_tag.setAttribute("props", domain_obj.props)
                if domain_obj.char_length:
                    domain_tag.setAttribute("char_length", str(domain_obj.char_length))
                if domain_obj.scale:
                    domain_tag.setAttribute("scale", str(domain_obj.scale))
                domains_tag.appendChild(domain_tag)
            self.root_node.appendChild(domains_tag)

    def _add_fields(self, table, table_tag):
        if table_tag.__class__ == MiniDom.Element and table.__class__ == ddl_classes.Table:
            for field_obj in table.fields:
                field_tag = self.xml_root.createElement("field")
                field_tag.setAttribute("name", field_obj.name)
                if field_obj.rname:
                    field_tag.setAttribute("rname", field_obj.rname)
                field_tag.setAttribute("type", field_obj.description)
                if field_obj.description:
                    field_tag.setAttribute("description", field_obj.description)
                if field_obj.domain_name:                                 # if 'named' domain
                    field_tag.setAttribute("domain", field_obj.domain_name)
                else:
                    if field_obj.domain.name:
                        field_tag.setAttribute("domain", field_obj.domain.name)
                    else:                                                 # if unnamed domain
                        field_tag.setAttribute("domain.type", field_obj.domain.description)
                        if field_obj.domain.align:
                            field_tag.setAttribute("domain.align", field_obj.domain.align)
                        if field_obj.domain.length:
                            field_tag.setAttribute("domain.length", str(field_obj.domain.length))
                        if field_obj.domain.width:
                            field_tag.setAttribute("domain.width", str(field_obj.domain.width))
                        if field_obj.domain.precision:
                            field_tag.setAttribute("domain.precision", str(field_obj.domain.precision))
                        if field_obj.domain.char_length:
                            field_tag.setAttribute("domain.char_length", str(field_obj.domain.char_length))
                        if field_obj.domain.scale:
                            field_tag.setAttribute("domain.scale", str(field_obj.domain.scale))
                if field_obj.props:
                    field_tag.setAttribute("props", field_obj.props)
                table_tag.appendChild(field_tag)

    def _add_constraints(self, table, table_tag):
        if table_tag.__class__ == MiniDom.Element and table.__class__ == ddl_classes.Table:
            if table.pr_constraints:
                for pr_constr_obj in table.pr_constraints:
                    pr_constr = self.xml_root.createElement("constraint")
                    if pr_constr_obj.name:
                        pr_constr.setAttribute("name", pr_constr_obj.name)
                    pr_constr.setAttribute("kind", "PRIMARY")
                    pr_constr.setAttribute("items", pr_constr_obj.item_name)
                    table_tag.appendChild(pr_constr)
            if table.fr_constraints:
                for fr_constr_obj in table.fr_constraints:
                    for_constr = self.xml_root.createElement("constraint")
                    if fr_constr_obj.name:
                        for_constr.setAttribute("name", fr_constr_obj.name)
                    for_constr.setAttribute("kind", "FOREIGN")
                    for_constr.setAttribute("items", fr_constr_obj.item_name)
                    for_constr.setAttribute("reference", fr_constr_obj.ref_name)
                    if fr_constr_obj.props:
                        for_constr.setAttribute("props", fr_constr_obj.props)
                    table_tag.appendChild(for_constr)
            if table.ch_constraints:
                for ch_const_obj in table.ch_constraints:
                    ch_constr = self.xml_root.createElement("constraint")
                    ch_constr.setAttribute("name", ch_const_obj.name)
                    ch_constr.setAttribute("expression", ch_const_obj.expression)
                    table_tag.appendChild(ch_constr)

    def _add_indices(self, table, table_tag):
        if table_tag.__class__ == MiniDom.Element and table.__class__ == ddl_classes.Table:
            if table.indices:
                for index_obj in table.indices:
                    index_tag = self.xml_root.createElement("index")
                    index_tag.setAttribute("field", index_obj.field_name)
                    if index_obj.props:
                        index_tag.setAttribute("props", index_obj.field_name)
                    table_tag.appendChild(index_tag)

    def _add_tables(self):
        if self.root_node.__class__ == MiniDom.Element:
            tables_tag = self.xml_root.createElement("tables")
            for table in self.schema.tables:
                table_tag = self.xml_root.createElement("table")
                table_tag.setAttribute("name", table.name)
                if table.description:
                    table_tag.setAttribute("description", table.description)
                if table.props:
                    table_tag.setAttribute("props", table.props)
                if table.ht_table_flags:
                    table_tag.setAttribute("ht_table_flags", table.ht_table_flags)
                else:
                    table_tag.setAttribute("ht_table_flags", "rws")
                if table.means:
                    table_tag.setAttribute("means", table.means)
                table_tag.setAttribute("access_level", "0")
                self._add_fields(table, table_tag)
                self._add_constraints(table, table_tag)
                self._add_indices(table, table_tag)
                tables_tag.appendChild(table_tag)
            self.root_node.appendChild(tables_tag)

    def init_xml_root(self):
        self._set_schema()
        custom_tag = self.xml_root.createElement("custom")
        self.root_node.appendChild(custom_tag)
        self._add_domains()
        self._add_tables()

    def root_into_xml(self):
        self.xml_path = "tasks2.xml"  # todo: remove this debug line
        with open(self.xml_path, "wb") as xml_file:
            xml_file.write(self.xml_root.toprettyxml(indent='  ', encoding="utf-8"))
        return True

    def write_schema(self):
        self.init_xml_root()
        return self.root_into_xml()
