from caseless_str_equals import caseless_equal


class Domain:
    # TODO Нужно подумать, нужно ли где-то копирование
    def __init__(self, name_i=None, descr_i=None, type_i=None, align_i=None, width_i=None, length_i=None,
                 precision_i=None, scale_i=None, props_i="", char_length_i=None):
        self.name = name_i
        self.description = descr_i
        self.type = type_i
        self.align = align_i
        self.length = length_i
        self.width = width_i
        self.precision = precision_i
        self.props = props_i
        self.char_length = char_length_i
        self.scale = scale_i

    def eq(self, other):
        if other.__class__.__name__ != "Domain":
            return False
        else:
            return caseless_equal(self.type, other.type) and (self.length == other.length) \
                   and (self.precision == other.precision) and (self.scale == other.scale)


class Table:
    def __init__(self, name_i=None, descr_i=None, props_i="", fields_lst=None, ht_table_flags="", prim_constraint_i=None,
                 for_constraints_i=None, ch_const_i=None, ind_lst=None):
        self.name = name_i
        self.description = descr_i
        self.props = props_i
        self.ht_table_flags = ht_table_flags
        if fields_lst.__class__.__name__ == "list":
            self.fields = {fld.name: fld for fld in fields_lst if fields_lst.__class__.__name__ == "Field"}
            # self.fields_name_lst = [fld.name for fld in fields_lst if fields_lst.__class__.__name__ == "Field"]
        else:
            self.fields = {}
            # self.fields_name_lst = []
        self.pr_constraint = prim_constraint_i if (prim_constraint_i.__class__.__name__ == "PrConstraint") else None
        self.fr_constraints = for_constraints_i if (for_constraints_i.__class__.__name__ == "list") else []
        self.indices = ind_lst if (ind_lst.__class__.__name__ == "list") else []
        self.ch_constraint = ch_const_i if (ch_const_i.__class__.__name__ == "CheckConstraint") else None

    def append_field(self, field):
        if type(field).__name__ == "Field":
            if (field.name is not None) and (field.name is not ""):
                self.fields[field.name] = field  # Add field with name as adding item to a dict
                # self.fields_name_lst.append(field.name)


class Field:
    def __init__(self, name_i=None, rname_i=None, descr_i=None, domain_name_i=None, props_i=""):
        self.name = name_i
        self.rname = rname_i
        self.description = descr_i
        self.domain_name = domain_name_i
        self.domain = None
        self.props = props_i

    def init_domain(self, domains):
        if type(domains).__name__ == "list":
            for domain_item in domains:
                if type(domain_item).__name__ == "Domains":
                    if domain_item.name == self.domain_name:
                        self.domain = domain_item
                        break


class PrConstraint:
    const_type = "PRIMARY"

    def __init__(self, item_i=None, name_i=None):
        if type(item_i).__name__ == "str":
            self.item_name = item_i
            self.item = None
        else:
            if type(item_i).__name__ == "Field":
                self.item_name = item_i.name
                self.item = item_i
            else:
                self.item_name = None
                self.item = None
        self.name = name_i


class ForConstraint:
    const_type = "FOREIGN"

    def __init__(self, item_i=None, ref_item=None, props_i="", name_i=None):
        if type(item_i).__name__ == "str":
            self.item_name = item_i
            self.item = None
        else:
            if type(item_i).__name__ == "Field":
                self.item_name = item_i.name
                self.item = item_i
            else:
                self.item_name = None
                self.item = None
        if type(ref_item).__name__ == "str":
            self.ref_name = ref_item
            self.reference = None
        else:
            if type(ref_item).__name__ == "Table":
                self.ref_name = ref_item.name
                self.reference = ref_item
            else:
                self.ref_name = None
                self.ref_item = None
        self.props = props_i
        self.name = name_i


class CheckConstraint:
    const_type = "CHECK"

    def __init__(self, expression_i=None, props_i="", name_i=None):
        self.expression = expression_i
        self.props = props_i
        self.name = name_i


class Index:
    def __init__(self, field_varr=None, props_i="", expr_i=None, name_i=None):
        clazz = type(field_varr).__name__
        if clazz == "str":
            self.field_name = field_varr
            self.field = None
        else:
            if clazz == "Field":
                self.field_name = field_varr.name
                self.field = field_varr
            else:
                self.field_name = None
                self.field = None
        self.props = props_i
        self.name = name_i
        self.expression = expr_i
