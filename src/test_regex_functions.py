import unittest

from regex_functions import extract_markdown_images, extract_markdown_links
from textnode import TextType

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

    def test_extract_markdown_images_empty_url(self):
        text = "Image with no URL: ![alt text]()"
        matches = extract_markdown_images(text)
        self.assertListEqual([("alt text", "")], matches)

    def test_extract_markdown_images_no_images(self):
        text = "This text has no images at all."
        matches = extract_markdown_images(text)
        self.assertListEqual([], matches)

    def test_extract_markdown_images_with_links_mixed(self):
        text = "Mixed content: ![image](https://example.com/img.png) and [link](https://example.com)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("image", "https://example.com/img.png")], matches)

    def text_extract_markdown_links_with_images_mixed(self):
        text = "Mixed content: [link](https://example.com) and ![image](https://example.com/img.png)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("link", "https://example.com")], matches)

    def test_extract_markdown_images_special_characters_in_alt(self):
        text = "![Image with special chars: @#$%^&*()!](https://example.com/img.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("Image with special chars: @#$%^&*()!", "https://example.com/img.png")], matches)

    def test_extract_markdown_images_spaces_in_alt(self):
        text = "![Image with   multiple   spaces](https://example.com/img.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("Image with   multiple   spaces", "https://example.com/img.png")], matches)

    def test_extract_markdown_images_multiline(self):
        text = """This is a multiline text
        with an image ![test image](https://example.com/img.png) in it
        and some more text"""
        matches = extract_markdown_images(text)
        self.assertListEqual([("test image", "https://example.com/img.png")], matches)

    def test_extract_markdown_links_multiple(self):
        text = "Check out [Google](https://google.com) and [GitHub](https://github.com) for more info."
        matches = extract_markdown_links(text)
        expected = [("Google", "https://google.com"), ("GitHub", "https://github.com")]
        self.assertListEqual(expected, matches)

    def test_extract_markdown_links_empty_text(self):
        text = "Link with no text: [](https://example.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("", "https://example.com")], matches)

    def test_extract_markdown_links_empty_url(self):
        text = "Link with no URL: [click here]()"
        matches = extract_markdown_links(text)
        self.assertListEqual([("click here", "")], matches)

    def test_extract_markdown_links_no_links(self):
        text = "This text has no links at all."
        matches = extract_markdown_links(text)
        self.assertListEqual([], matches)

    def test_extract_markdown_links_special_characters_in_text(self):
        text = "[Link with special chars: @#$%^&*()!](https://example.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("Link with special chars: @#$%^&*()!", "https://example.com")], matches)

    def test_extract_markdown_links_spaces_in_text(self):
        text = "[Link with   multiple   spaces](https://example.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("Link with   multiple   spaces", "https://example.com")], matches)

    def test_extract_markdown_links_multiline(self):
        text = """This is a multiline text
        with a link [test link](https://example.com) in it
        and some more text"""
        matches = extract_markdown_links(text)
        self.assertListEqual([("test link", "https://example.com")], matches)

    def test_extract_markdown_links_nested_brackets(self):
        text = "Link with [nested [brackets] inside](https://example.com)"
        matches = extract_markdown_links(text)
        # The regex uses non-greedy matching, so it captures everything up to the first closing bracket
        self.assertListEqual([("nested [brackets] inside", "https://example.com")], matches)

    def test_extract_markdown_images_nested_brackets(self):
        text = "Image with ![nested [brackets] inside](https://example.com/img.png)"
        matches = extract_markdown_images(text)
        # The regex uses non-greedy matching, so it captures everything up to the first closing bracket
        self.assertListEqual([("nested [brackets] inside", "https://example.com/img.png")], matches)

    def test_extract_markdown_images_complex_urls(self):
        text = "![Complex URL](https://example.com/path/to/image.png?query=value&another=param#fragment)"
        matches = extract_markdown_images(text)
        self.assertListEqual([("Complex URL", "https://example.com/path/to/image.png?query=value&another=param#fragment")], matches)

    def test_extract_markdown_links_complex_urls(self):
        text = "[Complex URL](https://example.com/path/to/page?query=value&another=param#fragment)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("Complex URL", "https://example.com/path/to/page?query=value&another=param#fragment")], matches)

    def test_extract_markdown_images_relative_paths(self):
        text = "![Local image](./images/local.png) and ![Another local](../assets/img.jpg)"
        matches = extract_markdown_images(text)
        expected = [("Local image", "./images/local.png"), ("Another local", "../assets/img.jpg")]
        self.assertListEqual(expected, matches)

    def test_extract_markdown_links_relative_paths(self):
        text = "[Local page](./pages/about.html) and [Another page](../docs/readme.md)"
        matches = extract_markdown_links(text)
        expected = [("Local page", "./pages/about.html"), ("Another page", "../docs/readme.md")]
        self.assertListEqual(expected, matches)

    def test_extract_markdown_images_with_title_attributes(self):
        # This tests the current behavior - the regex doesn't handle title attributes
        text = '![Alt text](https://example.com/img.png "Title text")'
        matches = extract_markdown_images(text)
        self.assertListEqual([("Alt text", 'https://example.com/img.png "Title text"')], matches)

    def test_extract_markdown_links_with_title_attributes(self):
        # This tests the current behavior - the regex doesn't handle title attributes
        text = '[Link text](https://example.com "Title text")'
        matches = extract_markdown_links(text)
        self.assertListEqual([("Link text", 'https://example.com "Title text"')], matches)

    def test_extract_markdown_images_escaped_characters(self):
        text = r"![Alt with \[\] brackets](https://example.com/img.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual([(r"Alt with \[\] brackets", "https://example.com/img.png")], matches)

    def test_extract_markdown_links_escaped_characters(self):
        text = r"[Link with \[\] brackets](https://example.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual([(r"Link with \[\] brackets", "https://example.com")], matches)

    def test_extract_markdown_images_unicode_characters(self):
        text = "![测试图片](https://example.com/img.png) and ![🖼️ emoji](https://example.com/emoji.png)"
        matches = extract_markdown_images(text)
        expected = [("测试图片", "https://example.com/img.png"), ("🖼️ emoji", "https://example.com/emoji.png")]
        self.assertListEqual(expected, matches)

    def test_extract_markdown_links_unicode_characters(self):
        text = "[测试链接](https://example.com) and [🔗 emoji](https://example.com/emoji)"
        matches = extract_markdown_links(text)
        expected = [("测试链接", "https://example.com"), ("🔗 emoji", "https://example.com/emoji")]
        self.assertListEqual(expected, matches)

    def test_extract_markdown_images_malformed_missing_closing_bracket(self):
        text = "Malformed image: ![alt text(https://example.com/img.png)"
        matches = extract_markdown_images(text)
        # Should not match malformed markdown
        self.assertListEqual([], matches)

    def test_extract_markdown_links_malformed_missing_closing_bracket(self):
        text = "Malformed link: [link text(https://example.com)"
        matches = extract_markdown_links(text)
        # Should not match malformed markdown
        self.assertListEqual([], matches)

    def test_extract_markdown_images_malformed_missing_opening_paren(self):
        text = "Malformed image: ![alt text]https://example.com/img.png)"
        matches = extract_markdown_images(text)
        # Should not match malformed markdown
        self.assertListEqual([], matches)

    def test_extract_markdown_links_malformed_missing_opening_paren(self):
        text = "Malformed link: [link text]https://example.com)"
        matches = extract_markdown_links(text)
        # Should not match malformed markdown
        self.assertListEqual([], matches)

    def test_extract_markdown_images_adjacent_to_text(self):
        text = "Before![image](https://example.com/img.png)After"
        matches = extract_markdown_images(text)
        self.assertListEqual([("image", "https://example.com/img.png")], matches)

    def test_extract_markdown_links_adjacent_to_text(self):
        text = "Before[link](https://example.com)After"
        matches = extract_markdown_links(text)
        self.assertListEqual([("link", "https://example.com")], matches)

    def test_extract_markdown_images_with_newlines_in_alt(self):
        text = "![alt text\nwith newline](https://example.com/img.png)"
        matches = extract_markdown_images(text)
        # The regex doesn't match across newlines by default (. doesn't match \n)
        self.assertListEqual([], matches)

    def test_extract_markdown_links_with_newlines_in_text(self):
        text = "[link text\nwith newline](https://example.com)"
        matches = extract_markdown_links(text)
        # The regex doesn't match across newlines by default (. doesn't match \n)
        self.assertListEqual([], matches)

    def test_extract_markdown_images_very_long_alt_text(self):
        long_alt = "A" * 1000  # Very long alt text
        text = f"![{long_alt}](https://example.com/img.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual([(long_alt, "https://example.com/img.png")], matches)

    def test_extract_markdown_links_very_long_text(self):
        long_text = "A" * 1000  # Very long link text
        text = f"[{long_text}](https://example.com)"
        matches = extract_markdown_links(text)
        self.assertListEqual([(long_text, "https://example.com")], matches)

    def test_extract_markdown_images_very_long_url(self):
        long_url = "https://example.com/" + "a" * 1000  # Very long URL
        text = f"![image]({long_url})"
        matches = extract_markdown_images(text)
        self.assertListEqual([("image", long_url)], matches)

    def test_extract_markdown_links_very_long_url(self):
        long_url = "https://example.com/" + "a" * 1000  # Very long URL
        text = f"[link]({long_url})"
        matches = extract_markdown_links(text)
        self.assertListEqual([("link", long_url)], matches)

if __name__ == "__main__":
    unittest.main()