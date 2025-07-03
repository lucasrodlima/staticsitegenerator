import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "This is a paragraph")
        self.assertEqual(node.to_html(), "<p>This is a paragraph</p>")

    def test_no_value_leaf(self):
        node = LeafNode("i")
        with self.assertRaises(ValueError) as e:
            node.to_html()
        self.assertEqual(str(e.exception), "Error: No value provided for LeafNode.")

    def test_leaf_to_html_i(self):
        node = LeafNode("i", "This is italic text")
        self.assertEqual(node.to_html(), "<i>This is italic text</i>")
