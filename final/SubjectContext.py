import nltk, re, os.path, pickle, wikipedia, urllib

class SubjectContext:
    """
    A Context for deriving synonyms of a specified word
    """
    
    def __init__(self, subject, depth=2, max_searches=5):
        """
        Initialize SubjectContext with a specific context. If we have already used
        that conext before, load it. Otherwise, gather context data from Wikipedia
        using specified DEPTH and MAX_SEARCHES.
        """
        self.subject = subject
        self.depth = depth
        self.max_searches = max_searches

        fileName = self.subject + '-' + str(self.depth) + '-' + str(self.max_searches) + '.wbdat'
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
        count, text_list, visited, queue = 0, [], set(), list() 
        queue.append((self.subject, self.depth))

        while len(queue) > 0:
            next = queue.pop(0)
            try:
                if next[0] not in visited and next[1] >= 0:
                    visited.add(next[0])
                    results = wikipedia.search(next[0], self.max_searches, False)
                    for pagename in results:
                        queue.append((pagename, next[1]-1))
                    text_list.extend(wikipedia.page(next[0]).content.split())
                    count+=1
            except:
                pass

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
        
        synonyms_a = re.findall(r'<span class="text">([a-z\ ]+)<\/span>', html)
        synonyms_b = re.findall(r'<a href="[^\"]+">\n([a-z\ ]+)<\/a>', html)

        return synonyms_a + synonyms_b, synonyms_a
       
    def get(self, word):
        """
        Return optimal and secondary replacements for WORD. Optimal replacements are
        those whose synonyms are used in context within our dataset. Secondary replacements
        are not necesiraly used in context, but are used individually within our dataset.
        """
        optimal, secondary = [], []
        extended_syn, basic_syn = self.get_thesaurus(word)

        context = nltk.ContextIndex(self.data_list)
        text = nltk.Text(self.data_list)
        candidates = context.similar_words(word, n=10000)

        optimal = [word for word in candidates if word in extended_syn]

        print('Optimal:\n', optimal)
        secondary = [[word, text.count(word)] for word in basic_syn]

        secondary = [t[0] for t in list(reversed(sorted(secondary, key =lambda x: x[1])))]
        print('Secondary:\n', secondary)

        return optimal, secondary
