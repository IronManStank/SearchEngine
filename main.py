import sys
import webbrowser
from time import sleep

import requests
from lxml import etree
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
from config import Config
from get_img import BackGroundPic
from searchui import Ui_MainWindow


class main(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.backgroundpic = BackGroundPic()
        self.config = Config()
        self.initUI(self.backgroundpic.current_pic, self.config)

    def initUI(self, backgraoundpic: str, config: Config):
        self.setStyle(QStyleFactory.create('Fusion'))
        self.setWindowIcon(QIcon('./assets/img/xhy.png'))
        self.setWindowTitle('SearchEngine')

        # 设置背景
        if config.back_enable:
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
                               'quark': r'https://quark.sm.cn/s'}
        self.url = self.search_url_dic['baidu']
        self.linkXpath = {'baidu': r'//div[@class="result c-container xpath-log new-pmd"]',
                          'bing': r'//main/ol/li[@class="b_algo"]',
                          'quark': r'/html/body//div[@id="results"]/div'}

        self.subxpath = {'baidu': r'.//h3/a',
                         'bing': [r'.//div[@class="b_title"]/h2/a', r'.//div[@class="b_algoheader"]/a'],
                         'quark': r'./div[1]/a'}

        self.engine_params = {'baidu': {'wd': self.keyword, 'pn': 1, 'tn': 'baiduhome', 'ie': 'utf-8'},
                              'bing': {'q': self.keyword, 'first': 1},
                              'quark': {'q': self.keyword, 'snum': '10', 'page': 1}
                              }

        self.headers = {
            'User-Agent':
            'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) \
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Mobile Safari/537.36 Edg/109.0.1518.55',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        }

        self.lineEdit.textChanged.connect(self.setkeyword)
        self.spinBox.valueChanged.connect(self.setpage_all_num)
        self.pushButton.clicked.connect(self.search)

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
        print(e.text())
        if e.text() == '百度':
            self.url = self.search_url_dic['baidu']
        elif e.text() == '必应':
            self.url = self.search_url_dic['bing']
        else:
            self.url = self.search_url_dic['quark']

    @staticmethod
    def get_list(**kwargs) -> list:
        result = []
        r = requests.get(
            url=kwargs['url'], headers=kwargs['headers'], params=kwargs['params'])

        with open('test.html', 'wb') as f:
            f.write(r.content)

        t = etree.HTML(r.content)

        print(kwargs['linkXpath'])
        selector = t.xpath(kwargs['linkXpath'])
        print(selector)

        for item in selector:
            # link = item.xpath(kwargs['subxpath'])
            # print(link)
            print(item)
            if len(kwargs['subxpath']) != 1:
                try:
                    for rule in kwargs['subxpath']:
                        print(rule)

                        link = item.xpath(rule)[0].get('href')
                        print(link)
                        result.append(link)
                except Exception as e:
                    print(e)
                    break

                # finally:
                #     continue
            else:
                link = item.xpath(kwargs['subxpath'])[0].get('href')
                print(link)
                result.append(link)

        return result

    @staticmethod
    def open_link(linklist):
        for link in linklist:
            webbrowser.open(url=link)
            sleep(0.3)

    def search(self):

        if self.baidu.isChecked():
            self.engine_params['baidu']['wd'] = self.keyword
            for page in range(self.page_num):
                self.engine_params['baidu']['pn'] = str(page*10+1)

                r = requests.get(
                    url=self.url, headers=self.headers, params=self.engine_params['baidu'])

                t = etree.HTML(r.content)
                selector = t.xpath(self.linkXpath['baidu'])
                print(selector)
                for item in selector:
                    link = item.xpath(self.subxpath['baidu'])[0].get('href')

                    self.linklist.append(link)
            self.open_link(self.linklist)

        elif self.bing.isChecked():

            self.engine_params['bing']['q'] = self.keyword
            for page in range(self.page_num):
                self.engine_params['baidu']['first'] = str(page*10+1)

                r = requests.get(
                    url=self.url, headers=self.headers, params=self.engine_params['bing'])

                t = etree.HTML(r.content)
                selector = t.xpath(self.linkXpath['bing'])

                for i in self.subxpath['bing']:
                    try:
                        for item in selector:

                            link = item.xpath(i)[0].get('href')

                            self.linklist.append(link)
                    except IndexError:
                        print("bing引擎sub规则匹配失败，尝试其他规则中……")

                        break

                    finally:
                        continue

            self.open_link(self.linklist)
            self.linklist.clear()

        else:
            self.engine_params['quark']['q'] = self.keyword
            for page in range(1, self.page_num+1):
                self.engine_params['quark']['page'] = page

                r = requests.get(
                    url=self.url, headers=self.headers, params=self.engine_params['quark'])

                t = etree.HTML(r.content)
                selector = t.xpath(self.linkXpath['quark'])

                for item in selector:
                    temp = item.xpath(self.subxpath['quark'])
                    if len(temp):
                        link = temp[0].get('href')
                        self.linklist.append(link)

            self.open_link(self.linklist)


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = main()
    window.show()
    window.backgroundpic.update()
    sys.exit(app.exec_())
