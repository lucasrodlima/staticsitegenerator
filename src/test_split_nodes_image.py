import unittest

from split_nodes import split_nodes_image
from textnode import TextNode, TextType

class SplitNodesImageTest(unittest.TestCase):
    def test_split_image(self):
        node = TextNode("This is a text with an ![image](https://example.com/image.png) word", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is a text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://example.com/image.png"),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_split_multiple_images(self):
        node = TextNode("This is a text with an ![image1](https://example.com/image1.png) and ![image2](https://example.com/image2.png) word", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is a text with an ", TextType.TEXT),
                TextNode("image1", TextType.IMAGE, "https://example.com/image1.png"),
                TextNode(" and ", TextType.TEXT),
                TextNode("image2", TextType.IMAGE, "https://example.com/image2.png"),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_with_multiple_texts_with_images(self):
        node1 = TextNode("This is a text with an ![image1](https://example.com/image1.png)", TextType.TEXT)
        node2 = TextNode("And this is another text with an ![image2](https://example.com/image2.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node1, node2])
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is a text with an ", TextType.TEXT),
                TextNode("image1", TextType.IMAGE, "https://example.com/image1.png"),
                TextNode("And this is another text with an ", TextType.TEXT),
                TextNode("image2", TextType.IMAGE, "https://example.com/image2.png"),
            ],
        )

    def test_no_images(self):
        node = TextNode("This is a text without images", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(new_nodes, [node])

    def test_image_with_no_alt_text(self):
        node = TextNode("This is a text with an ![](https://example.com/image.png) word", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is a text with an ", TextType.TEXT),
                TextNode("", TextType.IMAGE, "https://example.com/image.png"),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_image_at_end(self):
        node = TextNode("This is a text with an ![image](https://example.com/image.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is a text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://example.com/image.png"),
            ],
        )

    def test_image_with_no_url(self):
        node = TextNode("This is a text with an ![image]() word", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            new_nodes,
            [
                TextNode("This is a text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, ""),
                TextNode(" word", TextType.TEXT),
            ],
        )

if __name__ == "__main__":
    unittest.main()