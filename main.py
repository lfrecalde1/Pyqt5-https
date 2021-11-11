#!/home/fer/.virtualenvs/cv/bin/python
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import requests
import numpy as np


class Another(QWidget):
    def __init__(self):
        super().__init__()

        self.w_width = 500
        self.w_height = 350
        self.setGeometry(100, 100, self.w_width, self.w_height)
        self.setWindowTitle("Secundary Window")

        # label heigh
        self.height_name = QLabel(self)
        self.mass_name = QLabel(self)
        self.hair_name = QLabel(self)
        self.skin_name = QLabel(self)
        self.eye_name = QLabel(self)
        self.birth_name = QLabel(self)
        self.gender_name = QLabel(self)

        self.name_obj = [self.height_name, self.mass_name, self.hair_name, self.skin_name, self.eye_name, self.birth_name, self.gender_name]
        self.names = ["Height", "Mass", "hair_color", "Skin_color", "Eye_color", "Birth_year", "Gender"]

        self.height_data = QLabel(self)
        self.mass_data = QLabel(self)
        self.hair_data = QLabel(self)
        self.skin_data = QLabel(self)
        self.eye_data = QLabel(self)
        self.birth_data = QLabel(self)
        self.gender_data = QLabel(self)

        self.data_obj = [self.height_data, self.mass_data, self.hair_data, self.skin_data, self.eye_data, self.birth_data, self.gender_data]

    def show_name(self, data, pos_x, obj):
        aux = 10
        for k in range(0, len(data)):
            obj[k].move(pos_x, aux)
            obj[k].setText(data[k])
            aux = aux + 40
        return None

    def show_data(self, name, pos_x, obj, dic):
        aux = 10
        for k in range(0, len(name)):
            obj[k].move(pos_x, aux)
            aux_lower = name[k]
            aux_lower = aux_lower.lower()
            data = dic[aux_lower]
            obj[k].setText(data)
            aux = aux + 40
        return None


class Myapp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.base = []
        self.w = None
        self.initUI()


    def button_clicked(self):

        self.listWidget.clear()
        # Definition of random vector
        random_number = np.random.uniform(low=1, high=83, size=(1, 10))

        # definition of https
        path = "https://swapi.dev/api/people/"

        self.base = []

        for k in range(0, random_number.shape[1]):
            # Path random to find
            aux = path+str(int(random_number[0, k]))

            # Request to http
            req = requests.get(aux)

            # convert Info to Jason Dictionary
            data = req.json()

            item = QListWidgetItem(data['name'])
            self.listWidget.addItem(item)

            # Data Base
            self.base.append(data)

    def initUI(self):
        # Title windows
        self.setGeometry(200, 200, 500, 500)
        self.setWindowTitle("Postulante para ROBOTILSA S.A")

        # label Name
        self.label = QLabel(self)
        self.label.setText("Luis F. Recalde")
        self.label.move(280,50)

        # Label time
        self.time = QLabel(self)
        self.time.move(280,100)

        # Label date
        self.date = QLabel(self)
        self.date.move(280,170)

        # Bottom
        self.b1 = QPushButton(self)
        self.b1.move(270, 250)
        self.b1.setText("REQUEST")
        self.b1.setIcon((QIcon("bottom.jpg")))
        self.b1.clicked.connect(self.button_clicked)

        # Creation list
        self.listWidget = QListWidget(self)
        self.listWidget.setGeometry(50, 70, 150, 300)
        self.listWidget.installEventFilter(self)
        #self.listWidget.itemDoubleClicked.connect(self.get_item)

        timer = QTimer(self)
        timer.timeout.connect(self.time_system)
        timer.start(1000)

        self.time_system()

    def get_item(self):
        aux = self.listWidget.currentRow()
        if aux >= 0:
            data = self.base[aux]
            self.w = Another()
            self.w.show_name(self.w.names, 40, self.w.name_obj)
            self.w.show_data(self.w.names, 200, self.w.data_obj, data)
            self.w.show()


    def eventFilter(self, source, event):
        if event.type() == QEvent.ContextMenu and source is self.listWidget:
            menu = QMenu()
            menu.addAction("Inf Personaje")
            if menu.exec_(event.globalPos()):
                item = source.itemAt(event.pos())
                self.get_item()
            return True
        return super().eventFilter(source, event)


    def time_system(self):
        # Create time object
        time = QTime.currentTime()
        text_t = time.toString('hh:mm:ss')
        self.time.setText(text_t) 

        date = QDate.currentDate()
        text_d = date.toString('dd/MM/yyyy')
        self.date.setText(text_d)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myapp = Myapp()
    myapp.show()
    try:
        app.exec_()
    except SystemExit:
        print("Closing Window")

