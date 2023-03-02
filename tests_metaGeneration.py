import unittest

import json

from os import path
import sys
 

from pathlib import Path
root_dir = Path.cwd()
sys.path.append(root_dir)

import nodes_meta

class TestMetaGeneration(unittest.TestCase):

    def test_generate_meta_data(self):
        meta_gen = nodes_meta.Generator()
        meta_gen.register_group("node1", "group1")
        meta_gen.register_group("node2", "group2")
        meta_gen.register_group("node3", "group3")

        node_groups_1 = meta_gen.get_node_groups()
        expected_node_groups_1 = {
            "node1": "group1",
            "node2": "group2",
            "node3": "group3"
        }

        self.assertEqual(node_groups_1, expected_node_groups_1)

        meta_gen.reset()
        node_groups_2 = meta_gen.get_node_groups()
        self.assertEqual(node_groups_2, {})
        
        meta_gen.register_group("node4", "group4")
        meta_gen.register_group("node5", "group12")
        node_groups_3 = meta_gen.get_node_groups()

        expected_node_groups_2 = {
            "node4": "group4",
            "node5": "group12"
        }
        self.assertEqual(node_groups_3, expected_node_groups_2)
