import urllib2
import base64
import re
import json

from document import *
from Rocchio import *


TEST = 1
accountKey = "We+IL0UpPGqKJiHi0Nk2W9DgUdByhqNogVJ4VIEuUYw"
alpha = 1
beta = 1
gamma = 1


def __print(message):
    if TEST:
        print message


def search(query):
    query = re.sub('[\s\t]+', "%20", query)
    bingUrl = 'https://api.datamarket.azure.com/Bing/Search/Web?Query=%27' + query + '%27&$top=10&$format=json'
    accountKeyEnc = base64.b64encode(accountKey + ':' + accountKey)
    headers = {'Authorization': 'Basic ' + accountKeyEnc}
    req = urllib2.Request(bingUrl, headers = headers)
    response = urllib2.urlopen(req)
    content = response.read()
    decoded_json = json.loads(content)
    search_result = decoded_json['d']['results']
    return search_result


def remove_stopword(words):
    return words


def remove_punctuation(words):
    return words


def stemming(words):
    return words


def process_doc(words):
    words = words.encode("utf8").split()
    words = remove_stopword(words)
    words = remove_punctuation(words)
    words = stemming(words)
    return words


if __name__ == "__main__":

    query = "bill gates"  # TODO: as user input
    precision = 0.9

    correctness = 0
    while correctness < precision:
        correct = 0
        total = 0

        # search
        search_result = search(query)
        print search_result

        # save result
        document_list = []
        total = min(len(search_result), 10)
        for i in range(total):
            item = search_result[i]
            print '\n' + '-'*20
            print "%-12s" % "Title: ", item['Title'].encode("utf8")
            print "%-12s" % "URL: ", item['Url'].encode("utf8")
            print "%-12s" % "Description: ", item['Description'].encode("utf8")
            relevant = raw_input("Is this document relevant? (y/n)") # TODO input processing
            if relevant == 'y':
                correct += 1

            new_doc = document()
            new_doc.title = process_doc(item['Title'])  # input a str, return a list
            new_doc.description = process_doc(item['Description'])
            new_doc.url = item['Url'].encode("utf8")
            new_doc.relevant = relevant

            document_list.append(new_doc)

        correctness = correct/float(total)
        query = silly_algo(document_list, query, alpha, beta, gamma)
        print query
















