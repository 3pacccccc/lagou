# -*- coding:utf-8 -*-
__author__ = 'maruimin'
import re

a = 'python/222'
if '/' in a:
    b = a.split('/')[0]
else:
    b = a
print(b)