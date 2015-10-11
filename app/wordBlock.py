import nltk, re, os.path, pickle
from parse import depth_parse
from thes import get_synonyms


#Subject is subject matter of user's doc/data set we want from wiki
#word is the word
#num is number of search queries to bfs through
def main(Subject, word):
    retList = []
    depth = 1 #play around w/ this
    #FileName format = ".Subject_word_num"
    fileName = '.' + Subject
    if (os.path.isfile(fileName)): #if it already exists, we already crawled wiki, reload from file
        data_list = pickle.load(open(fileName, 'rb'))
    else:
        data_list = depth_parse(Subject, depth, 5) #get our LARGE dataset from wiki on subject content
        #data_list still contains unicode shit that cant be printed!
        pickle.dump(data_list, open(fileName, 'wb'))

    context = nltk.ContextIndex(data_list)
    synonyms = get_synonyms(word) #get synonyms from thesaurus.com
    
    candidates = context.similar_words(word, n=10000)
    for candidate in candidates:
        if candidate in synonyms:
            retList.append(candidate)
    return retList


