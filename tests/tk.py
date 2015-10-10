
import nltk, re, wikipedia

# with open('sample.txt') as f:
#     text = f.read().lower()
text = wikipedia.page("William Shakespeare").content
text = re.sub(r'[^a-z\ \']+', ' ', text)
syn = ['comedy', 'drama', 'hit', 'musical', 'opera', 'performance', 'show']
conttext = nltk.ContextIndex(list(text.split()))

candidates = conttext.similar_words('play', n=100000)

print(candidates)

for c in candidates:
    if c in syn:
        print(c)
