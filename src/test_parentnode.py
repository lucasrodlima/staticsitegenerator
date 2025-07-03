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

    def test_parent_with_no_children(self):
        parent_node = ParentNode("span")
        with self.assertRaises(ValueError) as e:
            parent_node.to_html()
        self.assertEqual(str(e.exception), "Error: No children provided for ParentNode.")

    def test_parent_with_props(self):
        child_node = LeafNode("p", "This is a paragraph")
        parent_node = ParentNode("div", [child_node], {"class": "container"})
        self.assertEqual(
            parent_node.to_html(),
            '<div class="container"><p>This is a paragraph</p></div>',
        )

    def test_parent_with_no_children_and_props(self):
        parent_node = ParentNode("div", props={"class": "container"})
        with self.assertRaises(ValueError) as e:
            parent_node.to_html()
        self.assertEqual(str(e.exception), "Error: No children provided for ParentNode.")

    def test_repr(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], {"class": "container"})
        expected_repr = "HTMLNode(div, [LeafNode(span, child, None)], {'class': 'container'})"
        self.assertEqual(repr(parent_node), expected_repr)

    def test_parent_with_multiple_children(self):
        child1 = LeafNode("p", "First paragraph")
        child2 = LeafNode("p", "Second paragraph")
        parent_node = ParentNode("div", [child1, child2])
        self.assertEqual(
            parent_node.to_html(),
            "<div><p>First paragraph</p><p>Second paragraph</p></div>",
        )

    def test_parent_with_empty_children(self):
        parent_node = ParentNode("div", [])
        with self.assertRaises(ValueError) as e:
            parent_node.to_html()
        self.assertEqual(str(e.exception), "Error: No children provided for ParentNode.")

    def test_parent_with_multiple_children_and_props(self):
        parent_node = ParentNode(
            "div",
            [LeafNode("p", "First paragraph"), LeafNode("p", "Second paragraph")],
            {"class": "container"},
        )
        self.assertEqual(
            parent_node.to_html(),
            '<div class="container"><p>First paragraph</p><p>Second paragraph</p></div>',
        )

    def test_parent_with_no_props(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_parent_with_multiple_children_and_multiple_grandchildren(self):
        grandchild1 = LeafNode("b", "grandchild1")
        grandchild2 = LeafNode("i", "grandchild2")
        child_node1 = ParentNode("span", [grandchild1])
        child_node2 = ParentNode("span", [grandchild2])
        parent_node = ParentNode("div", [child_node1, child_node2])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild1</b></span><span><i>grandchild2</i></span></div>",
        )


if __name__ == "__main__":
    unittest.main()
