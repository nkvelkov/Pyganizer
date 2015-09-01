import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QTextBrowser, QDateTimeEdit, QTimeEdit, QDateEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QWidget, QToolTip, 
    QPushButton, QApplication)
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QLineEdit, QTextEdit, QDesktopWidget, QApplication, QMessageBox
import sys
from PyQt5.QtWidgets import QMainWindow, QTextEdit, QAction, QApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTime, QDate
import arrow
from pyganizer import Pyganizer
from task import Task, TaskEncoder, as_task
from event import Event, EventEncoder, as_event
import json

class IconWidget(QMainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
        self.pyganizer = Pyganizer("pending_tasks.txt", "active_tasks.txt",
                                   "pending_events.txt", "active_events.txt")

    def initUI(self):

        QToolTip.setFont(QFont('SansSerif', 10))        
        self.setToolTip('This is a <b>Pyganizer</b>.')
       
        self.prepare_tasks_UI()
        self.prepare_events_UI()

        self.prepare_geometry()
        self.center()

        self.show()

    def prepare_tasks_UI(self):
        self.add_task_line_edit_fields()
        self.add_tasks_table()
        self.add_task_date_time_edit()
        
        self.add_task_refresh_button()
        self.add_task_button()

    def prepare_events_UI(self):
        self.add_event_line_edit_fields()
        self.add_event_start_date_time_edit()
        self.add_event_end_date_time_edit()

        self.add_events_table()
        self.add_event_refresh_button()
        self.add_event_button()

    def add_tasks_table(self):
        self.table = QTextBrowser(self)
        self.table.setReadOnly(True)
        self.table.move(200, 40)
        self.table.resize(self.table.sizeHint())
        self.table.setText(" Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed lacus urna, semper sit amet metus eu, vestibulum tempus arcu. Curabitur ornare condimentum massa id consectetur. Curabitur volutpat odio sollicitudin quam venenatis, sed ornare justo auctor. Aenean aliquet metus non nulla dignissim, sed pellentesque lacus sollicitudin. Etiam interdum quis odio eget. ")
    
    def add_events_table(self):
        self.table = QTextBrowser(self)
        self.table.setReadOnly(True)
        self.table.move(200, 450)
        self.table.resize(self.table.sizeHint())
        self.table.setText(" Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed lacus urna, semper sit amet metus eu, vestibulum tempus arcu. Curabitur ornare condimentum massa id consectetur. Curabitur volutpat odio sollicitudin quam venenatis, sed ornare justo auctor. Aenean aliquet metus non nulla dignissim, sed pellentesque lacus sollicitudin. Etiam interdum quis odio eget. ")
    
    def add_task_date_time_edit(self):
        self.task_date_time_edit = QDateTimeEdit(self)
        self.task_date_time_edit.resize(self.task_date_time_edit.sizeHint())
        self.task_date_time_edit.move(30, 70)

    def add_event_start_date_time_edit(self):
        self.event_start_date_time_edit = QDateTimeEdit(self)
        self.event_start_date_time_edit.resize(self.event_start_date_time_edit.sizeHint())
        self.event_start_date_time_edit.move(30, 450)

    def add_event_end_date_time_edit(self):
        self.event_end_date_time_edit = QDateTimeEdit(self)
        self.event_end_date_time_edit.resize(self.event_end_date_time_edit.sizeHint())
        self.event_end_date_time_edit.move(30, 420)

    def add_task_line_edit_fields(self):
        self.task_name = QLineEdit('task_name', self)
        self.task_name.resize(self.task_name.sizeHint())
        self.task_name.move(30, 10)

        self.task_message = QLineEdit('task_message', self)
        self.task_message.resize(self.task_message.sizeHint())
        self.task_message.move(30, 40)

        self.task_completeness = QLineEdit('100', self)
        self.task_completeness.setGeometry(QtCore.QRect(10, 70, 13, 27))
        self.task_completeness.resize(self.task_completeness.sizeHint())
        self.task_completeness.move(30, 130)

        self.task_priority = QLineEdit('1', self)
        self.task_priority.resize(self.task_priority.sizeHint())
        self.task_priority.move(30, 100)

    def add_event_line_edit_fields(self):
        self.event_name = QLineEdit('event_name', self)
        self.event_name.resize(self.event_name.sizeHint())
        self.event_name.move(30, 480)

        self.event_message = QLineEdit('event_message', self)
        self.event_message.resize(self.event_message.sizeHint())
        self.event_message.move(30, 510)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    '''
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QMessageBox.Yes | 
            QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
        else: 
            event.ignore()
            # event.ignore()
    '''
    def add_task_refresh_button(self):
        self.refresh_button = QPushButton('refresh', self)
        self.refresh_button.setToolTip('<b>Refresh task</b>')
        self.refresh_button.clicked.connect(self.load_tasks)
        self.refresh_button.resize(self.refresh_button.sizeHint())
        self.refresh_button.move(200, 10) 
    
    def add_event_refresh_button(self):
        self.event_refresh_button = QPushButton('refresh', self)
        self.event_refresh_button.setToolTip('<b>Refresh task</b>')
        self.event_refresh_button.clicked.connect(self.load_tasks)
        self.event_refresh_button.resize(self.refresh_button.sizeHint())
        self.event_refresh_button.move(200, 420) 

    def add_task_button(self):
        self.task_button = QPushButton('AddTask', self)
        self.task_button.setToolTip('<b>AddTask</b>')
        self.task_button.clicked.connect(self.text_handle_func)
        self.task_button.resize(self.task_button.sizeHint())
        self.task_button.move(30, 160)

    def add_event_button(self):
        self.event_button = QPushButton('AddEvent', self)
        self.event_button.setToolTip('<b>AddEvent</b>')
        self.event_button.clicked.connect(self.text_handle_func)
        self.event_button.resize(self.event_button.sizeHint())
        self.event_button.move(30, 540)

    def prepare_geometry(self):
        self.setGeometry(300, 300, 625, 768)
        self.setWindowTitle('Pyganizer!')
        self.setWindowIcon(QIcon('1440359594_document_text_edit.ico')) 

    def text_handle_func(self):
        name = self.task_name.text()
        message = self.task_message.text()
        comleteness = int(self.task_completeness.text())
        priority = int(self.task_priority.text())

        current_date = self.date_time_edit.date()
        current_time = self.date_time_edit.time()
        start_date = arrow.Arrow(current_date.year(), current_date.month(),
                        current_date.day(), current_time.hour(),
                        current_time.minute(), current_time.second())
        print(name)
        print(message)
        print(start_date)
        print(comleteness)
        print(priority)
        print(type(start_date))    
        self.pyganizer.add_task(start_date, name, message, comleteness, priority)
        
        self.task_priority.setText("") 
        self.task_completeness.setText("")
        self.task_message.setText("")
        self.task_name.setText("")
        self.date_time_edit.setDate(QDate(0, 0, 0))
        self.date_time_edit.setTime(QTime(0, 0))

    def load_tasks(self):
        print("load_tasks")
        with open("active_tasks.txt", "r") as f:
            active_tasks = f.readlines()
            print(active_tasks)
            self.expose_tasks(active_tasks)

    def expose_tasks(self, lines):
        display_content = ''        
        for line in lines:
            print(line)
            task = json.loads(line, object_hook=as_task)
            display_content = '{}{}\n'.format(display_content, str(task))
        self.table.setText(display_content)


if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = IconWidget()
    sys.exit(app.exec_())  
