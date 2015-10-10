
import nltk, re

with open('essay.txt') as f:
    text = f.read().lower()
    text = re.sub(r'[^a-z\ \']+', ' ', text)

syn = ['accent', 'dialect', 'expression', 'jargon', 'prose', 'sound', 'speech', 'style']
syni = ['appearance', 'copy', 'drawing', 'figure', 'form', 'icon', 'illustration', 'likeness', 'model', 'photograph', 'picture', 'portrait', 'statue']
conttext = nltk.ContextIndex(list(text.split()))

candidates = conttext.similar_words('language', n=100000)

#print(candidates)

for c in candidates:
    if c in syn:
        print(c)
