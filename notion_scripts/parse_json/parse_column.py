def parse_column(data, column):
    if column.column_type == "id":
        return data[column.title]

    if data["properties"].get(column.title) is not None:

        data = data["properties"][column.title][column.column_type]

        if column.column_type == "rollup":
            return [find_out_the_type(data["array"][i][column.column_subtype], column.column_subtype) for i in
                    range(len(data["array"]))]
        return find_out_the_type(data, column.column_type)

    return None


def find_out_the_type(data, column_type):
    if column_type == "select":
        return data["name"]
    if column_type == "rich_text":
        if data:
            return data[0]['text']["content"]
        return None
    if column_type == "date":
        return data["start"]
    if column_type == "relation":
        return [i["id"] for i in data]
    if column_type == "title":
        return data[0]['plain_text']
    return data
