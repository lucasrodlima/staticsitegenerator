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

    def test_parent_equality(self):
        child_node1 = LeafNode("span", "child")
        child_node2 = LeafNode("span", "child")
        parent_node1 = ParentNode("div", [child_node1], {"class": "container"})
        parent_node2 = ParentNode("div", [child_node2], {"class": "container"})
        self.assertEqual(parent_node1, parent_node2)

    def test_parent_inequality_different_tag(self):
        child_node = LeafNode("span", "child")
        parent_node1 = ParentNode("div", [child_node])
        parent_node2 = ParentNode("section", [child_node])
        self.assertNotEqual(parent_node1, parent_node2)

    def test_parent_inequality_different_children(self):
        child_node1 = LeafNode("span", "child1")
        child_node2 = LeafNode("span", "child2")
        parent_node1 = ParentNode("div", [child_node1])
        parent_node2 = ParentNode("div", [child_node2])
        self.assertNotEqual(parent_node1, parent_node2)

    def test_parent_inequality_different_props(self):
        child_node = LeafNode("span", "child")
        parent_node1 = ParentNode("div", [child_node], {"class": "one"})
        parent_node2 = ParentNode("div", [child_node], {"class": "two"})
        self.assertNotEqual(parent_node1, parent_node2)

    def test_parent_with_none_children(self):
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError) as e:
            parent_node.to_html()
        self.assertEqual(str(e.exception), "Error: No children provided for ParentNode.")

    def test_parent_with_mixed_children_types(self):
        leaf_child = LeafNode("span", "leaf text")
        parent_child = ParentNode("p", [LeafNode("b", "bold text")])
        parent_node = ParentNode("div", [leaf_child, parent_child])
        expected = "<div><span>leaf text</span><p><b>bold text</b></p></div>"
        self.assertEqual(parent_node.to_html(), expected)

    def test_parent_with_deeply_nested_children(self):
        deep_child = LeafNode("em", "deeply nested")
        level3 = ParentNode("strong", [deep_child])
        level2 = ParentNode("i", [level3])
        level1 = ParentNode("b", [level2])
        root = ParentNode("p", [level1])
        expected = "<p><b><i><strong><em>deeply nested</em></strong></i></b></p>"
        self.assertEqual(root.to_html(), expected)

    def test_parent_with_multiple_props(self):
        child_node = LeafNode("span", "content")
        parent_node = ParentNode("div", [child_node], {
            "class": "container",
            "id": "main",
            "data-test": "value"
        })
        result = parent_node.to_html()
        # Check that all props are present (order might vary)
        self.assertIn('<div', result)
        self.assertIn('class="container"', result)
        self.assertIn('id="main"', result)
        self.assertIn('data-test="value"', result)
        self.assertIn('><span>content</span></div>', result)

    def test_parent_repr_no_props(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        expected = "HTMLNode(div, [LeafNode(span, child, None)], None)"
        self.assertEqual(repr(parent_node), expected)

    def test_parent_repr_no_children(self):
        parent_node = ParentNode("div", [])
        expected = "HTMLNode(div, [], None)"
        self.assertEqual(repr(parent_node), expected)

    def test_parent_repr_complex_structure(self):
        grandchild = LeafNode("b", "bold")
        child = ParentNode("span", [grandchild])
        parent = ParentNode("div", [child], {"class": "wrapper"})
        expected = "HTMLNode(div, [HTMLNode(span, [LeafNode(b, bold, None)], None)], {'class': 'wrapper'})"
        self.assertEqual(repr(parent), expected)

    def test_parent_with_special_tag_names(self):
        child_node = LeafNode("span", "content")
        # Test HTML5 semantic tags
        header = ParentNode("header", [child_node])
        nav = ParentNode("nav", [child_node])
        article = ParentNode("article", [child_node])
        section = ParentNode("section", [child_node])
        
        self.assertEqual(header.to_html(), "<header><span>content</span></header>")
        self.assertEqual(nav.to_html(), "<nav><span>content</span></nav>")
        self.assertEqual(article.to_html(), "<article><span>content</span></article>")
        self.assertEqual(section.to_html(), "<section><span>content</span></section>")

    def test_parent_with_self_closing_tag_children(self):
        # Test with children that represent self-closing tags (though LeafNode doesn't self-close)
        img_child = LeafNode("img", "", {"src": "test.jpg", "alt": "Test"})
        br_child = LeafNode("br", "")
        parent_node = ParentNode("div", [img_child, br_child])
        expected = '<div><img src="test.jpg" alt="Test"></img><br></br></div>'
        self.assertEqual(parent_node.to_html(), expected)

    def test_parent_initialization_order(self):
        child_node = LeafNode("span", "child")
        # Test different parameter orders
        parent1 = ParentNode("div", [child_node], {"class": "test"})
        parent2 = ParentNode(tag="div", children=[child_node], props={"class": "test"})
        parent3 = ParentNode(children=[child_node], tag="div", props={"class": "test"})
        
        expected = '<div class="test"><span>child</span></div>'
        self.assertEqual(parent1.to_html(), expected)
        self.assertEqual(parent2.to_html(), expected)
        self.assertEqual(parent3.to_html(), expected)

    def test_parent_with_large_number_of_children(self):
        children = [LeafNode("span", f"child{i}") for i in range(10)]
        parent_node = ParentNode("div", children)
        result = parent_node.to_html()
        
        self.assertTrue(result.startswith("<div>"))
        self.assertTrue(result.endswith("</div>"))
        for i in range(10):
            self.assertIn(f"<span>child{i}</span>", result)

    def test_parent_children_attribute_access(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        
        # Test that we can access children
        self.assertEqual(len(parent_node.children), 1)
        self.assertEqual(parent_node.children[0], child_node)

    def test_parent_tag_attribute_access(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        
        # Test that we can access tag
        self.assertEqual(parent_node.tag, "div")

    def test_parent_props_attribute_access(self):
        child_node = LeafNode("span", "child")
        props = {"class": "container", "id": "main"}
        parent_node = ParentNode("div", [child_node], props)
        
        # Test that we can access props
        self.assertEqual(parent_node.props, props)
        self.assertEqual(parent_node.props["class"], "container")
        self.assertEqual(parent_node.props["id"], "main")

    def test_parent_value_is_none(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        
        # ParentNode should always have None value (inherited from HTMLNode)
        self.assertIsNone(parent_node.value)

    def test_parent_with_children_containing_props(self):
        child1 = LeafNode("a", "Link 1", {"href": "http://example1.com"})
        child2 = LeafNode("a", "Link 2", {"href": "http://example2.com", "target": "_blank"})
        parent_node = ParentNode("nav", [child1, child2], {"class": "navigation"})
        
        result = parent_node.to_html()
        self.assertIn('<nav class="navigation">', result)
        self.assertIn('<a href="http://example1.com">Link 1</a>', result)
        self.assertIn('<a href="http://example2.com" target="_blank">Link 2</a>', result)
        self.assertIn('</nav>', result)
