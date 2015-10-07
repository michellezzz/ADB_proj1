import string
import re
import copy

'''
file = open("stop.rtf")
stop_word_list = []
for eachline in file:
    stop_word_list.append(eachline[0:-1])
file.close()


print stop_word_list


def remove_stopword(words):
    result = []
    for word in words:
        if word not in stop_word_list:
            result.append(word)
    return result

def remove_punctuation(words):  # words is a string
    exclude = set(string.punctuation)
    words = ''.join(ch for ch in words if ch not in exclude)
    return words

words = "today|| | , ,, |--is, a good. | day, Michelle"
print words
print remove_punctuation(words)

print 'gil%20asd'.split('%20')
'''

def permutation(query, left):
    '''
    input: a list of word
    output: a list of permutation
    '''
    if left == len(query):
        return [query]
    else:
        result = []
        for i in range(left, len(query)):
            new_query = copy.deepcopy(query)
            new_query[left], new_query[i] = new_query[i], new_query[left]
            result.extend(permutation(new_query, left+1))
    return result


def change_order(query, document_list):   # query is a list of word
    # calculate the bigram_dict
    title_weight = 2
    description_weight = 1
    bigram_dict = defaultdict(float)
    for doc in document_list:
        for i in range(len(doc.title)-1):
            bigram_dict[' '.join([doc.title[i], doc.title[i+1]])] += title_weight
        for i in range(len(doc.description)-1):
            bigram_dict[' '.join([doc.description[i], doc.description[i+1]])] += description_weight

    # get permutation of query
    query_list = permutation(query)

    # get the best query
    best_score = 0
    best_query = query
    for query in query_list:
        score = 0
        for i in range(len(query)-1):
            score += bigram_dict[' '.join([query[i], query[i+1]])]
        if score>best_score:
            best_score = score
            best_query = query
    return best_query


'''
# test permutation
query = ['a','b','c','d']
per = permutation(query, 0)
for p in per:
    print p
'''


# test stemming
from stemming.porter2 import stem
print stem("factionally")
print stem("this and that")
print stem("Bill Gates!")
print stem("Gates")
print stem("foxes")
print stem("levis")
print stem('|')


def lower_case(words):  # words is a string
    return words.lower()


# test lower_case
l = lower_case("Hello, how ARe you, little RabBit?")
print l



def stemming(words):
    result = []
    for word in words:
        result.append(stem(word))
    return result


# test stemming
words = ['this', 'that', 'foxes', 'people', 'registration', 'levis', 'factionally']
print stemming(words)