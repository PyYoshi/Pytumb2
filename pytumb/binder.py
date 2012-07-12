#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time

import requests

from pytumb.parser import ModelParser
from pytumb.error import PytumbError

class Binder:
    def __init__(self, api, api_url, api_auth_type, http_method,
                 response_type, response_list=False, api_parameters=None):
        """ description """
        self.api = api
        self.api_url = api_url
        self.api_auth_type = api_auth_type
        self.http_method = http_method
        self.response_type = response_type
        self.response_list = response_list
        self.api_parameters = api_parameters

    def execute(self,allow_redirects=True):
        # Add api_key
        if self.api_auth_type == self.api.AUTH_TYPE_APIKEY: self.api_parameters['api_key'] = self.api.auth._consumer.consumer.key
        # Run API
        retries_performed = 0
        while retries_performed < self.api.retry_count + 1:
            if self.api_auth_type == self.api.AUTH_TYPE_OAUTH:
                res = self.api.auth.apply_auth(url=self.api_url,http_method=self.http_method,parameters=self.api_parameters,allow_redirects=allow_redirects)
            else:
                if self.http_method == self.api.HTTP_METHOD_GET:
                    res = requests.get(self.api_url,params=self.api_parameters,allow_redirects=allow_redirects)
                elif self.http_method == self.api.HTTP_METHOD_POST:
                    res = requests.post(self.api_url,params=self.api_parameters,allow_redirects=allow_redirects)
                else:
                    raise PytumbError("This method( %s ) is not supported." % http_method) # methodはgetとpost以外ないので、その他のmethodはExceptionする。
            # Catch error and retry to run
            if self.api.retry_errors:
                if res.status_code not in self.api.retry_errors:
                    break
                else:
                    if res.status_code == 200:
                        break
            # Sleep
            time.sleep(self.api.retry_delay)
            retries_performed += 1
        # Generate parser
        parser = ModelParser()
        self.api.last_response = res
        # Parse error
        if res.status_code not in (200,201,301):
            error_msg = parser.parse_error(res.content)
            raise PytumbError(error_msg, res
            )
        # Parse content
        result = parser.parse(self,res.content)
        return result

