from notion.client import NotionClient
from config import NOTION_TOKEN, notion_test_page


async def change_title(new_title):
    client = NotionClient(token_v2=NOTION_TOKEN)
    page = client.get_block(notion_test_page)
    print("The old title is:", page.title)
    page.title = new_title
