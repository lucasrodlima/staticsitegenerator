import unittest

from parentnode import ParentNode
from leafnode import LeafNode


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_parent_with_no_tag(self):
        child_node = LeafNode("p", "This is a paragraph")
        parent_node = ParentNode(children=[child_node])
        with self.assertRaises(ValueError) as e:
            parent_node.to_html()
        self.assertEqual(str(e.exception), "Error: No tag provided for ParentNode.")

    # def test_parent_with_no_children(self):
    #     parent_node = ParentNode("span")
    #     with self.assertRaises(ValueError) as e:
    #         parent_node.to_html()
    #     self.assertEqual(str(e.exception), "Error: No tag provided for ParentNode.")


if __name__ == "__main__":
    unittest.main()
