from __future__ import annotations

import re

from htmlnode import LeafNode

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"


class TextNode:
    def __init__(self, text: str, text_type: str, url: str = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other: TextNode) -> bool:
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    if text_node.text_type == text_type_text:
        return LeafNode(tag=None, value=text_node.text)
    if text_node.text_type == text_type_bold:
        return LeafNode(tag="b", value=text_node.text)
    if text_node.text_type == text_type_italic:
        return LeafNode(tag="i", value=text_node.text)
    if text_node.text_type == text_type_code:
        return LeafNode(tag="code", value=text_node.text)
    if text_node.text_type == text_type_link:
        return LeafNode(tag="a", value=text_node.text, props={"href": text_node.url})
    if text_node.text_type == text_type_image:
        return LeafNode(
            tag="img", value="", props={"src": text_node.url, "alt": text_node.text}
        )
    raise Exception(f"Unknown node type {text_node.text_type}")


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: str
) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        split_strings = node.text.split(delimiter)
        if len(split_strings) % 2 == 0:
            raise Exception(f"Invalid Markdown syntax. No closing {delimiter} found.")

        for i, n in enumerate(split_strings):
            if len(n) == 0:
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(text=n, text_type=text_type_text))
            else:
                new_nodes.append(TextNode(text=n, text_type=text_type))
    return new_nodes


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        images: list[tuple[str, str]] = extract_markdown_images(node.text)
        if not images:
            new_nodes.append(node)
            continue
        text = node.text
        for alt, url in images:
            text_node_text, _, text = text.partition(f"![{alt}]({url})")
            if text_node_text:
                new_nodes.append(
                    TextNode(text=text_node_text, text_type=text_type_text)
                )
            new_nodes.append(TextNode(text_type=text_type_image, text=alt, url=url))
        if text:
            new_nodes.append(TextNode(text=text, text_type=text_type_text))
    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        links: list[tuple[str, str]] = extract_markdown_links(node.text)
        if not links:
            new_nodes.append(node)
            continue
        text = node.text
        for val, url in links:
            text_node_text, _, text = text.partition(f"[{val}]({url})")
            if text_node_text:
                new_nodes.append(
                    TextNode(text=text_node_text, text_type=text_type_text)
                )
            new_nodes.append(TextNode(text_type=text_type_link, text=val, url=url))
        if text:
            new_nodes.append(TextNode(text=text, text_type=text_type_text))
    return new_nodes


def text_to_textnodes(text: str) -> list[TextNode]:
    return split_nodes_link(
        split_nodes_image(
            split_nodes_delimiter(
                split_nodes_delimiter(
                    split_nodes_delimiter(
                        [TextNode(text=text, text_type=text_type_text)],
                        delimiter="**",
                        text_type=text_type_bold,
                    ),
                    delimiter="*",
                    text_type=text_type_italic,
                ),
                delimiter="`",
                text_type=text_type_code,
            )
        )
    )


def markdown_to_blocks(markdown: str) -> list[str]:
    return [block.strip() for block in markdown.split("\n\n") if block]


text = """This is **bolded** paragraph








This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items"""

print(markdown_to_blocks(text))
