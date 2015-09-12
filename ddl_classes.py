class Domain:
    name = ""
    description = ""
    type = ""
    align = ""
    width = 0
    precision = ""
    props = ""
    char_length = 0
    # attrs = {}

    def __init__(self, attr_dict):
        self.name = attr_dict.get("name", "")
        # TODO Использование .pop() изменит объект снаружи, однако это уменшит поиск, в теории. Нужно ли заменить?
        self.description = attr_dict.get("description", "")
        self.type = attr_dict.get("type", "")
        self.align = attr_dict.get("align", "")
        self.width = attr_dict.get("width", 0)
        self.precision = attr_dict.get("precision", 0)
        self.props = attr_dict.get("props", "")
        self.char_length = attr_dict.get("align", 0)

    def __init__(self, name_i, type_i, align_i, width_i, descr_i="", precision_i="", props_i="", char_length_i=0):
        self.name = name_i
        self.description = descr_i
        self.type = type_i
        self.align = align_i
        self.width = width_i
        self.precision = precision_i
        self.props = props_i
        self.char_length = char_length_i

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
    name = ""
    description = ""
    props = ""
    ht_table_flags = ""
    fields = []
    pr_constraint = None
    fr_constraints = []
    # attrs = {}

    def __init__(self, attr_dict):
        self.name = attr_dict.get("name", "")
        self.description = attr_dict.get("description", "")
        self.props = attr_dict.get("props", "")
        self.ht_table_flags = attr_dict.get("ht_table_flags", "")

    def __init__(self, attr_dict, fields_lst, prim_constraint, for_constraints):
        self.name = attr_dict.get("name", "")
        self.description = attr_dict.get("description", "")
        self.props = attr_dict.get("props", "")
        self.ht_table_flags = attr_dict.get("ht_table_flags", "")
        self.fields = fields_lst
        self.pr_constraint = prim_constraint
        self.fr_constraints = for_constraints


# TODO Нужно подумать, нужно ли где-то копирование
    def __init__(self, name_i, description_i, props_i, ht_table_flags_i, fields_i, pr_constraint_i, fr_constraints_i):
        self.name = name_i
        self.description = description_i
        self.props = props_i
        self.ht_table_flags = ht_table_flags_i
        self.fields = pr_constraint_i
        self.pr_constraint = pr_constraint_i
        self.fr_constraints = fr_constraints_i


class Field:
    name = ""
    rname = ""
    domain_name = ""
    domain = None
    description = ""
    props = ""

    def __init__(self, attr_dict):
        self.name = attr_dict.get("name", "")
        self.rname = attr_dict.get("rname", "")
        self.domain_name = attr_dict.get("domain", "")
        self.description = attr_dict.get("description", "")
        self.props = attr_dict.get("props", "")

    def __init__(self, attr_dict, domain_list):
        self.name = attr_dict.get("name", "")
        self.rname = attr_dict.get("rname", "")
        self.domain_name = attr_dict.get("domain", "")
        self.description = attr_dict.get("description", "")
        self.props = attr_dict.get("props", "")
        # domain = "{}"d for d in domain_list if d.name==self.domain_name]
        for node in domain_list:
            if node.name == self.domain_name:
                self.domain = node
                break


class Constraint:
    item_name = ""
    item = None

    def init_item(self, item_i):
        if item_i is None:
            self.item = None
        else:
            if type(item_i) == "string":
                self.item_name = item_i
            else:
                self.item = item_i
                self.item_name = item_i.name


class PrConstraint (Constraint):
    def __init__(self, item_i):
        self.init_item(item_i)
        self.item_name = item_i.name


class ForConstraint (Constraint):
    reference = None
    ref_name = ""
    props = ""

    def __init__(self, item_i, refer_item, props_i):
        self.init_item(item_i)
        self.item_name = item_i.name
        self.reference = refer_item
        self.props = props_i


class Index:
    field_name = ""
    field = None
    props = ""

    def __init__(self, field_i, props_i=""):
        if field_i is None:
            self.field = None
        else:
            if type(field_i) == "string":
                self.field_name = field_i
            else:
                self.field = field_i
                self.field_name = field_i.name
        self.props = props_i

