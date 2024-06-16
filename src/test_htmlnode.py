import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_with_no_props(self):
        node = HTMLNode()
        self.assertEqual(None, node.props_to_html())

    def test_props_to_html_one_prop(self):
        node = HTMLNode(props={"href": "https://www.google.com"})
        self.assertEqual(' href="https://www.google.com"', node.props_to_html())

    def test_props_to_html_two_props(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(
            ' href="https://www.google.com" target="_blank"', node.props_to_html()
        )


class TestLeafNode(unittest.TestCase):
    def test_to_html_no_value_should_raise_value_error(self):
        with self.assertRaises(ValueError):
            LeafNode(value=None).to_html()

    def test_to_html_with_only_value_shoud_return_str(self):
        node = LeafNode(value="Hello, World!")
        self.assertEqual("Hello, World!", node.to_html())

    def test_to_html_with_tag_value(self):
        node = LeafNode(tag="p", value="This is a paragraph of text.")
        self.assertEqual("<p>This is a paragraph of text.</p>", node.to_html())

    def test_to_html_with_tag_value_props(self):
        node = LeafNode(
            tag="a", value="Click me!", props={"href": "https://www.google.com"}
        )
        self.assertEqual(
            '<a href="https://www.google.com">Click me!</a>', node.to_html()
        )


class TestParentNode(unittest.TestCase):
    def test_to_html_with_one_child(self):
        node = ParentNode(tag="p", children=[LeafNode(tag="b", value="Bold text")])
        self.assertEqual("<p><b>Bold text</b></p>", node.to_html())

    def test_to_html_with_two_children(self):
        node = ParentNode(
            tag="p",
            children=[
                LeafNode(tag="b", value="Bold text"),
                LeafNode(tag=None, value="Normal text"),
            ],
        )
        self.assertEqual("<p><b>Bold text</b>Normal text</p>", node.to_html())

    def test_to_html_with_four_children(self):
        node = ParentNode(
            tag="p",
            children=[
                LeafNode(tag="b", value="Bold text"),
                LeafNode(tag=None, value="Normal text"),
                LeafNode(tag="i", value="italic text"),
                LeafNode(tag=None, value="Normal text"),
            ],
        )
        self.assertEqual(
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
            node.to_html(),
        )

    def test_to_html_one_nested_parent_one_child(self):
        node = ParentNode(
            tag="p",
            children=[
                ParentNode(tag="p", children=[LeafNode(tag="b", value="Bold text")])
            ],
        )
        self.assertEqual("<p><p><b>Bold text</b></p></p>", node.to_html())

    def test_to_html_one_nested_parent_two_children(self):
        node = ParentNode(
            tag="p",
            children=[
                ParentNode(
                    tag="p",
                    children=[
                        LeafNode(tag="b", value="Bold text"),
                        LeafNode(
                            tag="a", value="Click me!", props={"href": "www.google.com"}
                        ),
                    ],
                )
            ],
        )
        self.assertEqual(
            '<p><p><b>Bold text</b><a href="www.google.com">Click me!</a></p></p>',
            node.to_html(),
        )

    def test_to_html_two_nested_parents_two_children(self):
        node = ParentNode(
            tag="p",
            children=[
                LeafNode(tag=None, value="Normal text"),
                ParentNode(
                    tag="p",
                    children=[
                        LeafNode(tag="b", value="Bold text"),
                        LeafNode(
                            tag="a", value="Click me!", props={"href": "www.google.com"}
                        ),
                        ParentNode(
                            tag="i", children=[LeafNode(tag="b", value="This is text")]
                        ),
                    ],
                ),
            ],
        )
        self.assertEqual(
            '<p>Normal text<p><b>Bold text</b><a href="www.google.com">Click me!</a><i><b>This is text</b></i></p></p>',
            node.to_html(),
        )


if __name__ == "__main__":
    unittest.main()
