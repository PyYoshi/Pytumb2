#!/usr/bin/env python
# -*- coding: utf-8 -*-

__all__ = ['API','OldAPI']

import os
import datetime

from pytumb.auth import OAuthHandler,BasicAuthHandler
from pytumb.binder import Binder
from pytumb.utils import Utils
from pytumb.error import PytumbError

class API:
    """Tumblr API v2"""
    # http://www.tumblr.com/docs/en/api/v2

    API_HOST = 'api.tumblr.com'
    API_VERSION = 'v2'
    API_METHOD_BLOG = 'blog'
    API_METHOD_USER = 'user'

    HTTP_METHOD_GET = 'GET'
    HTTP_METHOD_POST = 'POST'

    AUTH_TYPE_APIKEY = 'apikey'
    AUTH_TYPE_NONE = 'N/A'
    AUTH_TYPE_OAUTH = 'oauth'

    RESPONSE_TYPE_BLOGINFO = 'bloginfo'
    RESPONSE_TYPE_AVATAR = 'avatar'
    RESPONSE_TYPE_FOLLOWERS = 'followers'
    RESPONSE_TYPE_BLOGPOSTS = 'blogposts'
    RESPONSE_TYPE_POST = 'post'
    RESPONSE_TYPE_USERINFO = 'userinfo'
    RESPONSE_TYPE_DASHBOARD = 'dashbord'
    RESPONSE_TYPE_LIKES = 'likes'
    RESPONSE_TYPE_FOLLOWINGS = 'followings'
    RESPONSE_TYPE_RAW = 'raw'

    POST_TYPE_TEXT = 'text'
    POST_TYPE_QUOTE = 'quote'
    POST_TYPE_LINK = 'link'
    POST_TYPE_ANSWER = 'answer'
    POST_TYPE_VIDEO = 'video'
    POST_TYPE_AUDIO = 'audio'
    POST_TYPE_PHOTO = 'photo'
    POST_TYPE_CHAT = 'chat'

    POST_FILTER_NONE = None
    POST_FILTER_RAW = 'raw'
    POST_FILTER_TEXT = 'text'

    STATE_PUBLISHED = 'published'
    STATE_DRAFT = 'draft'
    STATE_QUEUE = 'queue'

    FILE_MAX_SIZE_IMAGE = 10 # MB
    FILE_MAX_SIZE_AUDIO = 10 # MB
    FILE_MAX_SIZE_VIDEO = 100 # MB

    def __init__(self, auth_handler, retry_count=0, retry_delay=0, retry_errors=list()):
        """ description
        Args:
            none
        Returns:
            none
        Exceptions:
            none
        Warnings:
            none
        """
        if not isinstance(auth_handler,OAuthHandler): raise PytumbError("This API is only supported OAuthHandler.") # auth_handlerはOAuthHandlerのみ。BasicAuthHandlerは弾くようにする。
        self.auth = auth_handler
        self.retry_count = retry_count
        self.retry_delay = retry_delay
        self.retry_errors = retry_errors
        self.blog_hostname = None

    def __build_api_url(self,secure, api_method, endpoint):
        """ description """
        if secure:
            scheme = 'https'
        else:
            scheme = 'http'
        return scheme + '://' + self.API_HOST + '/' + self.API_VERSION + '/' + api_method + '/' + endpoint

    def __check_file(self,filename, max_size, binary=True):
        """ description """
        file_size = os.path.getsize(filename)
        if file_size > (max_size* 1024): raise PytumbError('File is too big, must be less than %d' % (max_size * 1024))
        if binary:
            mode = 'rb'
        else:
            mode = 'r'
        data = file(filename, mode).read()
        return data, file_size

    ############################## Blog Methods ##############################

    def get_bloginfo(self,blog_hostname):
        """ description
        Args:
            blog_hostname: str,
                e.g.) staff.tumblr.com
        Returns:
            none
        Exceptions:
            none
        Warnings:
            none
        """
        # Type checking
        Utils.check_type(blog_hostname,'blog_hostname',str)

        # Setting
        self.blog_hostname = blog_hostname
        secure = False
        api_method = self.API_METHOD_BLOG
        endpoint = blog_hostname + '/' + 'info'
        api_auth_type = self.AUTH_TYPE_APIKEY
        http_method = self.HTTP_METHOD_GET
        response_type = self.RESPONSE_TYPE_BLOGINFO
        response_list = False
        api_parameters = {

        }
        api_url = self.__build_api_url(secure, api_method, endpoint)
        binder = Binder(
            api=self,
            api_url=api_url,
            api_auth_type=api_auth_type,
            http_method=http_method,
            response_type=response_type,
            response_list=response_list,
            api_parameters=api_parameters
        )
        return binder.execute()

    def get_avatar(self,blog_hostname, size=64, binary=False):
        """ description
        Args:
            blog_hostname: str,
                e.g.) staff.tumblr.com
            size: int, avatar image size,
                Must be one of the values: [16, 24, 30, 40, 48, 64, 96, 128, 512]
            binary: bool, False is to return avatar img-url. True is to return avatar img-binary(StringIO Object).
        Returns:
            str, img-url || {'data':StringIO, 'content_type':str}, img-binary
        Exceptions:
            none
        Warnings:
            none
        """
        # Type checking
        Utils.check_type(blog_hostname,'blog_hostname',str)
        if not size in [16, 24, 30, 40, 48, 64, 96, 128, 512]: raise PytumbError('Invalid size. Must be one of the values: 16, 24, 30, 40, 48, 64, 96, 128, 512')
        Utils.check_type(binary,'binary',bool)

        # Setting
        self.blog_hostname = blog_hostname
        if binary:
            allow_redirects=True
        else:
            allow_redirects=False
        secure = False
        api_method = self.API_METHOD_BLOG
        endpoint = blog_hostname + '/' + 'avatar' + '/' + str(size)
        api_auth_type = self.AUTH_TYPE_NONE
        http_method = self.HTTP_METHOD_GET
        response_type = self.RESPONSE_TYPE_AVATAR
        response_list = False
        api_parameters = {

        }
        api_url = self.__build_api_url(secure, api_method, endpoint)
        binder = Binder(
            api=self,
            api_url=api_url,
            api_auth_type=api_auth_type,
            http_method=http_method,
            response_type=response_type,
            response_list=response_list,
            api_parameters=api_parameters
        )
        return binder.execute(allow_redirects=allow_redirects)

    def get_followers(self,blog_hostname, limit=20, offset=0):
        """ description
        Args:
            blog_hostname: str,
                e.g.) staff.tumblr.com
            limit: int, The number of results to return
                1–20, inclusive
            offset: int, Result to start at
        Returns:
            none
        Exceptions:
            none
        Warnings:
            none
        """
        # Type checking
        Utils.check_type(blog_hostname,'blog_hostname',str)
        if not limit in range(1,21): raise PytumbError('Invalid limit. Must be one of the values: range(1,21)')
        Utils.check_type(offset,'offset',int)

        # Setting
        self.blog_hostname = blog_hostname
        secure = False
        api_method = self.API_METHOD_BLOG
        endpoint = blog_hostname + '/' + 'followers'
        api_auth_type = self.AUTH_TYPE_OAUTH
        http_method = self.HTTP_METHOD_GET
        response_type = self.RESPONSE_TYPE_FOLLOWERS
        response_list = False
        api_parameters = {
            'limit':limit,
            'offset':offset
        }
        api_url = self.__build_api_url(secure, api_method, endpoint)
        binder = Binder(
            api=self,
            api_url=api_url,
            api_auth_type=api_auth_type,
            http_method=http_method,
            response_type=response_type,
            response_list=response_list,
            api_parameters=api_parameters
        )
        return binder.execute()

    def get_posts(self,blog_hostname, post_type=None, post_id=None, tag=list(), limit=20, offset=0, reblog_info=False, notes_info=False, post_filter=POST_FILTER_NONE):
        """ description
        Args:
            blog_hostname: str,
                e.g.) staff.tumblr.com
            post_type: str, The type of post to return,
                Must be one of the values: None or API.POST_TYPE_TEXT, API.POST_TYPE_QUOTE, API.POST_TYPE_LINK, API.POST_TYPE_ANSWER, API.POST_TYPE_VIDEO, API.POST_TYPE_AUDIO, API.POST_TYPE_PHOTO, API.POST_TYPE_CHAT
            post_id: str, post id
            tag: list, Limits the response to posts with the specified tag
            limit: int, The number of results to return
                1–20, inclusive
            offset: int, Result to start at
            reblog_info: bool, Indicates whether to return reblog information (specify true or false). Returns the various reblogged_ fields.
            notes_info: bool, Indicates whether to return notes information (specify true or false). Returns note count and note metadata.
            post_filter: str, Specifies the post format to return, other than HTML
                Must be one of the values: POST_FILTER_NONE, POST_FILTER_RAW, POST_FILTER_TEXT
        Returns:
            none
        Exceptions:
            PytumbError
        Warnings:
            none
        """
        # Type checking
        Utils.check_type(blog_hostname,'blog_hostname',str)
        if post_type in [self.POST_TYPE_TEXT, self.POST_TYPE_QUOTE, self.POST_TYPE_LINK, self.POST_TYPE_ANSWER, self.POST_TYPE_VIDEO, self.POST_TYPE_AUDIO, self.POST_TYPE_PHOTO, self.POST_TYPE_CHAT]:
            endpoint = blog_hostname + '/' + 'posts' + '/' + post_type
        else:
            endpoint = blog_hostname + '/' + 'posts'
        Utils.check_type(post_id,'post_id',str)
        Utils.check_type(tag,'tag',list)
        if not limit in range(1,21): raise PytumbError('Invalid limit. Must be one of the values: range(1,21)')
        Utils.check_type(offset,'offset',int)
        Utils.check_type(reblog_info,'reblog_info',bool)
        Utils.check_type(notes_info,'notes_info',bool)
        Utils.check_type(post_filter,'post_filter',str)

        # Setting
        self.blog_hostname = blog_hostname
        tag = Utils.join_string(tag,',')
        secure = False
        api_method = self.API_METHOD_BLOG
        api_auth_type = self.AUTH_TYPE_APIKEY
        http_method = self.HTTP_METHOD_GET
        response_type = self.RESPONSE_TYPE_BLOGPOSTS
        response_list = False
        api_parameters = {
            'id':post_id,
            'tag':tag,
            'limit':limit,
            'offset':offset,
            'reblog_info':reblog_info,
            'notes_info':notes_info,
            'filter':post_filter,
        }
        api_url = self.__build_api_url(secure, api_method, endpoint)
        binder = Binder(
            api=self,
            api_url=api_url,
            api_auth_type=api_auth_type,
            http_method=http_method,
            response_type=response_type,
            response_list=response_list,
            api_parameters=api_parameters
        )
        return binder.execute()

    def get_queue_posts(self,my_blog_hostname):
        """ description
        Args:
            my_blog_hostname: str,
                e.g.) staff.tumblr.com
        Returns:
            none
        Exceptions:
            none
        Warnings:
            none
        """
        # Type checking
        Utils.check_type(my_blog_hostname,'my_blog_hostname',str)

        # Setting
        self.blog_hostname = my_blog_hostname
        secure = False
        api_method = self.API_METHOD_BLOG
        endpoint = my_blog_hostname + '/' + 'posts' + '/' + 'queue'
        api_auth_type = self.AUTH_TYPE_OAUTH
        http_method = self.HTTP_METHOD_GET
        response_type = self.RESPONSE_TYPE_POST
        response_list = True
        api_parameters = {

        }
        api_url = self.__build_api_url(secure, api_method, endpoint)
        binder = Binder(
            api=self,
            api_url=api_url,
            api_auth_type=api_auth_type,
            http_method=http_method,
            response_type=response_type,
            response_list=response_list,
            api_parameters=api_parameters
        )
        return binder.execute()

    def get_draft_posts(self,my_blog_hostname):
        """ description
        Args:
            my_blog_hostname: str,
                e.g.) staff.tumblr.com
        Returns:
            none
        Exceptions:
            none
        Warnings:
            none
        """
        # Type checking
        Utils.check_type(my_blog_hostname,'my_blog_hostname',str)

        # Setting
        self.blog_hostname = my_blog_hostname
        secure = False
        api_method = self.API_METHOD_BLOG
        endpoint = my_blog_hostname + '/' + 'posts' + '/' + 'draft'
        api_auth_type = self.AUTH_TYPE_OAUTH
        http_method = self.HTTP_METHOD_GET
        response_type = self.RESPONSE_TYPE_POST
        response_list = True
        api_parameters = {

        }
        api_url = self.__build_api_url(secure, api_method, endpoint)
        binder = Binder(
            api=self,
            api_url=api_url,
            api_auth_type=api_auth_type,
            http_method=http_method,
            response_type=response_type,
            response_list=response_list,
            api_parameters=api_parameters
        )
        return binder.execute()

    def get_submission_posts(self,my_blog_hostname):
        """ description
        Args:
            my_blog_hostname: str,
                e.g.) staff.tumblr.com
        Returns:
            none
        Exceptions:
            none
        Warnings:
            none
        """
        # Type checking
        Utils.check_type(my_blog_hostname,'my_blog_hostname',str)

        # Setting
        self.blog_hostname = my_blog_hostname
        secure = False
        api_method = self.API_METHOD_BLOG
        endpoint = my_blog_hostname + '/' + 'posts' + '/' + 'submission'
        api_auth_type = self.AUTH_TYPE_OAUTH
        http_method = self.HTTP_METHOD_GET
        response_type = self.RESPONSE_TYPE_POST
        response_list = True
        api_parameters = {

        }
        api_url = self.__build_api_url(secure, api_method, endpoint)
        binder = Binder(
            api=self,
            api_url=api_url,
            api_auth_type=api_auth_type,
            http_method=http_method,
            response_type=response_type,
            response_list=response_list,
            api_parameters=api_parameters
        )
        return binder.execute()

    def update_text_post(self,my_blog_hostname, body,state=STATE_PUBLISHED, tags=list(),
                    tweet=None, date=None, markdown=False, slug=None, title=None):
        """ description
        Args:
            my_blog_hostname: str,
                e.g.) staff.tumblr.com
            state: str, The state of the post.
                Must be one of the values: API.STATE_PUBLISHED ,API.STATE_DRAFT ,API.STATE_QUEUE
            tags: list, Comma-separated tags for this post
            tweet: str, Manages the autotweet (if enabled) for this post: set to off for no tweet, or enter text to override the default tweet
            date: datetime.datetime, Time of the post
            markdown: bool, Indicates whether the post uses markdown syntax
            slug: str, Add a short text summary to the end of the post URL
            body: str, The full post body, HTML allowed
            title: str, The optional title of the post, HTML entities must be escaped
        Returns:
            none
        Exceptions:
            none
        Warnings:
            none
        """
        # Type checking
        if not state in [self.STATE_DRAFT,self.STATE_PUBLISHED,self.STATE_QUEUE]: raise PytumbError('Invalid state. Must be one of the values: API.STATE_PUBLISHED ,API.STATE_DRAFT ,API.STATE_QUEUE')
        Utils.check_type(my_blog_hostname,'my_blog_hostname',str)
        Utils.check_type(tags,'tags',list)
        Utils.check_type(tweet,'tweet',str)
        Utils.check_type(date,'date',datetime.datetime)
        Utils.check_type(markdown,'markdown',bool)
        Utils.check_type(slug,'slug',str)
        Utils.check_type(body,'body',str)
        Utils.check_type(title,'title',str)

        # Setting
        self.blog_hostname = my_blog_hostname
        tags = Utils.join_string(tags,'+')
        date = Utils.datetime2gmtstring(date)
        post_type = self.POST_TYPE_TEXT
        secure = False
        api_method = self.API_METHOD_BLOG
        endpoint = my_blog_hostname + '/' + 'post'
        api_auth_type = self.AUTH_TYPE_OAUTH
        http_method = self.HTTP_METHOD_POST
        response_type = self.RESPONSE_TYPE_RAW
        response_list = False
        api_parameters = {
            'type':post_type,
            'state':state,
            'tags':tags,
            'tweet':tweet,
            'date':date,
            'markdown':markdown,
            'slug':slug,
            'body':body,
            'title':title,
            }
        api_url = self.__build_api_url(secure, api_method, endpoint)
        binder = Binder(
            api=self,
            api_url=api_url,
            api_auth_type=api_auth_type,
            http_method=http_method,
            response_type=response_type,
            response_list=response_list,
            api_parameters=api_parameters
        )
        return binder.execute()

    def update_photo_post(self,my_blog_hostname, state=STATE_PUBLISHED, tags=list(),
                        tweet=None, date=None, markdown=False, slug=None,caption=None,link=None,source=None,files=list()):
        """ description
        Args:
            my_blog_hostname: str,
                e.g.) staff.tumblr.com
            state: str, The state of the post.
                Must be one of the values: API.STATE_PUBLISHED ,API.STATE_DRAFT ,API.STATE_QUEUE
            tags: list, Comma-separated tags for this post
            tweet: str, Manages the autotweet (if enabled) for this post: set to off for no tweet, or enter text to override the default tweet
            date: datetime.datetime, Time of the post
            markdown: bool, Indicates whether the post uses markdown syntax
            slug: str, Add a short text summary to the end of the post URL
            caption: str, The user-supplied caption, HTML allowed
            link: str, The "click-through URL" for the photo
            source: str, The photo source URL
                either source or files
            files: list, list of file path
                either source or files
        Returns:
            none
        Exceptions:
            none
        Warnings:
            none
        """
        # Type checking
        if not state in [self.STATE_DRAFT,self.STATE_PUBLISHED,self.STATE_QUEUE]: raise PytumbError('Invalid state. Must be one of the values: API.STATE_PUBLISHED ,API.STATE_DRAFT ,API.STATE_QUEUE')
        Utils.check_type(my_blog_hostname,'my_blog_hostname',str)
        Utils.check_type(tags,'tags',list)
        Utils.check_type(tweet,'tweet',str)
        Utils.check_type(date,'date',datetime.datetime)
        Utils.check_type(markdown,'markdown',bool)
        Utils.check_type(slug,'slug',str)
        Utils.check_type(caption,'caption',str)
        Utils.check_type(link,'link',str)
        Utils.check_type(source,'source',str)
        Utils.check_type(files,'files',list)
        if source and files: raise PytumbError('Either source or files.')
        if not source and (not files or files == []): raise PytumbError('Either source or files.')

        # Setting
        self.blog_hostname = my_blog_hostname
        tags = Utils.join_string(tags,'+')
        date = Utils.datetime2gmtstring(date)
        post_type = self.POST_TYPE_PHOTO
        secure = False
        api_method = self.API_METHOD_BLOG
        endpoint = my_blog_hostname + '/' + 'post'
        api_auth_type = self.AUTH_TYPE_OAUTH
        http_method = self.HTTP_METHOD_POST
        response_type = self.RESPONSE_TYPE_RAW
        response_list = False
        api_parameters = {
            'type':post_type,
            'state':state,
            'tags':tags,
            'tweet':tweet,
            'date':date,
            'markdown':markdown,
            'slug':slug,
            'caption':caption,
            'link':link,
            }
        if source:
            api_parameters['source'] = source
        elif files:
            api_parameters['data_list'] = files
        api_url = self.__build_api_url(secure, api_method, endpoint)
        binder = Binder(
            api=self,
            api_url=api_url,
            api_auth_type=api_auth_type,
            http_method=http_method,
            response_type=response_type,
            response_list=response_list,
            api_parameters=api_parameters
        )
        return binder.execute()

    def update_quote_post(self,my_blog_hostname, quote, state=STATE_PUBLISHED, tags=list(),
                        tweet=None, date=None, markdown=False, slug=None, source=None):
        """ description
        Args:
            my_blog_hostname: str,
                e.g.) staff.tumblr.com
            state: str, The state of the post.
                Must be one of the values: API.STATE_PUBLISHED ,API.STATE_DRAFT ,API.STATE_QUEUE
            tags: list, Comma-separated tags for this post
            tweet: str, Manages the autotweet (if enabled) for this post: set to off for no tweet, or enter text to override the default tweet
            date: datetime.datetime, Time of the post
            markdown: bool, Indicates whether the post uses markdown syntax
            slug: str, Add a short text summary to the end of the post URL
            quote: str, The full text of the quote, HTML entities must be escaped
            source: str, Cited source, HTML allowed
        Returns:
            none
        Exceptions:
            none
        Warnings:
            none
        """
        # Type checking
        if not state in [self.STATE_DRAFT,self.STATE_PUBLISHED,self.STATE_QUEUE]: raise PytumbError('Invalid state. Must be one of the values: API.STATE_PUBLISHED ,API.STATE_DRAFT ,API.STATE_QUEUE')
        Utils.check_type(my_blog_hostname,'my_blog_hostname',str)
        Utils.check_type(tags,'tags',list)
        Utils.check_type(tweet,'tweet',str)
        Utils.check_type(date,'date',datetime.datetime)
        Utils.check_type(markdown,'markdown',bool)
        Utils.check_type(slug,'slug',str)
        Utils.check_type(quote,'quote',str)
        Utils.check_type(source,'source',str)

        # Setting
        self.blog_hostname = my_blog_hostname
        tags = Utils.join_string(tags,'+')
        date = Utils.datetime2gmtstring(date)
        post_type = self.POST_TYPE_QUOTE
        secure = False
        api_method = self.API_METHOD_BLOG
        endpoint = my_blog_hostname + '/' + 'post'
        api_auth_type = self.AUTH_TYPE_OAUTH
        http_method = self.HTTP_METHOD_POST
        response_type = self.RESPONSE_TYPE_RAW
        response_list = False
        api_parameters = {
            'type':post_type,
            'state':state,
            'tags':tags,
            'tweet':tweet,
            'date':date,
            'markdown':markdown,
            'slug':slug,
            'quote':quote,
            'source':source,
            }
        api_url = self.__build_api_url(secure, api_method, endpoint)
        binder = Binder(
            api=self,
            api_url=api_url,
            api_auth_type=api_auth_type,
            http_method=http_method,
            response_type=response_type,
            response_list=response_list,
            api_parameters=api_parameters
        )
        return binder.execute()

    def update_link_post(self,my_blog_hostname, url, state=STATE_PUBLISHED, tags=list(),
                        tweet=None, date=None, markdown=False, slug=None, title=None):
        """ description
        Args:
            my_blog_hostname: str,
                e.g.) staff.tumblr.com
            state: str, The state of the post.
                Must be one of the values: API.STATE_PUBLISHED ,API.STATE_DRAFT ,API.STATE_QUEUE
            tags: list, Comma-separated tags for this post
            tweet: str, Manages the autotweet (if enabled) for this post: set to off for no tweet, or enter text to override the default tweet
            date: datetime.datetime, Time of the post
            markdown: bool, Indicates whether the post uses markdown syntax
            slug: str, Add a short text summary to the end of the post URL
            title: str, The title of the page the link points to, HTML entities should be escaped
            url: str, The link
        Returns:
            none
        Exceptions:
            none
        Warnings:
            none
        """
        # Type checking
        if not state in [self.STATE_DRAFT,self.STATE_PUBLISHED,self.STATE_QUEUE]: raise PytumbError('Invalid state. Must be one of the values: API.STATE_PUBLISHED ,API.STATE_DRAFT ,API.STATE_QUEUE')
        Utils.check_type(my_blog_hostname,'my_blog_hostname',str)
        Utils.check_type(tags,'tags',list)
        Utils.check_type(tweet,'tweet',str)
        Utils.check_type(date,'date',datetime.datetime)
        Utils.check_type(markdown,'markdown',bool)
        Utils.check_type(slug,'slug',str)
        Utils.check_type(title,'title',str)
        Utils.check_type(url,'url',str)

        # Setting
        self.blog_hostname = my_blog_hostname
        tags = Utils.join_string(tags,'+')
        date = Utils.datetime2gmtstring(date)
        post_type = self.POST_TYPE_LINK
        secure = False
        api_method = self.API_METHOD_BLOG
        endpoint = my_blog_hostname + '/' + 'post'
        api_auth_type = self.AUTH_TYPE_OAUTH
        http_method = self.HTTP_METHOD_POST
        response_type = self.RESPONSE_TYPE_RAW
        response_list = False
        api_parameters = {
            'type':post_type,
            'state':state,
            'tags':tags,
            'tweet':tweet,
            'date':date,
            'markdown':markdown,
            'slug':slug,
            'title':title,
            'url':url
            }
        api_url = self.__build_api_url(secure, api_method, endpoint)
        binder = Binder(
            api=self,
            api_url=api_url,
            api_auth_type=api_auth_type,
            http_method=http_method,
            response_type=response_type,
            response_list=response_list,
            api_parameters=api_parameters
        )
        return binder.execute()

    def update_chat_post(self,my_blog_hostname, conversation, state=STATE_PUBLISHED, tags=list(),
                        tweet=None, date=None, markdown=False, slug=None,title=None):
        """ description
        Args:
            my_blog_hostname: str,
                e.g.) staff.tumblr.com
            state: str, The state of the post.
                Must be one of the values: API.STATE_PUBLISHED ,API.STATE_DRAFT ,API.STATE_QUEUE
            tags: list, Comma-separated tags for this post
            tweet: str, Manages the autotweet (if enabled) for this post: set to off for no tweet, or enter text to override the default tweet
            date: datetime.datetime, Time of the post
            markdown: bool, Indicates whether the post uses markdown syntax
            slug: str, Add a short text summary to the end of the post URL
            title: str, The title of the chat
            conversation: str, The text of the conversation/chat, with dialogue labels(no HTML)
        Returns:
            none
        Exceptions:
            none
        Warnings:
            none
        """
        # Type checking
        if not state in [self.STATE_DRAFT,self.STATE_PUBLISHED,self.STATE_QUEUE]: raise PytumbError('Invalid state. Must be one of the values: API.STATE_PUBLISHED ,API.STATE_DRAFT ,API.STATE_QUEUE')
        Utils.check_type(my_blog_hostname,'my_blog_hostname',str)
        Utils.check_type(tags,'tags',list)
        Utils.check_type(tweet,'tweet',str)
        Utils.check_type(date,'date',datetime.datetime)
        Utils.check_type(markdown,'markdown',bool)
        Utils.check_type(slug,'slug',str)
        Utils.check_type(title,'title',str)
        Utils.check_type(conversation,'conversation',str)

        # Setting
        self.blog_hostname = my_blog_hostname
        tags = Utils.join_string(tags,'+')
        date = Utils.datetime2gmtstring(date)
        post_type = self.POST_TYPE_CHAT
        secure = False
        api_method = self.API_METHOD_BLOG
        endpoint = my_blog_hostname + '/' + 'post'
        api_auth_type = self.AUTH_TYPE_OAUTH
        http_method = self.HTTP_METHOD_POST
        response_type = self.RESPONSE_TYPE_RAW
        response_list = False
        api_parameters = {
            'type':post_type,
            'state':state,
            'tags':tags,
            'tweet':tweet,
            'date':date,
            'markdown':markdown,
            'slug':slug,
            'title':title,
            'conversation':conversation
            }
        api_url = self.__build_api_url(secure, api_method, endpoint)
        binder = Binder(
            api=self,
            api_url=api_url,
            api_auth_type=api_auth_type,
            http_method=http_method,
            response_type=response_type,
            response_list=response_list,
            api_parameters=api_parameters
        )
        return binder.execute()

    def update_audio_post(self,my_blog_hostname, data, state=STATE_PUBLISHED, tags=list(),
                        tweet=None, date=None, markdown=False, slug=None, caption=None, external_url=None):
        """ description
        Args:
            my_blog_hostname: str,
                e.g.) staff.tumblr.com
            state: str, The state of the post.
                Must be one of the values: API.STATE_PUBLISHED ,API.STATE_DRAFT ,API.STATE_QUEUE
            tags: list, Comma-separated tags for this post
            tweet: str, Manages the autotweet (if enabled) for this post: set to off for no tweet, or enter text to override the default tweet
            date: datetime.datetime, Time of the post
            markdown: bool, Indicates whether the post uses markdown syntax
            slug: str, Add a short text summary to the end of the post URL
            caption: str, The user-supplied caption
            external_url: str, The URL of the site that hosts the audio file (not tumblr)
                Either external_url or data
            data: str, An audio file path
                Either external_url or data
        Returns:
            none
        Exceptions:
            none
        Warnings:
            none
        """
        # Type checking
        if not state in [self.STATE_DRAFT,self.STATE_PUBLISHED,self.STATE_QUEUE]: raise PytumbError('Invalid state. Must be one of the values: API.STATE_PUBLISHED ,API.STATE_DRAFT ,API.STATE_QUEUE')
        Utils.check_type(my_blog_hostname,'my_blog_hostname',str)
        Utils.check_type(tags,'tags',list)
        Utils.check_type(tweet,'tweet',str)
        Utils.check_type(date,'date',datetime.datetime)
        Utils.check_type(markdown,'markdown',bool)
        Utils.check_type(slug,'slug',str)
        Utils.check_type(caption,'caption',str)
        Utils.check_type(external_url,'external_url',str)
        Utils.check_type(data,'data',str)
        if external_url and data: raise PytumbError('Either external_url or files.')
        if not (external_url and data): raise PytumbError('Either external_url or files.')

        # Setting
        self.blog_hostname = my_blog_hostname
        tags = Utils.join_string(tags,'+')
        date = Utils.datetime2gmtstring(date)
        post_type = self.POST_TYPE_AUDIO
        secure = False
        api_method = self.API_METHOD_BLOG
        endpoint = my_blog_hostname + '/' + 'post'
        api_auth_type = self.AUTH_TYPE_OAUTH
        http_method = self.HTTP_METHOD_POST
        response_type = self.RESPONSE_TYPE_RAW
        response_list = False
        api_parameters = {
            'type':post_type,
            'state':state,
            'tags':tags,
            'tweet':tweet,
            'date':date,
            'markdown':markdown,
            'slug':slug,
            'caption':caption,
            'external_url':external_url,
            'data':data
            }
        api_url = self.__build_api_url(secure, api_method, endpoint)
        binder = Binder(
            api=self,
            api_url=api_url,
            api_auth_type=api_auth_type,
            http_method=http_method,
            response_type=response_type,
            response_list=response_list,
            api_parameters=api_parameters
        )
        return binder.execute()

    def update_video_post(self,my_blog_hostname, state=STATE_PUBLISHED, tags=list(),
                        tweet=None, date=None, markdown=False, slug=None, caption=None, embed=None, data=None):
        """ description
        Args:
            my_blog_hostname: str,
                e.g.) staff.tumblr.com
            state: str, The state of the post.
                Must be one of the values: API.STATE_PUBLISHED ,API.STATE_DRAFT ,API.STATE_QUEUE
            tags: list, Comma-separated tags for this post
            tweet: str, Manages the autotweet (if enabled) for this post: set to off for no tweet, or enter text to override the default tweet
            date: datetime.datetime, Time of the post
            markdown: bool, Indicates whether the post uses markdown syntax
            slug: str, Add a short text summary to the end of the post URL
            caption: str, The user-supplied caption
            embed: str, HTML embed code for the video
                Either embed or data
            data: str(urlencoded), A video file path
                Either embed or data
        Returns:
            none
        Exceptions:
            none
        Warnings:
            none
        """
        # Type checking
        if not state in [self.STATE_DRAFT,self.STATE_PUBLISHED,self.STATE_QUEUE]: raise PytumbError('Invalid state. Must be one of the values: API.STATE_PUBLISHED ,API.STATE_DRAFT ,API.STATE_QUEUE')
        Utils.check_type(my_blog_hostname,'my_blog_hostname',str)
        Utils.check_type(tags,'tags',list)
        Utils.check_type(tweet,'tweet',str)
        Utils.check_type(date,'date',datetime.datetime)
        Utils.check_type(markdown,'markdown',bool)
        Utils.check_type(slug,'slug',str)
        Utils.check_type(caption,'caption',str)
        Utils.check_type(embed,'embed',str)
        Utils.check_type(data,'data',str)
        if embed and data: raise PytumbError('Either embed or data.')
        if not (embed and data): raise PytumbError('Either source or data.')

        # Setting
        self.blog_hostname = my_blog_hostname
        tags = Utils.join_string(tags,'+')
        date = Utils.datetime2gmtstring(date)
        post_type = self.POST_TYPE_VIDEO
        secure = False
        api_method = self.API_METHOD_BLOG
        endpoint = my_blog_hostname + '/' + 'post'
        api_auth_type = self.AUTH_TYPE_OAUTH
        http_method = self.HTTP_METHOD_POST
        response_type = self.RESPONSE_TYPE_RAW
        response_list = False
        api_parameters = {
            'type':post_type,
            'state':state,
            'tags':tags,
            'tweet':tweet,
            'date':date,
            'markdown':markdown,
            'slug':slug,
            'caption':caption
            }
        if embed:
            api_parameters['embed'] = embed
        elif data:
            api_parameters['data'] = data
        api_url = self.__build_api_url(secure, api_method, endpoint)
        binder = Binder(
            api=self,
            api_url=api_url,
            api_auth_type=api_auth_type,
            http_method=http_method,
            response_type=response_type,
            response_list=response_list,
            api_parameters=api_parameters
        )
        return binder.execute()

    ### /post/edit: POST, AUTH_TYPE_OAUTH
    ## api.tumblr.com/v2/blog/{base-hostname}/post/edit
    ## id: int, The ID of the post to edit
    ##  requires
    # TODO: API.update_*_post()の引数にpost_idを入れて、/post/editの対応を行う。

    def update_reblog(self,my_blog_hostname, post_id, reblog_key, comment=None):
        """ description
        Args:
            my_blog_hostname: str,
                e.g.) staff.tumblr.com
            post_id: str, The ID of the reblogged post on tumblelog
            reblog_key: str, The reblog key for the reblogged post - get the reblog key with a /post request
            comment: str, A comment added tot the reblogged post
        Returns:
            none
        Exceptions:
            none
        Warnings:
            none
        """
        # Type checking
        Utils.check_type(my_blog_hostname,'my_blog_hostname',str)
        Utils.check_type(post_id,'post_id',str)
        Utils.check_type(reblog_key,'reblog_key',str)
        Utils.check_type(comment,'comment',str)

        # Setting
        secure = False
        api_method = self.API_METHOD_BLOG
        endpoint = blog_hostname + '/' + 'post' + '/' + 'reblog'
        api_auth_type = self.AUTH_TYPE_OAUTH
        http_method = self.HTTP_METHOD_POST
        response_type = self.RESPONSE_TYPE_RAW
        response_list = False
        api_parameters = {
            'id':post_id,
            'reblog_key':reblog_key,
            'comment':comment
        }
        api_url = self.__build_api_url(secure, api_method, endpoint)
        binder = Binder(
            api=self,
            api_url=api_url,
            api_auth_type=api_auth_type,
            http_method=http_method,
            response_type=response_type,
            response_list=response_list,
            api_parameters=api_parameters
        )
        return binder.execute()

    def delete_post(self,my_blog_hostname,post_id):
        """ description
        Args:
            my_blog_hostname: str,
                e.g.) staff.tumblr.com
        Returns:
            none
        Exceptions:
            none
        Warnings:
            none
        """
        # Type checking
        Utils.check_type(my_blog_hostname,'my_blog_hostname',str)
        Utils.check_type(post_id,'post_id',str)

        # Setting
        self.blog_hostname = my_blog_hostname
        secure = False
        api_method = self.API_METHOD_BLOG
        endpoint = blog_hostname + '/' + 'post' + '/' + 'delete'
        api_auth_type = self.AUTH_TYPE_OAUTH
        http_method = self.HTTP_METHOD_POST
        response_type = self.RESPONSE_TYPE_RAW
        response_list = False
        api_parameters = {
            'id':post_id
        }
        api_url = self.__build_api_url(secure, api_method, endpoint)
        binder = Binder(
            api=self,
            api_url=api_url,
            api_auth_type=api_auth_type,
            http_method=http_method,
            response_type=response_type,
            response_list=response_list,
            api_parameters=api_parameters
        )
        return binder.execute()

    ############################## User Methods ##############################

    def get_userinfo(self):
        """ description
        Args:
            none
        Returns:
            none
        Exceptions:
            none
        Warnings:
            none
        """
        # Setting
        secure = False
        api_method = self.API_METHOD_USER
        endpoint = 'user'
        api_auth_type = self.AUTH_TYPE_OAUTH
        http_method = self.HTTP_METHOD_POST
        response_type = self.RESPONSE_TYPE_USERINFO
        response_list = False
        api_parameters = {

        }
        api_url = self.__build_api_url(secure, api_method, endpoint)
        binder = Binder(
            api=self,
            api_url=api_url,
            api_auth_type=api_auth_type,
            http_method=http_method,
            response_type=response_type,
            response_list=response_list,
            api_parameters=api_parameters
        )
        return binder.execute()

    def get_dashbord(self, limit=20, offset=0, post_type=None, since_id=None, reblog_info=False, notes_info=False):
        """ description
        Args:
            post_type: str, The type of post to return,
                Must be one of the values: None or API.POST_TYPE_TEXT, API.POST_TYPE_QUOTE, API.POST_TYPE_LINK, API.POST_TYPE_ANSWER, API.POST_TYPE_VIDEO, API.POST_TYPE_AUDIO, API.POST_TYPE_PHOTO, API.POST_TYPE_CHAT
            limit: int, The number of results to return
                1–20, inclusive
            offset: int, Result to start at
            since_id: str, Return posts that have appeared after this ID
            reblog_info: bool, Indicates whether to return reblog information (specify true or false). Returns the various reblogged_ fields.
            notes_info: bool, Indicates whether to return notes information (specify true or false). Returns note count and note metadata.
        Returns:
            none
        Exceptions:
            none
        Warnings:
            none
        """
        # Type checking
        if post_type in [self.POST_TYPE_TEXT, self.POST_TYPE_QUOTE, self.POST_TYPE_LINK, self.POST_TYPE_ANSWER, self.POST_TYPE_VIDEO,
                         self.POST_TYPE_AUDIO, self.POST_TYPE_PHOTO, self.POST_TYPE_CHAT]: raise PytumbError('Invalid post_type. Must be one of the values: None or API.POST_TYPE_TEXT, API.POST_TYPE_QUOTE, API.POST_TYPE_LINK, API.POST_TYPE_ANSWER, API.POST_TYPE_VIDEO, API.POST_TYPE_AUDIO, API.POST_TYPE_PHOTO, API.POST_TYPE_CHAT')
        if not limit in range(1,21): raise PytumbError('Invalid limit. Must be one of the values: range(1,21)')
        Utils.check_type(since_id,'since_id',str)
        Utils.check_type(offset,'offset',int)
        Utils.check_type(reblog_info,'reblog_info',bool)
        Utils.check_type(notes_info,'notes_info',bool)

        # Setting
        secure = False
        api_method = self.API_METHOD_USER
        endpoint = 'dashboard'
        api_auth_type = self.AUTH_TYPE_OAUTH
        http_method = self.HTTP_METHOD_GET
        response_type = self.RESPONSE_TYPE_DASHBOARD
        response_list = True
        api_parameters = {
            'limit':limit,
            'offset':offset,
            'type':post_type,
            'since_id':since_id,
            'reblog_info':reblog_info,
            'notes_info':notes_info
        }
        api_url = self.__build_api_url(secure, api_method, endpoint)
        binder = Binder(
            api=self,
            api_url=api_url,
            api_auth_type=api_auth_type,
            http_method=http_method,
            response_type=response_type,
            response_list=response_list,
            api_parameters=api_parameters
        )
        return binder.execute()

    def get_likes(self,limit=20,offset=0):
        """ description
        Args:
            limit: int, The number of results to return
            offset: int, Liked post number to start at
        Returns:
            none
        Exceptions:
            none
        Warnings:
            none
        """
        # Type checking
        if not limit in range(1,21): raise PytumbError('Invalid limit. Must be one of the values: range(1,21)')
        Utils.check_type(offset,'offset',int)

        # Setting
        secure = False
        api_method = self.API_METHOD_USER
        endpoint = 'likes'
        api_auth_type = self.AUTH_TYPE_OAUTH
        http_method = self.HTTP_METHOD_GET
        response_type = self.RESPONSE_TYPE_LIKES
        response_list = True
        api_parameters = {
            'limit':limit,
            'offset':offset
        }
        api_url = self.__build_api_url(secure, api_method, endpoint)
        binder = Binder(
            api=self,
            api_url=api_url,
            api_auth_type=api_auth_type,
            http_method=http_method,
            response_type=response_type,
            response_list=response_list,
            api_parameters=api_parameters
        )
        return binder.execute()

    def get_followings(self,limit=20,offset=0):
        """ description
        Args:
            limit: int, The number of results to return
            offset: int, Liked post number to start at
        Returns:
            none
        Exceptions:
            none
        Warnings:
            none
        """
        # Type checking
        if not limit in range(1,21): raise PytumbError('Invalid limit. Must be one of the values: range(1,21)')
        Utils.check_type(offset,'offset',int)

        # Setting
        secure = False
        api_method = self.API_METHOD_USER
        endpoint = 'following'
        api_auth_type = self.AUTH_TYPE_OAUTH
        http_method = self.HTTP_METHOD_GET
        response_type = self.RESPONSE_TYPE_FOLLOWINGS
        response_list = True
        api_parameters = {
            'limit':limit,
            'offset':offset
        }
        api_url = self.__build_api_url(secure, api_method, endpoint)
        binder = Binder(
            api=self,
            api_url=api_url,
            api_auth_type=api_auth_type,
            http_method=http_method,
            response_type=response_type,
            response_list=response_list,
            api_parameters=api_parameters
        )
        return binder.execute()

    def follow_blog(self,blog_url):
        """ description
        Args:
            blog_url: str, The URL of the blog to follow
        Returns:
            none
        Exceptions:
            none
        Warnings:
            none
        """
        # Type checking
        Utils.check_type(blog_url,'blog_url',str)

        # Setting
        secure = False
        api_method = self.API_METHOD_USER
        endpoint = 'follow'
        api_auth_type = self.AUTH_TYPE_OAUTH
        http_method = self.HTTP_METHOD_POST
        response_type = self.RESPONSE_TYPE_RAW
        response_list = False
        api_parameters = {
            'url':blog_url
        }
        api_url = self.__build_api_url(secure, api_method, endpoint)
        binder = Binder(
            api=self,
            api_url=api_url,
            api_auth_type=api_auth_type,
            http_method=http_method,
            response_type=response_type,
            response_list=response_list,
            api_parameters=api_parameters
        )
        return binder.execute()

    def unfollow_blog(self,blog_url):
        """ description
        Args:
            blog_url: str, The URL of the blog to unfollow
        Returns:
            none
        Exceptions:
            none
        Warnings:
            none
        """
        # Type checking
        Utils.check_type(blog_url,'blog_url',str)

        # Setting
        secure = False
        api_method = self.API_METHOD_USER
        endpoint = 'unfollow'
        api_auth_type = self.AUTH_TYPE_OAUTH
        http_method = self.HTTP_METHOD_POST
        response_type = self.RESPONSE_TYPE_RAW
        response_list = False
        api_parameters = {
            'url':blog_url
        }
        api_url = self.__build_api_url(secure, api_method, endpoint)
        binder = Binder(
            api=self,
            api_url=api_url,
            api_auth_type=api_auth_type,
            http_method=http_method,
            response_type=response_type,
            response_list=response_list,
            api_parameters=api_parameters
        )
        return binder.execute()

    def like_post(self,post_id,reblog_key):
        """ description
        Args:
            post_id: int, The ID of the post to like
            reblog_key: str, The reblog key for the post id
        Returns:
            none
        Exceptions:
            none
        Warnings:
            none
        """
        # Type checking
        Utils.check_type(post_id,'post_id',str)
        Utils.check_type(reblog_key,'reblog_key',str)

        # Setting
        secure = False
        api_method = self.API_METHOD_USER
        endpoint = 'like'
        api_auth_type = self.AUTH_TYPE_OAUTH
        http_method = self.HTTP_METHOD_POST
        response_type = self.RESPONSE_TYPE_RAW
        response_list = False
        api_parameters = {
            'id':post_id,
            'reblog_key':reblog_key
        }
        api_url = self.__build_api_url(secure, api_method, endpoint)
        binder = Binder(
            api=self,
            api_url=api_url,
            api_auth_type=api_auth_type,
            http_method=http_method,
            response_type=response_type,
            response_list=response_list,
            api_parameters=api_parameters
        )
        return binder.execute()

    def unlike_post(self,post_id,reblog_key):
        """ description
        Args:
            post_id: int, The ID of the post to like
            reblog_key: str, The reblog key for the post id
        Returns:
            none
        Exceptions:
            none
        Warnings:
            none
        """
        # Type checking
        Utils.check_type(post_id,'post_id',str)
        Utils.check_type(reblog_key,'reblog_key',str)

        # Setting
        secure = False
        api_method = self.API_METHOD_USER
        endpoint = 'unlike'
        api_auth_type = self.AUTH_TYPE_OAUTH
        http_method = self.HTTP_METHOD_POST
        response_type = self.RESPONSE_TYPE_RAW
        response_list = False
        api_parameters = {
            'id':post_id,
            'reblog_key':reblog_key
        }
        api_url = self.__build_api_url(secure, api_method, endpoint)
        binder = Binder(
            api=self,
            api_url=api_url,
            api_auth_type=api_auth_type,
            http_method=http_method,
            response_type=response_type,
            response_list=response_list,
            api_parameters=api_parameters
        )
        return binder.execute()

