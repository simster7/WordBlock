import re, random

def create_markov_dict(source):

	# Gather words from source
	with open(source, encoding="utf8") as f:
		text = f.read().lower()

	text = re.sub(r'[^a-z\ \']+', " ", text)
	words = list(text.split())

	markov_dict = {word:[] for word in words}		# Create "Markov Dictionary"


	# Populate dictionary
	for i in range(len(words) - 1):
		markov_dict[words[i]].append(words[i+1])

	#print(markov_dict)
	return markov_dict


def create_sentence(first_word, length, markov_dict):

	assert first_word in markov_dict, "No such word in source"

	setnence, current_word = first_word + " ", first_word
	for x in range(length):
		next_word = random.choice(markov_dict[current_word])
		setnence, current_word = setnence + next_word + " ", next_word

	return setnence

mdict = create_markov_dict('gchat.txt')
#first_word = random.choice(list(mdict.keys()))		# Randomly choose first word
print("-", create_sentence('simon', 16, mdict))
