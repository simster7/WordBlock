import wikipedia

# Returns list of lists: elements are lines of Wikipedia text delimited by newline
# Recursively finds new pages via "See also" section
def rec_parse(querystr, depth):
    text_list = []
    results = wikipedia.search(querystr)
    page = wikipedia.page(results[0])

    def parse(page, depth):
        if (depth > 0 and page.section("See also")):
            text_list.append(page.content.splitlines())
            link_names = page.section("See also").splitlines()
            for name in link_names:
                parse(wikipedia.page(name), depth-1)

    parse(page, depth)
    return text_list

# Returns list of lists: elements are lines of Wikipedia text delimited by newline (same return behavior)
# Finds new pages by iterating through the search results
def iter_parse(querystr):
    text_list = []
    results = wikipedia.search(querystr)
    for page in results:
        text_list.append(page.content.splitlines())
    return text_list
j