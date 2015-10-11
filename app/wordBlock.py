import nltk, re
from parse import depth_parse
from thes import get_synonyms


def main(Subject, word):
    retList = []
    depth = 1
    data_list = depth_parse(Subject, depth, 5); #get our LARGE dataset from wiki on subject content
    #data_list still contains unicode shit that cant be printed!
    synonyms = get_synonyms(word); #get synonyms from thesaurus.com
    context = nltk.ContextIndex(data_list)
    candidates = context.similar_words(word, n=10000)
    for candidate in candidates:
        if candidate in synonyms:
            retList.append(candidate)
    return retList
