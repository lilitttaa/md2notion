# md2notion

## usecase 
``` python
def run(markdown_str):
    page_id = "xxx"
    page = NotionPageGenerator().generate(
        page_id, "title", MarkdownTransformer(markdown_str).trans_to_ast_node()
    )
    NotionPageUploader().upload(
        os.environ.get("NOTION_TOKEN"), page
    )

```