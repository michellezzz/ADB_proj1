from collections import defaultdict

def silly_algo(document_list, query, alpha, beta, gamma):
    query = query.split()
    word_space = []
    for doc in document_list:
        for word in doc.title:
            if word not in word_space:
                word_space.append(word)

    vector = defaultdict(int)
    for doc in document_list:
        vector[doc.url] = defaultdict(int)
        for word in word_space:
            if word in doc.title:
                vector[doc.url][word] += 1
            else:
                vector[doc.url][word] = 0

    print "hi"
    for item in vector:
        print item, vector[item]

    # generate vector for query
    query_vector = defaultdict(int)
    for word in word_space:
            if word in query:
                query_vector[word] += 1
            else:
                query_vector[word] = 0

    num_relevant = 0
    num_irrelevant = 0
    for doc in document_list:
        if doc.relevant == 'y':
            num_relevant += 1
        else:
            num_irrelevant += 1

    new_query_vector = defaultdict(int)
    for word in word_space:
        new_query_vector[word] = alpha * query_vector[word]
        sum_relevant = 0
        sum_irrelevant = 0
        for doc in document_list:
            if doc.relevant == 'y':
                sum_relevant += vector[doc.url][word]
            else:
                sum_irrelevant += vector[doc.url][word]
        if num_relevant:
            new_query_vector[word] += beta * sum_relevant / float(num_relevant)
        if num_irrelevant:
            new_query_vector[word] -= gamma * sum_irrelevant / float(num_irrelevant)

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

    query.append(max_word)
    query.append(next_max_word)
    return '%20'.join(query)









