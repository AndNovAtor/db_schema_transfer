class Domain:
    def __init__(self):
        self.name = ""
        self.description = ""
        self.type = ""
        self.align = ""
        self.width = 0
        self.precision = ""
        self.props = ""
        self.char_length = 0

    # def __init__(self, attr_dict):
    #     self.name = attr_dict.get("name", "")
    #     # TODO Использование .pop() изменит объект снаружи, однако это уменшит поиск, в теории. Нужно ли заменить?
    #     self.description = attr_dict.get("description", "")
    #     self.type = attr_dict.get("type", "")
    #     self.align = attr_dict.get("align", "")
    #     self.width = int(attr_dict.get("width", 0))
    #     self.precision = attr_dict.get("precision", 0)
    #     self.props = attr_dict.get("props", "")
    #     self.char_length = int(attr_dict.get("char_length", 0))

    # def __init__(self, name_i, type_i, align_i, width_i, descr_i="", precision_i="", props_i="", char_length_i=0):
    #     self.name = name_i
    #     self.description = descr_i
    #     self.type = type_i
    #     self.align = align_i
    #     self.width = width_i
    #     self.precision = precision_i
    #     self.props = props_i
    #     self.char_length = char_length_i

    # def get_val(self, attr_name, default=None):
    #     return {
    #         "name": self.name,
    #         "description": self.description,
    #         "type": self.type,
    #         "align": self.align,
    #         "width": self.width,
    #         "props": self.props,
    #         "char_length": self.char_length,
    #     }.get(attr_name.lower(), self.attrs.get(attr_name, default))


class Table:
    def __init__(self):
        self.name = ""
        self.description = ""
        self.props = ""
        self.ht_table_flags = ""
        self.fields = []
        self.pr_constraint = None
        self.fr_constraints = []

    # def __init__(self, attr_dict):
    #     self.name = attr_dict.get("name", "")
    #     self.description = attr_dict.get("description", "")
    #     self.props = attr_dict.get("props", "")
    #     self.ht_table_flags = attr_dict.get("ht_table_flags", "")
    #     self.fields = []
    #     self.pr_constraint = None
    #     self.fr_constraints = []

    # # TODO Нужно подумать, нужно ли где-то копирование
    # def __init__(self, name_i, fields_lst, prim_constraint, for_constraints, descr_i="", props_i="", ht_table_flags=""):
    #     self.name = name_i
    #     self.description = descr_i
    #     self.props = props_i
    #     self.ht_table_flags = ht_table_flags
    #     self.fields = fields_lst
    #     self.pr_constraint = prim_constraint
    #     self.fr_constraints = for_constraints

    # def __init__(self, attr_dict, fields_lst, prim_constraint, for_constraints):
    #     self.name = attr_dict.get("name", "")
    #     self.description = attr_dict.get("description", "")
    #     self.props = attr_dict.get("props", "")
    #     self.ht_table_flags = attr_dict.get("ht_table_flags", "")
    #     self.fields = fields_lst
    #     self.pr_constraint = prim_constraint
    #     self.fr_constraints = for_constraints

    def append_field(self, field):
        if type(field).__name__ == "Field":
            self.fields.append(field)


class Field:
    def __init__(self):
        self.name = ""
        self.rname = ""
        self.description = ""
        self.domain_name = ""
        self.domain = None
        self.props = ""

    def init_domain(self, domains):
        if type(domains).__name__ == "list":
            for domain_item in domains:
                if type(domain_item).__name__ == "Domains":
                    if domain_item.name == self.domain_name:
                        self.domain = domain_item
                        break

    # def __init__(self, name_i, rname_i, domain_name_i, descr_i="", props_i=""):
    #     self.name = name_i
    #     self.rname = rname_i
    #     self.description = descr_i
    #     self.domain_name = domain_name_i
    #     self.domain = None
    #     self.props = props_i

    # def __init__(self, attr_dict):
    #     self.name = attr_dict.get("name", "")
    #     self.rname = attr_dict.get("rname", "")
    #     self.domain_name = attr_dict.get("domain", "")
    #     self.description = attr_dict.get("description", "")
    #     self.props = attr_dict.get("props", "")

    # def __init__(self, attr_dict, domain_list):
    #     self.name = attr_dict.get("name", "")
    #     self.rname = attr_dict.get("rname", "")
    #     self.domain_name = attr_dict.get("domain", "")
    #     self.description = attr_dict.get("description", "")
    #     self.props = attr_dict.get("props", "")
    #     # domain = "{}"d for d in domain_list if d.name==self.domain_name]
    #     for node in domain_list:
    #         if node.name == self.domain_name:
    #             self.domain = node
    #             break


class Constraint:

    def _init_item(self, item_i):
        if item_i is not None:
            if type(item_i).__name__ == "string":
                self.item_name = item_i
                self.item = None
            else:
                if type(item_i).__name__ == "Field":
                    self.item_name = item_i.name
                    self.item = item_i


class PrConstraint (Constraint):
    def __init__(self):
        self.item_name = ""
        self.item = None

    def __init__(self, item_i):
        self._init_item(item_i)

    # def __init__(self, attr_dict):
    #     self.item_name = attr_dict.get("items", "")
    #     self.item = None


class ForConstraint (Constraint):
    def __init__(self):
        self.item_name = ""
        self.item = None
        self.ref_name = ""
        self.reference = None
        self.props = ""

    def _init_ref(self, ref_item):
        if ref_item is None:
            self.ref_name = ""
            self.ref_item = None
        else:
            if type(ref_item).__name__ == "string":
                self.ref_name = ref_item
                self.reference = None
            else:
                self.ref_name = ref_item.name
                self.reference = ref_item

    def __init__(self, item_i, refer_item, props_i=""):
        self._init_item(item_i)
        self._init_ref(refer_item)
        self.props = props_i

    # def __init__(self, attr_dict):
    #     self.item_name = attr_dict.get("items", "")
    #     self.item = None
    #     self.ref_name = attr_dict.get("reference", "")
    #     self.reference = None


class Index:
    def __init__(self):
        self.field_name = ""
        self.field = None
        self.props = ""

    def __init__(self, field_varr, props_i=""):
        if field_varr is not None:
            if type(field_varr).__name__ == "string":
                self.field_name = field_varr
                self.field = None
            else:
                if type(field_varr).__name__ == "Field":
                    self.field_name = field_varr.name
                    self.field = field_varr
                else:
                    self.field_name = ""
                    self.field = None
        self.props = props_i

    # def __init__(self, attr_dict):
    #     self.field_name = attr_dict.get("field", "")
    #     self.props = attr_dict.get("props", "")


