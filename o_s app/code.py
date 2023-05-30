# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import skimage.exposure as exposure
from matplotlib.patches import Rectangle
import cv2
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib import pyplot as plt
import numpy as np
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QComboBox,QVBoxLayout,QTextEdit,QStackedWidget,QDialog,QMainWindow ,QApplication ,QPushButton ,QLabel ,QFileDialog ,QLineEdit
from PyQt5 import uic 
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QPixmap,QImage
import sys
import threading
import time
import random
from PyQt5.QtCore import Qt
import json
import copy
from sys import *
from math import gcd
from collections import OrderedDict
import matplotlib.pyplot as plt
import numpy as np
import statistics as st
from collections import defaultdict

tasks = dict()
RealTime_task = dict()
metrics = defaultdict(dict)
d = dict()
dList = []
T = []
n=0
C = []
I=0
U = []
# For gantt chart
y_axis  = []
from_x = []
to_x = []

ITEMS=0
counter=0
BUFFER_SIZE=0
buffer = []
buffer_lock = threading.Lock()
buffer_not_full = threading.Condition(buffer_lock)
buffer_not_empty = threading.Condition(buffer_lock)


class Producer(threading.Thread):
    def __init__(self, Messages,Messages_Buffer):
        super(Producer, self).__init__()
        self.Messages = Messages
        self.Messages_Buffer=Messages_Buffer
    global counter
    print(ITEMS)
    def run(self):
        text=self.Messages
        text_buffer=self.Messages_Buffer
        global buffer
        global ITEMS
        while (counter<ITEMS):
            
            item = random.randint(1, 10)
            buffer_lock.acquire()
            while len(buffer) == BUFFER_SIZE:
                text.append("Buffer is full, producer is waiting")
                text_buffer.append(f"Buffer is full,Num of Items in Buffer Now {len(buffer)}")
                print("Buffer is full, producer is waiting")
                buffer_not_full.wait()
            buffer.append(item)
            text.append(f"Produced {item}")
            text_buffer.append(f"Num of Items in Buffer Now {len(buffer)}")
            QCoreApplication.processEvents()  # Process GUI events
            print(f"Produced {item}")
            buffer_not_empty.notify()
            buffer_lock.release()
            time.sleep(random.random())
            
           
class Consumer(threading.Thread):
    def __init__(self, Messages,Messages_Buffer):
        super(Consumer, self).__init__()
        self.Messages = Messages
        self.Messages_Buffer=Messages_Buffer
    def run(self):
        text=self.Messages
        text_buffer=self.Messages_Buffer
        global buffer
        global ITEMS
        global counter
        while (counter<ITEMS):
            
            buffer_lock.acquire()
            while len(buffer) == 0:
                text.append("Buffer is empty, consumer is waiting")
                text_buffer.append(f"Buffer is empty, Num of Items in Buffer Now {len(buffer)}")
                print("Buffer is empty, consumer is waiting")
                buffer_not_empty.wait()
            item = buffer.pop(0)
            counter+=1
            text.append(f"Consumed {item}")
            text_buffer.append(f"Num of Items in Buffer Now {len(buffer)}")
            QCoreApplication.processEvents()  # Process GUI events
            print(f"Consumed {item}")
            buffer_not_full.notify()
            buffer_lock.release()
            time.sleep(random.random())



class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow,self).__init__()
        
        uic.loadUi("screen1.ui",self)
        #self.button=self.findChild(QPushButton,"gotoscreen2")
        self.gotoscreen2.clicked.connect(self.clicker)
        self.gotoChapter2.clicked.connect(self.Chapter2clicker)
        self.gotoChapter4.clicked.connect(self.Chapter4clicker)
        self.RoundRobin.clicked.connect(self.RoundRobinclicker)
        self.RMA.clicked.connect(self.RMAclicker)
        self.DMA.clicked.connect(self.DMAclicker)
        self.Minimum_Laxity_First.clicked.connect(self.Minimum_Laxity_Firstclicker)
        self.EDF.clicked.connect(self.EDFclicker)
        self.Test.clicked.connect(self.Testclicker)
        self.FIFO.clicked.connect(self.FIFOclicker)
        #click the dropdown box
        #self.button.clicked.connect(self.clicker)

        
    def clicker(self):
        screen2=Screen2()
        widget.addWidget(screen2)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
    def Chapter2clicker(self):
        screen3=Screen3()
        widget.addWidget(screen3)
        widget.setCurrentIndex(widget.currentIndex()+2)
    def Chapter4clicker(self):
        screen4=Screen4()
        widget.addWidget(screen4)
        widget.setCurrentIndex(widget.currentIndex()+3)
    def RoundRobinclicker(self):
        screen5=Screen5()
        widget.addWidget(screen5)
        widget.setCurrentIndex(widget.currentIndex()+4)
    def RMAclicker(self):
        screen6=Screen6()
        widget.addWidget(screen6)
        widget.setCurrentIndex(widget.currentIndex()+5)
    def DMAclicker(self):
        screen7=Screen7()
        widget.addWidget(screen7)
        widget.setCurrentIndex(widget.currentIndex()+6)
    def Minimum_Laxity_Firstclicker(self):
        screen8=Screen8()
        widget.addWidget(screen8)
        widget.setCurrentIndex(widget.currentIndex()+7)
    def EDFclicker(self):
        screen9=Screen9()
        widget.addWidget(screen9)
        widget.setCurrentIndex(widget.currentIndex()+8)
    def Testclicker(self):
        screen10=Screen10()
        widget.addWidget(screen10)
        widget.setCurrentIndex(widget.currentIndex()+9)
        
    def FIFOclicker(self):
        screen11=Screen11()
        widget.addWidget(screen11)
        widget.setCurrentIndex(widget.currentIndex()+9)
        
      
class Screen2(QDialog):
    def __init__(self):
        super(Screen2, self).__init__()
        
        uic.loadUi("screen2.ui", self)
        self.Buffer=self.findChild(QLineEdit,"Buffer")
        self.item=self.findChild(QLineEdit,"ITEMS")
        self.Messages=self.findChild(QTextEdit,"Messages")
        self.Messages_Buffer=self.findChild(QTextEdit,"Messages_Buffer")
        self.MainMenu.clicked.connect(self.gotoMainMenu)
        self.Start.clicked.connect(self.runprogram
                                   )
    
    def gotoMainMenu(self):
        mainwindow=MainWindow()
        widget.addWidget(mainwindow)
        widget.setCurrentIndex(widget.currentIndex()+1)    
    def runprogram(self):
        self.Messages.clear()
        self.Messages_Buffer.clear()
        global ITEMS
        global counter
        counter=0
        global BUFFER_SIZE
        BUFFER_SIZE =int(self.Buffer.text())
        ITEMS=int(self.item.text())
        
        # Create producer and consumer threads
        producer_thread = Producer(self.Messages,self.Messages_Buffer)
        consumer_thread = Consumer(self.Messages,self.Messages_Buffer)

        # Start the threads
        producer_thread.start()
        consumer_thread.start()

        # Main thread waits for the threads to complete
        producer_thread.join()
        consumer_thread.join()
        
from matplotlib import pyplot as plt
import math
from PyQt5.QtWidgets import QDialog, QLineEdit, QTextEdit
from PyQt5 import uic

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
        self.Headmovement=self.findChild(QLineEdit,"Headmovement")
        self.FCFS.clicked.connect(self.FCFS_graph)
        self.SCAN.clicked.connect(self.SCAN_graph)
        self.CSCAN.clicked.connect(self.CSCAN_graph)
        self.LOOK.clicked.connect(self.LOOK_graph)
        self.CLOOK.clicked.connect(self.CLOOK_graph)
        self.direction_combo=self.findChild(QComboBox,"Combo_direction")
        self.SSTF.clicked.connect(self.SSTF_graph)
        plt.savefig('SCAN.png')
        self.pixmap_2=QPixmap('SCAN.png')
        self.label_2.setPixmap(self.pixmap_2)

    def addseqclicked(self):
        self.sequenceslist.append(int(self.sequence_atr.text()))
        self.seqlist.append(f"{self.sequence_atr.text()}")
        
    def FCFS_graph(self):
        CYLINDER_MAX = int(self.CYLINDER.text())
        sequence=self.sequenceslist.copy()
        temp = sequence.copy()
        start=int(self.start.text())
        temp.insert(0,start)
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
        plt.plot(x, y, color="green", markerfacecolor='blue', marker='o', markersize=5, linewidth=2, label="FCFS")
        plt.ylim = (0, size)
        plt.xlim = (0, CYLINDER_MAX)
        plt.yticks([])
        plt.title("First Come First Served Scheduling Algorithm")
        plt.text(172.5, -8.85, string, horizontalalignment='center', verticalalignment='center', fontsize=12)
        plt.text(172.5, -9.5, string2, horizontalalignment='center', verticalalignment='center', fontsize=12)
        plt.savefig('FCFS.png')
        self.pixmap_2=QPixmap('FCFS.png')
        self.label_2.setPixmap(self.pixmap_2)
        plt.show()
        
        
    def SSTF_graph(self):
        CYLINDER_MAX = int(self.CYLINDER.text())
        sequence=self.sequenceslist
        temp = sequence.copy()
        start=int(self.start.text())
        def next_in_sequence(seq, val):
            diff = 0
            mindiff = math.inf
            nextval = 0
            for i in range(0, len(seq)):
                if seq[i] != val:
                    diff = abs(seq[i] - val)
                    if diff < mindiff:
                        mindiff = diff
                        nextval = seq[i]
            return nextval

        temp.insert(0,start)
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

        plt.plot(x, y, color="green", markerfacecolor='blue', marker='o', markersize=5, linewidth=2, label="SSTF")
        plt.ylim = (0, size)
        plt.xlim = (0,CYLINDER_MAX)
        plt.yticks([])
        plt.title("Shortest Seek Time First Scheduling Algorithm")
        plt.text(182.5, -10.85, string, horizontalalignment='center',verticalalignment='center',fontsize=12)
        plt.text(182.5, -11.5, string2, horizontalalignment='center',verticalalignment='center',fontsize=12)
        plt.savefig('SSTF.png')
        self.pixmap_2=QPixmap('SSTF.png')
        self.label_2.setPixmap(self.pixmap_2)
        plt.show()
        
    # #SCAN  
    def SCAN_graph(self):
        CYLINDER_MAX = int(self.CYLINDER.text())
        direction=self.direction_combo.currentText()
        print(direction)
        sequence=self.sequenceslist
        temp = sequence.copy()
        start=int(self.start.text())
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

        plt.plot(x, y, color="green", markerfacecolor='blue', marker='o', markersize=5, linewidth=2, label="SCAN")
        plt.plot(x_approx, y_approx, dashes=[6, 2], color="red", markerfacecolor='red', marker='D', markersize=5,
                 linewidth=0.5, label="Approx SCAN")
        plt.ylim = (0, size)
        plt.xlim = (0, CYLINDER_MAX)
        plt.yticks([])
        plt.title("SCAN Scheduling Algorithm")
        plt.text(182.5, -10.85, string, horizontalalignment='center', verticalalignment='center', fontsize=12)
        plt.text(182.5, -12.5, string2, horizontalalignment='center', verticalalignment='center', fontsize=12)
        plt.savefig('SCAN.png')
        self.pixmap_2=QPixmap('SCAN.png')
        self.label_2.setPixmap(self.pixmap_2)
        plt.show()
        
        
        
    def CSCAN_graph(self):
        CYLINDER_MAX = int(self.CYLINDER.text())
        direction=self.direction_combo.currentText()
        print(direction)
        sequence=self.sequenceslist
        start=int(self.start.text())
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
            headmovement_approx = abs(start - 199)
            headmovement_approx = headmovement_approx + abs(199 - 0)
            headmovement_approx = headmovement_approx + abs(0 - x[-1])

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
        
        plt.plot(x, y, color="green", markerfacecolor='blue', marker='o', markersize=5, linewidth=2, label="CSCAN")
        plt.plot(x_approx, y_approx, dashes=[6, 2], color="red", markerfacecolor='red', marker='D', markersize=5,
                 linewidth=0.5, label="Approx CSCAN")
        plt.ylim = (0, size)
        plt.xlim = (0, CYLINDER_MAX)
        plt.yticks([])
        plt.title("CSCAN Scheduling Algorithm")
        plt.text(182.5, -10.85, string, horizontalalignment='center', verticalalignment='center', fontsize=12)
        plt.text(182.5, -12.5, string2, horizontalalignment='center', verticalalignment='center', fontsize=12)
        plt.savefig('CSCAN.png')
        self.pixmap_2=QPixmap('CSCAN.png')
        self.label_2.setPixmap(self.pixmap_2)
        plt.show()
    
    def LOOK_graph(self):
        CYLINDER_MAX = int(self.CYLINDER.text())
        direction=self.direction_combo.currentText()
        print(direction)
        sequence=self.sequenceslist
        start=int(self.start.text())
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

        plt.plot(x, y, color="green", markerfacecolor='blue', marker='o', markersize=5, linewidth=2, label="LOOK")
        plt.plot(x_approx, y_approx, dashes=[6, 2], color="red", markerfacecolor='red', marker='D', markersize=5,
                 linewidth=0.5, label="Approx LOOK")
        plt.ylim = (0, size)
        plt.xlim = (0, CYLINDER_MAX)
        plt.yticks([])
        plt.title("LOOK Scheduling Algorithm")
        plt.text(182.5, -10.85, string, horizontalalignment='center', verticalalignment='center', fontsize=12)
        plt.text(182.5, -12.5, string2, horizontalalignment='center', verticalalignment='center', fontsize=12)
        plt.savefig('LOOK.png')
        self.pixmap_2=QPixmap('LOOK.png')
        self.label_2.setPixmap(self.pixmap_2)
        plt.show()
        
    def CLOOK_graph(self):
        CYLINDER_MAX = int(self.CYLINDER.text())
        direction=self.direction_combo.currentText()
        print(direction)
        sequence=self.sequenceslist
        start=int(self.start.text())
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

        plt.plot(x, y, color="green", markerfacecolor='blue', marker='o', markersize=5, linewidth=2, label="CLOOK")
        plt.plot(x_approx, y_approx, dashes=[6, 2], color="red", markerfacecolor='red', marker='D', markersize=5,
                 linewidth=0.5, label="Approx CLOOK")
        plt.ylim = (0, size)
        plt.xlim = (0, CYLINDER_MAX)
        plt.yticks([])
        plt.title("CLOOK Scheduling Algorithm")
        plt.text(182.5, -10.85, string, horizontalalignment='center', verticalalignment='center', fontsize=12)
        plt.text(182.5, -12.5, string2, horizontalalignment='center', verticalalignment='center', fontsize=12)
        plt.savefig('CLOOK.png')
        self.pixmap_2=QPixmap('CLOOK.png')
        self.label_2.setPixmap(self.pixmap_2)
        plt.show()
        
import json
import copy
from sys import *
from math import gcd
from collections import OrderedDict
import matplotlib.pyplot as plt
import numpy as np
import statistics as st
from collections import defaultdict

        
 
class Screen4(QDialog):
    def __init__(self):
        super(Screen4, self).__init__()
        uic.loadUi("screen4.ui", self)
        #self.ADDNumTasks.clicked.connect(self.TaskNumber)
        self.numoftasks=self.findChild(QLineEdit,"NumofTasks")
        #self.ADDTask.clicked.connect(self.newTask)
        self.label_3=self.findChild(QLabel,"label_3")
        self.period=self.findChild(QLineEdit,"Period")
        self.wcet=self.findChild(QLineEdit,"WCET")
        #self.RMA.clicked.connect(self.runRMA)
        self.pixmap_2=QPixmap('RMA.png')
        self.label_3.setPixmap(self.pixmap_2)
        
from collections import deque
import math
class Task:
    def __init__(self, name, period, release_time, deadline, execution_time):
        self.name = name
        self.period = period
        self.release_time = release_time
        self.deadline = deadline
        self.execution_time = execution_time
        self.remaining_time = execution_time
  
class Screen5(QDialog):
    def __init__(self):
        super(Screen5, self).__init__()
        uic.loadUi("screen5.ui", self)
        
        self.label_2=self.findChild(QLabel,"label_2")
        self.release_time_label=self.findChild(QLineEdit,"ReleaseTime")
        self.period_time_label=self.findChild(QLineEdit,"PeriodTime")
        self.dead_line_label=self.findChild(QLineEdit,"DeadLine")
        self.excution_time_label=self.findChild(QLineEdit,"ExcutionTime")
        self.quantum_time_label=self.findChild(QLineEdit,"QuantumTime")
        self.listoftask=[]
        self.AddTask.clicked.connect(self.clicker2)
        self.RunProgram.clicked.connect(self.runtaskclicker)
        self.release_times=[]
        self.taskreport=self.findChild(QTextEdit,"textEdit")
        self.MainMenu.clicked.connect(self.gotoMainMenu)
    def clicker2(self):
        taskname="Task "+str(len(self.listoftask))
        self.listoftask.append(Task(taskname,float(self.period_time_label.text()),float(self.release_time_label.text()),float(self.dead_line_label.text()),float(self.excution_time_label.text())))
        self.taskreport.append(taskname+f" , period_time_label : {self.period_time_label.text()} , release_time : {self.release_time_label.text()} , dead_line : {self.dead_line_label.text()} , excution_time_label : {self.excution_time_label.text()}")
            
    def runtaskclicker(self):
            for i in self.listoftask:
                self.release_times.append(i.release_time)
            self.schedule_tasks(self.listoftask,self.listoftask,self.listoftask,float(self.quantum_time_label.text()))
        
        
    def schedule_tasks(self,tasks,tasks2,task3, time_quantum):
        queue = tasks
        period_queue=tasks2
        ready_queue = deque()
        running_queue = deque()
        waiting_time = [0] * len(tasks)
        turnaround_time = [0] * len(tasks)
        total_waiting_time = 0
        total_turnaround_time = 0
        gantt_chart = []
        current_time = 0.0
        current_task = None
    
        
    
        while (queue or current_task or ready_queue or running_queue or period_queue) and current_time <=14:
          for w in self.release_times:
            if current_time >=w:
              for l in queue :
                ready_queue.append(l)
                queue.remove(l)
                get_out=True
                self.release_times.remove(w)
                break
            if get_out==True:
              get_out=False
              break
          counter=0
          for f in period_queue:
            if current_time >=f.period+f.release_time:
              if(counter>0):
                period_queue[period_queue.index(f)]=Task(f.name,f.period,current_time,f.deadline,f.execution_time)
                running_queue.append(f)
                continue
              period_queue[period_queue.index(f)]=Task(f.name,f.period,current_time,f.deadline,f.execution_time)
              ready_queue.append(f)
              counter+=1      
          
          if ready_queue:
            current_task = ready_queue.popleft()
          elif running_queue:
            current_task = running_queue.popleft()
          else:
            current_time+=time_quantum
            continue
    
    
          
          if current_task.remaining_time > 0:
              if current_task.remaining_time <= time_quantum:
                time_taken = current_task.remaining_time
                gantt_chart.append((current_task.name, current_time, current_time + time_taken))
                current_time+=time_taken
                current_task=None
              else:
                if len(running_queue)==0: 
                  current_time += time_quantum
                  flag=False
                  for s in queue :
                    if s.release_time<=current_time:
                      current_task.remaining_time -= time_quantum
                      time_taken = current_task.remaining_time
                      gantt_chart.append((current_task.name, current_time-time_quantum, current_time-time_quantum+ time_taken))
                      running_queue.append(current_task)
                      current_task=None
                      flag=True
                      break
                  if flag==True:
                    flag=False
                    continue
                  flag4=False
                  for h in queue:
                    if current_task.remaining_time >h.release_time:
                      current_task.remaining_time -= h.release_time
                      time_taken = h.release_time
                      gantt_chart.append((current_task.name, current_time-time_quantum, current_time-time_quantum+ time_taken))
                      running_queue.append(current_task)
                      current_task=None
                      flag4=True
                      current_time -= time_quantum
                      current_time+=h.release_time
                      break
                  if(flag4==True):
                    flag4=False
                    continue
                  flag7=False
                  
                  for x in period_queue :
                    if x.period+x.release_time<current_time-time_quantum+current_task.remaining_time:
                      current_task.remaining_time -= -(current_time-time_quantum-x.period)
                      time_taken =-(current_time-time_quantum-x.period)
                      gantt_chart.append((current_task.name, current_time-time_quantum, current_time-time_quantum+ time_taken))
                      current_time=x.period+x.release_time
                      running_queue.append(current_task)
                      current_task=None
                      flag7=True
                      break
                  if flag7==True:
                    flag7=False
                    continue
                  time_taken = current_task.remaining_time
                  gantt_chart.append((current_task.name, current_time-time_quantum, current_time-time_quantum + time_taken))
                  current_time =current_time-time_quantum+time_taken
                  current_task=None 
                else:
                  time_taken = time_quantum
                  current_task.remaining_time -=time_quantum
                  gantt_chart.append((current_task.name, current_time, current_time + time_taken))
                  current_time += time_quantum
                  running_queue.append(current_task)
                  current_task=None
        self.plot_gantt_chart(gantt_chart,0.25)   
        
        
    def plot_gantt_chart(self,gantt_chart, quantum_time):
            fig, gnt = plt.subplots()
        
            gnt.set_title('Round Robin Scheduling')
            gnt.set_xlabel('Time')
            gnt.set_ylabel('Tasks')
        
            colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan']
            task_colors = {}
        
            for i, task in enumerate(gantt_chart):
                task_name = task[0]
                start_time = task[1]
                end_time = task[2]
                color = task_colors.get(task_name)
        
                if color is None:
                    color = colors[len(task_colors) % len(colors)]
                    task_colors[task_name] = color
        
                # Set y-dimension to 5 for all tasks
                y_dimension = 5
        
                # Set the position of the task rectangle in line with the x-axis
                y_position = 0
        
                gnt.broken_barh([(start_time, end_time - start_time)], (y_position, y_dimension), facecolors=color, edgecolor='black')
            # Specify x-axis ticks based on the quantum time
            x_ticks = [i for i in range(int(gantt_chart[0][1]), int(gantt_chart[-1][2]) + 1) if i % quantum_time == 0]
            plt.xticks(x_ticks)
        
            # Hide the y-axis
            gnt.spines['left'].set_visible(False)
            gnt.yaxis.set_visible(False)
        
            plt.grid(True)
            
            # Convert the plot to a QImage
            canvas = FigureCanvas(plt.gcf())
            canvas.draw()
            plot_image = QImage(canvas.buffer_rgba(), canvas.width(), canvas.height(), QImage.Format_RGBA8888)
    
            # Convert the QImage to QPixmap
            pixmap = QPixmap.fromImage(plot_image)
    
            # Set the QPixmap as the pixmap of the QLabel
            self.label_2.setPixmap(pixmap)
    
            # Optional: Resize the QLabel to fit the plot
            self.label_2.setFixedSize(pixmap.size())
        
            plt.show()
                
                    
    def gotoMainMenu(self):
        mainwindow=MainWindow()
        widget.addWidget(mainwindow)
        widget.setCurrentIndex(widget.currentIndex()+1)
        


def rangeFloat(start, end, step):
    rangelist = [start]
    if step !=0:
        while True:
            start += step
            if start > end:
                break
            rangelist.append(round(start, 2))
    return rangelist

class Task_RMA:
    def __init__(self, taskName, releaseTime, period, executionTime, deadline, maxTime):
        self.taskName = taskName
        self.releaseTime = releaseTime
        self.period = period
        self.executionTime = executionTime
        self.remainingExecution = 0
        self.deadline = deadline
        self.deadlineBroken = False
        self.maxtime = maxTime
        self.priority = None
        self.readyTimes = [time for time in rangeFloat(releaseTime, maxTime+1, period)]
        self.readyTimes.append(self.readyTimes[-1]+period)
        self.deadlines = [readyTime+self.deadline for readyTime in self.readyTimes]
        self.executionTimes = []
        self.brokenDeadlines = []

    def updateDeadline(self, t):
        for deadline in self.deadlines:
            if deadline > t:
                self.deadline = deadline
                break
            
            
from rmawithplot import RMAOS
from DMA import DMAOS
from EDF import EDFOS
from Minimum_Laxity_First import Minimum_Laxity_FirstOS

class Screen6(QDialog):
    def __init__(self):
        super(Screen6, self).__init__()
        uic.loadUi("screen6.ui", self)
        
        self.label_2=self.findChild(QLabel,"label_2")
        self.release_time_label=self.findChild(QLineEdit,"ReleaseTime")
        self.period_time_label=self.findChild(QLineEdit,"PeriodTime")
        self.dead_line_label=self.findChild(QLineEdit,"DeadLine")
        self.excution_time_label=self.findChild(QLineEdit,"ExcutionTime")
        self.max_time_label=self.findChild(QLineEdit,"MaxTime")
        self.listoftask=[]
        self.AddTask.clicked.connect(self.clicker2)
        self.RunProgram.clicked.connect(self.runtaskclicker)
        self.release_times=[]
        self.taskreport=self.findChild(QTextEdit,"textEdit")
        self.MainMenu.clicked.connect(self.gotoMainMenu)
    def clicker2(self):
        taskname="Task "+str(len(self.listoftask))
        self.listoftask.append(Task_RMA(taskname,float(self.release_time_label.text()),float(self.period_time_label.text()),float(self.excution_time_label.text()),float(self.dead_line_label.text()),float(self.max_time_label.text())))
        self.taskreport.append(taskname+f" , period_time_label : {self.period_time_label.text()} , release_time : {self.release_time_label.text()} , dead_line : {self.dead_line_label.text()} , excution_time : {self.excution_time_label.text()}")
            
    def runtaskclicker(self):
        rma=RMAOS(self.listoftask, float(self.max_time_label.text()))
        #uncomment the below line to get the results in the CLI
        self.plot(rma.returnTasks())
        rma.getResults()
    
    
    def plot(self,Tasks):
        exedict = {}
        for i, task in enumerate(Tasks):
            exedict[f"{task.taskName}"] = task.executionTimes
    
        colors = ['blue', 'orange', 'purple']
        plt.figure(figsize=(10, 7))
    
        # Calculate the total number of tasks and intervals
        num_tasks = len(exedict)
        num_intervals = sum(len(intervals) for intervals in exedict.values())
    
        # Calculate the height and gap between each task
        task_height = 0.6 / num_tasks
        gap = task_height * 0.2
    
        # Calculate the y-axis positions for each task
        y_positions = np.arange(num_tasks) * (task_height + gap)
    
        # Draw the timing diagram with distinct colors
        for i, (task, intervals) in enumerate(exedict.items()):
            for start, end in intervals:
                duration = end - start
                rect = Rectangle((start, y_positions[i]), duration, task_height, edgecolor='black',
                                 facecolor=colors[i % len(colors)])
                plt.gca().add_patch(rect)
    
                # Add task label in the middle of the rectangle
                plt.text(start + duration / 2, y_positions[i] + task_height / 2, task, ha='center', va='center')
    
        # Set the x-axis limits
        maxtime = max([end for _, intervals in exedict.items() for _, end in intervals])
        plt.xlim(0, maxtime)
    
        # Set the y-axis limits
        plt.ylim(-gap, num_tasks * (task_height + gap))
    
        # Remove the top and right spines of the plot
        plt.gca().spines['top'].set_visible(False)
        plt.gca().spines['right'].set_visible(False)
    
        # Remove y-axis ticks and labels
        plt.yticks([])
    
        # Add gridlines
        plt.grid(True, axis='y', linestyle='--')
        
        
        # Convert the plot to a QImage
        canvas = FigureCanvas(plt.gcf())
        canvas.draw()
        plot_image = QImage(canvas.buffer_rgba(), canvas.width(), canvas.height(), QImage.Format_RGBA8888)

        # Convert the QImage to QPixmap
        pixmap = QPixmap.fromImage(plot_image)

        # Set the QPixmap as the pixmap of the QLabel
        self.label_2.setPixmap(pixmap)

        # Optional: Resize the QLabel to fit the plot
        self.label_2.setFixedSize(pixmap.size())
    
        # Show the plot
        plt.show()   
 
    
    def gotoMainMenu(self):
        mainwindow=MainWindow()
        widget.addWidget(mainwindow)
        widget.setCurrentIndex(widget.currentIndex()+1)


class Task_DMA:
    def __init__(self, taskName, releaseTime, period, executionTime, deadline, maxTime):
        self.taskName = taskName
        self.releaseTime = releaseTime
        self.period = period
        self.executionTime = executionTime
        self.remainingExecution = 0
        self.deadline = deadline
        self.deadlineBroken = False
        self.maxtime = maxTime
        self.priority = None
        self.readyTimes = [time for time in rangeFloat(releaseTime, maxTime+1, period)]
        self.readyTimes.append(self.readyTimes[-1] + period)
        self.deadlines = [readyTime+self.deadline for readyTime in self.readyTimes]
        self.executionTimes = []
        self.brokenDeadlines = []

    def updateDeadline(self, t):
        for deadline in self.deadlines:
            if deadline > t:
                self.deadline = deadline
                break

class Screen7(QDialog):
    def __init__(self):
        super(Screen7, self).__init__()
        uic.loadUi("screen7.ui", self)
        
        self.label_2=self.findChild(QLabel,"label_2")
        self.release_time_label=self.findChild(QLineEdit,"ReleaseTime")
        self.period_time_label=self.findChild(QLineEdit,"PeriodTime")
        self.dead_line_label=self.findChild(QLineEdit,"DeadLine")
        self.excution_time_label=self.findChild(QLineEdit,"ExcutionTime")
        self.max_time_label=self.findChild(QLineEdit,"MaxTime")
        self.listoftask=[]
        self.AddTask.clicked.connect(self.clicker2)
        self.RunProgram.clicked.connect(self.runtaskclicker)
        self.release_times=[]
        self.taskreport=self.findChild(QTextEdit,"textEdit")
        self.MainMenu.clicked.connect(self.gotoMainMenu)
    def clicker2(self):
        taskname="Task "+str(len(self.listoftask))
        self.listoftask.append(Task_DMA(taskname,float(self.release_time_label.text()),float(self.period_time_label.text()),float(self.excution_time_label.text()),float(self.dead_line_label.text()),float(self.max_time_label.text())))
        self.taskreport.append(taskname+f" , period_time_label : {self.period_time_label.text()} , release_time : {self.release_time_label.text()} , dead_line : {self.dead_line_label.text()} , excution_time : {self.excution_time_label.text()}")
            
    def runtaskclicker(self):
        rma=DMAOS(self.listoftask, float(self.max_time_label.text()))
        #uncomment the below line to get the results in the CLI
        self.plot(rma.returnTasks())
        rma.getResults()
    
    
    def plot(self,Tasks):
        exedict = {}
        for i, task in enumerate(Tasks):
            exedict[f"{task.taskName}"] = task.executionTimes
    
        colors = ['blue', 'orange', 'purple']
        plt.figure(figsize=(10, 7))
    
        # Calculate the total number of tasks and intervals
        num_tasks = len(exedict)
        num_intervals = sum(len(intervals) for intervals in exedict.values())
    
        # Calculate the height and gap between each task
        task_height = 0.6 / num_tasks
        gap = task_height * 0.2
    
        # Calculate the y-axis positions for each task
        y_positions = np.arange(num_tasks) * (task_height + gap)
    
        # Draw the timing diagram with distinct colors
        for i, (task, intervals) in enumerate(exedict.items()):
            for start, end in intervals:
                duration = end - start
                rect = Rectangle((start, y_positions[i]), duration, task_height, edgecolor='black',
                                 facecolor=colors[i % len(colors)])
                plt.gca().add_patch(rect)
    
                # Add task label in the middle of the rectangle
                plt.text(start + duration / 2, y_positions[i] + task_height / 2, task, ha='center', va='center')
    
        # Set the x-axis limits
        maxtime = max([end for _, intervals in exedict.items() for _, end in intervals])
        plt.xlim(0, maxtime)
    
        # Set the y-axis limits
        plt.ylim(-gap, num_tasks * (task_height + gap))
    
        # Remove the top and right spines of the plot
        plt.gca().spines['top'].set_visible(False)
        plt.gca().spines['right'].set_visible(False)
    
        # Remove y-axis ticks and labels
        plt.yticks([])
    
        # Add gridlines
        plt.grid(True, axis='y', linestyle='--')
        
        
        # Convert the plot to a QImage
        canvas = FigureCanvas(plt.gcf())
        canvas.draw()
        plot_image = QImage(canvas.buffer_rgba(), canvas.width(), canvas.height(), QImage.Format_RGBA8888)

        # Convert the QImage to QPixmap
        pixmap = QPixmap.fromImage(plot_image)

        # Set the QPixmap as the pixmap of the QLabel
        self.label_2.setPixmap(pixmap)

        # Optional: Resize the QLabel to fit the plot
        self.label_2.setFixedSize(pixmap.size())
    
        # Show the plot
        plt.show()   
    
    def gotoMainMenu(self):
        mainwindow=MainWindow()
        widget.addWidget(mainwindow)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
class Task_Minimum_Laxity_First:
    def __init__(self, taskName, releaseTime, period, executionTime, deadLine, maxTime):
        self.taskName = taskName
        self.releaseTime = releaseTime
        #assuming that the period of a task is the same as its deadline
        self.period = period
        # executionTime of task.
        self.executionTime = executionTime
        # remaining of executionTime
        self.remainingExecution = 0
        # deadLine of a task.
        self.deadLine = deadLine
        self.deadlineBroken = False
        # list of times where a new job of the task is ready to execute.
        self.readyTimes = [time for time in rangeFloat(self.releaseTime, maxTime+1, self.period)]
        self.readyTimes.append(self.readyTimes[-1] + period)
        #list that contain all deadline of the task during execution
        self.deadlines = [time + self.deadLine for time in self.readyTimes]
        #list that contains times of execution
        self.executionTimes = []
        # list that contains the times where slack time of a task is a negative number
        self.negativeSlackTimes = []
        self.brokenDeadlines = []
    def calcSlackTime(self, t):
        # if task has already finished execution means there is no need to calculate its slack time and return -1
        if self.remainingExecution!=0:
            # if there is sill remaining execution time we calculate the slack time of the task then return it.
            slackTime = (self.deadLine - t)-self.remainingExecution
            if slackTime<0:
                self.negativeSlackTimes.append((t, slackTime)) # broken deadlines
            return slackTime
        return None

    def updateDeadline(self, t):
        for deadline in self.deadlines:
            if deadline > t:
                self.deadLine = deadline
                break    

        
class Screen8(QDialog):
    def __init__(self):
        super(Screen8, self).__init__()
        uic.loadUi("screen8.ui", self)
        
        self.label_2=self.findChild(QLabel,"label_2")
        self.release_time_label=self.findChild(QLineEdit,"ReleaseTime")
        self.period_time_label=self.findChild(QLineEdit,"PeriodTime")
        self.dead_line_label=self.findChild(QLineEdit,"DeadLine")
        self.excution_time_label=self.findChild(QLineEdit,"ExcutionTime")
        self.max_time_label=self.findChild(QLineEdit,"MaxTime")
        self.listoftask=[]
        self.AddTask.clicked.connect(self.clicker2)
        self.RunProgram.clicked.connect(self.runtaskclicker)
        self.release_times=[]
        self.taskreport=self.findChild(QTextEdit,"textEdit")
        self.MainMenu.clicked.connect(self.gotoMainMenu)
    def clicker2(self):
        taskname="Task "+str(len(self.listoftask))
        self.listoftask.append(Task_Minimum_Laxity_First(taskname,float(self.release_time_label.text()),float(self.period_time_label.text()),float(self.excution_time_label.text()),float(self.dead_line_label.text()),float(self.max_time_label.text())))
        self.taskreport.append(taskname+f" , period_time_label : {self.period_time_label.text()} , release_time : {self.release_time_label.text()} , dead_line : {self.dead_line_label.text()} , excution_time : {self.excution_time_label.text()}")
            
    def runtaskclicker(self):
        rma=Minimum_Laxity_FirstOS(self.listoftask, float(self.max_time_label.text()))
        #uncomment the below line to get the results in the CLI
        self.plot(rma.returnTasks())
        rma.getResults()
    
    
    def plot(self,Tasks):
        exedict = {}
        for i, task in enumerate(Tasks):
            exedict[f"{task.taskName}"] = task.executionTimes
    
        colors = ['blue', 'orange', 'purple']
        plt.figure(figsize=(10, 7))
    
        # Calculate the total number of tasks and intervals
        num_tasks = len(exedict)
        num_intervals = sum(len(intervals) for intervals in exedict.values())
    
        # Calculate the height and gap between each task
        task_height = 0.6 / num_tasks
        gap = task_height * 0.2
    
        # Calculate the y-axis positions for each task
        y_positions = np.arange(num_tasks) * (task_height + gap)
    
        # Draw the timing diagram with distinct colors
        for i, (task, intervals) in enumerate(exedict.items()):
            for start, end in intervals:
                duration = end - start
                rect = Rectangle((start, y_positions[i]), duration, task_height, edgecolor='black',
                                 facecolor=colors[i % len(colors)])
                plt.gca().add_patch(rect)
    
                # Add task label in the middle of the rectangle
                plt.text(start + duration / 2, y_positions[i] + task_height / 2, task, ha='center', va='center')
    
        # Set the x-axis limits
        maxtime = max([end for _, intervals in exedict.items() for _, end in intervals])
        plt.xlim(0, maxtime)
    
        # Set the y-axis limits
        plt.ylim(-gap, num_tasks * (task_height + gap))
    
        # Remove the top and right spines of the plot
        plt.gca().spines['top'].set_visible(False)
        plt.gca().spines['right'].set_visible(False)
    
        # Remove y-axis ticks and labels
        plt.yticks([])
    
        # Add gridlines
        plt.grid(True, axis='y', linestyle='--')
        
        
        # Convert the plot to a QImage
        canvas = FigureCanvas(plt.gcf())
        canvas.draw()
        plot_image = QImage(canvas.buffer_rgba(), canvas.width(), canvas.height(), QImage.Format_RGBA8888)

        # Convert the QImage to QPixmap
        pixmap = QPixmap.fromImage(plot_image)

        # Set the QPixmap as the pixmap of the QLabel
        self.label_2.setPixmap(pixmap)

        # Optional: Resize the QLabel to fit the plot
        self.label_2.setFixedSize(pixmap.size())
    
        # Show the plot
        plt.show()   
    
    def gotoMainMenu(self):
        mainwindow=MainWindow()
        widget.addWidget(mainwindow)
        widget.setCurrentIndex(widget.currentIndex()+1)
        


class Task_EDF:
    def __init__(self, taskName, releaseTime, period, executionTime, deadLine, maxTime):
        self.taskName = taskName
        self.releaseTime = releaseTime
        self.period = period
        # executionTime of task.
        self.executionTime = executionTime
        # remaining of executionTime
        self.remainingExecution = 0
        # deadLine of a task.
        self.deadLine = deadLine
        self.deadlineBroken = False
        # list of times where a new job of the task is ready to execute.
        self.readyTimes = [time for time in rangeFloat(self.releaseTime, maxTime+1, self.period)]   
        self.readyTimes.append(self.readyTimes[-1] + period)
        # print(self.readyTimes)
        #list that contain all deadline of the task during execution
        self.deadlines = [time + self.deadLine for time in self.readyTimes]
        #list that contains times of execution
        self.executionTimes = []
        #list that contains any broken deadlines
        self.brokenDeadlines = []
    def getDeadline(self):
        if self.remainingExecution != 0:
            return self.deadLine
        return None

    def updateDeadline(self, t):
        for deadline in self.deadlines:
            if deadline > t:
                self.deadLine = deadline
                break

class Screen9(QDialog):
    def __init__(self):
        super(Screen9, self).__init__()
        uic.loadUi("screen9.ui", self)
        
        self.label_2=self.findChild(QLabel,"label_2")
        self.release_time_label=self.findChild(QLineEdit,"ReleaseTime")
        self.period_time_label=self.findChild(QLineEdit,"PeriodTime")
        self.dead_line_label=self.findChild(QLineEdit,"DeadLine")
        self.excution_time_label=self.findChild(QLineEdit,"ExcutionTime")
        self.max_time_label=self.findChild(QLineEdit,"MaxTime")
        self.listoftask=[]
        self.AddTask.clicked.connect(self.clicker2)
        self.RunProgram.clicked.connect(self.runtaskclicker)
        self.release_times=[]
        self.taskreport=self.findChild(QTextEdit,"textEdit")
        self.MainMenu.clicked.connect(self.gotoMainMenu)
    def clicker2(self):
        taskname="Task "+str(len(self.listoftask))
        self.listoftask.append(Task_EDF(taskname,float(self.release_time_label.text()),float(self.period_time_label.text()),float(self.excution_time_label.text()),float(self.dead_line_label.text()),float(self.max_time_label.text())))
        self.taskreport.append(taskname+f" , period_time_label : {self.period_time_label.text()} , release_time : {self.release_time_label.text()} , dead_line : {self.dead_line_label.text()} , excution_time : {self.excution_time_label.text()}")
            
    def runtaskclicker(self):
        rma=EDFOS(self.listoftask, float(self.max_time_label.text()))
        #uncomment the below line to get the results in the CLI
        self.plot(rma.returnTasks())
        rma.getResults()
    
    
    def plot(self,Tasks):
        exedict = {}
        for i, task in enumerate(Tasks):
            exedict[f"{task.taskName}"] = task.executionTimes
    
        colors = ['blue', 'orange', 'purple']
        plt.figure(figsize=(10, 7))
    
        # Calculate the total number of tasks and intervals
        num_tasks = len(exedict)
        num_intervals = sum(len(intervals) for intervals in exedict.values())
    
        # Calculate the height and gap between each task
        task_height = 0.6 / num_tasks
        gap = task_height * 0.2
    
        # Calculate the y-axis positions for each task
        y_positions = np.arange(num_tasks) * (task_height + gap)
    
        # Draw the timing diagram with distinct colors
        for i, (task, intervals) in enumerate(exedict.items()):
            for start, end in intervals:
                duration = end - start
                rect = Rectangle((start, y_positions[i]), duration, task_height, edgecolor='black',
                                 facecolor=colors[i % len(colors)])
                plt.gca().add_patch(rect)
    
                # Add task label in the middle of the rectangle
                plt.text(start + duration / 2, y_positions[i] + task_height / 2, task, ha='center', va='center')
    
        # Set the x-axis limits
        maxtime = max([end for _, intervals in exedict.items() for _, end in intervals])
        plt.xlim(0, maxtime)
    
        # Set the y-axis limits
        plt.ylim(-gap, num_tasks * (task_height + gap))
    
        # Remove the top and right spines of the plot
        plt.gca().spines['top'].set_visible(False)
        plt.gca().spines['right'].set_visible(False)
    
        # Remove y-axis ticks and labels
        plt.yticks([])
    
        # Add gridlines
        plt.grid(True, axis='y', linestyle='--')
        
        
        # Convert the plot to a QImage
        canvas = FigureCanvas(plt.gcf())
        canvas.draw()
        plot_image = QImage(canvas.buffer_rgba(), canvas.width(), canvas.height(), QImage.Format_RGBA8888)

        # Convert the QImage to QPixmap
        pixmap = QPixmap.fromImage(plot_image)

        # Set the QPixmap as the pixmap of the QLabel
        self.label_2.setPixmap(pixmap)

        # Optional: Resize the QLabel to fit the plot
        self.label_2.setFixedSize(pixmap.size())
    
        # Show the plot
        plt.show()   
    
    def gotoMainMenu(self):
        mainwindow=MainWindow()
        widget.addWidget(mainwindow)
        widget.setCurrentIndex(widget.currentIndex()+1)
        
class Task_Completion_Time_Test:
    def __init__(self, name ,period, execution_times):
        self.name=name
        self.period = period
        self.execution_times = execution_times
        self.deadline = period
        
    


class Screen10(QDialog):
    def __init__(self):
        super(Screen10, self).__init__()
        uic.loadUi("screen10.ui", self)
        
        self.period_time_label=self.findChild(QLineEdit,"PeriodTime")
        self.excution_time_label=self.findChild(QLineEdit,"ExcutionTime")
        self.listoftask=[]
        self.listoftask2=[]
        self.AddTask.clicked.connect(self.clicker2)
        self.RunProgram.clicked.connect(self.runtaskclicker)
        self.taskreport=self.findChild(QTextEdit,"textEdit")
        self.Report_edit=self.findChild(QTextEdit,"Report")
        self.PeriodTransformation.clicked.connect(self.runperiodclicker)
        self.MainMenu.clicked.connect(self.gotoMainMenu)
        self.t=0
        self.counter=0
        
    def clicker2(self):
        taskname="Task "+str(len(self.listoftask)+1)
        self.listoftask2.append(Task_Completion_Time_Test(taskname,float(self.period_time_label.text()),float(self.excution_time_label.text())))
        self.listoftask.append(Task_Completion_Time_Test(taskname,float(self.period_time_label.text()),float(self.excution_time_label.text())))
        self.taskreport.append(taskname+f" , period_time_label : {self.period_time_label.text()} , dead_line : {self.period_time_label.text()} , excution_time : {self.excution_time_label.text()}")
    def runtaskclicker(self):
            
            
            n=len(self.listoftask)
            
            bound=n*(2**(1/n)-1)
            self.Report_edit.append(f"Bound of Tasks = {bound}")
            accumulativeutilization=0
            for i in self.listoftask:
                accumulativeutilization+=i.execution_times / i.period
            self.Report_edit.append(f"accumulative utilization of Tasks = {accumulativeutilization}")
            
            if accumulativeutilization>bound:
                self.Report_edit.append("accumulativeutilization > bound ")
                self.Report_edit.append("Tasks cannot be schedule according to accumulativeutilization")
            else:
                self.Report_edit.append("System Can be Schedule according to accumulativeutilization")
            
            self.Report_edit.append("\n !---------------------------!")
            
            self.t=0
            self.listoftask.sort(key=lambda x: x.period)  # Sort tasks based on periods in ascending order
            self.t+=self.listoftask[0].execution_times
            flag=True
            for i in range(1,len(self.listoftask)):
                if self.schedule_task(self.listoftask[i]) ==False:
                    self.Report_edit.append(f"Task {i} cannot be schedul due to deadline broken ")
                    print(f"Task {i} cannot be schedul due to deadline broken ")
                    self.Report_edit.append("System Cannot be Schedule")
                    print("System Cannot be Schedule")
                    flag=False
                    break
            if flag==True:
                self.Report_edit.append("System Can be Schedule")
                print("System Can be Schedule according to Completion Time Test")
            
    def schedule_task(self,task):
              w=self.t+task.execution_times
              if w>task.deadline:
                self.Report_edit.append(f"w(t) = {w} > deadline of {task.name} = {task.deadline}")
                return False
              higher_priority_tasks=[]
              for i in range(0,self.listoftask.index(task)):
                higher_priority_tasks.append(self.listoftask[i])
              for h in higher_priority_tasks:
                if w>h.period:
                  h.period+=h.period
                  w+=h.execution_times
                  if w>task.deadline:
                    self.Report_edit.append(f"w(t) = {w} > deadline of {task.name} = {task.deadline}")
                    return False
              self.Report_edit.append(f"w(t) = {w} and deadline of {task.name} = {task.deadline} so {task.name} is scheduable")
              self.t=w
              return True
      
    def runperiodclicker(self):
        flag=False
        while flag==False:
            flag=True
            self.t=0
            for i in self.listoftask:
                for y in self.listoftask2:
                    if i.name==y.name:
                        i.period=y.period
            self.listoftask.sort(key=lambda x: x.period)  # Sort tasks based on periods in ascending order
            self.t+=self.listoftask[0].execution_times
            for i in range(1,len(self.listoftask)):
                if self.schedule_task(self.listoftask[i]) ==False:
                    self.Report_edit.append(f"Task {i} cannot be schedul due to deadline broken ")
                    print(f"Task {i} cannot be schedul due to deadline broken ")
                    self.Report_edit.append("System Cannot be Schedule")
                    print("System Cannot be Schedule")
                    flag=False
                    if self.counter==0:
                        self.listoftask[i].name="new Task"
                        self.listoftask2[i].name="new Task"
                        self.listoftask[i].period/=2
                        self.listoftask2[i].period/=2
                        self.listoftask[i].deadline/=2
                        self.listoftask[i].execution_times/=2
                        self.counter+=1
                    else:
                        indextask=0
                        for m in self.listoftask2:
                            if m.name=="new Task":
                                indextask=self.listoftask2.index(m)
                        for x in self.listoftask:
                            if x.name=="new Task":
                                x.period/=2
                                self.listoftask2[indextask].period/=2
                                x.deadline/=2
                                x.execution_times/=2
                                
                    break
        if flag==True:
            print(counter)
            self.Report_edit.append("System Can be Schedule")
            print("System Can be Schedule according to Completion Time Test")
          
    
    def gotoMainMenu(self):
        mainwindow=MainWindow()
        widget.addWidget(mainwindow)
        widget.setCurrentIndex(widget.currentIndex()+1)


class Task_FIFO:
    def __init__(self, name, release_time, execution_time, deadline, period):
        self.name = name
        self.release_time = release_time
        self.execution_time = execution_time
        self.deadline = deadline
        self.period = period


        
class Screen11(QDialog):
    def __init__(self):
        super(Screen11, self).__init__()
        uic.loadUi("screen11.ui", self)
        
        self.label_2=self.findChild(QLabel,"label_2")
        self.release_time_label=self.findChild(QLineEdit,"ReleaseTime")
        self.period_time_label=self.findChild(QLineEdit,"PeriodTime")
        self.dead_line_label=self.findChild(QLineEdit,"DeadLine")
        self.excution_time_label=self.findChild(QLineEdit,"ExcutionTime")
        self.stop_time=self.findChild(QLineEdit,"MaxTime")
        self.deadbroken=self.findChild(QTextEdit,"DeadLineBroken")
        self.listoftask=[]
        self.gantt_chart=[]
        self.AddTask.clicked.connect(self.clicker2)
        self.RunProgram.clicked.connect(self.runtaskclicker)
        self.release_times=[]
        self.taskreport=self.findChild(QTextEdit,"textEdit")
        self.MainMenu.clicked.connect(self.gotoMainMenu)
    def clicker2(self):
        taskname="Task "+str(len(self.listoftask))
        self.listoftask.append(Task_FIFO(taskname,float(self.release_time_label.text()),float(self.excution_time_label.text()),float(self.dead_line_label.text()),float(self.period_time_label.text())))
        self.taskreport.append(taskname+f" , period_time_label : {self.period_time_label.text()} , release_time : {self.release_time_label.text()} , dead_line : {self.dead_line_label.text()} , excution_time_label : {self.excution_time_label.text()}")
            
    def runtaskclicker(self):
            for i in self.listoftask:
                self.release_times.append(i.release_time)
            self.fifo(self.listoftask,float(self.stop_time.text()))
            self.plot_gantt_chart2(self.gantt_chart,1)
            
            
    def fifo(self,tasks, stop_time):
        current_time=0
        flag=True
        while flag==True :
          tasks.sort(key=lambda x: x.release_time)
          if current_time>=tasks[0].release_time:
            self.gantt_chart.append((tasks[0].name, current_time, current_time+tasks[0].execution_time))
            current_time+=tasks[0].execution_time
            tasks[0].release_time+=tasks[0].period
            for i in tasks:
              if(current_time==23):
                print(i.release_time+i.deadline)
              if current_time+i.execution_time> i.release_time+i.deadline:
                print(f"deadline of {i.name} is broken because current time = {current_time } and deadline ={i.release_time+i.deadline}  ")
                self.deadbroken.append(f"deadline of {i.name} is broken because current time = {current_time } and deadline ={i.release_time+i.deadline}  ")
                flag=False
                break
                return
          else:
            current_time=tasks[0].release_time
          if(current_time>=stop_time):
            return
    
    def plot_gantt_chart2(self,gantt_chart, quantum_time):
        fig, gnt = plt.subplots()
    
        gnt.set_title('FIFO Scheduling')
        gnt.set_xlabel('Time')
        gnt.set_ylabel('Tasks')
    
        colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan']
        task_colors = {}
    
        for i, task in enumerate(gantt_chart):
            task_name = task[0]
            start_time = task[1]
            end_time = task[2]
            color = task_colors.get(task_name)
    
            if color is None:
                color = colors[len(task_colors) % len(colors)]
                task_colors[task_name] = color
    
            # Set y-dimension to 5 for all tasks
            y_dimension = 5
    
            # Set the position of the task rectangle in line with the x-axis
            y_position = 0
    
            gnt.broken_barh([(start_time, end_time - start_time)], (y_position, y_dimension), facecolors=color, edgecolor='black')
        # Specify x-axis ticks based on the quantum time
        x_ticks = [i for i in range(int(gantt_chart[0][1]), int(gantt_chart[-1][2]) + 1) if i % quantum_time == 0]
        plt.xticks(x_ticks)
    
        # Hide the y-axis
        gnt.spines['left'].set_visible(False)
        gnt.yaxis.set_visible(False)
    
        plt.grid(True)
        
        
        # Convert the plot to a QImage
        canvas = FigureCanvas(plt.gcf())
        canvas.draw()
        plot_image = QImage(canvas.buffer_rgba(), canvas.width(), canvas.height(), QImage.Format_RGBA8888)

        # Convert the QImage to QPixmap
        pixmap = QPixmap.fromImage(plot_image)

        # Set the QPixmap as the pixmap of the QLabel
        self.label_2.setPixmap(pixmap)

        # Optional: Resize the QLabel to fit the plot
        self.label_2.setFixedSize(pixmap.size())
    
    
        plt.show()

    
          
    def gotoMainMenu(self):
        mainwindow=MainWindow()
        widget.addWidget(mainwindow)
        widget.setCurrentIndex(widget.currentIndex()+1)

app=QApplication(sys.argv)

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

