import unittest

from inline_markdown import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
from textnode import (
    TextNode,
    text_type_bold,
    text_type_code,
    text_type_image,
    text_type_italic,
    text_type_link,
    text_type_text,
)


class TestInlineMarkdown(unittest.TestCase):
    def test_split_nodes_delimiter1(self):
        node = TextNode(
            text="This is text with a `code block` word", text_type=text_type_text
        )
        new_nodes = split_nodes_delimiter([node], "`", text_type_code)
        self.assertEqual(
            [
                TextNode("This is text with a ", text_type_text),
                TextNode("code block", text_type_code),
                TextNode(" word", text_type_text),
            ],
            new_nodes,
        )

    def test_split_nodes_delimiter2(self):
        node = TextNode("**This is** text with a bold block word", text_type_text)
        self.assertEqual(
            [
                TextNode(text="This is", text_type=text_type_bold),
                TextNode(text=" text with a bold block word", text_type=text_type_text),
            ],
            split_nodes_delimiter([node], delimiter="**", text_type=text_type_bold),
        )

    def test_split_nodes_delimiter_bold_and_italic(self):
        node = TextNode(
            text="**This is bold**, and *this is italic* text.",
            text_type=text_type_text,
        )
        new_nodes = split_nodes_delimiter(
            [node], delimiter="**", text_type=text_type_bold
        )
        self.assertEqual(
            [
                TextNode(text="This is bold", text_type=text_type_bold),
                TextNode(text=", and *this is italic* text.", text_type=text_type_text),
            ],
            new_nodes,
        )
        self.assertEqual(
            [
                TextNode(text="This is bold", text_type=text_type_bold),
                TextNode(text=", and ", text_type=text_type_text),
                TextNode(text="this is italic", text_type=text_type_italic),
                TextNode(text=" text.", text_type=text_type_text),
            ],
            split_nodes_delimiter(new_nodes, delimiter="*", text_type=text_type_italic),
        )

    def test_split_nodes_delimiter_no_matching_delimiter_raises_value_error(self):
        node = TextNode(
            text="This is text ** with no closing bold syntax", text_type=text_type_text
        )
        with self.assertRaises(Exception):
            split_nodes_delimiter(
                old_nodes=[node], delimiter="**", text_type=text_type_bold
            )

    def test_split_nodes_image(self):
        node = TextNode(
            "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png) and text at the end.",
            text_type_text,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(
            [
                TextNode("This is text with an ", text_type_text),
                TextNode(
                    "image",
                    text_type_image,
                    "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
                ),
                TextNode(" and another ", text_type_text),
                TextNode(
                    "second image",
                    text_type_image,
                    "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png",
                ),
                TextNode(text=" and text at the end.", text_type=text_type_text),
            ],
            new_nodes,
        )

    def test_split_nodes_image_with_no_images(self):
        node = TextNode(text="Just Text, no image", text_type=text_type_text)
        self.assertEqual(
            [TextNode(text="Just Text, no image", text_type=text_type_text)],
            split_nodes_image([node]),
        )

    def test_split_nodes_link(self):
        node = TextNode(
            text="This is text with a [link](https://www.example.com) and [another](https://www.example.com/another). Here is also text.",
            text_type=text_type_text,
        )
        self.assertEqual(
            [
                TextNode(text="This is text with a ", text_type=text_type_text),
                TextNode(
                    text="link", text_type=text_type_link, url="https://www.example.com"
                ),
                TextNode(text=" and ", text_type=text_type_text),
                TextNode(
                    text="another",
                    text_type=text_type_link,
                    url="https://www.example.com/another",
                ),
                TextNode(text=". Here is also text.", text_type=text_type_text),
            ],
            split_nodes_link([node]),
        )

    def test_split_nodes_link_with_no_links(self):
        node = TextNode(text="Just Text, no links", text_type=text_type_text)
        self.assertEqual(
            [TextNode(text="Just Text, no links", text_type=text_type_text)],
            split_nodes_image([node]),
        )

    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"

        self.assertEqual(
            [
                TextNode("This is ", text_type_text),
                TextNode("text", text_type_bold),
                TextNode(" with an ", text_type_text),
                TextNode("italic", text_type_italic),
                TextNode(" word and a ", text_type_text),
                TextNode("code block", text_type_code),
                TextNode(" and an ", text_type_text),
                TextNode(
                    "image",
                    text_type_image,
                    "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
                ),
                TextNode(" and a ", text_type_text),
                TextNode("link", text_type_link, "https://boot.dev"),
            ],
            text_to_textnodes(text),
        )

    def test_extract_markdown_images(self):
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"

        self.assertEqual(
            [
                (
                    "image",
                    "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png",
                ),
                (
                    "another",
                    "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png",
                ),
            ],
            extract_markdown_images(text),
        )

    def test_extract_markdown_links(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        self.assertEqual(
            [
                ("link", "https://www.example.com"),
                ("another", "https://www.example.com/another"),
            ],
            extract_markdown_links(text),
        )


if __name__ == "__main__":
    unittest.main()
