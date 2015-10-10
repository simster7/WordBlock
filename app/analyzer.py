import re

class Markov:

    def __init__(self, source):
        self.source = source

    def parse_dict(self, dic):
        _new = {}
        for word in dic:
            if word not in _new.keys():
                _new[word] = 0
            _new[word] += 1
        for key, item in _new.items():
            _new[key] = round(_new[key] / len(dic), 4)

        return _new

    @property
    def m_dict(self):

        #Gather words from source
        with open(self.source, encoding='utf-8') as f:
            text = f.read().lower()
            text = re.sub(r'[^a-z\ \']+', " ", text)
            words = list(text.split())

        markov_dict = {word:[[],[]] for word in words}

        for i in range(1, len(words) - 1):
            markov_dict[words[i]][0].append(words[i - 1])
            markov_dict[words[i]][1].append(words[i + 1])

        markov_dict[words[0]][1].append(words[1])
        markov_dict[words[len(words) - 1]][0].append(words[len(words) - 2])

        for key, item in markov_dict.items():
            markov_dict[key] = [self.parse_dict(item[0]), self.parse_dict(item[1])]

        return markov_dict

    def usage(self, prev, curr, next):
        u_prev, u_next = 0, 0
        try:
            u_prev = self.m_dict[curr][0][prev]
        except:
            print(prev, 'was not found before', curr)
        try:
            u_next = self.m_dict[curr][1][next]
        except:
            print(next, 'was not found after', curr)
        
        return u_prev + u_next

def print_stats(word, dic):
    assert word in dic
    print('Looking for', word)
    print('Occurences before:')
    for key, val in dic[word][0].items():
        print('\t', key, str(val * 100) + '%')
    print('Occurences after:')
    for key, val in dic[word][1].items():
        print('\t', key, str(round(val * 100, 2)) + '%')

mar = Markov('essay.txt')
print_stats('understand', mar.m_dict)

print('should understand me', mar.usage('should', 'understand', 'me'))
print('should explain me', mar.usage('should', 'explain', 'me'))
