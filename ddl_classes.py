from caseless_str_equals import caseless_equal


class Domain:
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
        if other.__class__ != Domain:
            return False
        else:
            return caseless_equal(self.type, other.type) and (self.length == other.length) \
                   and (self.precision == other.precision) and (self.scale == other.scale)


class Table:
    def __init__(self, name_i=None, descr_i=None, props_i="", fields_lst=None, ht_table_flags="", means_i="",
                 prim_constraints_i=None, for_constraints_i=None, ch_consts_i=None, ind_lst=None):
        self.name = name_i
        self.description = descr_i
        self.props = props_i
        self.ht_table_flags = ht_table_flags
        if fields_lst.__class__ == list:
            self.fields = fields_lst
            self.fields_map = {fld.name: fld for fld in fields_lst if fields_lst.__class__ == Field}
        else:
            self.fields = []
            self.fields_map = {}
        self.means = means_i
        self.pr_constraints = prim_constraints_i if (prim_constraints_i.__class__ == list) else []
        self.fr_constraints = for_constraints_i if (for_constraints_i.__class__ == list) else []
        self.indices = ind_lst if (ind_lst.__class__ == list) else []
        self.ch_constraints = ch_consts_i if (ch_consts_i.__class__ == list) else []

    def append_field(self, field):
        if type(field) == Field:
            if (field.name is not None) and (field.name is not ""):
                self.fields.append(field)
                self.fields_map[field.name] = field  # Add field with name as adding item to a dict

    def append_constraint(self, constr):
        if constr.__class__ == ForConstraint:
            self.fr_constraints.append(constr)
        else:
            if constr.__class__ == PrConstraint:
                self.pr_constraints.append(constr)
            else:
                if constr.__class__ == CheckConstraint:
                    self.ch_constraints.append(constr)

    def append_index(self, ind):
        if type(ind) == Index:
            self.indices.append(ind)


class Field:
    def __init__(self, name_i=None, rname_i=None, descr_i=None, domain_name_i=None, props_i=""):
        self.name = name_i
        self.rname = rname_i
        self.description = descr_i
        self.domain_name = domain_name_i
        self.domain = None
        self.props = props_i

        self.position = None

    def init_domain(self, domains):
        if type(domains) == list:
            for domain_item in domains:
                if type(domain_item) == Domain:
                    if domain_item.name == self.domain_name:
                        self.domain = domain_item
                        break

    def set_domain(self, domain_i):
        if type(domain_i) == Domain:
            self.domain = domain_i
            self.domain_name = domain_i.name


class PrConstraint:
    const_type = "PRIMARY"

    def __init__(self, item_i=None, name_i=None):
        if type(item_i) == str:
            self.item_name = item_i
            self.item = None
        else:
            if type(item_i) == Field:
                self.item_name = item_i.name
                self.item = item_i
            else:
                self.item_name = None
                self.item = None
        self.name = name_i


class ForConstraint:
    const_type = "FOREIGN"

    def __init__(self, item_i=None, ref_item=None, props_i="", name_i=None):
        if type(item_i) == str:
            self.item_name = item_i
            self.item = None
        else:
            if type(item_i) == Field:
                self.item_name = item_i.name
                self.item = item_i
            else:
                self.item_name = None
                self.item = None
        if type(ref_item) == str:
            self.ref_name = ref_item
            self.reference = None
        else:
            if type(ref_item) == Table:
                self.ref_name = ref_item.name
                self.reference = ref_item
            else:
                self.ref_name = None
                self.ref_item = None
        self.props = props_i
        self.name = name_i

        self.position = None


class CheckConstraint:
    const_type = "CHECK"

    def __init__(self, expression_i="", field_item=None, name_i=None):
        self.expression = expression_i
        self.name = name_i
        if field_item.__class__ == Field:
            self.item = field_item
            self.item_name = field_item.name
        else:
            if field_item.__class__ == str:
                self.item = None
                self.item_name = field_item
            else:
                self.item = None
                self.item_name = None
        


class Index:
    def __init__(self, field_varr=None, props_i="", expr_i=None, name_i=None):
        clazz = type(field_varr)
        if clazz == str:
            self.field_name = field_varr
            self.field = None
        else:
            if clazz == Field:
                self.field_name = field_varr.name
                self.field = field_varr
            else:
                self.field_name = None
                self.field = None
        self.props = props_i
        self.name = name_i
        self.expression = expr_i

        self.position = None


class Schema:
    def __init__(self, domains_lst=None, un_dom_lst=None, tables_lst=None, const_num=0, indices_num=0, name_i=""):
        self.name = name_i
        self.domains = [d for d in domains_lst if d.__class__ == Domain] if domains_lst is not None else []
        self.un_domains = [un_d for un_d in un_dom_lst if un_d.__class__ == Domain] if un_dom_lst is not None else []
        self.tables = [t for t in tables_lst if t.__class__ == Table] if tables_lst is not None else []
        self.tables_map = {}
        self.con_num = const_num
        self.ind_num = indices_num

    def get_all_domains(self):
        return self.domains+self.un_domains

    #def append_table(self, table):
    #    if table.__class__ == Table:
    #        self.tables.append(table)
    #        if table.name:
    #            self.tables_map[table.name] = table
