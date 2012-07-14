#!/usr/bin/env python
# -*- coding: utf-8 -*-

__vesion__ = '1.0.0'
__author__ = 'PyYoshi'
__license__ = 'MIT License'
__url__ = 'https://github.com/PyYoshi/Pytumb2'

from pytumb.auth import OAuthHandler
from pytumb.api import API
from pytumb.utils import Utils

# 全体的な TODO: ユーザ側が使用する関数のドキュメントの構築
# 全体的な TODO: 重複処理の簡素化。新たに変数を生成しなくてもいい処理等。  ※ただし、可読性を悪くする修正は行わないこと。