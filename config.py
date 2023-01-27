#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# 文件: config.py
# 说明: 配置文件
# 时间: 2023/01/27 15:26:12

import json
from typing import Dict, Any
from os.path import isfile


class Config(object):
    CONFIG_PATH = './config.json'

    def __init__(self) -> None:
        self.back_enable = True

        self.read_conf_file()

    @property
    def data(self):
        return {
            "back_enable": self.back_enable
        }

    def write_to_config(self):
        '''写入配置'''
        with open(self.CONFIG_PATH, 'w', encoding='utf-8') as fr:
            json.dump(self.data, fr, indent=1, ensure_ascii=False)

    def read_conf_file(self) -> Dict[str, Any]:
        '''
        读取配置文件
        '''
        if not isfile(self.CONFIG_PATH):
            self.write_to_config()
            return self.data
        else:
            with open(self.CONFIG_PATH, 'r', encoding='utf-8') as fr:
                content = json.load(fr)

            # 更新属性们
            self.back_enable = content['back_enable']

            return content
