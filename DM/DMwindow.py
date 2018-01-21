# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'self.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from collections import defaultdict as dd
import network
from threading import Thread
import DMConsole

class Entity:
    def __init__(self,idnum,x,y,sprite,properties):
        self.id = idnum
        self.x=x
        self.y=y
        self.sprite=QtGui.QPixMap(sprite).toImage()
        self.props = dd()
        for p in properties:
            prop = p.split(':')
            if prop[1]=='int':
                self.props[prop[0]]=int(prop[2])
            elif prop[1]=='float':
                self.props[prop[0]]=float(prop[2])
            else:
                self.props[prop[0]]=prop[1]

class MapCell:
    def __init__(self,x,y,backdrop):
        self.x=x
        self.y=y
        self.backdrop=QtGui.QPixMap(backdrop).toImage()

class DMWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(DMWindow, self).__init__()
        
        
        self.CANVASHEIGHT=525
        self.CANVASWIDTH=1085
        self.GRIDSIZE= 35

        self.name = 'PabloTODO'
        self.gridx=0
        self.gridy=0
        self.map = dd()
        self.entities= dd()
        self.players = dd()
        
        self.setObjectName("PlayerWindow")
        self.resize(1316, 701)
        self.centralWidget = QtWidgets.QWidget(self)
        self.centralWidget.setObjectName("centralWidget")
        self.listWidget = QtWidgets.QListWidget(self.centralWidget)
        self.listWidget.setGeometry(QtCore.QRect(1120, 0, 201, 330))
        self.listWidget.setObjectName("listWidget")
        self.frame = QtWidgets.QFrame(self.centralWidget)
        self.frame.setGeometry(QtCore.QRect(0, 560, 560, 151))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.frame_2 = QtWidgets.QFrame(self.centralWidget)
        self.frame_2.setGeometry(QtCore.QRect(560, 560, 560, 151))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.listView = QtWidgets.QListView(self.centralWidget)
        self.listView.setGeometry(QtCore.QRect(1120, 330, 201, 371))
        self.listView.setObjectName("listView")
        self.setCentralWidget(self.centralWidget)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

        self.port = 0
        try:
            self.port = network.initnet(self)
        except Exception as ex:
            print(ex)
        
        DMConsole.window = self
        t=Thread(target=DMConsole.run)
        t.start()
        self.show()
    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("DnD", "Dnd"))

    def mouseReleaseEvent(self, QMouseEvent):
        grid=(int(QMouseEvent.pos().x()/self.GRIDSIZE),int(QMouseEvent.pos().y()/self.GRIDSIZE))
        print(grid)

    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.draw(qp)
        qp.end()

    def recv(self,m,name):
        if m[0]=='load':
            try:
                pdata=open(name+'.sav').read()
                self.players[name]=dd()
                for d in pdata.split('\n'):
                    k,v = d.split(':')
                    if ',' in v:
                        self.players[name][k] = v.split(',')
                    else:
                        try:
                            self.players[name][k] = int(v)
                        except:
                            try:
                                self.players[name][k] = float(v)
                            except:
                                self.players[name][k] = v
                    if k!='x' and k!='y':
                        network.send('Player\n'+k+'\n'+v,name)
                network.send('Player\nPosition\n'+players[name]['x']+'\n'+players[name]['y'],name)
            except:
                print('Please create a character file for: '+name)
            
    def draw(self,qp):
        for m in self.map:
            qp.drawImage(QtCore.QRect((m.x-self.gridx)*self.GRIDSIZE,(m.y-self.gridy)*self.GRIDSIZE,self.GRIDSIZE,self.GRIDSIZE),m.backdrop)
        for m in self.entities:
            qp.drawImage(QtCore.QRect((m.x-self.gridx)*self.GRIDSIZE,(m.y-self.gridy)*self.GRIDSIZE,self.GRIDSIZE,self.GRIDSIZE),m.sprite)
        for i in range(int(self.CANVASHEIGHT/self.GRIDSIZE)):
            qp.drawLine(0,i*self.GRIDSIZE,self.CANVASWIDTH,i*self.GRIDSIZE)
        for i in range(int(self.CANVASWIDTH/self.GRIDSIZE)):
            qp.drawLine(i*self.GRIDSIZE,0,i*self.GRIDSIZE,self.CANVASHEIGHT)
            

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    d=DMWindow()
    sys.exit(app.exec_())
