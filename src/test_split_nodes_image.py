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

if __name__ == "__main__":
    unittest.main()