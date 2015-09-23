import urllib2
import base64
import re


TEST = 1
accountKey = "We+IL0UpPGqKJiHi0Nk2W9DgUdByhqNogVJ4VIEuUYw"


def __print(message):
    if TEST:
        print message


if __name__ == "__main__":
    query = "little pink   rabbit"
    query = re.sub('[\s\t]+', "%20", query)
    bingUrl = 'https://api.datamarket.azure.com/Bing/Search/Web?Query=%27' + query + '%27&$top=10&$format=Atom'

    __print(bingUrl)
    __print(accountKey)

    accountKeyEnc = base64.b64encode(accountKey + ':' + accountKey)
    headers = {'Authorization': 'Basic ' + accountKeyEnc}
    req = urllib2.Request(bingUrl, headers = headers)
    response = urllib2.urlopen(req)
    content = response.read()

    __print(content)

