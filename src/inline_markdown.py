import re
from textnode import (
    TextNode,
    text_type_bold,
    text_type_code,
    text_type_image,
    text_type_italic,
    text_type_link,
    text_type_text,
)


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


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)
