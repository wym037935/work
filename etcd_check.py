#coding=utf-8
import etcd
import re
import os
import sys,urllib

import wymlog
import logging
import mod_config

logger = wymlog.Logger('etcd_log.txt','mysql').getlog()


