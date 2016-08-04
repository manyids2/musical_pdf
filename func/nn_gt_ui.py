import sys
import numpy as np
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from scipy.misc import *
from time import sleep
from time import time
import datetime
from os.path import join
import pickle

def getNames():
   path = '/home/mukunar1/workspace/wonderingEar/music_learn/musical_pdf/data/pdfs/'
   books = dict()
   f = open('../data/temp/all_pages.txt','r')
   for line in f:
      l_ = line.split('/')
      if not l_[-2] in books: books[l_[-2]] = []
      books[l_[-2]].append(l_[-1][:-1])
   f.close()
   return path,books

def to_rgb1(im):
    w, h = im.shape
    ret = np.empty((w, h, 3), dtype=np.uint8)
    ret[:, :, 0] = im
    ret[:, :, 1] = im
    ret[:, :, 2] = im
    return ret

class MainWindow(QWidget):

   s    = 25
   l    = 50
   h    = 1000
   N    = (h-l)/s
   b_now= 0
   p_now= 30
   now  = 30

   [path,books] = getNames()
   b_all        = books.keys()
   n_books      = len(b_all)
   n_pages      = len(books[b_all[b_now]])

   # page = getPage()
   def getPageGT(self):
      b_ = self.b_all[self.b_now]
      p_ = self.books[b_][self.p_now]
      b1 = self.gt[b_]
      print b1[p_]

   def readImg(self):
      b_         = self.b_all[self.b_now]
      p_         = self.books[b_][self.p_now]
      path_      = join(self.path,b_,p_)
      image      = imread(path_,True)
      image      = imresize(image,(1000,500))
      self.image = image

   def getGT(self,mode):
      if mode=='new':
         path = '/home/mukunar1/workspace/wonderingEar/music_learn/musical_pdf/data/pdfs/'
         gt   = dict()
         for b_ in self.b_all:
            gt[b_] = dict()
            n_     = len(self.books[b_])
            for i in range(n_): gt[b_][self.books[b_][i]] = np.zeros(self.N)
         st = datetime.datetime.fromtimestamp(time()).strftime('%Y-%m-%d %H:%M:%S')
         st = st + '_gt.p'
         pickle.dump( gt, open( "save.p", "wb" ) )
      if mode=='load':
         gt = pickle.load( open( "save.p", "rb" ) )
      return gt


   def getImg(self):
      image      = np.copy(self.image)
      col_ind    = np.zeros((image.shape[0],100))
      [x1,x2]    = self.getRows()
      col_ind[x1:x2,:] = 255
      image  [x1:x2,:] = 255 - image[x1:x2,:]
      image      = np.hstack((image,col_ind))
      image      = to_rgb1(image)
      image      = QImage(image, image.shape[1], image.shape[0], image.shape[1] * 3,QImage.Format_RGB888)
      return QPixmap(image)

   def getPatch(self):
      [x1,x2]  = self.getRows()
      image    = np.copy(self.image[x1:x2,:])
      image    = imresize(image,(200,1000))
      image    = to_rgb1(image)
      image    = QImage(image, image.shape[1], image.shape[0], image.shape[1] * 3,QImage.Format_RGB888)
      return QPixmap(image)

   def buttonClicked(self):
      sender = self.sender()
      self.getPageGT()
      if sender.text()=='Previous':
         self.now = self.now-1
      if sender.text()=='Next':
         self.now = self.now+1

      if sender.text()=='Yes':
         # write yes to file
         b_ = self.b_all[self.b_now]
         p_ = self.books[b_][self.p_now]
         b1 = self.gt[b_]
         b1[p_][self.now] = 3
         print self.now, p_
         print b1[p_]
         self.now = self.now+1

      if sender.text()=='No':
         # write no to file
         b_ = self.b_all[self.b_now]
         p_ = self.books[b_][self.p_now]
         b1 = self.gt[b_]
         b1[p_][self.now] = 1
         print self.now, p_
         print b1[p_]
         self.now = self.now+1

      if sender.text()=='Maybe':
         # write maybe to file
         b_ = self.b_all[self.b_now]
         p_ = self.books[b_][self.p_now]
         b1 = self.gt[b_]
         b1[p_][self.now] = 2
         print self.now, p_
         print b1[p_]
         self.now = self.now+1

      if self.now==self.N:
         # turn page
         pickle.dump( self.gt, open( "save.p", "wb" ) )
         self.now = 0
         self.p_now = min(self.p_now+1,self.n_pages-1)
         self.readImg()
      if self.now==-1:
         # turn back page
         pickle.dump( self.gt, open( "save.p", "wb" ) )
         self.now = 0
         self.p_now = max(self.p_now-1,0)
         self.readImg()

      b_ = self.b_all[self.b_now]
      p_ = self.books[b_][self.p_now]
      self.edt_indx.setText(str(self.now))
      self.edt_page.setText(p_)
      self.img_page.setPixmap(self.getImg()  )
      self.img_ptch.setPixmap(self.getPatch())

   def getRows(self):
      return [self.now*self.s,self.now*self.s+self.l]

   def __init__(self, parent = None):
      super(MainWindow, self).__init__(parent)
      self.initUI()

   def initUI(self):

      self.gt  = self.getGT('load')
      lo       = QHBoxLayout()
      box_img  = QHBoxLayout()
      self.img_page = QLabel()
      self.readImg()
      self.img_page.setPixmap(self.getImg())
      box_img.addWidget(self.img_page)
      box_ctrl = QVBoxLayout()
      box_book = QHBoxLayout()
      lbl_book = QLabel("Book")
      cmb_book = QComboBox()
      box_book.addWidget(lbl_book)
      box_book.addWidget(cmb_book)
      box_ctrl.addLayout(box_book)
      box_page = QHBoxLayout()
      lbl_page = QLabel("Page")
      self.edt_page = QLineEdit()
      box_page.addWidget(lbl_page)
      box_page.addWidget(self.edt_page)
      box_ctrl.addLayout(box_page)
      box_indx = QHBoxLayout()
      lbl_indx = QLabel("Index")
      self.edt_indx = QLineEdit()
      box_indx.addWidget(lbl_indx)
      box_indx.addWidget(self.edt_indx)
      box_ctrl.addLayout(box_indx)
      box_navg = QHBoxLayout()
      btn_prev = QPushButton()
      btn_next = QPushButton()
      btn_prev.setText("Previous")
      btn_next.setText("Next"    )
      btn_prev.clicked.connect(self.buttonClicked)
      btn_next.clicked.connect(self.buttonClicked)
      box_navg.addWidget(btn_prev)
      box_navg.addWidget(btn_next)
      box_ctrl.addLayout(box_navg)
      box_ptch = QHBoxLayout()
      self.img_ptch = QLabel()
      self.img_ptch.setPixmap(self.getPatch())
      box_ptch.addWidget(self.img_ptch)
      box_ctrl.addLayout(box_ptch)
      box_lbl  = QHBoxLayout()
      btn_y    = QPushButton()
      btn_n    = QPushButton()
      btn_m    = QPushButton()
      btn_y.setText("Yes"  )
      btn_n.setText("No"   )
      btn_m.setText("Maybe")
      btn_y.clicked.connect(self.buttonClicked)
      btn_n.clicked.connect(self.buttonClicked)
      btn_m.clicked.connect(self.buttonClicked)
      box_lbl.addWidget(btn_y)
      box_lbl.addWidget(btn_m)
      box_lbl.addWidget(btn_n)
      box_ctrl.addLayout(box_lbl)
      lo.addLayout(box_img)
      lo.addLayout(box_ctrl)
      self.setLayout(lo)
      self.setGeometry(0,0,1100,1200)
      self.setWindowTitle("GT Tool")


def main():
   app = QApplication(sys.argv)
   ex  = MainWindow()
   ex.show()
   sys.exit(app.exec_())

if __name__ == '__main__':
   main()