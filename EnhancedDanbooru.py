# endpoint :5555/?tags=xxx yyy&page=zzz
# return {pic: [], nextPage: int}
import requests
import json
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib import parse

sources = {
    'danbooru': {
        'endpoint': 'http://danbooru.donmai.us/posts.json',
        'tagLine': 'tag_string',  # the entry for tags in returned JSON objects
        'pageIndicator': 'page',  # the parameter for page number to use with the endpoint
    },
    'yandere': {
        'endpoint': 'https://yande.re/post.json',
        'tagLine': 'tags',
        'pageIndicator': 'page',
    },
    'konachan': {
        'endpoint': 'http://konachan.com/post.json',
        'tagLine': 'tags',
        'pageIndicator': 'page',
    },
    'gelbooru': {
        'endpoint': 'https://gelbooru.com/index.php',
        'tagLine': 'tags',
        'pageIndicator': 'pid',  # need special attention as it starts from 0 instead of 1
    },
}

gelbooruStartingDict = {
    'page': 'dapi',
    's': 'post',
    'q': 'index',
    'json': 1,
}


class DanbooruPostQuery:
    def __init__(self, tagString, startPage=1, source='danbooru'):
        self.endpoint = sources[source]['endpoint']
        self.tagLine = sources[source]['tagLine']
        self.pageIndicator = sources[source]['pageIndicator']
        self.source = source

        tmp = tagString.split()
        tmpNegativeTagList = []
        tmpTagList = []
        for i in tmp:
            if i[0] == '-':
                tmpNegativeTagList.append(i[1:])
            else:
                tmpTagList.append(i)
        self.negativeTags = set(tmpNegativeTagList)

        if self.source == "gelbooru":
            self.params = gelbooruStartingDict
            self.params[self.pageIndicator] = int(startPage) - 1  # accomodating gelbooru's page numbering
        else:
            self.params = {}
            self.params[self.pageIndicator] = int(startPage)
        if len(tmpTagList) >= 2:
            self.params['tags'] = " ".join(tmpTagList[:2])
            self.additionalTags = set(tmpTagList[2:])
        else:
            self.params['tags'] = tagString
            self.additionalTags = set([])

    def queryData(self):
        allData = []
        count = 10  # Page counter, browse 10 pages at a time
        print(self.params)
        while True:
            if (count == 0):
                break
            resp = requests.get(url=self.endpoint, params=self.params)
            jsonData = json.loads(resp.text)
            self.params[self.pageIndicator] += 1
            count -= 1
            if (len(jsonData) == 0):
                break
            allData.extend(jsonData)
        return allData

    def filterData(self):
        listOfJSONObject = self.queryData()
        filteredData = []
        for obj in listOfJSONObject:
            tmpSet = set(obj[self.tagLine].split())
            if self.additionalTags.issubset(tmpSet) and self.negativeTags.isdisjoint(tmpSet):
                filteredData.append(obj)
        return filteredData

    def getNextBatch(self):
        if self.source == "gelbooru":
            tmp = dict(
                nextPage=self.params[self.pageIndicator] + 11,  # accomodate gelbooru page numbering
                pics=self.filterData(),
            )
        else:
            tmp = dict(
                nextPage=self.params[self.pageIndicator] + 10,
                pics=self.filterData(),
            )
        return tmp


if __name__ == "__main__":
    pass
