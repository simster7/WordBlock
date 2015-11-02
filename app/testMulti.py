import threading
import logging
import nltk, re, os.path, pickle, wikipedia, urllib

class SubjectContext:
    """
    A Context for deriving synonyms of a specified word
    """
    
    def __init__(self, subject, depth=3, max_searches=5):
        """
        Initialize SubjectContext with a specific context. If we have already used
        that conext before, load it. Otherwise, gather context data from Wikipedia
        using specified DEPTH and MAX_SEARCHES.
        """
        assert type(depth) == int, 'depth must be an int'
        assert type(max_searches) == int, 'max_searches must be an int'

        self.subject = subject
        self.depth = depth
        self.max_searches = max_searches

        fileName = './data/' + self.subject + '-' + str(self.depth) + '-' + str(self.max_searches) + '.wbdat'
        if (os.path.isfile(fileName)):
            self.data_list = pickle.load(open(fileName, 'rb'))
        else:
            self.data_list = self.context_data
            pickle.dump(self.data_list, open(fileName, 'wb'))

    @property
    def context_data(self):
        """
        Gather data from Wikipedia based on user-inputed SUBJECT. 
        """
        print("derp")
        text_list, visited, q = [], set(), list()
        q.append(self.subject)

        depth_counter = 0

        def search_worker(query):
            print("Starting query, depth is ", depth_counter)
            try:
                visited.add(query)
                text = wikipedia.page(query).content
                text_list.extend(text.split())
                next_queries = wikipedia.search(query, self.max_searches, False)
                for pagename in next_queries:
                    if pagename not in visited:
                        q.append(pagename)
            except:
                pass

        while (depth_counter <= self.depth):
            thread_list = []
            for query in q:
                t = threading.Thread(target=search_worker, args=(query,))
                t.start()
                thread_list.append(t)
            for thread in thread_list:
                t.join()
            depth_counter+=1

        q = list()
        q.append(self.subject)

        depth_counter = 0

        def see_also_worker(query):
            print("Starting query, depth is ", depth_counter)
            try:
                visited.add(query)
                page = wikipedia.page(query)
                text_list.extend(text.content.split())
                next_queries = page.section("See also").splitlines()
                for pagename in next_queries:
                    if pagename not in visited:
                        q.append(pagename)
            except:
                pass

        while (depth_counter <= self.depth):
            thread_list = []
            for query in q:
                t = threading.Thread(target=see_also_worker, args=(query,))
                t.start()
                thread_list.append(t)
            for thread in thread_list:
                t.join()
            depth_counter+=1
        print(text_list[0:20])
        return text_list
     
    def get_thesaurus(self, word):
        """
        Get Thesaurus.com synonyms for requested WORD. synonyms_a contains synonyms
        of the various meanings of WORD only. synonyms_b extends to related words 
        and their synonyms.
        """

        opener = urllib.request.build_opener()
        
        html = opener.open('http://www.thesaurus.com/browse/' + word).read(100000).\
                decode(encoding='utf-8', errors='replace')

        try:
            antonym_index = html.index('<section class="container-info antonyms">')
            html = html[:antonym_index] + html[html.index('</section>', antonym_index)]
        except:
            pass 
                   
        synonyms_a = re.findall(r'<span class="text">([a-z\ ]+)<\/span>', html)
        synonyms_b = re.findall(r'<a href="[^\"]+">\n([a-z\ ]+)<\/a>', html)

        return synonyms_a + synonyms_b, synonyms_a
       
    def get(self, word):
        """
        Return optimal and secondary replacements for WORD. Optimal replacements are
        those whose synonyms are used in context within our dataset. Secondary replacements
        are not necesiraly used in context, but are used individually within our dataset.
        """
        optimal, secondary, visited = [], [], []
        print('thes')
        extended_syn, basic_syn = self.get_thesaurus(word)
        print('donethes')

        context = nltk.ContextIndex(self.data_list)
        text = nltk.Text(self.data_list)
        candidates = context.similar_words(word, n=10000)

        print('Optimal:\n')
        for word in candidates: 
            if word in extended_syn and word not in visited: 
                optimal.append(word)
                visited.append(word)
                print(word)
        print('\n')

        #print('Optimal:\n', optimal)
        print('Secondary:\n')

        secondary_list = [[word, text.count(word)] for word in basic_syn]
        secondary_list = [t[0] for t in list(reversed(sorted(secondary_list, key =lambda x: x[1])))]
        for word in secondary_list: 
            if word not in visited: 
                secondary.append(word)
                visited.append(word)
                print(word)
        print('\n')

        return optimal, secondary
