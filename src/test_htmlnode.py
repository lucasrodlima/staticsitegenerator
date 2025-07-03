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


if __name__ == "__main__":
    unittest.main()
