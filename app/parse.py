import wikipedia

# Returns list: elements are lines of Wikipedia text delimited by newline
# Recursively finds new pages via "See also" section
def rec_parse(querystr, depth):
    text_list = []
    results = wikipedia.search(querystr)
    page = wikipedia.page(results[0])

    def parse(page, depth):
        if (depth > 0 and page.section("See also")):
            text_list.extend(page.content.splitlines())
            link_names = page.section("See also").splitlines()
            for name in link_names:
                parse(wikipedia.page(name), depth-1)

    parse(page, depth)
    return text_list

# Returns list: elements are lines of Wikipedia text delimited by newline (same return behavior)
# Finds new pages by iterating through the search results
def iter_parse(querystr):
    text_list = []
    results = wikipedia.search(querystr)
    for pagename in results:
        page = wikipedia.page(pagename)
        text_list.extend(page.content.splitlines())
    return text_list

# Returns list (see above)
# Breadth first search to level of "depth"
# max_searches caps the number queries per page
def depth_parse(querystr, depth, max_searches):
    count = 0 
    text_list = []
    visited = set()
    # list of tuples
    queue = list()
    queue.append((querystr, depth+1))
    while len(queue) > 0:
        next = queue.pop(0)
        try:
            if next[0] not in visited and next[1] >= 0:
                print("name=",next[0], ", depth=",next[1])
                visited.add(next[0])
                results = wikipedia.search(next[0], max_searches, False)
                for pagename in results:
                    queue.append((pagename, next[1]-1))
                text_list.extend(wikipedia.page(next[0]).content.split())
                count+=1
        except:
            pass
    return text_list

