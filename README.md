# WordBlock
Program Objective: 

WordBlock's primarily goal is to replace redundant words in written text with a synonym. However, most synonyms from a thesaurus in the English language don't properly flow with the context they are placed in. WordBlock aims to provide optimal synonyms for a given context that the user inputs. 

Example of Program Usefulness: 

John may be writing a short paragraph about himself and say "I like to create things." He may feel like he used the word "create" far too many times and look to the thesaurus to replace the particular word. The thesauarus may suggest the option to replace the word, "create", with "procreate". However, "procreate" isn't a valid substitute if the context given is not a biological one. Therefore, wordBlock will suggest appropriate synonyms in a hierarchical structure where words like "procreate" get a lower priority than optimal replacements like "build". 

How to Call this Program: 

As of right now, we do not have a GUI or website implemented to make the UI more desirable to people who aren't familiar with basic coding principles. In the current condition, a user will have to create a SubjectContext object in the command terminal by using the class's constructor and passing in a desired subject. Then, the user will have to call the object's get method by typing "object.get("WORD")" where WORD designates the word that the user wants to replace, which the program will display alternatives for based on the given context. 

How This Program is Implemented: 

We created a SubjectContext class that has an init method which takes in a user defined subject, depth(specified number of recursive searches to perform on the given subject query), and max_searches(specified number of wikipedia pages to grab text from). It initializes a SubjectContext with a specific context. If we've already used that context before, we load it. Otherwise, we gather context data from Wikipedia using specified DEPTH and MAX_SEARCHES. Using the specific context the user specifies, and the word to replace, the get(WORD) function returns optimal and secondary replacements for WORD. Optimal replacements are those whose synonyms are used in context within our dataset. Secondary replacements are not necessarily used in context, but are used individually within our dataset.

Drawbacks: 

Since a large part of our algorithm for determining replaceable alternatives for a word is based on the likelihood of the alternative being placed in a similar context, we include antonyms and other popular words that aren't necessarily synonyms in our secondary replacements list. Furthermore, we allow duplicates to be in this list, so it's not unique.