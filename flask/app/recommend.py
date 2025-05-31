def recommend_by_keyword(contents, keyword):
    keyword_lower = keyword.lower()
    return [c for c in contents if keyword_lower in c.keywords.lower()]
