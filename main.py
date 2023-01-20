import requests
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from searchui import Ui_MainWindow
import webbrowser
from lxml import etree
from time import sleep


class main(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        QApplication.setStyle(QStyleFactory.create('Fusion'))
        self.setupUi(self)
        # self.baidu.setChecked(True)

        self.baidu.stateChanged.connect(lambda: self.search_url(self.baidu))
        self.biying.stateChanged.connect(lambda: self.search_url(self.biying))
        self.kuake.stateChanged.connect(lambda: self.search_url(self.kuake))

        self.keyword = ''
        self.page_all_num = 10
        self.search_url_dic = {'baidu': r'https://www.baidu.com/s',
                               'biying': r'https://cn.bing.com/search?q={}&first={}',
                               'kuake': r'https://www.qwant.com/?q={}&count={}'}

        self.url = self.search_url_dic['baidu']
        self.item_div = r'//div[@class="result c-container xpath-log new-pmd"]'

        self.lineEdit.textChanged.connect(self.setkeyword)
        self.spinBox.valueChanged.connect(self.setpage_all_num)
        self.pushButton.clicked.connect(self.search)

        self.headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Mobile Safari/537.36 Edg/109.0.1518.55',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                        }

        rule =lambda x :x//10+1 if x % 10!=0 else x//10
        self.page_num = rule(self.page_all_num)
        self.params = {'wd': self.keyword, 'pn': str(
            self.page_all_num), 'tn': 'baiduhome', 'ie': 'utf-8'}

        self.linklist = []

    def setkeyword(self, keyword):
        self.keyword = keyword

    def setpage_all_num(self, page_all_num):
        self.page_all_num = page_all_num
        print(self.page_all_num)

    def search_url(self, e):
        print(e)
        if e.text() == '百度':
            self.url = self.search_url_dic['baidu']
        elif e.text() == '必应':
            self.url = self.search_url_dic['biying']
        else:
            self.url = self.search_url_dic['kuake']

    def search(self):
        for page in range(self.page_num):
            print(page)
            self.params['wd'] = self.keyword
            self.params['pn'] = str(page*10)

            r = requests.get(
                url=self.url, headers=self.headers, params=self.params)
            with open(file='test.html', mode='wb') as f:
                f.write(r.content)
            t = etree.HTML(r.text)

            selector = t.xpath(self.item_div)
            print(selector)
            for item in selector:
                print(item.xpath('.//h3/a')[0].text)
                link = item.xpath('.//h3/a')[0].get('href')
                self.linklist.append(link)

        for link in self.linklist:
            webbrowser.open(url=link)
            sleep(0.3)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = main()
    window.show()
    sys.exit(app.exec_())
