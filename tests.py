#!/usr/bin/env python
# -*- coding: utf-8 -*-

# nosetests --nocapture tests.py

import webbrowser
from urlparse import parse_qs,urlparse
from wsgiref.simple_server import make_server
import threading
import sys
import random

from nose.tools import eq_,ok_

import keys
from pytumb.auth import OAuthHandler
from pytumb.api import API

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

# Settings for API.update_*_post
POST_STATE = API.STATE_PUBLISHED
BODY = 'Hello World!! Here is Body'
TAGS = ['Pytumb','Python']
SLUG = 'Pytumb2 Test %f' % random.random()
TITLE = 'Testing Pytumb2!!'
CAPTION = BODY
LINK = r'https://github.com/PyYoshi/Pytumb2'
PHOTO_SOURCE = r'https://github.com/PyYoshi/Pytumb2/raw/master/testdata/test_img.jpg'
PHOTO_FILES = ['testdata/test_img_.jpg']
#PHOTO_FILES = ['testdata/test_img.jpg','testdata/test_img2.jpg','testdata/test_img3.jpg']
QUOTE = BODY
QUOTE_SOURCE = '<a href="https://github.com/PyYoshi/Pytumb2"> Pytumb2 is awesom. </a>'
CONVERSATION = """ Dev: Who are you?
Bot: I'm tumblr bot!! """
AUDIO_FILE = 'testdata/menuettm.mp3'
AUDIO_EXTERNAL_URL = 'http://github.com/PyYoshi/Pytumb2/raw/master/testdata/menuettm.mp3'
VIDEO_FILE = 'testdata/s_hoshi.mp4'
VIDEO_EMBED = '<iframe width="420" height="315" src="http://www.youtube.com/embed/9bK5Ur0Vi0Y" frameborder="0" allowfullscreen></iframe>'

REBLOG_POSTID = '25090053296'
REBLOG_REBLOGKEY = 'H6R0DPp0'
REBLOG_COMMENT = BODY

FOLLOW_BLOG_URL = 'http://staff.tumblr.com/'

class TestPytumb:
    def __init__(self):
        self.auth = OAuthHandler(consumer_key=CONSUMER_KEY,consumer_secret=CONSUMER_SECRET,callback_url=CALLBACK_URL)
        self.auth.set_access_token(ACCESS_TOKEN,ACCESS_SECRET_TOKEN)
        self.api = API(auth_handler=self.auth)

    def est_a_a_get_access_token(self):
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

    def test_a_blog_get_bloginfo(self):
        print('test_a_blog_get_bloginfo')
        result = self.api.get_bloginfo(BLOG_HOSTNAME)
        print result.__dict__
        print('===========================')

    def test_b_blog_get_avatar_binary(self):
        print('test_b_blog_get_avatar_binary')
        result = self.api.get_avatar(BLOG_HOSTNAME,binary=True)
        print result.__dict__
        print('===========================')

    def test_c_blog_get_avatar_url(self):
        print('test_c_blog_get_avatar_url')
        result = self.api.get_avatar(BLOG_HOSTNAME)
        print result.__dict__
        print('===========================')

    def test_d_blog_get_followers(self):
        print('test_d_blog_get_followers')
        result = self.api.get_followers(BLOG_HOSTNAME)
        print result.__dict__
        print('===========================')

    def test_e_blog_get_posts(self):
        print('test_e_blog_get_posts')
        result = self.api.get_posts(BLOG_HOSTNAME)
        print result.__dict__
        print result.next().__dict__
        print('===========================')

    def test_f_blog_get_queue_draft(self):
        print('test_f_blog_get_queue_draft')
        result = self.api.get_queue_posts(BLOG_HOSTNAME)
        print result.__dict__
        print('===========================')

    def test_g_blog_get_draft_posts(self):
        print('test_g_blog_get_draft_posts')
        result = self.api.get_draft_posts(BLOG_HOSTNAME)
        print result.__dict__
        print('===========================')

    def test_h_blog_get_submission_posts(self):
        print('test_g_blog_get_submission_posts')
        result = self.api.get_submission_posts(BLOG_HOSTNAME)
        print result.__dict__
        print('===========================')

    def test_j_blog_update_text_post(self):
        print('test_g_blog_update_text_post')
        result = self.api.update_text_post(my_blog_hostname=BLOG_HOSTNAME,
            body=BODY, state=POST_STATE, tags=TAGS, slug=SLUG, title=TITLE)
        print result.__dict__
        print('===========================')

    def test_j_blog_update_photo_post_source(self):
        print('test_g_update_photo_post_source')
        result = self.api.update_photo_post(BLOG_HOSTNAME, source=PHOTO_SOURCE, caption=CAPTION,slug=SLUG,link=LINK)
        print result.__dict__
        print('===========================')

    def est_j_blog_update_photo_post_binary(self):
        print('test_g_update_photo_post_binary')
        result = self.api.update_photo_post(BLOG_HOSTNAME, files=PHOTO_FILES, caption=CAPTION,slug=SLUG,link=LINK)
        print result.__dict__
        print('===========================')

    def test_k_blog_update_quote_post(self):
        print('test_g_blog_update_quote_pos')
        result = self.api.update_quote_post(BLOG_HOSTNAME,QUOTE,POST_STATE,TAGS,slug=SLUG,source=QUOTE_SOURCE)
        print result.__dict__
        print('===========================')

    def test_l_blog_update_link_post(self):
        print('test_g_blog_update_link_post')
        result = self.api.update_link_post(BLOG_HOSTNAME,LINK,POST_STATE,TAGS,slug=SLUG,title=TITLE)
        print result.__dict__
        print('===========================')

    def test_n_blog_update_chat_post(self):
        print('test_g_blog_update_chat_post')
        result = self.api.update_chat_post(BLOG_HOSTNAME,CONVERSATION,POST_STATE,TAGS,slug=SLUG,title=TITLE)
        print result.__dict__
        print('===========================')

    def test_m_blog_update_audio_post_source(self):
        print('test_g_blog_update_audio_post_source')
        result = self.api.update_audio_post(BLOG_HOSTNAME,POST_STATE,TAGS,slug=SLUG,caption=CAPTION,external_url=AUDIO_EXTERNAL_URL)
        print result.__dict__
        print('===========================')

    def est_o_blog_update_audio_post_binary(self):
        print('test_g_blog_update_audio_post_binary')
        result = self.api.update_audio_post(BLOG_HOSTNAME,POST_STATE,TAGS,slug=SLUG,caption=CAPTION,data=AUDIO_FILE)
        print result.__dict__
        print('===========================')

    def test_p_blog_update_video_post_source(self):
        print('test_g_blog_update_video_post_source')
        result = self.api.update_video_post(BLOG_HOSTNAME,POST_STATE,TAGS,slug=SLUG,caption=CAPTION,embed=VIDEO_EMBED)
        print result.__dict__
        print('===========================')

    def est_q_blog_update_video_post_binary(self):
        print('test_g_blog_update_video_post_binary')
        result = self.api.update_video_post(BLOG_HOSTNAME,POST_STATE,TAGS,slug=SLUG,caption=CAPTION,data=VIDEO_FILE)
        print result.__dict__
        print('===========================')

    def test_e_blog_update_reblog_and_delete_this_post(self):
        print('test_g_blog_update_reblog')
        result = self.api.update_reblog(BLOG_HOSTNAME,REBLOG_POSTID,REBLOG_REBLOGKEY,REBLOG_COMMENT)
        print result.__dict__
        result2 = self.api.delete_post(BLOG_HOSTNAME,result.id)
        print result2.__dict__
        print('===========================')

    def test_s_user_get_userinfo(self):
        print('test_g_user_get_userinfo')
        result = self.api.get_userinfo()
        print result.__dict__
        print('===========================')

    def test_t_uget_dashbord(self):
        print('test_g_get_dashbord')
        result = self.api.get_dashbord()
        print result.__dict__
        result2 = result.next()
        print result2.__dict__
        print result.posts[-1].__dict__
        print result2.posts[0].__dict__
        print('===========================')

    def test_u_user_get_likes(self):
        print('test_g_user_get_likes')
        result = self.api.get_likes()
        print result.__dict__
        print result.next().__dict__
        print('===========================')

    def test_v_user_get_followings(self):
        print('test_g_user_get_followings')
        result = self.api.get_followings()
        print result.__dict__
        print result.next().__dict__
        print('===========================')

    def test_x_user_follow_unfollow(self):
        print('test_g_user_follow_unfollow')
        result = self.api.follow_blog(FOLLOW_BLOG_URL)
        print result.__dict__
        result2 = self.api.unfollow_blog(FOLLOW_BLOG_URL)
        print result2.__dict__
        print('===========================')

    def test_w_user_like_unlike(self):
        print('test_g_user_like_unlike')
        result = self.api.like_post(REBLOG_POSTID,REBLOG_REBLOGKEY)
        print result.__dict__
        result2 = self.api.unlike_post(REBLOG_POSTID,REBLOG_REBLOGKEY)
        print result2.__dict__
        print('===========================')