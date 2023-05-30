# -*- coding: utf-8 -*-
"""

"""
from PyQt5 import uic
from PyQt5.QtWidgets import QDialog, QLineEdit, QTextEdit
import math
import skimage.exposure as exposure
import cv2
from matplotlib import pyplot as plt
import numpy as np
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QComboBox, QVBoxLayout, QTextEdit, QStackedWidget, QDialog, QMainWindow, QApplication, QPushButton, QLabel, QFileDialog, QLineEdit
from PyQt5 import uic
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QPixmap
import sys
import threading
import time
import random
from PyQt5.QtCore import Qt


ITEMS = 0
counter = 0
BUFFER_SIZE = 0
buffer = []
# threading lock is used to prevent other threads to access the same resources
buffer_lock = threading.Lock()
buffer_not_full = threading.Condition(buffer_lock)
buffer_not_empty = threading.Condition(buffer_lock)


class Producer(threading.Thread):
    def __init__(self, Messages, Messages_Buffer):
        super(Producer, self).__init__()
        self.Messages = Messages
        self.Messages_Buffer = Messages_Buffer
    global counter
    print(ITEMS)

    def run(self):
        text = self.Messages
        text_buffer = self.Messages_Buffer
        global buffer
        global ITEMS
        while (counter < ITEMS):

            item = random.randint(1, 10)
            buffer_lock.acquire()
            # acuire manage access to shared resources
            while len(buffer) == BUFFER_SIZE:
                text.append("Buffer is full, producer is waiting")
                text_buffer.append(
                    f"Buffer is full,Num of Items in Buffer Now {len(buffer)}")
                print("Buffer is full, producer is waiting")
                # .wait is used to block the excution of the threading until anothr thread finishes
                buffer_not_full.wait()
            buffer.append(item)
            text.append(f"Produced {item}")
            text_buffer.append(f"Num of Items in Buffer Now {len(buffer)}")
            QCoreApplication.processEvents()  # Process GUI events
            print(f"Produced {item}")
            buffer_not_empty.notify()
            # here release is used to release the lock
            buffer_lock.release()
            time.sleep(random.random())


class Consumer(threading.Thread):
    def __init__(self, Messages, Messages_Buffer):
        super(Consumer, self).__init__()
        self.Messages = Messages
        self.Messages_Buffer = Messages_Buffer

    def run(self):
        text = self.Messages
        text_buffer = self.Messages_Buffer
        global buffer
        global ITEMS
        global counter
        while (counter < ITEMS):

            buffer_lock.acquire()
            # acuire manage access to shared resources

            while len(buffer) == 0:
                text.append("Buffer is empty, consumer is waiting")
                text_buffer.append(
                    f"Buffer is empty, Num of Items in Buffer Now {len(buffer)}")
                print("Buffer is empty, consumer is waiting")
                buffer_not_empty.wait()
            item = buffer.pop(0)
            counter += 1
            text.append(f"Consumed {item}")
            text_buffer.append(f"Num of Items in Buffer Now {len(buffer)}")
            QCoreApplication.processEvents()  # Process GUI events
            print(f"Consumed {item}")
            buffer_not_full.notify()
            buffer_lock.release()
            time.sleep(random.random())


class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()

        uic.loadUi("screen1.ui", self)
        # self.button=self.findChild(QPushButton,"gotoscreen2")
        self.gotoscreen2.clicked.connect(self.clicker)
        self.gotoChapter2.clicked.connect(self.Chapter2clicker)
        # click the dropdown box
        # self.button.clicked.connect(self.clicker)

    def clicker(self):
        screen2 = Screen2()
        widget.addWidget(screen2)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def Chapter2clicker(self):
        screen3 = Screen3()
        widget.addWidget(screen3)
        widget.setCurrentIndex(widget.currentIndex()+2)


class Screen2(QDialog):
    def __init__(self):
        super(Screen2, self).__init__()

        uic.loadUi("screen2.ui", self)
        self.Buffer = self.findChild(QLineEdit, "Buffer")
        self.item = self.findChild(QLineEdit, "ITEMS")
        self.Messages = self.findChild(QTextEdit, "Messages")
        self.Messages_Buffer = self.findChild(QTextEdit, "Messages_Buffer")
        self.MainMenu.clicked.connect(self.gotoMainMenu)
        self.Start.clicked.connect(self.runprogram
                                   )

    def gotoMainMenu(self):
        mainwindow = MainWindow()
        widget.addWidget(mainwindow)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def runprogram(self):
        self.Messages.clear()
        self.Messages_Buffer.clear()
        global ITEMS
        global counter
        counter = 0
        global BUFFER_SIZE
        # using .text uou can dunamicaly change the content of the widget
        BUFFER_SIZE = int(self.Buffer.text())
        ITEMS = int(self.item.text())

        # Create producer and consumer threads
        producer_thread = Producer(self.Messages, self.Messages_Buffer)
        consumer_thread = Consumer(self.Messages, self.Messages_Buffer)

        # Start the threads
        producer_thread.start()
        consumer_thread.start()

        # Main thread waits for the threads to complete
        producer_thread.join()
        consumer_thread.join()


class Screen3(QDialog):
    def __init__(self):
        super(Screen3, self).__init__()
        uic.loadUi("screen3.ui", self)
        self.sequenceslist = []
        self.sequence_atr = self.findChild(QLineEdit, "sequence_")
        self.start = self.findChild(QLineEdit, "StartTime")
        self.CYLINDER = self.findChild(QLineEdit, "CylinderMax")
        self.seqlist = self.findChild(QTextEdit, "sequences")
        self.AddSequences.clicked.connect(self.addseqclicked)
        self.Headmovement = self.findChild(QLineEdit, "Headmovement")
        self.FCFS.clicked.connect(self.FCFS_graph)
        self.SCAN.clicked.connect(self.SCAN_graph)
        self.CSCAN.clicked.connect(self.CSCAN_graph)
        self.LOOK.clicked.connect(self.LOOK_graph)
        self.CLOOK.clicked.connect(self.CLOOK_graph)
        self.direction_combo = self.findChild(QComboBox, "Combo_direction")
        self.SSTF.clicked.connect(self.SSTF_graph)
        self.label_2 = self.findChild(QLabel, "label_2")

    def addseqclicked(self):
        self.sequenceslist.append(int(self.sequence_atr.text()))
        self.seqlist.append(f"{self.sequence_atr.text()}")


###########################
############


    def FCFS_graph(self):
        CYLINDER_MAX = int(self.CYLINDER.text())
        sequence = self.sequenceslist.copy()
        temp = sequence.copy()
        start = int(self.start.text())
        temp.insert(0, start)
        plt.rcParams['xtick.bottom'] = plt.rcParams['xtick.labelbottom'] = False
        plt.rcParams['xtick.top'] = plt.rcParams['xtick.labeltop'] = True
        size = len(temp)
        x = temp
        y = []
        headmovement = 0
        for i in range(0, size):
            y.append(-i)
            if i != size - 1:
                headmovement = headmovement + abs(temp[i] - temp[i + 1])
        string = 'Headmovement = ' + str(headmovement) + ' cylinders'
        string2 = str(temp)
        self.Headmovement.setText(str(headmovement))
        plt.plot(x, y, color="green", markerfacecolor='blue',
                 marker='o', markersize=5, linewidth=2, label="FCFS")
        plt.ylim = (0, size)
        plt.xlim = (0, CYLINDER_MAX)
        plt.yticks([])
        plt.title("First Come First Served Scheduling Algorithm")
        plt.text(172.5, -8.85, string, horizontalalignment='center',
                 verticalalignment='center', fontsize=12)
        plt.text(172.5, -9.5, string2, horizontalalignment='center',
                 verticalalignment='center', fontsize=12)
        plt.savefig('FCFS.png')
        self.pixmap_2 = QPixmap('FCFS.png')
        self.label_2.setPixmap(self.pixmap_2)
        plt.show()

    ###############################################################
    # ################################################
    #    ##############################
    #             3################

    def SSTF_graph(self):
        CYLINDER_MAX = int(self.CYLINDER.text())
        sequence = self.sequenceslist
        temp = sequence.copy()
        start = int(self.start.text())
       # next in sequence is the fuction used to get the next value

        def next_in_sequence(seq, val):
            diff = 0
            mindiff = math.inf
            nextval = 0
            for i in range(0, len(seq)):
                if seq[i] != val:
                    # abs is used to calculate the absloute differnce value
                    diff = abs(seq[i] - val)
                    if diff < mindiff:
                        mindiff = diff
                        nextval = seq[i]
            return nextval
    # temp is the sequence of the copy
        temp.insert(0, start)
        val = start
        x = []
        y = []
        size = 0
        x.append(start)
        headmovement = 0
        while len(temp):
            val = next_in_sequence(temp, val)
            x.append(val)
            temp.remove(val)
        size = len(x)
        for i in range(0, size):
            y.append(-i)
            if i != (size - 1):
                headmovement = headmovement + abs(x[i] - x[i + 1])
        string = 'Headmovement = ' + str(headmovement) + ' cylinders'
        string2 = str(x)
        self.Headmovement.setText(str(headmovement))

        plt.plot(x, y, color="green", markerfacecolor='blue',
                 marker='o', markersize=5, linewidth=2, label="SSTF")
        plt.ylim = (0, size)
        plt.xlim = (0, CYLINDER_MAX)
        plt.yticks([])
        plt.title("Shortest Seek Time First Scheduling Algorithm")
        plt.text(182.5, -10.85, string, horizontalalignment='center',
                 verticalalignment='center', fontsize=12)
        plt.text(182.5, -11.5, string2, horizontalalignment='center',
                 verticalalignment='center', fontsize=12)
        plt.savefig('SSTF.png')
        self.pixmap_2 = QPixmap('SSTF.png')
        self.label_2.setPixmap(self.pixmap_2)
        plt.show()

    # #SCAN
    def SCAN_graph(self):
        # ,text here is used to take the input from the widgets in the gui
        CYLINDER_MAX = int(self.CYLINDER.text())
        direction = self.direction_combo.currentText()
        print(direction)
        sequence = self.sequenceslist
        temp = sequence.copy()
        start = int(self.start.text())
        left = []
        right = []
        x = []
        y = []
        x_approx = []
        y_approx = []
        headmovement = 0
        headmovement_approx = 0
        x.append(start)
        if direction == "Left":
            for i in temp:
                if i < start:
                    left.append(i)
                else:
                    right.append(i)
                    # after adding all the sequnces in the list we must sort them to make the head move from the the first to the end
            # ;and use reverse true to make it sort descending from the largest to the lowest
            left.sort(reverse=True)
            for i in left:
                x.append(i)

            right.sort()
            for i in right:
                x.append(i)

            x_approx.append(start)
            x_approx.append(min(x))
            x_approx.append(max(x))
            headmovement_approx = abs(start - 0)
            headmovement_approx = headmovement_approx + abs(0 - max(x))
        elif direction == "Right":
            for i in temp:
                if i > start:
                    right.append(i)
                else:
                    left.append(i)
            right.sort()
            for i in right:
                x.append(i)

            x.append(CYLINDER_MAX)
            left.sort(reverse=True)
            for i in left:
                x.append(i)
            x_approx.append(start)
            x_approx.append(max(x))
            x_approx.append(min(x))
            headmovement_approx = abs(start - 199)
            headmovement_approx = headmovement_approx + abs(199 - min(x))

        y_approx.append(0)
        size = len(x)
        for i in range(0, size):
            y.append(-i)
            if x[i] == 0 or x[i] == 199:
                y_approx.append(-i)
            if i != (size - 1):
                headmovement = headmovement + abs(x[i] - x[i + 1])
            else:
                y_approx.append(-i)
        string = 'Headmovement = ' + str(headmovement) + ' cylinders'
        string2 = str(x)
        self.Headmovement.setText(str(headmovement))

        plt.plot(x, y, color="green", markerfacecolor='blue',
                 marker='o', markersize=5, linewidth=2, label="SCAN")
        plt.plot(x_approx, y_approx, dashes=[6, 2], color="red", markerfacecolor='red', marker='D', markersize=5,
                 linewidth=0.5, label="Approx SCAN")
        plt.ylim = (0, size)
        plt.xlim = (0, CYLINDER_MAX)
        plt.yticks([])
        plt.title("SCAN Scheduling Algorithm")
        plt.text(182.5, -10.85, string, horizontalalignment='center',
                 verticalalignment='center', fontsize=12)
        plt.text(182.5, -12.5, string2, horizontalalignment='center',
                 verticalalignment='center', fontsize=12)
        plt.savefig('SCAN.png')
        self.pixmap_2 = QPixmap('SCAN.png')
        self.label_2.setPixmap(self.pixmap_2)
        plt.show()
####################################################
    #######################################
        #########################
        #################

    def CSCAN_graph(self):
        CYLINDER_MAX = int(self.CYLINDER.text())
        direction = self.direction_combo.currentText()
        print(direction)
        sequence = self.sequenceslist
        start = int(self.start.text())
        temp = sequence.copy()
        left = []
        right = []
        x = []
        y = []
        x_approx = []
        y_approx = []
        headmovement = 0
        headmovement_approx = 0
        x.append(start)
        if direction == "Left":
            for i in temp:
                if i < start:
                    left.append(i)
                else:
                    right.append(i)
# alawys at the left list we must make the sort reverse
            left.sort(reverse=True)
            for i in left:
                x.append(i)
            x.append(0)
            x.append(CYLINDER_MAX)
            right.sort(reverse=True)
            for i in right:
                x.append(i)
            x_approx.append(start)
            x_approx.append(min(x))
            x_approx.append(max(x))
            x_approx.append(x[-1])
            headmovement_approx = abs(start - 0)
            headmovement_approx = headmovement_approx + abs(0 - max(x))
            headmovement_approx = headmovement_approx + abs(0 - x[-1])
        elif direction == "Right":
            for i in temp:
                if i > start:
                    right.append(i)
                else:
                    left.append(i)
            right.sort()
            for i in right:
                x.append(i)
            x.append(CYLINDER_MAX)
            x.append(0)
            left.sort()
            for i in left:
                x.append(i)
            x_approx.append(start)
            x_approx.append(CYLINDER_MAX)
            x_approx.append(0)
            x_approx.append(x[-1])
            # 3
            headmovement_approx = abs(start - 199)
            headmovement_approx = headmovement_approx + abs(199 - 0)
            headmovement_approx = headmovement_approx + abs(0 - x[-1])
            ##############################################################
        y_approx.append(0)
        size = len(x)
        for i in range(0, size):
            y.append(-i)
            if x[i] == 0 or x[i] == 199:
                y_approx.append(-i)
            if i != (size - 1):
                headmovement = headmovement + abs(x[i] - x[i + 1])
            else:
                y_approx.append(-i)
        string = 'Headmovement = ' + str(headmovement) + ' cylinders'
        string2 = str(x)
        self.Headmovement.setText(str(headmovement))

        plt.plot(x, y, color="green", markerfacecolor='blue',
                 marker='o', markersize=5, linewidth=2, label="CSCAN")
        plt.plot(x_approx, y_approx, dashes=[6, 2], color="red", markerfacecolor='red', marker='D', markersize=5,
                 linewidth=0.5, label="Approx CSCAN")
        plt.ylim = (0, size)
        plt.xlim = (0, CYLINDER_MAX)
        plt.yticks([])
        plt.title("CSCAN Scheduling Algorithm")
        plt.text(182.5, -10.85, string, horizontalalignment='center',
                 verticalalignment='center', fontsize=12)
        plt.text(182.5, -12.5, string2, horizontalalignment='center',
                 verticalalignment='center', fontsize=12)
        plt.savefig('CSCAN.png')
        self.pixmap_2 = QPixmap('CSCAN.png')
        self.label_2.setPixmap(self.pixmap_2)
        plt.show()
#############################################################################
#################################################
###############################

    def LOOK_graph(self):
        CYLINDER_MAX = int(self.CYLINDER.text())
        direction = self.direction_combo.currentText()
        print(direction)
        sequence = self.sequenceslist
        start = int(self.start.text())
        temp = sequence.copy()
        left = []
        right = []
        x = []
        y = []
        x_approx = []
        y_approx = []
        headmovement = 0
        headmovement_approx = 0
        x.append(start)
        if direction == "Left":
            for i in temp:
                if i < start:
                    left.append(i)
                else:
                    right.append(i)
            left.sort(reverse=True)
            # after sorting the sequences then we appent them all to the list from left to the right
            for i in left:
                x.append(i)
            right.sort()
            for i in right:
                x.append(i)
            x_approx.append(start)
            x_approx.append(min(x))
            x_approx.append(max(x))
            headmovement_approx = abs(start - min(x))
            headmovement_approx = headmovement_approx + abs(min(x) - max(x))
        elif direction == "Right":
            for i in temp:
                if i > start:
                    right.append(i)
                else:
                    left.append(i)
            right.sort()
            for i in right:
                x.append(i)
            left.sort(reverse=True)
            for i in left:
                x.append(i)
            x_approx.append(start)
            x_approx.append(max(x))
            x_approx.append(min(x))
            headmovement_approx = abs(start - max(x))
            headmovement_approx = headmovement_approx + abs(max(x) - min(x))

        y_approx.append(0)
        size = len(x)
        for i in range(0, size):
            y.append(-i)
            if (x[i] == max(x) or x[i] == min(x)) and (i != size):
                y_approx.append(-i)
            if i != (size - 1):
                headmovement = headmovement + abs(x[i] - x[i + 1])
        string = 'Headmovement = ' + str(headmovement) + ' cylinders'
        string2 = str(x)
        self.Headmovement.setText(str(headmovement))

        plt.plot(x, y, color="green", markerfacecolor='blue',
                 marker='o', markersize=5, linewidth=2, label="LOOK")
        plt.plot(x_approx, y_approx, dashes=[6, 2], color="red", markerfacecolor='red', marker='D', markersize=5,
                 linewidth=0.5, label="Approx LOOK")
        plt.ylim = (0, size)
        plt.xlim = (0, CYLINDER_MAX)
        plt.yticks([])
        plt.title("LOOK Scheduling Algorithm")
        plt.text(182.5, -10.85, string, horizontalalignment='center',
                 verticalalignment='center', fontsize=12)
        plt.text(182.5, -12.5, string2, horizontalalignment='center',
                 verticalalignment='center', fontsize=12)
        plt.savefig('LOOK.png')
        self.pixmap_2 = QPixmap('LOOK.png')
        self.label_2.setPixmap(self.pixmap_2)
        plt.show()
###################################
############################
##################
#######

    def CLOOK_graph(self):
        CYLINDER_MAX = int(self.CYLINDER.text())
        direction = self.direction_combo.currentText()
        print(direction)
        sequence = self.sequenceslist
        start = int(self.start.text())
        temp = sequence.copy()
        left = []
        right = []
        x = []
        y = []
        x_approx = []
        y_approx = []
        headmovement = 0
        headmovement_approx = 0
        x.append(start)
        if direction == "Left":
            for i in temp:
                if i < start:
                    left.append(i)
                else:
                    right.append(i)
            left.sort(reverse=True)
            for i in left:
                x.append(i)
            right.sort(reverse=True)
            for i in right:
                x.append(i)
            x_approx.append(start)
            x_approx.append(min(x))
            x_approx.append(max(x))
            x_approx.append(x[-1])
            headmovement_approx = abs(start - min(x))
            headmovement_approx = headmovement_approx + abs(min(x) - max(x))
            headmovement_approx = headmovement_approx + abs(max(x) - x[-1])
        elif direction == "Right":
            # for loop to check all the values inside the sequences
            for i in temp:
                if i > start:
                    right.append(i)
                else:
                    left.append(i)
            right.sort()
            for i in right:
                x.append(i)
            left.sort()
            for i in left:
                x.append(i)
            x_approx.append(start)
            x_approx.append(max(x))
            x_approx.append(min(x))
            x_approx.append(x[-1])
            headmovement_approx = abs(start - max(x))
            headmovement_approx = headmovement_approx + abs(max(x) - min(x))
            headmovement_approx = headmovement_approx + abs(min(x) - x[-1])

        y_approx.append(0)
        size = len(x)
        for i in range(0, size):
            y.append(-i)
            if (x[i] == min(x) or x[i] == max(x)) and (i != size):
                y_approx.append(-i)
            if i != (size - 1):
                headmovement = headmovement + abs(x[i] - x[i + 1])
            else:
                y_approx.append(-i)
        string = 'Headmovement = ' + str(headmovement) + ' cylinders'
        string2 = str(x)
        self.Headmovement.setText(str(headmovement))

        plt.plot(x, y, color="green", markerfacecolor='blue',
                 marker='o', markersize=5, linewidth=2, label="CLOOK")
        plt.plot(x_approx, y_approx, dashes=[6, 2], color="red", markerfacecolor='red', marker='D', markersize=5,
                 linewidth=0.5, label="Approx CLOOK")
        plt.ylim = (0, size)
        plt.xlim = (0, CYLINDER_MAX)
        plt.yticks([])
        plt.title("CLOOK Scheduling Algorithm")
        plt.text(182.5, -10.85, string, horizontalalignment='center',
                 verticalalignment='center', fontsize=12)
        plt.text(182.5, -12.5, string2, horizontalalignment='center',
                 verticalalignment='center', fontsize=12)
        plt.savefig('CLOOK.png')
        self.pixmap_2 = QPixmap('CLOOK.png')
        self.label_2.setPixmap(self.pixmap_2)
        plt.show()


app = QApplication(sys.argv)

widget = QStackedWidget()
mainwindow = MainWindow()
widget.addWidget(mainwindow)
screen2 = Screen2()
widget.addWidget(screen2)
screen_rect = QApplication.primaryScreen().availableGeometry()
widget.setFixedWidth(screen_rect.width())
widget.setFixedHeight(700)
widget.show()
try:
    sys.exit(app.exec_())
except Exception as e:
    print("EXITING:", str(e))
