from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PIL.Image import*
from PIL.ImageDraw import*
from os import listdir
import gui

class Main(QDialog, gui.Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.images = "images"
        self.results = "results"
        self.root = "SHIFRATOR" 
        for i in os.listdir(f"{self.root}\{self.images}"):
            self.comboBox.addItem(i)
        self.comboBox.activated[str].connect(self.draw)
        self.pushButton.clicked.connect(self.encrypt)
        self.pushButton_1.clicked.connect(self.decrypt)
        
    def draw(self):
        self.file = f"{self.root}\{self.images}\{self.comboBox.currentText()}"
        if self.comboBox.currentText() in os.listdir(f"{self.root}\{self.images}"):
            pixmap = QPixmap(self.file)
            self.label_2.setPixmap(pixmap)
        else:
            self.label_2.setText("NO SUCH FILE")

    def binmessage(self,data):
        binmes = []
        for i in data:
            binmes.append(format(ord(i.encode('cp1251')), '08b'))
        return binmes
    
    def NewPix(self,pix,data):
        datalist = self.binmessage(data)
        lendata = len(datalist)
        imdata = iter(pix)
        for i in range(lendata):
            pix = [value for value in imdata.__next__()[:3] +
                                      imdata.__next__()[:3] +
                                      imdata.__next__()[:3]]
            for j in range(0, 8):
                if (datalist[i][j]=='0') and (pix[j]% 2 != 0):
                    if (pix[j]% 2 != 0):
                        pix[j] -= 1
                elif (datalist[i][j] == '1') and (pix[j] % 2 == 0):
                    pix[j] -= 1
            if (i == lendata - 1):
                if (pix[-1] % 2 == 0):
                    pix[-1] -= 1
            else:
                if (pix[-1] % 2 != 0):
                    pix[-1] -= 1
            pix = tuple(pix)
            yield pix[0:3]
            yield pix[3:6]
            yield pix[6:9]

    def encode(self,data):
        image = Image.open(self.file, 'r')
        self.newname = f"#{self.comboBox.currentText()}"
        newimg = image.copy()
        w = newimg.size[0]
        (x, y) = (0, 0)
        for pixel in self.NewPix(newimg.getdata(),data):
            newimg.putpixel((x, y), pixel)
            if (x == w - 1):
                x = 0
                y += 1
            else:
                x += 1
        newimg.save(f"{self.root}\{self.results}\{self.newname}")
        
    def encrypt(self):
        data = self.lineEdit.text()
        if self.comboBox.currentText() in os.listdir(f"{self.root}\{self.images}"):
            if self.lineEdit.text() == "":
                self.label_2.setText("PLEASE ENTER A MESSAGE")
            else:
                self.draw()
                self.encode(data)
        else:
            self.label_2.setText("NO SUCH FILE")
    
    def decode(self):
        image = Image.open(self.file, 'r')
        imgdata = iter(image.getdata())
        data = ''
        while (True):
            pixels = [value for value in imgdata.__next__()[:3] + 
                                         imgdata.__next__()[:3] +
                                         imgdata.__next__()[:3]]
            binstr = ''
            for i in pixels[:8]:
                if (i % 2 == 0):
                    binstr += '0'
                else:
                    binstr += '1'
            data += chr(int(binstr, 2))
            if (pixels[-1] % 2 != 0):
                data = str(data)
                data = data.encode('cp1252').decode('cp1251')
                return self.lineEdit.setText(f'{data}')
    
    def decrypt(self):
        if self.comboBox.currentText() in os.listdir(f"{self.root}\{self.images}"):
                self.draw()
                self.decode()
        else:
            self.label_2.setText("NO SUCH FILE")
            
if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = Main()
    form.show()
    app.exec()
