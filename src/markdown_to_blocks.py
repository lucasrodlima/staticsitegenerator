def markdown_to_blocks(markdown):
    blocks = list(map(lambda x: x.strip(), markdown.split("\n\n")))

    return blocks