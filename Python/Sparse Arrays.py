def matchingStrings(strings, queries):
    return [Counter(strings)[query] if query in Counter(strings) else 0 for query in queries]
