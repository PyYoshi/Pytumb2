#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    import cStringIO as StringIO
except ImportError:
    import StringIO

from pytumb.utils import Utils

class Model:
    def __init__(self, api=None):
        self._api = api

    def __getstate__(self):
        pickle = dict(self.__dict__)
        try:
            del pickle['_api']
        except KeyError:
            pass
        return pickle

    @classmethod
    def parse(cls, api, json):
        raise NotImplementedError

    @classmethod
    def parse_list(cls, api, json_list):
        results = list()
        for obj in json_list:
            if obj:
                results.append(cls.parse(api, obj))
        return results

class BlogInfo(Model):
    @classmethod
    def parse(cls, api, json):
        bloginfo = cls(api)
        for k,v in json.get('blog', json).items():
            if k == 'updated':
                if v == 0:
                    v = None
                else:
                    v = Utils.unixtime2datetime(v)
            setattr(bloginfo, k, v)
        return bloginfo

    def follow(self):
        # TODO: follow関数のサポート
        raise NotImplementedError

    def unfollow(self):
        # TODO: unfollow関数のサポート
        raise NotImplementedError

    def get_avatar(self,binary=False):
        # TODO: get_avatar関数のサポート
        raise NotImplementedError

class BlogAvatar(Model):
    @classmethod
    def parse(cls, api, data):
        avatar = cls(api)
        res = api.last_response
        if res.history == []:
            setattr(avatar,'image_url',res.headers['location'])
        else:
            setattr(avatar,'image',StringIO.StringIO(data))
            setattr(avatar,'content_type',res.headers['content-type'])
        return avatar

class User(Model):
    @classmethod
    def parse(cls, api, json):
        user = cls(api)
        for k,v in json.items():
            if k == 'updated':
                if v == 0:
                    v = None
                else:
                    v = Utils.unixtime2datetime(v)
            setattr(user,k,v)
        return user

    def follow(self):
        # TODO: follow関数のサポート
        raise NotImplementedError

    def unfollow(self):
        # TODO: unfollow関数のサポート
        raise NotImplementedError

    def get_avatar(self,binary=False):
        # TODO: get_avatar関数のサポート
        raise NotImplementedError

class BlogFollowers(Model):
    TOTAL = 0
    @classmethod
    def parse(cls, api, json):
        users = User.parse_list(api,json['users'])
        cls.TOTAL += len(users)
        followers = cls(api)
        setattr(followers,'users',users)
        setattr(followers,'total_users', json['total_users'])
        return followers

    def next(self):
        return self._api.get_posts(self._api.blog_hostname, offset=self.TOTAL, limit=20)

class Post(Model):
    @classmethod
    def parse(cls, api, json):
        post = cls(api)
        for k,v in json.items():
            if k == 'timestamp': # Unnecessary value
                pass
            elif k == 'date':
                setattr(post,'date',Utils.gmtstring2datetime(v))
            else:
                setattr(post,k,v)
        return post

    @classmethod
    def parse_list(cls, api, json_list):
        results = list()
        try:
            posts = json_list.get('posts',json_list)
        except AttributeError:
            posts = json_list
        for obj in posts:
            if obj:
                results.append(cls.parse(api, obj))
        return results

    def follow(self):
        # TODO: follow関数のサポート
        raise NotImplementedError

    def unfollow(self):
        # TODO: unfollow関数のサポート
        raise NotImplementedError

    def like_post(self):
        # TODO: like_post関数のサポート
        raise NotImplementedError

    def unlike_post(self):
        # TODO: unlike_post関数のサポート
        raise NotImplementedError

class TextPost(Post):
    pass

class PhotoPost(Post):
    pass

class QuotePost(Post):
    pass

class LinkPost(Post):
    pass

class ChatPost(Post):
    pass

class AudioPost(Post):
    pass

class VideoPost(Post):
    pass

class AnswerPost(Post):
    pass

def autodetect_posts_type(api,posts_obj):
    results = []
    for post_obj in posts_obj:
        post_type = post_obj['type']
        if post_type == api.POST_TYPE_TEXT:
            result = TextPost.parse(api,post_obj)
        elif post_type == api.POST_TYPE_PHOTO:
            result = PhotoPost.parse(api,post_obj)
        elif post_type == api.POST_TYPE_QUOTE:
            result = QuotePost.parse(api,post_obj)
        elif post_type == api.POST_TYPE_LINK:
            result = LinkPost.parse(api,post_obj)
        elif post_type == api.POST_TYPE_CHAT:
            result = ChatPost.parse(api,post_obj)
        elif post_type == api.POST_TYPE_AUDIO:
            result = AudioPost.parse(api,post_obj)
        elif post_type == api.POST_TYPE_VIDEO:
            result = VideoPost.parse(api,post_obj)
        elif post_type == api.POST_TYPE_ANSWER:
            result = AnswerPost.parse(api,post_obj)
        else:
            result = Post.parse(api,post_obj)
        results.append(result)
    return results

class BlogPosts(Model):
    TOTAL = 0
    @classmethod
    def parse(cls, api, json):
        blogposts = cls(api)
        for k,v in json.items():
            if k == 'blog':
                v = BlogInfo.parse(api,v)
            elif k == 'posts':
                v = autodetect_posts_type(api,v)
                cls.TOTAL += len(v)
            setattr(blogposts,k,v)
        return blogposts

    def next(self):
        api_parameters = self._api.last_api_parameters
        path_endpoint = Utils.urlparse(self._api.last_api_url).path.split('/')[-1]
        if path_endpoint == self._api.POST_TYPE_TEXT:
            post_type = path_endpoint
        elif path_endpoint == self._api.POST_TYPE_QUOTE:
            post_type = path_endpoint
        elif path_endpoint == self._api.POST_TYPE_LINK:
            post_type = path_endpoint
        elif path_endpoint == self._api.POST_TYPE_ANSWER:
            post_type = path_endpoint
        elif path_endpoint == self._api.POST_TYPE_VIDEO:
            post_type = path_endpoint
        elif path_endpoint == self._api.POST_TYPE_AUDIO:
            post_type = path_endpoint
        elif path_endpoint == self._api.POST_TYPE_PHOTO:
            post_type = path_endpoint
        elif path_endpoint == self._api.POST_TYPE_CHAT:
            post_type = path_endpoint
        else:
            post_type=None
        return self._api.get_posts(self._api.blog_hostname
            ,post_type=post_type,reblog_info=api_parameters['reblog_info'],
            notes_info=api_parameters['notes_info'],post_filter=api_parameters['filter'],offset=self.TOTAL,limit=20)

class UserInfo(Model):
    @classmethod
    def parse(cls, api, json):
        userinfo = cls(api)
        for k,v in json['user'].items():
            if k == 'blogs': v = BlogInfo.parse_list(api,v)
            setattr(userinfo,k,v)
        return userinfo

class UserDashboard(Model):
    @classmethod
    def parse(cls, api, json):
        dashboard = cls(api)
        for k,v in json.items():
            if k == 'posts': v = Post.parse_list(api,v)
            setattr(dashboard,k,v)
        return dashboard

    def next(self):
        api_parameters = self._api.last_api_parameters
        since_id = self.posts[-1].id
        return self._api.get_dashbord(limit=20, post_type=api_parameters['type'],
            since_id=since_id,reblog_info=api_parameters['reblog_info'],
            notes_info=api_parameters['notes_info'])

class UserLikes(Model):
    TOTAL = 0
    @classmethod
    def parse(cls, api, json):
        likes = cls(api)
        for k,v in json.items():
            if k == 'liked_post':
                v = Post.parse_list(api,v)
                cls.TOTAL += len(v)
            setattr(likes,k,v)
        return likes

    def next(self):
        return self._api.get_likes(offset=self.TOTAL)

class UserFollowings(Model):
    TOTAL = 0
    @classmethod
    def parse(cls, api, json):
        following = cls(api)
        for k,v in json.items():
            if k == 'blogs':
                v = BlogInfo.parse_list(api,v)
                cls.TOTAL += len(v)
            setattr(following,k,v)
        return following

    def next(self):
        return self._api.get_followings(offset=self.TOTAL)

class Raw(Model):
    @classmethod
    def parse(cls, api, json):
        raw = cls(api)
        try:
            for k, v in json.items():
                setattr(raw, k, v)
        except AttributeError:
            pass
        return raw

    @classmethod
    def parse_list(cls, api, json_list):
        raw = cls(api)
        for k, v in json_list.items():
            setattr(raw, k, v)
        return raw

class UpdatePost(Raw):
    @classmethod
    def parse(cls, api, json):
        updatepost = cls(api)
        for k,v in json.items():
            setattr(updatepost,k,v)
        return updatepost

    def delete_post(self):
        raise NotImplementedError

class ModelFactory:
    bloginfo = BlogInfo
    avatar = BlogAvatar
    followers = BlogFollowers
    blogposts = BlogPosts
    post = Post
    updatepost = UpdatePost
    userinfo = UserInfo
    dashboard = UserDashboard
    likes = UserLikes
    followings = UserFollowings
    raw = Raw