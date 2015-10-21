class Domain:
    _attrs = {}
    # _attrs = {'' : ''}

    def __init__(self, attr_dict):
        self._attrs = attr_dict.copy()

    def add(self, attr_dict):
        self._attrs.update(attr_dict)

    def get_val(self, attr_name, default=None):
        return self._attrs.get(attr_name, default)

