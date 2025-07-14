import unittest
from markdown_to_blocks import markdown_to_blocks


class TestMarkDownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)

        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_extra_inbetween_newline_markdown_to_blocks(self):
        md = """
This is a paragraph with an extra newline below


This is another paragraph
"""
        blocks = markdown_to_blocks(md)

        self.assertEqual(
            blocks,
            [
                "This is a paragraph with an extra newline below",
                "This is another paragraph",
            ],
        )

    def test_empty_markdown(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_single_block_no_newlines(self):
        md = "This is a single paragraph with no double newlines"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a single paragraph with no double newlines"])

    def test_only_whitespace(self):
        md = "   \n\n   \n\n   "
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_multiple_consecutive_newlines(self):
        md = """
First paragraph



Second paragraph after many newlines


Third paragraph
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "First paragraph",
                "Second paragraph after many newlines",
                "Third paragraph",
            ],
        )

    def test_leading_and_trailing_whitespace(self):
        md = """   

    This paragraph has leading/trailing spaces    

Another paragraph with tabs	and spaces   

   """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This paragraph has leading/trailing spaces",
                "Another paragraph with tabs	and spaces",
            ],
        )

    def test_code_blocks(self):
        md = """Here is a code block:

```python
def hello():
    print("Hello, World!")
```

And here is inline `code` in a paragraph."""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "Here is a code block:",
                '```python\ndef hello():\n    print("Hello, World!")\n```',
                "And here is inline `code` in a paragraph.",
            ],
        )

    def test_headers_and_formatting(self):
        md = """# Main Header

## Sub Header

**Bold text** and *italic text*

> This is a blockquote
> spanning multiple lines

1. Numbered list item
2. Another numbered item"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# Main Header",
                "## Sub Header",
                "**Bold text** and *italic text*",
                "> This is a blockquote\n> spanning multiple lines",
                "1. Numbered list item\n2. Another numbered item",
            ],
        )

    def test_mixed_content_with_links(self):
        md = """Check out [this link](https://example.com)

![Alt text](image.jpg)

---

Horizontal rule above and table below:

| Column 1 | Column 2 |
|----------|----------|
| Cell 1   | Cell 2   |"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "Check out [this link](https://example.com)",
                "![Alt text](image.jpg)",
                "---",
                "Horizontal rule above and table below:",
                "| Column 1 | Column 2 |\n|----------|----------|\n| Cell 1   | Cell 2   |",
            ],
        )

    def test_nested_lists(self):
        md = """- Top level item
  - Nested item
  - Another nested item
- Second top level

* Different bullet style
  * Nested with asterisk
    * Double nested"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "- Top level item\n  - Nested item\n  - Another nested item\n- Second top level",
                "* Different bullet style\n  * Nested with asterisk\n    * Double nested",
            ],
        )


if __name__ == "__main__":
    unittest.main()

