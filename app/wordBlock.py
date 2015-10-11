import nltk, re
from parse import depth_parse
from thes import get_synonyms


def main(Subject, word):
    retList = []
    depth = 2
    data_list = depth_parse(Subject, depth); #get our LARGE dataset from wiki on subject content
    synonyms = get_synonyms(word); #get synonyms from thesaurus.com
    candidates = nltk.ContextIndex(data_list).similar_words(word, n=10000)
    for candidate in candidates:
        if candidate in synonyms:
            retList.append(candidate)
    return retList
