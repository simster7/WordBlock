from nltk.corpus import wordnet as wn


for syn in wn.synsets('small'):
    print(syn.lemma_names())
