#!/usr/bin/env python
# -*- coding: utf-8 -*-

# nosetests --nocapture tests.py

import webbrowser
from urlparse import parse_qs,urlparse
from wsgiref.simple_server import make_server
import threading
import sys

from nose.tools import eq_,ok_

import keys
from pytumb.auth import OAuthHandler

try:
    import keys
    CONSUMER_KEY = keys.CONSUMER_KEY
    CONSUMER_SECRET = keys.CONSUMER_SECRET
    ACCESS_TOKEN = keys.ACCESS_TOKEN
    ACCESS_SECRET_TOKEN = keys.ACCESS_SECRET_TOKEN
    BLOG_HOSTNAME = keys.BLOG_HOSTNAME
    CALLBACK_URL = keys.CALLBACK_URL
except ImportError:
    CONSUMER_KEY = None
    CONSUMER_SECRET = None
    ACCESS_TOKEN = None
    ACCESS_SECRET_TOKEN = None
    BLOG_HOSTNAME = None
    CALLBACK_URL = "http://127.0.0.1:8859/login/"

class TestPytumb:
    def __init__(self):
        self.auth = OAuthHandler(consumer_key=CONSUMER_KEY,consumer_secret=CONSUMER_SECRET,callback_url=CALLBACK_URL)

    #def test_a_get_access_token(self):
    def get_access_token(self):
        print('')
        url = self.auth.get_authorization_url()
        request_tokens = self.auth.get_request_token()
        def get_atoken(env, res):
            if env['PATH_INFO']=='/login/':
                if env['REQUEST_METHOD']=='GET':
                    QUERY_STRING = env['QUERY_STRING']
                    if QUERY_STRING:
                        QUERY_STRING = parse_qs(QUERY_STRING)
                        oauth_token = QUERY_STRING['oauth_token'][0]
                        oauth_verifier = QUERY_STRING['oauth_verifier'][0]
                        threading.Thread(target=httpd.shutdown).start()
                        self.auth.set_request_token(request_tokens[0], request_tokens[1])
                        access_tokens = self.auth.get_access_token(oauth_verifier)
                        print('access_token:', access_tokens[0])
                        print('access_token_secret:', access_tokens[1])
                        res('200 OK',[('Content-type','text/html')])
                        html = "<html><head><title>Authenticated Successfully!</title></head><body>Authenticated Successfully!</body></html>"
                        return html
        try:
            if webbrowser.open(url) == False:
                raise webbrowser.Error
        except webbrowser.Error:
            print('webbrowser.Error')
            sys.exit(-1)
        except KeyboardInterrupt:
            sys.exit(1)
        host,port = urlparse(CALLBACK_URL).netloc.split(':')
        httpd = make_server(host,int(port),get_atoken)
        httpd.serve_forever()
