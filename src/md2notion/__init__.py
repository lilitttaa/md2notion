import json
from typing import List, Mapping, MappingView, Sequence, Union
import mistletoe
from mistletoe.ast_renderer import ASTRenderer
from notion_client import Client


# Notion API:https://developers.notion.com/reference/block


class MarkdownTransformer:
    def __init__(self, markdown_str: str):
        self.markdown_str = markdown_str

    def trans_to_ast_node(self):
        ast_node_str = mistletoe.markdown(self.markdown_str, ASTRenderer)
        ast_node = json.loads(ast_node_str)
        return ast_node


class NotionPageUploader:
    def __init__(self) -> None:
        pass

    def upload(self, token: str, notion_page: dict) -> None:
        notion = Client(auth=token)
        notion.pages.create(**notion_page)


class NotionPageGenerator:
    def __init__(self) -> None:
        pass

    def generate(self, parent_page_id: str, title: str, ast_node: dict) -> dict:
        if not ast_node:
            raise ValueError("ast_node is empty")
        if ast_node["type"] != "Document":
            raise ValueError("ast_node is not a Document")
        children = []
        children.append(
            {"type": "table_of_contents", "table_of_contents": {"color": "default"}}
        )
        for child in ast_node["children"]:
            for block in self._generate_notion_blocks(child):
                children.append(block)
        return {
            "parent": {
                "page_id": parent_page_id,
            },
            "properties": {
                "title": {
                    "title": [{"type": "text", "text": {"content": title}}],
                },
            },
            "children": children,
        }

    def _generate_notion_blocks(self, ast_node: dict) -> List[dict]:
        if ast_node["type"] == "Heading":
            level = ast_node["level"]
            type = f"heading_{level}"
            content = ast_node["children"][0]["content"]
            return [
                {
                    "object": "block",
                    "type": type,
                    type: {
                        "rich_text": [{"type": "text", "text": {"content": content}}]
                    },
                }
            ]
        elif ast_node["type"] == "Paragraph":
            if ast_node["children"][0]["type"] == "RawText":
                return [
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [
                                {
                                    "type": "text",
                                    "text": {
                                        "content": ast_node["children"][0]["content"]
                                    },
                                }
                            ]
                        },
                    }
                ]
            elif ast_node["children"][0]["type"] == "AutoLink":
                return [
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [
                                {
                                    "type": "text",
                                    "text": {
                                        "content": ast_node["children"][0]["target"]
                                    },
                                    "href": ast_node["children"][0]["target"],
                                }
                            ],
                        },
                    }
                ]
            else:
                raise ValueError(
                    f"ast_node type {ast_node['children'][0]['type']} is not supported"
                )
        elif ast_node["type"] == "List" and ast_node["start"] != None:
            return self._generate_list_block(ast_node["children"])
        elif ast_node["type"] == "ListItem":
            return [
                {
                    "object": "block",
                    "type": "numbered_list_item",
                    "numbered_list_item": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": ast_node["children"][0]["children"][0][
                                        "content"
                                    ]
                                },
                            }
                        ],
                        "children": self._generate_list_block(ast_node["children"][1:]),
                    },
                }
            ]
        elif ast_node["type"] == "CodeFence":
            return [
                {
                    "type": "code",
                    "code": {
                        "caption": [],
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {"content": ast_node["children"][0]["content"]},
                            }
                        ],
                        "language": ast_node["language"],
                    },
                }
            ]
        else:
            raise ValueError(f"ast_node type {ast_node['type']} is not supported")

    def _generate_list_block(self, child_nodes: List[dict]) -> list[dict]:
        return [
            block
            for node in child_nodes
            for block in self._generate_notion_blocks(node)
        ]
