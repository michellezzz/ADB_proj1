from collections import defaultdict
import math
import copy


def normalization(vector):
    square_sum = 0
    for key in vector:
        square_sum += vector[key] * vector[key]
    if square_sum == 0:
        return vector
    for key in vector:
        vector[key] /= square_sum
    return vector


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
    query_list = permutation(query, 0)

    # get the best query
    best_score = 0
    best_query = query
    for query in query_list:
        score = 0
        for i in range(len(query)-1):
            score += bigram_dict[' '.join([query[i], query[i+1]])]
        if score > best_score:
            best_score = score
            best_query = query
    return best_query


def generate_score(document_list, scope='title'):
    word_space = []
    for doc in document_list:
        if scope=='title':
            for word in doc.title:
                if word not in word_space:
                    word_space.append(word)
        elif scope=='description':
            for word in doc.description:
                if word not in word_space:
                    word_space.append(word)


    vector = defaultdict(int)   # TF
    for doc in document_list:
        vector[doc.url] = defaultdict(int)
        for word in word_space:
            if scope=='title':
                if word in doc.title:
                    vector[doc.url][word] += 1
                else:
                    vector[doc.url][word] = 0
            elif scope=='description':
                if word in doc.description:
                    vector[doc.url][word] += 1
                else:
                    vector[doc.url][word] = 0


    DF_vector = defaultdict(int)  # DF
    for word in word_space:
        for doc in document_list:
            if scope=='title':
                if word in doc.title:
                    DF_vector[word] += 1
            elif scope=='description':
                if word in doc.description:
                    DF_vector[word] += 1

    score_vector = defaultdict(int)  # log(TF(w,d)+1)*log(IDF(w))
    num_of_docs = len(document_list)
    for doc in document_list:
        score_vector[doc.url] = defaultdict(int)
        for word in word_space:
            if DF_vector[word]==0:
                print "fatal", scope, word, doc.description
            score = math.log(vector[doc.url][word]+1) * math.log(float(num_of_docs)/DF_vector[word])  # TODO
            score_vector[doc.url][word] = score

    return score_vector, word_space


def merge_score(sv1, sv2, weight1, weight2):
    result = defaultdict(int)
    for doc in sv1:
        result[doc] = defaultdict(int)
        for word in sv1[doc]:
            result[doc][word] += weight1 * sv1[doc][word]
        for word in sv2[doc]:
            result[doc][word] += weight2 * sv2[doc][word]
    return result


def silly_algo(document_list, query, alpha, beta, gamma):  # based on title
    title_weight = 2
    description_weight = 1

    # get score vector for both title and description
    score_vector_for_title, word_space_for_title = generate_score(document_list, 'title')
    score_vector_for_description, word_space_for_description = generate_score(document_list, 'description')

    # merge the score vector for title and description
    score_vector = merge_score(score_vector_for_title, score_vector_for_description, title_weight, description_weight)
    word_space = list(set(word_space_for_title)|set(word_space_for_description))

    # generate vector for query
    query_vector = defaultdict(int)
    for word in word_space:
            if word in query:
                query_vector[word] += 1
            else:
                query_vector[word] = 0

    # count num of relevant and irrelevant
    num_relevant = 0
    num_irrelevant = 0
    for doc in document_list:
        if doc.relevant == 'y':
            num_relevant += 1
        else:
            num_irrelevant += 1

    # calculate the new query vector
    new_query_vector = defaultdict(int)
    for word in word_space:
        new_query_vector[word] = alpha * query_vector[word]
        sum_relevant = 0
        sum_irrelevant = 0
        for doc in document_list:
            score_vector[doc.url] = normalization(score_vector[doc.url])
            if doc.relevant == 'y':
                sum_relevant += score_vector[doc.url][word]
            else:
                sum_irrelevant += score_vector[doc.url][word]
        if num_relevant:
            new_query_vector[word] += beta * sum_relevant / float(num_relevant)
        if num_irrelevant:
            new_query_vector[word] -= gamma * sum_irrelevant / float(num_irrelevant)

    # get the word with max score from the new_query_vector
    max_score = 0
    next_max_score = 0
    max_word = ''
    next_max_word = ''
    for word in new_query_vector:
        if word not in query:
            if new_query_vector[word] > max_score:
                next_max_score = max_score
                next_max_word = max_word
                max_score = new_query_vector[word]
                max_word = word
            elif new_query_vector[word] > next_max_score:
                next_max_score = new_query_vector[word]
                next_max_word = word

    # add the best new word into query
    if max_word:
        query.append(max_word)

    # change the order of the query
    query = change_order(query, document_list)  # query is a list of word
    #if next_max_word:
    #query.append(next_max_word)
    return query









