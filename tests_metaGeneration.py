import unittest

import json

from os import path
import sys
 

from pathlib import Path
root_dir = Path.cwd()
sys.path.append(root_dir)

import nodes_meta

class TestMetaGeneration(unittest.TestCase):

    def test_generate_meta_data_groups(self):
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
        
    def test_generate_meta_data_includes(self):
        meta_gen = nodes_meta.Generator()
        meta_gen.register_include("include_1.h")
        meta_gen.register_include("include_2.h")
        meta_gen.register_include("include_3.h")
        
        includes_1 = meta_gen.get_includes()
        expected_includes_1 = [
            "include_1.h",
            "include_2.h",
            "include_3.h",
        ]

        includes_1.sort()
        self.assertEqual(includes_1, expected_includes_1)

        meta_gen.reset()
        includes_2 = meta_gen.get_includes()
        self.assertEqual(includes_2, [])
        
        meta_gen.register_include("include_4.h")
        meta_gen.register_include("include_5.h")
        meta_gen.register_include("include_4.h")
        includes_3 = meta_gen.get_includes()

        expected_includes_3 = [
            "include_4.h",
            "include_5.h",
        ]
        includes_3.sort()
        self.assertEqual(includes_3, expected_includes_3)
