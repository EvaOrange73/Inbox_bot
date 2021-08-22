def h1(text):
    return {
        "object": "block",
        "type": "heading_1",
        "heading_1": {
            "text": [{"type": "text", "text": {"content": text}}]
        }
    }


def h2(text):
    return {
        "object": "block",
        "type": "heading_2",
        "heading_2": {
            "text": [{"type": "text", "text": {"content": text}}]
        }
    }


def h3(text):
    return {
        "object": "block",
        "type": "heading_3",
        "heading_3": {
            "text": [{"type": "text", "text": {"content": text}}]
        }
    }


def paragraph(text):
    return {
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "text": [
                {
                    "type": "text",
                    "text": {
                        "content": text,
                        # "link": {"url": "https://en.wikipedia.org/wiki/Lacinato_kale"}
                    }
                }
            ]
        }
    }


def bold_paragraph(text):
    return {
        "object": "block",
        "type": "paragraph",
        "paragraph": {
            "text": [
                {
                    "type": "text",
                    "text": {
                        "content": text
                    },
                    "annotations": {
                        "bold": True
                    }
                }
            ]
        }
    }


def bulleted_list_item(text):
    return {
        "object": "block",
        "type": "bulleted_list_item",
        "bulleted_list_item": {
            "text": [
                {
                    "type": "text",
                    "text": {
                        "content": text,
                    }
                }
            ]
        }
    }
