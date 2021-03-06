from EnhancedDanbooru import DanbooruPostQuery
from flask import Flask, request
import json
server = Flask(__name__)


@server.route("/")
def respond():
    query = DanbooruPostQuery(
        tagString=request.args.get("tags", ""),
        startPage=request.args.get("page", 1),
        source=request.args.get("source", "danbooru"))
    resp = server.make_response(json.JSONEncoder().encode(query.getNextBatch()).encode("utf_8"))
    resp.headers["Content-Type"] = "application/json; charset=utf-8"
    resp.headers["Access-Control-Allow-Origin"] = "*"
    return resp


if __name__ == "__main__":
    server.run(host="0.0.0.0", port=5555)
