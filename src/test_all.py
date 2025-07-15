import unittest

from classes import TextNode, TextType, HTMLNode, LeafNode, ParentNode, BlockType
from functions import (
    text_node_to_html, extract_markdown_images, extract_markdown_links,
    split_nodes_delimiter, split_nodes_image, split_nodes_link,
    text_to_textnodes, markdown_to_blocks, block_to_blocktype, markdown_to_html_node, extract_title
)


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_with_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "google.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "google.com")
        self.assertEqual(node, node2)

    def test_different_url(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD, "google.com")
        self.assertNotEqual(node, node2)

    def test_different_text_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_different_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is another text node", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_repr_with_url(self):
        node = TextNode("This is a text node", TextType.LINK, "https://example.com")
        expected = "TextNode(This is a text node, link, https://example.com)"
        self.assertEqual(repr(node), expected)

    def test_repr_without_url(self):
        node = TextNode("This is a text node", TextType.BOLD)
        expected = "TextNode(This is a text node, bold, None)"
        self.assertEqual(repr(node), expected)

    def test_repr_with_all_text_types(self):
        # Test repr for all text types
        test_cases = [
            (TextType.TEXT, "text"),
            (TextType.BOLD, "bold"),
            (TextType.ITALIC, "italic"),
            (TextType.CODE, "code"),
            (TextType.LINK, "link"),
            (TextType.IMAGE, "image")
        ]

        for text_type, expected_type_str in test_cases:
            node = TextNode("Test", text_type)
            expected = f"TextNode(Test, {expected_type_str}, None)"
            self.assertEqual(repr(node), expected)

    def test_equality_with_none_vs_empty_string_url(self):
        node1 = TextNode("Text", TextType.LINK, None)
        node2 = TextNode("Text", TextType.LINK, "")
        self.assertNotEqual(node1, node2)

    def test_equality_returns_false_not_none(self):
        node1 = TextNode("Text1", TextType.TEXT)
        node2 = TextNode("Text2", TextType.TEXT)
        result = node1.__eq__(node2)
        self.assertIs(result, False)

    def test_equality_returns_true_not_none(self):
        node1 = TextNode("Text", TextType.TEXT)
        node2 = TextNode("Text", TextType.TEXT)
        result = node1.__eq__(node2)
        self.assertIs(result, True)

    def test_init_with_empty_text(self):
        node = TextNode("", TextType.TEXT)
        self.assertEqual(node.text, "")
        self.assertEqual(node.text_type, TextType.TEXT)
        self.assertIsNone(node.url)

    def test_init_with_special_characters(self):
        special_text = "Text with special chars: @#$%^&*()[]{}|\\:;\"'<>,.?/~`"
        node = TextNode(special_text, TextType.TEXT)
        self.assertEqual(node.text, special_text)
        self.assertEqual(node.text_type, TextType.TEXT)


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


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "This is a paragraph")
        self.assertEqual(node.to_html(), "<p>This is a paragraph</p>")

    def test_no_value_leaf(self):
        node = LeafNode("i")
        with self.assertRaises(ValueError) as e:
            node.to_html()
        self.assertEqual(str(e.exception),
                         "Error: No value provided for LeafNode.")

    def test_leaf_to_html_i(self):
        node = LeafNode("i", "This is italic text")
        self.assertEqual(node.to_html(), "<i>This is italic text</i>")

    def test_leaf_with_props(self):
        node = LeafNode("a", "Click me", {
                        "href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(
            node.to_html(), '<a href="https://www.google.com" target="_blank">Click me</a>')

    def test_leaf_no_tag_returns_value(self):
        node = LeafNode(None, "Just plain text")
        self.assertEqual(node.to_html(), "Just plain text")

    def test_leaf_with_single_prop(self):
        node = LeafNode("p", "Styled paragraph", {"class": "highlight"})
        self.assertEqual(
            node.to_html(), '<p class="highlight">Styled paragraph</p>')

    def test_leaf_no_tag_with_props_returns_value(self):
        # Props should be ignored when there's no tag
        node = LeafNode(None, "Plain text", {"class": "ignored"})
        self.assertEqual(node.to_html(), "Plain text")

    def test_leaf_empty_value_raises_error(self):
        node = LeafNode("p", "")
        # Empty string is still a value, so this should work
        self.assertEqual(node.to_html(), "<p></p>")

    def test_leaf_none_value_raises_error(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError) as e:
            node.to_html()
        self.assertEqual(str(e.exception),
                         "Error: No value provided for LeafNode.")

    def test_leaf_repr(self):
        node = LeafNode("p", "This is a paragraph", {"class": "text"})
        expected = "LeafNode(p, This is a paragraph, {'class': 'text'})"
        self.assertEqual(repr(node), expected)

    def test_leaf_repr_no_props(self):
        node = LeafNode("p", "This is a paragraph")
        expected = "LeafNode(p, This is a paragraph, None)"
        self.assertEqual(repr(node), expected)

    def test_leaf_repr_no_tag(self):
        node = LeafNode(None, "Just text")
        expected = "LeafNode(None, Just text, None)"
        self.assertEqual(repr(node), expected)

    def test_leaf_equality(self):
        node1 = LeafNode("p", "Same text", {"class": "same"})
        node2 = LeafNode("p", "Same text", {"class": "same"})
        self.assertEqual(node1, node2)

    def test_leaf_inequality_different_tag(self):
        node1 = LeafNode("p", "Same text")
        node2 = LeafNode("div", "Same text")
        self.assertNotEqual(node1, node2)

    def test_leaf_inequality_different_value(self):
        node1 = LeafNode("p", "Text 1")
        node2 = LeafNode("p", "Text 2")
        self.assertNotEqual(node1, node2)

    def test_leaf_inequality_different_props(self):
        node1 = LeafNode("p", "Same text", {"class": "one"})
        node2 = LeafNode("p", "Same text", {"class": "two"})
        self.assertNotEqual(node1, node2)

    def test_leaf_with_multiple_props(self):
        node = LeafNode(
            "img", "", {"src": "image.jpg", "alt": "Test image", "width": "100"})
        expected = '<img src="image.jpg" alt="Test image" width="100">'
        self.assertEqual(node.to_html(), expected)

    def test_leaf_with_special_characters_in_value(self):
        node = LeafNode("p", "Text with <special> & characters")
        # Note: This doesn't escape HTML entities, which might be a design choice
        self.assertEqual(
            node.to_html(), "<p>Text with <special> & characters</p>")

    def test_leaf_with_numbers_in_value(self):
        node = LeafNode("span", "123")
        self.assertEqual(node.to_html(), "<span>123</span>")

    def test_leaf_with_boolean_string_value(self):
        node = LeafNode("span", "True")
        self.assertEqual(node.to_html(), "<span>True</span>")


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


class TestTextNodeToHTML(unittest.TestCase):
    def test_text_node_to_html(self):
        text_node = TextNode("Hello, world!", TextType.TEXT)
        html_node = text_node_to_html(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.value, "Hello, world!")
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.props, None)

    def test_bold_text_node_to_html(self):
        text_node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.value, "Bold text")
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.props, None)

    def test_link_text_node_to_html(self):
        text_node = TextNode("Link text", TextType.LINK, url="https://example.com")
        html_node = text_node_to_html(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.value, "Link text")
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.props, {"href": "https://example.com"})

    def test_italic_text_node_to_html(self):
        text_node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.value, "Italic text")
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.props, None)

    def test_code_text_node_to_html(self):
        text_node = TextNode("Code text", TextType.CODE)
        html_node = text_node_to_html(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.value, "Code text")
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.props, None)

    def test_image_text_node_to_html(self):
        text_node = TextNode("Image alt text", TextType.IMAGE, url="https://example.com/image.jpg")
        html_node = text_node_to_html(text_node)
        self.assertIsInstance(html_node, LeafNode)
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.props, {"src": "https://example.com/image.jpg", "alt": "Image alt text"})

    def test_unsupported_text_type_raises_exception(self):
        # This test simulates an unsupported text type by modifying the enum temporarily
        text_node = TextNode("Test", TextType.TEXT)
        text_node.text_type = "unsupported"  # Simulate unsupported type
        with self.assertRaises(Exception) as e:
            text_node_to_html(text_node)
        self.assertIn("TextNode type not supported", str(e.exception))


class TestRegexFunctions(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)."
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_extract_markdown_images_multiple(self):
        text = "Here are two images: ![first](https://example.com/1.png) and ![second](https://example.com/2.jpg)"
        matches = extract_markdown_images(text)
        expected = [("first", "https://example.com/1.png"), ("second", "https://example.com/2.jpg")]
        self.assertListEqual(expected, matches)

    def test_extract_markdown_images_empty_alt_text(self):
        text = "Image with no alt text: ![](https://example.com/image.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("", "https://example.com/image.png")], matches)

    def test_extract_markdown_links_multiple(self):
        text = "Check out [Google](https://google.com) and [GitHub](https://github.com)"
        matches = extract_markdown_links(text)
        expected = [("Google", "https://google.com"), ("GitHub", "https://github.com")]
        self.assertListEqual(expected, matches)

    def test_extract_markdown_images_no_matches(self):
        text = "This text has no images"
        matches = extract_markdown_images(text)
        self.assertListEqual([], matches)

    def test_extract_markdown_links_no_matches(self):
        text = "This text has no links"
        matches = extract_markdown_links(text)
        self.assertListEqual([], matches)

    def test_extract_markdown_links_ignores_images(self):
        text = "This has an ![image](https://example.com/img.jpg) and a [link](https://example.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("link", "https://example.com")], matches)

    def test_extract_markdown_images_complex_urls(self):
        text = "Complex URL: ![test](https://example.com/path/to/image.jpg?param=value&another=param)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("test", "https://example.com/path/to/image.jpg?param=value&another=param")], matches)

    def test_extract_markdown_links_complex_urls(self):
        text = "Complex URL: [test](https://example.com/path?param=value&another=param#section)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("test", "https://example.com/path?param=value&another=param#section")], matches)


class TestSplitNodes(unittest.TestCase):
    def test_split_nodes_delimiter_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_delimiter_bold(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_delimiter_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_delimiter_no_delimiter(self):
        node = TextNode("This is plain text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [node])

    def test_split_nodes_delimiter_wrong_delimiter_for_code(self):
        node = TextNode("This is text", TextType.TEXT)
        with self.assertRaises(ValueError) as e:
            split_nodes_delimiter([node], "**", TextType.CODE)
        self.assertEqual(str(e.exception), "Delimiter for code must be '`'")

    def test_split_nodes_delimiter_wrong_delimiter_for_bold(self):
        node = TextNode("This is text", TextType.TEXT)
        with self.assertRaises(ValueError) as e:
            split_nodes_delimiter([node], "`", TextType.BOLD)
        self.assertEqual(str(e.exception), "Delimiter for bold must be '**'")

    def test_split_nodes_delimiter_wrong_delimiter_for_italic(self):
        node = TextNode("This is text", TextType.TEXT)
        with self.assertRaises(ValueError) as e:
            split_nodes_delimiter([node], "**", TextType.ITALIC)
        self.assertEqual(str(e.exception), "Delimiter for italic must be '_'")

    def test_split_nodes_delimiter_multiple_occurrences(self):
        node = TextNode("This has `code` and `more code` here", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This has ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("more code", TextType.CODE),
            TextNode(" here", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_delimiter_non_text_nodes_unchanged(self):
        text_node = TextNode("This has `code` here", TextType.TEXT)
        bold_node = TextNode("This is bold", TextType.BOLD)
        nodes = [text_node, bold_node]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        expected = [
            TextNode("This has ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" here", TextType.TEXT),
            bold_node  # Should remain unchanged
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_image(self):
        node = TextNode("This is text with an ![image](https://example.com/image.png) and more text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com/image.png"),
            TextNode(" and more text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_image_no_images(self):
        node = TextNode("This is plain text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(new_nodes, [node])

    def test_split_nodes_image_multiple_images(self):
        node = TextNode("Text ![img1](url1) middle ![img2](url2) end", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("Text ", TextType.TEXT),
            TextNode("img1", TextType.IMAGE, "url1"),
            TextNode(" middle ", TextType.TEXT),
            TextNode("img2", TextType.IMAGE, "url2"),
            TextNode(" end", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_link(self):
        node = TextNode("This is text with a [link](https://example.com) and more text", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(" and more text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_link_no_links(self):
        node = TextNode("This is plain text", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes, [node])

    def test_split_nodes_link_multiple_links(self):
        node = TextNode("Text [link1](url1) middle [link2](url2) end", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Text ", TextType.TEXT),
            TextNode("link1", TextType.LINK, "url1"),
            TextNode(" middle ", TextType.TEXT),
            TextNode("link2", TextType.LINK, "url2"),
            TextNode(" end", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_image_at_start(self):
        node = TextNode("![image](url) followed by text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [
            TextNode("", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "url"),
            TextNode(" followed by text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_link_at_end(self):
        node = TextNode("Text followed by [link](url)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [
            TextNode("Text followed by ", TextType.TEXT),
            TextNode("link", TextType.LINK, "url"),
        ]
        self.assertEqual(new_nodes, expected)
        

class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertEqual(nodes, expected)

    def test_text_to_textnodes_plain_text(self):
        text = "This is just plain text"
        nodes = text_to_textnodes(text)
        expected = [TextNode("This is just plain text", TextType.TEXT)]
        self.assertEqual(nodes, expected)

    def test_text_to_textnodes_only_bold(self):
        text = "**bold text**"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
        ]
        self.assertEqual(nodes, expected)

    def test_text_to_textnodes_only_italic(self):
        text = "_italic text_"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("", TextType.TEXT),
            TextNode("italic text", TextType.ITALIC),
        ]
        self.assertEqual(nodes, expected)

    def test_text_to_textnodes_only_code(self):
        text = "`code text`"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("", TextType.TEXT),
            TextNode("code text", TextType.CODE),
        ]
        self.assertEqual(nodes, expected)

    def test_text_to_textnodes_mixed_formatting(self):
        text = "Normal **bold** _italic_ `code` text"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("Normal ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(nodes, expected)

    def test_text_to_textnodes_complex_example(self):
        # Test a complex but valid example
        text = "Start **bold** then _italic_ and `code` end"
        nodes = text_to_textnodes(text)
        expected = [
            TextNode("Start ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" then ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" end", TextType.TEXT),
        ]
        self.assertEqual(nodes, expected)


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        markdown = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(markdown)
        expected = [
            "This is **bolded** paragraph",
            "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
            "- This is a list\n- with items"
        ]
        self.assertEqual(blocks, expected)

    def test_markdown_to_blocks_empty_blocks(self):
        markdown = """
Block 1


Block 2



Block 3
"""
        blocks = markdown_to_blocks(markdown)
        expected = ["Block 1", "Block 2", "Block 3"]
        self.assertEqual(blocks, expected)

    def test_markdown_to_blocks_whitespace(self):
        markdown = """  Block 1  

  Block 2  """
        blocks = markdown_to_blocks(markdown)
        expected = ["Block 1", "Block 2"]
        self.assertEqual(blocks, expected)

    def test_markdown_to_blocks_single_block(self):
        markdown = "Just one block"
        blocks = markdown_to_blocks(markdown)
        expected = ["Just one block"]
        self.assertEqual(blocks, expected)

    def test_markdown_to_blocks_empty_string(self):
        markdown = ""
        blocks = markdown_to_blocks(markdown)
        expected = []
        self.assertEqual(blocks, expected)

    def test_markdown_to_blocks_only_whitespace(self):
        markdown = "   \n\n   \n\n   "
        blocks = markdown_to_blocks(markdown)
        expected = []
        self.assertEqual(blocks, expected)

    def test_markdown_to_blocks_complex_content(self):
        markdown = """
# Heading 1

This is a paragraph with **bold** and *italic* text.

## Heading 2

1. List item 1
2. List item 2
3. List item 3

Another paragraph here.

```python
def hello():
    print("Hello, world!")
```

Final paragraph.
"""
        blocks = markdown_to_blocks(markdown)
        expected = [
            "# Heading 1",
            "This is a paragraph with **bold** and *italic* text.",
            "## Heading 2",
            "1. List item 1\n2. List item 2\n3. List item 3",
            "Another paragraph here.",
            "```python\ndef hello():\n    print(\"Hello, world!\")\n```",
            "Final paragraph."
        ]
        self.assertEqual(blocks, expected)


class TestBlockToBlockTypes(unittest.TestCase):
    def test_unordered_list_block_to_block_type(self):
        block = "- This is a list\n- with a few\n- items"
        
        block_type = block_to_blocktype(block)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)

    def test_ordered_list_block_to_block_type(self):
        block = "1. This is a list\n2. with a few\n3. items"
        
        block_type = block_to_blocktype(block)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)

    def test_paragraph_block_to_block_type(self):
        block = "This is a paragraph with some text."
        
        block_type = block_to_blocktype(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_code_block_to_block_type(self):
        block = "```python\nprint('Hello, world!')\n```"
        
        block_type = block_to_blocktype(block)
        self.assertEqual(block_type, BlockType.CODE)

    def test_quote_block_to_block_type(self):
        block = "> This is a quote\n> with multiple lines"
        
        block_type = block_to_blocktype(block)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_heading_block_to_block_type(self):
        block = "# This is a heading"
        
        block_type = block_to_blocktype(block)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_heading_two_block_to_block_type(self):
        block = "## This is a subheading"
        
        block_type = block_to_blocktype(block)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_heading_three_block_to_block_type(self):
        block = "### This is a sub-subheading"
        
        block_type = block_to_blocktype(block)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_heading_four_block_to_block_type(self):
        block = "#### This is a sub-sub-subheading"
        
        block_type = block_to_blocktype(block)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_heading_five_block_to_block_type(self):
        block = "##### This is a sub-sub-sub-subheading"
        
        block_type = block_to_blocktype(block)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_heading_six_block_to_block_type(self):
        block = "###### This is a sub-sub-sub-sub-subheading"
        
        block_type = block_to_blocktype(block)
        self.assertEqual(block_type, BlockType.HEADING)


class TestMarkdownToHtmlNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_headings(self):
        md = """
# Heading 1

## Heading 2

### Heading 3
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3</h3></div>",
        )
    
    def test_code(self):
        md = """
```
def hello():
    print("Hello, world!")
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><pre><code>def hello():\n    print("Hello, world!")\n</code></pre></div>',
        )

    def test_code_oneline(self):
        md = """
```
This is Code.
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><code>This is Code.</code></div>',
        )

    def test_quotes(self):
        md = "> This is a **quote**"

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><blockquote>This is a <b>quote</b></blockquote></div>',
        )

    def test_unordered_list(self):
        md = """
- This is a list
- with items
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><ul><li>This is a list</li><li>with items</li></ul></div>',
        )

    def test_ordered_list(self):
        md = """
1. This is a list
2. with items
3. and more items
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><ol><li>This is a list</li><li>with items</li><li>and more items</li></ol></div>',
        )

    def test_mixed_content(self):
        md = """
# Heading

This is a paragraph with **bold** text and _italic_ text.

- List item 1
- List item 2

> This is a quote.

```
print("Hello, world!")
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><h1>Heading</h1><p>This is a paragraph with <b>bold</b> text and <i>italic</i> text.</p><ul><li>List item 1</li><li>List item 2</li></ul><blockquote>This is a quote.</blockquote><code>print("Hello, world!")</code></div>',
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_paragraph_with_image(self):
        md = """
This is a paragraph with an ![image](https://example.com/image.png) in it.
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><p>This is a paragraph with an <img src="https://example.com/image.png" alt="image"> in it.</p></div>',
        )


class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        md = """
# This is the title

This is a paragraph.
"""
        title = extract_title(md)
        self.assertEqual(title, "This is the title")

    def test_extract_title_no_title(self):
        md = """
This is a paragraph without a title.
"""
        self.assertRaises(Exception, extract_title, md)

if __name__ == "__main__":
    unittest.main()
