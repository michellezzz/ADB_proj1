import urllib2
import base64
import re
import sys
import json
import string

from document import *
from Rocchio import *


TEST = 1
accountKey = "We+IL0UpPGqKJiHi0Nk2W9DgUdByhqNogVJ4VIEuUYw"
alpha = 1
beta = 1
gamma = 1


file = open("stop.rtf")
stop_word_list = []
for eachline in file:
    stop_word_list.append(eachline[0:-1])
file.close()

print stop_word_list


def __print(message):
    if TEST:
        print message


def search(query):
    query = re.sub('[\s\t]+', "%20", query)
    bingUrl = 'https://api.datamarket.azure.com/Bing/Search/Web?Query=%27' + query + '%27&$top=10&$format=json'
    accountKeyEnc = base64.b64encode(accountKey + ':' + accountKey)
    headers = {'Authorization': 'Basic ' + accountKeyEnc}
    req = urllib2.Request(bingUrl, headers=headers)
    response = urllib2.urlopen(req)
    content = response.read()
    decoded_json = json.loads(content)
    search_result = decoded_json['d']['results']
    return search_result, query


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


def stemming(words):
    return words


def lower_case(words):  # words is a string
    return words.lower()


def process_doc(words):
    words = remove_punctuation(words)
    words = lower_case(words)
    words = words.encode("utf8").split()
    words = remove_stopword(words)
    words = stemming(words)
    return words


if __name__ == "__main__":

    query = "Gates"  # TODO: as user input
    precision = 0.9

    url_set = set()
    correctness = 0
    document_list = []
    while correctness < precision:
        correct = 0
        total = 0

        # search
        query = query.lower()
        search_result, query = search(query)
        print search_result

        # save result
        total = min(len(search_result), 10)
        if total == 0:
            print "Not enough result. System exit."
            sys.exit()
        #print total
        for i in range(total):
            item = search_result[i]

            print '\n' + '-'*20
            print "%-12s" % "Title: ", item['Title'].encode("utf8")
            print "%-12s" % "URL: ", item['Url'].encode("utf8")
            print "%-12s" % "Description: ", item['Description'].encode("utf8")
            relevant = raw_input("Is this document relevant? (y/n)")  # TODO input processing
            if relevant == 'y':
                correct += 1

            new_doc = document()
            new_doc.title = process_doc(item['Title'])  # input a str, return a list
            new_doc.description = process_doc(item['Description'])
            new_doc.url = item['Url'].encode("utf8")
            new_doc.relevant = relevant
            if new_doc.url not in url_set:
                document_list.append(new_doc)
                url_set.add(new_doc.url)

        correctness = correct/float(total)
        query = silly_algo(document_list, query, alpha, beta, gamma)
        print query