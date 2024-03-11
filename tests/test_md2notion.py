import os
import pytest
from md2notion import MarkdownTransformer, NotionPageUploader, NotionPageGenerator
from tests.utils import assert_is_dict_contain_dict


@pytest.fixture
def markdown_heading():
    return """
# Heading1
## Heading2
### Heading3
"""


@pytest.fixture
def markdown_code():
    return """
```lua
xxx
```
"""


@pytest.fixture
def markdown_number_list():
    return """
# 什么是 TDD(Test Driven Development)
1. TDD 用最简单的话来说,就是实现之前先写测试.
2. 可以拆解为三个步骤
"""


@pytest.fixture
def markdown_nested_number_list():
    return """# 什么是 TDD(Test Driven Development)
1. TDD 用最简单的话来说,就是实现之前先写测试.
2. 可以拆解为三个步骤:

   Red:先写测试代码, 由于此时缺少实现, 所以测试代码会失败
   Green:编写实现代码, 使得测试代码通过
"""


def test_given_markdown_str_when_transform_then_return_ast_node(
    markdown_heading: str,
    markdown_code: str,
    markdown_number_list: str,
    markdown_nested_number_list: str,
):
    def test_markdown_heading():
        root_node = MarkdownTransformer(markdown_heading).trans_to_ast_node()
        assert_is_dict_contain_dict(
            root_node,
            {
                "type": "Document",
                "children": [
                    {
                        "type": "Heading",
                        "level": 1,
                        "children": [{"type": "RawText", "content": "Heading1"}],
                    },
                    {
                        "type": "Heading",
                        "level": 2,
                        "children": [{"type": "RawText", "content": "Heading2"}],
                    },
                    {
                        "type": "Heading",
                        "level": 3,
                        "children": [{"type": "RawText", "content": "Heading3"}],
                    },
                ],
            },
        )

    test_markdown_heading()

    def test_markdown_code():
        root_node = MarkdownTransformer(markdown_code).trans_to_ast_node()
        assert_is_dict_contain_dict(
            root_node,
            {
                "type": "Document",
                "children": [
                    {
                        "type": "CodeFence",
                        "language": "lua",
                        "children": [
                            {
                                "type": "RawText",
                                "content": "xxx\n",
                            }
                        ],
                    }
                ],
            },
        )

    test_markdown_code()

    def test_markdown_number_list():
        root_node = MarkdownTransformer(markdown_number_list).trans_to_ast_node()
        assert_is_dict_contain_dict(
            root_node,
            {
                "type": "Document",
                "children": [
                    {
                        "type": "Heading",
                        "level": 1,
                        "children": [
                            {
                                "type": "RawText",
                                "content": "什么是 TDD(Test Driven Development)",
                            }
                        ],
                    },
                    {
                        "type": "List",
                        "start": 1,
                        "children": [
                            {
                                "type": "ListItem",
                                "children": [
                                    {
                                        "type": "Paragraph",
                                        "children": [
                                            {
                                                "type": "RawText",
                                                "content": "TDD 用最简单的话来说,就是实现之前先写测试.",
                                            }
                                        ],
                                    }
                                ],
                            },
                            {
                                "type": "ListItem",
                                "children": [
                                    {
                                        "type": "Paragraph",
                                        "children": [
                                            {
                                                "type": "RawText",
                                                "content": "可以拆解为三个步骤",
                                            }
                                        ],
                                    }
                                ],
                            },
                        ],
                    },
                ],
            },
        )

    test_markdown_number_list()

    def test_markdown_nested_number_list():
        root_node = MarkdownTransformer(markdown_nested_number_list).trans_to_ast_node()
        assert_is_dict_contain_dict(
            root_node,
            {
                "type": "Document",
                "children": [
                    {
                        "type": "Heading",
                        "level": 1,
                        "children": [
                            {
                                "type": "RawText",
                                "content": "什么是 TDD(Test Driven Development)",
                            }
                        ],
                    },
                    {
                        "type": "List",
                        "start": 1,
                        "children": [
                            {
                                "type": "ListItem",
                                "children": [
                                    {
                                        "type": "Paragraph",
                                        "children": [
                                            {
                                                "type": "RawText",
                                                "content": "TDD 用最简单的话来说,就是实现之前先写测试.",
                                            }
                                        ],
                                    }
                                ],
                            },
                            {
                                "type": "ListItem",
                                "children": [
                                    {
                                        "type": "Paragraph",
                                        "children": [
                                            {
                                                "type": "RawText",
                                                "content": "可以拆解为三个步骤:",
                                            },
                                        ],
                                    },
                                    {
                                        "type": "Paragraph",
                                        "children": [
                                            {
                                                "type": "RawText",
                                                "content": "Red:先写测试代码, 由于此时缺少实现, 所以测试代码会失败",
                                            },
                                            {
                                                "type": "LineBreak",
                                            },
                                            {
                                                "type": "RawText",
                                                "content": "Green:编写实现代码, 使得测试代码通过",
                                            },
                                        ],
                                    },
                                ],
                            },
                        ],
                    },
                ],
            },
        )

    test_markdown_nested_number_list()


def test_given_markdown_str_when_generate_page_then_return_notion_page(
    markdown_heading: str,
    markdown_code: str,
    markdown_number_list: str,
    markdown_nested_number_list: str,
):
    parent_page_id = "123"
    title = "TDD:一种改变编程范式的方法"

    root_node = MarkdownTransformer(markdown_heading).trans_to_ast_node()
    page = NotionPageGenerator().generate(parent_page_id, title, root_node)
    assert_is_dict_contain_dict(
        page,
        {
            "parent": {"page_id": "123"},
            "properties": {
                "title": {
                    "title": [
                        {
                            "type": "text",
                            "text": {"content": "TDD:一种改变编程范式的方法"},
                        }
                    ]
                }
            },
            "children": [
                {"type": "table_of_contents"},
                {
                    "object": "block",
                    "type": "heading_1",
                    "heading_1": {
                        "rich_text": [{"type": "text", "text": {"content": "Heading1"}}]
                    },
                },
                {
                    "object": "block",
                    "type": "heading_2",
                    "heading_2": {
                        "rich_text": [{"type": "text", "text": {"content": "Heading2"}}]
                    },
                },
                {
                    "object": "block",
                    "type": "heading_3",
                    "heading_3": {
                        "rich_text": [{"type": "text", "text": {"content": "Heading3"}}]
                    },
                },
            ],
        },
    )

    root_node = MarkdownTransformer(markdown_code).trans_to_ast_node()
    page = NotionPageGenerator().generate(parent_page_id, title, root_node)
    assert_is_dict_contain_dict(
        page,
        {
            "parent": {"page_id": "123"},
            "properties": {
                "title": {
                    "title": [
                        {
                            "type": "text",
                            "text": {"content": "TDD:一种改变编程范式的方法"},
                        }
                    ]
                }
            },
            "children": [
                {"type": "table_of_contents"},
                {
                    "type": "code",
                    "code": {
                        "language": "lua",
                        "rich_text": [{"type": "text", "text": {"content": "xxx\n"}}],
                    },
                },
            ],
        },
    )

    root_node = MarkdownTransformer(markdown_number_list).trans_to_ast_node()
    page = NotionPageGenerator().generate(parent_page_id, title, root_node)
    assert_is_dict_contain_dict(
        page,
        {
            "parent": {"page_id": "123"},
            "properties": {
                "title": {
                    "title": [
                        {
                            "type": "text",
                            "text": {"content": "TDD:一种改变编程范式的方法"},
                        }
                    ]
                }
            },
            "children": [
                {"type": "table_of_contents"},
                {
                    "object": "block",
                    "type": "heading_1",
                    "heading_1": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": "什么是 TDD(Test Driven Development)"
                                },
                            }
                        ]
                    },
                },
                {
                    "object": "block",
                    "type": "numbered_list_item",
                    "numbered_list_item": {
                        "rich_text": [
                            {
                                "type": "text",
                                "text": {
                                    "content": "TDD 用最简单的话来说,就是实现之前先写测试."
                                },
                            }
                        ]
                    },
                },
                {
                    "object": "block",
                    "type": "numbered_list_item",
                    "numbered_list_item": {
                        "rich_text": [
                            {"type": "text", "text": {"content": "可以拆解为三个步骤"}}
                        ]
                    },
                },
            ],
        },
    )

    root_node = MarkdownTransformer(markdown_nested_number_list).trans_to_ast_node()
    page = NotionPageGenerator().generate(parent_page_id, title, root_node)
    # TODO
    # assert_is_dict_contain_dict(
    #     page,
    #     {
    #         "parent": {"page_id": "123"},
    #         "properties": {
    #             "title": {
    #                 "title": [
    #                     {
    #                         "type": "text",
    #                         "text": {"content": "TDD:一种改变编程范式的方法"},
    #                     }
    #                 ]
    #             }
    #         },
    #         "children": [
    #             {"type": "table_of_contents"},
    #             {
    #                 "object": "block",
    #                 "type": "heading_1",
    #                 "heading_1": {
    #                     "rich_text": [
    #                         {
    #                             "type": "text",
    #                             "text": {
    #                                 "content": "什么是 TDD(Test Driven Development)"
    #                             },
    #                         }
    #                     ]
    #                 },
    #             },
    #             {
    #                 "object": "block",
    #                 "type": "numbered_list_item",
    #                 "numbered_list_item": {
    #                     "rich_text": [
    #                         {
    #                             "type": "text",
    #                             "text": {
    #                                 "content": "TDD 用最简单的话来说,就是实现之前先写测试."
    #                             },
    #                         }
    #                     ]
    #                 },
    #             },
    #             {
    #                 "object": "block",
    #                 "type": "numbered_list_item",
    #                 "numbered_list_item": {
    #                     "rich_text": [
    #                         {
    #                             "type": "text",
    #                             "text": {"content": "可以拆解为三个步骤:"},
    #                         },
    #                     ],
    #                     "children": [
    #                         {
    #                             "object": "block",
    #                             "type": "paragraph",
    #                             "paragraph": {
    #                                 "rich_text": [
    #                                     {
    #                                         "type": "text",
    #                                         "text": {
    #                                             "content": "Red:先写测试代码, 由于此时缺少实现, 所以测试代码会失败"
    #                                         },
    #                                     },
    #                                     {
    #                                         "type": "line_break",
    #                                     },
    #                                     {
    #                                         "type": "text",
    #                                         "text": {
    #                                             "content": "Green:编写实现代码, 使得测试代码通过"
    #                                         },
    #                                     },
    #                                 ],
    #                             },
    #                         },
    #                     ],
    #                 },
    #             },
    #         ],
    #     },
    # )
