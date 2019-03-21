



class Level(QWidget):
    def __init__(self):
        super().__init__()
        self.setMouseTracking(True)
        self.initUI()

    def initUI(self):
        self.l1.clicked.connect(self.sl1)
        self.l2.clicked.connect(self.sl2)
        self.l3.clicked.connect(self.sl3)
        self.l4.clicked.connect(self.sl4)
        
    


 

class Menu(QWidget):
    def __init__(self):
        super().__init__()
        uic.loadUi('menu.ui', self)
        self.initUI()

    def initUI(self):
        self.b1.clicked.connect(self.start)
        self.b2.clicked.connect(self.vibor)
        self.b3.clicked.connect(self.exite)
        
    def vibor(self):

    def exite(self):
        sys.exit(self.exec())
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close()
