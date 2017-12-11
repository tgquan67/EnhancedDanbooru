# endpoint /?tags=xxx yyy&page=zzz
# return {pic: [], nextPage: int}
import requests
import json
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib import parse


class danbooruPostQuery:
    endpoint = "http://danbooru.donmai.us/posts.json"

    def __init__(self, tagString, startPage=1):
        tmp = tagString.split()
        tmpNegativeTagList = []
        tmpTagList = []
        for i in tmp:
            if i[0] == '-':
                tmpNegativeTagList.append(i[1:])
            else:
                tmpTagList.append(i)
        self.negativeTags = set(tmpNegativeTagList)

        if len(tmpTagList) >= 2:
            self.primaryTags = dict(
                tags=" ".join(tmpTagList[:2]),
                page=int(startPage),
            )
            self.additionalTags = set(tmpTagList[2:])
        else:
            self.primaryTags = dict(
                tags=tagString,
                page=int(startPage),
            )
            self.additionalTags = set([])

    def queryData(self):
        allData = []
        count = 10  # Page counter, browse 10 pages at a time
        while True:
            if (count == 0):
                break
            resp = requests.get(url=self.endpoint, params=self.primaryTags)
            jsonData = json.loads(resp.text)
            self.primaryTags["page"] += 1
            count -= 1
            if (len(jsonData) == 0):
                break
            allData.extend(jsonData)
        return allData

    def filterData(self):
        listOfJSONObject = self.queryData()
        filteredData = []
        for obj in listOfJSONObject:
            tmpSet = set(obj["tag_string"].split())
            if self.additionalTags.issubset(tmpSet) and self.negativeTags.isdisjoint(tmpSet):
                filteredData.append(obj)
        return filteredData

    def getNextBatch(self):
        tmp = dict(
            nextPage=self.primaryTags["page"] + 10,
            pics=self.filterData(),
        )
        return tmp


class danbooruHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if len(self.path) > 1:
            params = dict(x.split('=')
                          for x in parse.unquote_plus(self.path[2:]).split('&'))
            query = danbooruPostQuery(params.get(
                "tags", ""), params.get("page", 1))
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            jsonData = json.JSONEncoder().encode(query.getNextBatch())
            self.wfile.write(jsonData.encode("utf_8"))


def run():
    serverAddress = ("", 80)
    httpd = HTTPServer(serverAddress, danbooruHTTPRequestHandler)
    print("started, waiting for requests")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
