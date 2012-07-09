#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = ['OAuthHandler','BasicAuthHandler']

import urlparse
import urllib

from oauth_hook import OAuthHook
from oauth_hook.auth import Token
import requests
from requests.auth import HTTPBasicAuth

from pytumb.error import PytumbError

class AuthHandler:
    """ """
    def apply_auth(self, url, method, headers, parameters):
        raise NotImplementedError

class BasicAuthHandler(AuthHandler):
    """ """
    def __init__(self,email,password):
        self.__basic_auth = HTTPBasicAuth(username=email,password=password)

    def apply_auth(self, url, method, headers, parameters):
        if method == "GET":
            url = url + "?" + urllib.urlencode(parameters)
            return requests.get(url,auth=self.__basic_auth)
        elif method == "POST":
            return requests.post(url,parameters,auth=self.__basic_auth)
        else:
            raise PytumbError("This method(%s) is not supported." % method) # methodはgetとpost以外ないので、その他のmethodはExceptionする。

class OAuthHandler(AuthHandler):
    """ """

    OAUTH_HOST = 'www.tumblr.com'
    OAUTH_ROOT = '/oauth/'

    def __init__(self,consumer_key,consumer_secret,callback_url=None,secure=False):
        self.__consumer = OAuthHook(consumer_key=consumer_key,consumer_secret=consumer_secret)
        self.callback_url = callback_url
        self.secure = secure
        self.__request_tokens = None
        self.__access_tokens = None

    def __gen_oauth_url(self,endpoint):
        if self.secure:
            prefix = "https://"
        else:
            prefix = "http://"
        return prefix + self.OAUTH_HOST + self.OAUTH_ROOT + endpoint

    def __get_request_token(self):
        url = self.__gen_oauth_url('request_token')
        res = requests.post(url,{'oauth_callback':self.callback_url},hooks={'pre_request':self.__consumer})
        qs = urlparse.parse_qs(res.text)
        request_token = qs['oauth_token'][0]
        request_secret = qs['oauth_token_secret'][0]
        return request_token, request_secret

    def get_authorization_url(self):
        self.__request_tokens = self.__get_request_token()
        url = self.__gen_oauth_url('authorize' + '?oauth_token=%s'%(self.__request_tokens[0]))
        return url

    def get_request_token(self):
        return self.__request_tokens

    def set_request_token(self,key,secret):
        self.__request_tokens = [key, secret]

    def get_access_token(self,verifier):
        url = self.__gen_oauth_url('access_token')
        self.__consumer.token = Token(self.__request_tokens[0],self.__request_tokens[1])
        res = requests.post(url,{'oauth_verifier':verifier},hooks={'pre_request':self.__consumer})
        qs = urlparse.parse_qs(res.content)
        access_token = qs['oauth_token'][0]
        access_token_secret = qs['oauth_token_secret'][0]
        self.__access_tokens = [access_token,access_token_secret]
        return self.__access_tokens

    def set_access_token(self,access_token, access_token_secret):
        self.__access_tokens = [access_token,access_token_secret]

    def apply_auth(self, url, method, headers, parameters):
        if not self.__access_tokens:
            raise PytumbError("Requires access token. Please do OAuthHandler.set_access_token()") # access tokenがない場合Exception
        else:
            self.__consumer.token = Token(self.__access_tokens[0],self.__access_tokens[1])
        client = requests.session(hooks={'pre_request':self.__consumer})
        if method == "GET":
            qs = urllib.urlencode(parameters)
            url = url + '?' + qs
            return client.get(url)
        elif method == "POST":
            return client.post(url,parameters)
        else:
            raise PytumbError("This method( %s ) is not supported." % method) # methodはgetとpost以外ないので、その他のmethodはExceptionする。
