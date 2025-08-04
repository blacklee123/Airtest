# -*- coding: utf-8 -*-
from airtest.utils.resolution import cocos_min_strategy
import os
import cv2
import re

class Settings(object):

    DEBUG = False
    LOG_DIR = None
    LOG_FILE = "log.txt"
    RESIZE_METHOD = staticmethod(cocos_min_strategy)
    # keypoint matching: kaze/brisk/akaze/orb, contrib: sift/surf/brief
    CVSTRATEGY = ["mstpl", "tpl", "sift", "brisk"]
    
    # 使用元组比较替代 distutils.version
    # 将版本号转换为可比较的整数元组
    def parse_version(version_str):
        # 提取主要版本号部分 (忽略后缀如 -dev, +extra 等)
        version_match = re.match(r'(\d+)(?:\.(\d+))?(?:\.(\d+))?', version_str)
        if not version_match:
            return (0, 0, 0)  # 无法解析时返回最低版本
        
        major = int(version_match.group(1)) if version_match.group(1) else 0
        minor = int(version_match.group(2)) if version_match.group(2) else 0
        patch = int(version_match.group(3)) if version_match.group(3) else 0
        
        return (major, minor, patch)
    
    # 获取 OpenCV 版本并解析
    cv_version = parse_version(cv2.__version__)
    min_version = parse_version('3.4.2')
    max_version = parse_version('4.4.0')
    
    # 进行版本范围比较
    if min_version < cv_version < max_version:
        CVSTRATEGY = ["mstpl", "tpl", "brisk"]
    
    KEYPOINT_MATCHING_PREDICTION = True
    THRESHOLD = 0.7  # [0, 1]
    THRESHOLD_STRICT = None  # dedicated parameter for assert_exists
    OPDELAY = 0.1
    FIND_TIMEOUT = 20
    FIND_TIMEOUT_TMP = 3
    PROJECT_ROOT = os.environ.get("PROJECT_ROOT", "")  # for ``using`` other script
    SNAPSHOT_QUALITY = 10  # 1-100 https://pillow.readthedocs.io/en/5.1.x/handbook/image-file-formats.html#jpeg
    # Image compression size, e.g. 1200, means that the size of the screenshot does not exceed 1200*1200
    IMAGE_MAXSIZE = os.environ.get("IMAGE_MAXSIZE", None)
    SAVE_IMAGE = True