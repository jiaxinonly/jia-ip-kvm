# -*- coding: utf-8 -*-
# File: log.py
# Time: 2023/1/10 10:16
# Author: jiaxin
# Email: 1094630886@qq.com
import logging

formatter = logging.Formatter('[%(asctime)s] %(filename)s line %(lineno)d - %(levelname)s: %(message)s')
logger = logging.getLogger("jia-ip-kvm")
log_level = {'debug': logging.DEBUG, 'info': logging.INFO, 'warning': logging.WARNING, 'error': logging.ERROR,
             'critical': logging.CRITICAL}
DEFAULT_LEVEL = 'info'
DEFAULT_FILE = '../logs/jia-ip-kvm.log'

# file_handler = logging.FileHandler(DEFAULT_FILE)
# file_handler.setFormatter(formatter)
# logger.addHandler(file_handler)


logger.setLevel(log_level['debug'])

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)