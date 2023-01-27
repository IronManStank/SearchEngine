#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# 文件: get_img.py
# 说明: 获取图片
# 时间: 2023/01/27 12:18:09

'''
如何使用:

from get_img import BackGroundPic

backg = BackGroundPic() # 实例化就已经更新图片了
backg.update()          # 也可以手动更新
backg.current_pic       # 图片位置

'''

import shutil
from os import makedirs, remove
from os.path import isdir, isfile

import requests
from retry import retry


class GetPicError(Exception):
    pass


RANDOM_PIC_URL = 'http://123.249.20.186:3000/random'


@retry(tries=3)
def _get_one_random_pic(path: str):
    '''
    随机获取一个图片
    :param path: 保存路径
    '''
    res = requests.get(RANDOM_PIC_URL, timeout=5)
    if not res.ok:
        raise GetPicError('无法获取图片')
    else:
        with open(path, 'wb') as fr:
            fr.write(res.content)
        print(f'保存图片到: {path}')


class BackGroundPic(object):
    '''
    背景图片，获取一次新的，和多获取一个用来下次用
    '''

    # 保存图片的文件夹
    IMG_DIR = './imgs'

    def __init__(self) -> None:
        # 当前使用的图片
        self.__current_pic = f'{self.IMG_DIR}/0.jpg'
        # 下一个图片
        self.__next_pic = f'{self.IMG_DIR}/1.jpg'

        if not isdir(self.IMG_DIR):
            makedirs(self.IMG_DIR)
            print('创建文件夹:', self.IMG_DIR)

        self.update()

    def __rotate(self):
        '''删除旧的，获取新的'''
        # 删除旧的
        if isfile(self.__current_pic):
            remove(self.__current_pic)
        # 移动next到current
        if isfile(self.__next_pic):
            shutil.move(self.__next_pic, self.__current_pic)
        else:
            # 如果不存在就下载到 current
            _get_one_random_pic(self.__current_pic)
        # 下载 next
        _get_one_random_pic(self.__next_pic)

    def update(self):
        '''手动更新图片'''
        try:
            self.__rotate()
        except GetPicError as e:
            print(f'Err: {e}')

    @property
    def current_pic(self):
        '''图片地址，如果尝试3次都失败了会返回默认的'''
        if not isfile(self.__current_pic):
            return './assets/img/xhy.png'
        return self.__current_pic
