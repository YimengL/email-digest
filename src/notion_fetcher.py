import os
from notion_client import Client
from dotenv import load_dotenv

load_dotenv()

notion = Client(auth=os.environ.get("NOTION_API_KEY"))

def fetch_pages():
    result = notion.search(filter={"property": "object", "value": "page"})
    pages = []

    for page in result["results"]:
        page_id = page["id"]
        title = ""

        title_prop = page.get("properties", {}).get("title", {})
        title_list = title_prop.get("title", [])
        if title_list:
            title = title_list[0]["plain_text"]

        pages.append({
            "id": page_id,
            "title": title,
        })

    return pages

        
def fetch_page_content(page_id):
    blocks = notion.blocks.children.list(block_id=page_id)
    content = ""

    for block in blocks["results"]:
        block_type = block["type"]
        rich_text = block.get(block_type, {}).get("rich_text", [])

        for text in rich_text:
            content += text["plain_text"] + " "
    
    return content.strip()


if __name__ == "__main__":
    pages = fetch_pages()
    print(f"Found {len(pages)} pages:")
    for page in pages:
        print(f". {page['title']} ({page['id']})")
        content = fetch_page_content(page["id"])
        print(f"  Content preview: {content[:100]}")
        print("---")