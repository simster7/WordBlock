import wikipedia

# Returns list of lists: elements are lines of Wikipedia text delimited by newline
def query(querystr, depth):
    text_list = []
    page = wikipedia.page(querystr)

    def parse(page, depth):
        if (depth > 0 and page.section("See also")):
            text_list.append(page.content.splitlines())
            link_names = page.section("See also").splitlines()
            for name in link_names:
                parse(wikipedia.page(name), depth-1)

    parse(page, depth)
    return text_list
