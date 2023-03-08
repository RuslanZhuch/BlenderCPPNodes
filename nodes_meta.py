class Generator:
    
    def __init__(self):
        self._node_groups = {}
        self._includes = set()

    def register_group(self, node_name, node_group):
        self._node_groups[node_name] = node_group

    def register_include(self, include_line):
        self._includes.add(include_line)

    def get_node_groups(self):
        return self._node_groups

    def get_includes(self):
        return list(self._includes)

    def reset(self):
        self._node_groups.clear()
        self._includes.clear()