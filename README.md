# Enhanced Danbooru
I just want to search on Danbooru with more than 2 tags at the same time. The endpoint and return format is written at the top of the class file so I won't write it again here. Frontend is not included because I only wrote a crude one for my testing.

Used external lib:
- requests (and dependencies): the only way to make HTTP requests that I know of.
- Flask (and dependencies): I want to test Flask, the class file also includes a basic server if you don't want to use Flask.

Usage: start with `python3 server-flask.py` (server with Flask) or `python3 EnhancedDanbooru.py` (server without Flask). For anyone who feels lazy, I also prepared a docker image (dockerfile included in the repo), so use `docker run -p 5555:5555 tgquan67/enhanceddanbooru`.