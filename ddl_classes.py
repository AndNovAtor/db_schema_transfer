class Domain:
    # TODO Нужно подумать, нужно ли где-то копирование
    def __init__(self, name_i=None, descr_i=None, type_i=None, align_i=None, precision_i=None, props_i="", width_i=None,
                 char_length_i=None, length_i=None, scale_i=None):
        self.name = name_i
        self.description = descr_i
        self.type = type_i
        self.align = align_i
        self.width = width_i
        self.precision = precision_i
        self.props = props_i
        self.char_length = char_length_i
        self.length = length_i
        self.scale = scale_i


class Table:
    def __init__(self, name_i=None, descr_i=None, props_i="", fields_lst=None, ht_table_flags="", prim_constraint=None,
                 for_constraints=None, ind_lst=None):
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
        self.pr_constraint = prim_constraint
        self.fr_constraints = for_constraints if (for_constraints.__class__.__name__ == "list") else []
        self.indexes = ind_lst if (ind_lst.__class__.__name__ == "list") else []

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


class Constraint:
    def _init_item(self, item_i):
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


class PrConstraint(Constraint):
    def __init__(self, item_i=None):
        self._init_item(item_i)


class ForConstraint(Constraint):
    def _init_ref(self, ref_item):
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

    def __init__(self, item_i=None, refer_item=None, props_i=""):
        self._init_item(item_i)
        self._init_ref(refer_item)
        self.props = props_i


class Index:
    def __init__(self, field_varr=None, props_i=""):
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
