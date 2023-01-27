import sys
import webbrowser
from time import sleep

import requests
from lxml import etree
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *

from get_img import BackGroundPic
from searchui import Ui_MainWindow


class main(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.backgroundpic = BackGroundPic()
        self.initUI(self.backgroundpic.current_pic)

    def initUI(self, backgraoundpic: str):
        self.setStyle(QStyleFactory.create('Fusion'))
        self.setWindowIcon(QIcon('./assets/img/xhy.png'))
        self.setWindowTitle('SearchEngine')

        # 设置背景
        self.setStyleSheet(
            f"#MainWindow{{border-image:url({backgraoundpic})}}")

        self.setupUi(self)
        # self.baidu.setChecked(True)

        self.baidu.stateChanged.connect(lambda: self.search_url(self.baidu))
        self.bing.stateChanged.connect(lambda: self.search_url(self.bing))
        self.quark.stateChanged.connect(lambda: self.search_url(self.quark))

        self.keyword = ''
        self.page_all_num = 20
        self.page_num = 2

        self.search_url_dic = {'baidu': r'https://www.baidu.com/s',
                               'bing': r'https://cn.bing.com/search',
                               'quark': r'https://www.qwant.com/?q={}&count={}'}

        self.url = self.search_url_dic['baidu']
        self.linkXpath = {'baidu': r'//div[@class="result c-container xpath-log new-pmd"]',
                          'bing': r'/html/body/div[1]/main/ol/li[@class="b_algo"]',
                          'quark': r'//div[@class="result"]'}

        self.engine_params = {'baidu': {'wd': self.keyword, 'pn': 1, 'tn': 'baiduhome', 'ie': 'utf-8'},
                              'bing': {'q': self.keyword, 'first': 1},
                              'quark': {'q': self.keyword, 'count': 1}
                              }

        self.headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Mobile Safari/537.36 Edg/109.0.1518.55',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                        }

        self.lineEdit.textChanged.connect(self.setkeyword)
        self.spinBox.valueChanged.connect(self.setpage_all_num)
        self.pushButton.clicked.connect(self.search)

        self.params = {'wd': self.keyword, 'pn': str(
            self.page_all_num), 'tn': 'baiduhome', 'ie': 'utf-8'}

        self.linklist = []

    @staticmethod
    def rule(x): return x//10+1 if x % 10 != 0 else x//10

    def setkeyword(self, keyword):
        self.keyword = keyword

    def setpage_all_num(self, page_all_num):
        self.page_all_num = page_all_num
        self.page_num = self.rule(self.page_all_num)
        print(self.page_all_num)

    def search_url(self, e):
        print(e)
        if e.text() == '百度':
            self.url = self.search_url_dic['baidu']
        elif e.text() == '必应':
            self.url = self.search_url_dic['bing']
        else:
            self.url = self.search_url_dic['quark']

    def search(self):
        if self.baidu.isChecked():
            pass
        elif self.bing.isChecked():

            pass
        else:
            pass

        for page in range(self.page_num):
            print(page)
            self.engine_params['baidu']['wd'] = self.keyword
            self.engine_params['baidu']['pn'] = str(page*10)

            r = requests.get(
                url=self.url, headers=self.headers, params=self.engine_params['baidu'])

            t = etree.HTML(r.text)

            selector = t.xpath(self.linkXpath['baidu'])
            print(selector)
            for item in selector:
                print(item.xpath('.//h3/a')[0].text)
                link = item.xpath('.//h3/a')[0].get('href')
                self.linklist.append(link)

        for link in self.linklist:
            webbrowser.open(url=link)
            sleep(0.3)
        self.linklist.clear()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = main()
    window.show()
    window.backgroundpic.update()
    sys.exit(app.exec_())
