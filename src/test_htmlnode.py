import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_eq_paragraph(self):
        node = HTMLNode("p", "This is a paragraph")
        node2 = HTMLNode("p", "This is a paragraph")
        self.assertEqual(node, node2)

    def test_eq_image(self):
        node = HTMLNode("img", props={"src": "image.png", "alt": "An image"})
        node2 = HTMLNode("img", props={"src": "image.png", "alt": "An image"})
        self.assertEqual(node, node2)

    def test_to_html(self):
        node = HTMLNode("p", "This is a paragraph")
        with self.assertRaises(NotImplementedError) as e:
            node.to_html()
        self.assertEqual(str(e.exception), "Error: to_html method not implemented")

    def test_props_to_html(self):
        node = HTMLNode(
            "a",
            "This is a link",
            props={"href": "https://www.google.com", "target": "_blank"},
        )
        self.assertEqual(
            node.props_to_html(), ' href="https://www.google.com" target="_blank"'
        )

    def test_props_to_html_no_props(self):
        node = HTMLNode("p", "This is a paragraph")
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_empty_props(self):
        node = HTMLNode("p", "This is a paragraph", props={})
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_single_prop(self):
        node = HTMLNode("p", "Text", props={"class": "highlight"})
        self.assertEqual(node.props_to_html(), ' class="highlight"')

    def test_props_to_html_multiple_props(self):
        node = HTMLNode("img", props={"src": "test.jpg", "alt": "Test", "width": "100"})
        result = node.props_to_html()
        # Check that all properties are present (order might vary)
        self.assertIn('src="test.jpg"', result)
        self.assertIn('alt="Test"', result) 
        self.assertIn('width="100"', result)
        self.assertEqual(result.count(' '), 3)  # Should have 3 spaces (one before each prop)

    def test_init_with_all_params(self):
        children = [HTMLNode("span", "child")]
        props = {"class": "test"}
        node = HTMLNode("div", "value", children, props)
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "value")
        self.assertEqual(node.children, children)
        self.assertEqual(node.props, props)

    def test_init_with_defaults(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_init_with_tag_only(self):
        node = HTMLNode("p")
        self.assertEqual(node.tag, "p")
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_repr_all_params(self):
        children = [HTMLNode("span", "child")]
        props = {"class": "test"}
        node = HTMLNode("div", "value", children, props)
        expected = "HTMLNode(div, value, [HTMLNode(span, child, None, None)], {'class': 'test'})"
        self.assertEqual(repr(node), expected)

    def test_repr_minimal(self):
        node = HTMLNode("p")
        expected = "HTMLNode(p, None, None, None)"
        self.assertEqual(repr(node), expected)

    def test_repr_with_props_only(self):
        node = HTMLNode("p", props={"class": "text"})
        expected = "HTMLNode(p, None, None, {'class': 'text'})"
        self.assertEqual(repr(node), expected)

    def test_equality_same_nodes(self):
        node1 = HTMLNode("p", "text", None, {"class": "test"})
        node2 = HTMLNode("p", "text", None, {"class": "test"})
        self.assertEqual(node1, node2)

    def test_equality_different_tags(self):
        node1 = HTMLNode("p", "text")
        node2 = HTMLNode("div", "text")
        self.assertNotEqual(node1, node2)

    def test_equality_different_values(self):
        node1 = HTMLNode("p", "text1")
        node2 = HTMLNode("p", "text2")
        self.assertNotEqual(node1, node2)

    def test_equality_different_children(self):
        child1 = HTMLNode("span", "child1")
        child2 = HTMLNode("span", "child2")
        node1 = HTMLNode("p", "text", [child1])
        node2 = HTMLNode("p", "text", [child2])
        self.assertNotEqual(node1, node2)

    def test_equality_different_props(self):
        node1 = HTMLNode("p", "text", props={"class": "one"})
        node2 = HTMLNode("p", "text", props={"class": "two"})
        self.assertNotEqual(node1, node2)

    def test_equality_none_vs_empty_props(self):
        node1 = HTMLNode("p", "text", props=None)
        node2 = HTMLNode("p", "text", props={})
        self.assertNotEqual(node1, node2)

    def test_equality_none_vs_empty_children(self):
        node1 = HTMLNode("p", "text", children=None)
        node2 = HTMLNode("p", "text", children=[])
        self.assertNotEqual(node1, node2)

    def test_equality_with_nested_children(self):
        grandchild = HTMLNode("b", "bold")
        child1 = HTMLNode("span", "text", [grandchild])
        child2 = HTMLNode("span", "text", [grandchild])
        node1 = HTMLNode("div", None, [child1])
        node2 = HTMLNode("div", None, [child2])
        self.assertEqual(node1, node2)

    def test_equality_returns_false_not_none(self):
        node1 = HTMLNode("p", "text1")
        node2 = HTMLNode("p", "text2")
        result = node1.__eq__(node2)
        self.assertIs(result, False)  # Should return False, not None

    def test_equality_returns_true_not_none(self):
        node1 = HTMLNode("p", "text")
        node2 = HTMLNode("p", "text")
        result = node1.__eq__(node2)
        self.assertIs(result, True)  # Should return True, not None

    def test_props_to_html_with_special_characters(self):
        node = HTMLNode("a", "link", props={"href": "http://example.com?q=test&foo=bar"})
        expected = ' href="http://example.com?q=test&foo=bar"'
        self.assertEqual(node.props_to_html(), expected)

    def test_props_to_html_with_numbers(self):
        node = HTMLNode("img", props={"width": "100", "height": "200"})
        result = node.props_to_html()
        self.assertIn('width="100"', result)
        self.assertIn('height="200"', result)

    def test_children_can_be_empty_list(self):
        node = HTMLNode("div", "text", [])
        self.assertEqual(node.children, [])
        self.assertNotEqual(node.children, None)


if __name__ == "__main__":
    unittest.main()
