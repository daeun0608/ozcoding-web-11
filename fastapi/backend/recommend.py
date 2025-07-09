def recommend(preference: str, contents: list) -> list:
    return [
        item for item in contents
        if preference.lower() in [tag.lower() for tag in item['tags']]
    ]
