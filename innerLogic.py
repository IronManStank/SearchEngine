from innerui import Ui_Dialog
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import *
import sys

# import glo

# glo.__init__()


class Info:

    site_info = {
        "tb": r"https://www.taobao.com/",
        "jd": r"https://www.jd.com/?cu=true",
        "zhihu": r"https://www.zhihu.com/",
        "gitee": r"https://gitee.com/",
        "github": r"https://github.com/",
        "csdn": r"https://www.csdn.net/",
    }


class dialog(QDialog, Ui_Dialog, Info):
    def __init__(self):

        super(dialog, self).__init__()

        self.initUI()

    def initUI(self):

        self.setupUi(self)

        self.setWindowTitle("Advanced Options")

        self.init_params()

        self.checkBox_kw.setChecked(False)
        self.checkBox_filetype.setChecked(False)
        self.checkBox_site.setTristate(1)

        self.checkBox_site.setCheckState(Qt.PartiallyChecked)

        self.sub_box = [
            self.checkBox_tb,
            self.checkBox_jd,
            self.checkBox_gitee,
            self.checkBox_zhihu,
            self.checkBox_github,
            self.checkBox_cdsn,
        ]

        site_info = Info().site_info
        # 定义触发

        self.checkBox_filetype.stateChanged.connect(
            lambda: self.filetype(self.checkBox_filetype)
        )

        self.checkBox_kw.stateChanged.connect(self.set_allkw)

        self.checkBox_site.stateChanged.connect(self.choose_site)

        self.checkBox_closead.stateChanged.connect(self.close_add)

        for x in self.sub_box:
            x.stateChanged.connect(self.set_site)

        self.buttonBox.accepted.connect(self.confirm)
        self.buttonBox.rejected.connect(self.cancled)

    # 重置所有subbox

    def set_sub_false(self):
        for item in self.sub_box:
            item.setChecked(False)
            item.setCheckable(False)

    def set_sub_true(self):

        for item in self.sub_box:
            item.setChecked(False)
            item.setCheckable(True)

    # 定义全局逻辑关系

    def judger(self):

        if self.checkBox_site.checkState() != 2:

            self.set_sub_false()
        else:
            self.set_sub_true()

        # print(self.checkBox_site.checkState())

    # 注意高级功能的逻辑关系；首先添加关键字，最后加上引号
    def set_site(self):
        temp_str = " site: "
        if self.checkBox_tb.isChecked():
            self.site = temp_str + self.site_info["tb"]
        elif self.checkBox_jd.isChecked():
            self.site = temp_str + self.site_info["jd"]
        elif self.checkBox_zhihu.isChecked():
            self.site = temp_str + self.site_info["zhihu"]
        elif self.checkBox_gitee.isChecked():
            self.site = temp_str + self.site_info["gitee"]
        elif self.checkBox_github.isChecked():
            self.site = temp_str + self.site_info["github"]
        elif self.checkBox_cdsn.isChecked():
            self.site = temp_str + self.site_info["csdn"]
        else:
            self.site = None

    def choose_site(self):

        self.judger()
        self.set_site()

    def filetype(self, e):
        self.rule()

        if self.checkBox_filetype.isChecked():
            self.file_type = " filetype:pdf"
        else:
            self.file_type = None

    def rule(self):

        if self.checkBox_filetype.isChecked():

            self.checkBox_kw.setChecked(False)
            # self.checkBox_kw.setCheckable(False)
        elif self.checkBox_kw.isChecked():
            self.checkBox_filetype.setChecked(False)
            # self.checkBox_filetype.setCheckable(False)

    def set_allkw(self):
        self.set_sub_false()

        if self.checkBox_kw.isChecked():

            self.checkBox_filetype.setChecked(False)
            # self.checkBox_filetype.setCheckable(False)
            self.checkBox_site.setCheckable(False)
            self.checkBox_site.setTristate(1)

            self.all_kw = True
        else:

            self.checkBox_filetype.setCheckable(True)
            self.checkBox_site.setCheckable(True)

            self.all_kw = False

    # 未点击时默认开，防止过度点击。该变量不可访问.
    def close_add(self):

        if self.checkBox_closead.isChecked():

            self.ad_close = True

        else:

            self.ad_close = False

    # 确定关闭窗口
    def generate_cofigure(self):
        config = {
            "ad_close": self.ad_close,
            "all_kw": self.all_kw,
            "site": self.site,
            "filetype": self.file_type,
        }
        # glo.set_value('config', config)
        return config

    def init_params(self):
        self.file_type = None
        self.site = None
        self.all_kw = False
        self.ad_close = False

    def confirm(self):

        return self.generate_cofigure()

    def cancled(self):
        self.init_params()
        return None
        # self.close()


if __name__ == "__main__":

    app = QApplication(sys.argv)
    ex = dialog()
    ex.show()
    sys.exit(app.exec_())
