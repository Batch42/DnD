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
        self.backdrop=QtGui.QPixmap(backdrop).toImage()

class PlayerWindow(QtWidgets.QMainWindow):
    def __init__(self,name,port):
        super(PlayerWindow, self).__init__()

        self.CANVASHEIGHT=525
        self.CANVASWIDTH=1085
        self.GRIDSIZE= 35

        self.name = name
        self.gridx=0
        self.gridy=0
        self.map = dd()
        self.entities= dd()
        self.player= dd()
        
        
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

        try:
            network.initnet(port,self)
        except Exception as ex:
            print(ex)
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

    def recv(self,m):
        if m[0]=='MapCell':
            print(m)
            self.map[m[1]+" "+m[2]] = MapCell(int(m[1]),int(m[2]),m[3])
        elif m[0]=='Entity':
            self.entities[m[1]] = Entity(int(m[1]),int(m[2]),int(m[3]),m[4],m[5:])
        elif m[0]=='Player':
            if m[1] == 'Position':
                m['x']=int(m[2])
                m['y']=int(m[3])
                self.gridx=m['x']-self.CANVASWIDTH/self.GRIDSIZE/2
                self.gridy=m['y']-self.CANVASHEIGHT/self.GRIDSIZE/2
                print('pos set')
            elif m[1] == 'Avatar':
                self.player[m[1]] = QtGui.QPixmap(m[2]).toImage()
            else:
                try:
                    self.player[m[1]] = int(m[2])
                except:
                    try:
                        self.player[m[1]] = float(m[2])
                    except:
                        self.player[m[1]] = m[2]
            updatePlayerInfo()
            
    def updatePlayerInfo(self):
        self.listWidget.clear()
        for k in self.player:
            if k not in ['x','y','Avatar']:
                self.listWidget.addItem(k+': '+str(self.player[k]))
        
    def draw(self,qp):
        print('draw')
        for r in self.map:
            m=self.map[r]
            print(m)
            if m.x-self.gridx>=0 and m.y-self.gridy>=0 and m.x-self.gridx < self.CANVASWIDTH/self.GRIDSIZE and m.y-self.gridx < self.CANVASHEIGHT/self.GRIDSIZE:
                qp.drawImage(QtCore.QRect((m.x-self.gridx)*self.GRIDSIZE,(m.y-self.gridy)*self.GRIDSIZE,self.GRIDSIZE,self.GRIDSIZE),m.backdrop)
        for r in self.entities:
            m=self.entities[r]
            if m.x-self.gridx>=0 and m.y-self.gridy>=0 and m.x-self.gridx < self.CANVASWIDTH/self.GRIDSIZE and m.y-self.gridx < self.CANVASHEIGHT/self.GRIDSIZE:
                qp.drawImage(QtCore.QRect((m.x-self.gridx)*self.GRIDSIZE,(m.y-self.gridy)*self.GRIDSIZE,self.GRIDSIZE,self.GRIDSIZE),m.sprite)
        print('avatar at '+str(self.player['x']-self.gridx)+' '+str(self.player['y']-self.gridy))
        qp.drawImage(QtCore.QRect((self.player['x']-self.gridx)*self.GRIDSIZE,(self.player['y']-self.gridy)*self.GRIDSIZE,self.GRIDSIZE,self.GRIDSIZE),self.player['Avatar'])
        for i in range(int(self.CANVASHEIGHT/self.GRIDSIZE)):
            qp.drawLine(0,i*self.GRIDSIZE,self.CANVASWIDTH,i*self.GRIDSIZE)
        for i in range(int(self.CANVASWIDTH/self.GRIDSIZE)):
            qp.drawLine(i*self.GRIDSIZE,0,i*self.GRIDSIZE,self.CANVASHEIGHT)
        


