import requests, json, sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib import parse
class danbooruPostQuery:
    endpoint = 'http://danbooru.donmai.us/posts.json'
    def __init__(self,tagString,startPage=1):
        tmp=tagString.split()
        if len(tmp)>=2:
            self.primaryTags = dict (
                tags = " ".join(tmp[:2]),
                page = startPage,
            )
            self.additionalTags=set(tmp[2:])
        else:
            self.primaryTags = dict (
                tags = tagString,
                page = startPage,
            )
            self.additionalTags=set([])
    def queryData(self):
        allData = []
        count = 10 #Page counter, browse 10 pages at a time
        while True:
            if (count==0):
                break
            resp = requests.get(url=self.endpoint,params=self.primaryTags)
            jsonData = json.loads(resp.text)
            self.primaryTags['page']+=1
            count-=1
            if (len(jsonData)==0):
                break
            allData.extend(jsonData)
        return allData
    def filterData(self):
        listOfJSONObject = self.queryData()
        filteredData = []
        for obj in listOfJSONObject:
            if self.additionalTags.issubset(obj['tag_string'].split()):
                filteredData.append(obj)
        return filteredData
    def getNextBatch(self):
        return self.filterData()

class danbooruHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        query=danbooruPostQuery(parse.unquote_plus(self.path[1:]))
        self.send_response(200)
        self.send_header('Content-Type','application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin','*')
        self.end_headers()
        jsonData=json.JSONEncoder().encode(query.getNextBatch())
        self.wfile.write(jsonData.encode("utf_8"))

def run():
    serverAddress=('',80)
    httpd=HTTPServer(serverAddress,danbooruHTTPRequestHandler)
    print('started, waiting for requests')
    httpd.serve_forever()

if __name__ == '__main__':
    run()