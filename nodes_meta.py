class Generator:
    
    def __init__(self):
        self._node_groups = {}

    def register_group(self, node_name, node_group):
        self._node_groups[node_name] = node_group

    def get_node_groups(self):
        return self._node_groups

    def reset(self):
        self._node_groups.clear()