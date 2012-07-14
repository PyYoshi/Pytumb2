#!/usr/bin/env python
# -*- coding: utf-8 -*-

import webbrowser
from urlparse import parse_qs, urlparse
import threading
import sys
from wsgiref.simple_server import make_server

try:
    import cPickle as pickle
except ImportError:
    import pickle

from pytumb import OAuthHandler, API

# Setting
CONSUMER_KEY = ''
CONSUMER_SECRRET_KEY = ''
CALLBACK_URL = 'http://127.0.0.1:8957/login/'
PICKLE_FILENAME = 'atoken.pickle'
YOUR_BLOG_HOSTNAME = '' # e.g) your_tumblr.tumblr.com
TEXT_POST_BODY = 'Hello World!'

def get_access_token():
    auth = OAuthHandler(consumer_key=CONSUMER_KEY,consumer_secret=CONSUMER_SECRRET_KEY,callback_url=CALLBACK_URL)
    authorization_url = auth.get_authorization_url()
    request_tokens = auth.get_request_token()
    def get_atoken(env,res):
        if env['REQUEST_METHOD']=='GET':
            QUERY_STRING = env['QUERY_STRING']
            if QUERY_STRING:
                QUERY_STRING = parse_qs(QUERY_STRING)
                oauth_token = QUERY_STRING['oauth_token'][0]
                oauth_verifier = QUERY_STRING['oauth_verifier'][0]
                threading.Thread(target=httpd.shutdown).start()
                auth.set_request_token(request_tokens[0], request_tokens[1])
                access_tokens = auth.get_access_token(oauth_verifier)
                atoken_obj = {
                    'ACCESS_TOKEN':access_tokens[0],
                    'ACCESS_TOKEN_SECRET':access_tokens[1]
                }
                fp = file(PICKLE_FILENAME,'wb')
                pickle.dump(atoken_obj,fp)
                fp.close()
                res('200 OK',[('Content-type','text/html')])
                html = "<html><head><title>Authenticated Successfully!</title></head>"\
                       "<body>Authenticated Successfully!<br>"\
                       "Access Token: %s<br>"\
                       "Access Token Secret: %s<br></body></html>" % (access_tokens[0], access_tokens[1])
                return html
    try:
        if webbrowser.open(authorization_url) == False:
            raise webbrouwser.Error
    except webbrowser.Error as e:
        print(e)
        sys.exit(-1)
    except KeyboardInterrupt:
        sys.exit(1)

    host,port = urlparse(CALLBACK_URL).netloc.split(':')
    httpd = make_server(host,int(port),get_atoken)
    httpd.serve_forever()

def update_text(your_blog_hostname, body):
    auth = OAuthHandler(CONSUMER_KEY,CONSUMER_SECRRET_KEY)
    auth.set_access_token(ACCESS_TOKEN,ACCESS_TOKEN_SECRET)
    api = API(auth)
    return api.update_text_post(your_blog_hostname,body)

if __name__ in '__main__':
    print('Example 1: Get access token.')
    get_access_token()

    fp = file(PICKLE_FILENAME,'rb')
    key = pickle.load(fp)
    fp.close()
    ACCESS_TOKEN = key['ACCESS_TOKEN']
    ACCESS_TOKEN_SECRET = key['ACCESS_TOKEN_SECRET']

    print('Example 2: Update text post.')
    result = update_text(YOUR_BLOG_HOSTNAME,TEXT_POST_BODY)
    print(result.__dict__)


