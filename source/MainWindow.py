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
from pyganizer import *
from task import Task, TaskEncoder, as_task
from event import Event, EventEncoder, as_event
from my_exceptions import *
import json
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from dateutil import tz


class IconWidget(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.horizontal_offset = 120
        self.vertical_offset = 270
        self.label_x_offset = 10
        self.now = arrow.now()
        self.initUI()
        self.tasks_ical = 'work_files/tasks.ics'
        self.events_ical = 'work_files/events.ics'
        self.active_tasks = "work_files/active_tasks.txt"
        self.active_events = "work_files/active_events.txt"

        self.pyganizer = Pyganizer("work_files/pending_tasks.txt", self.active_tasks, self.tasks_ical,
                                   "work_files/pending_events.txt", self.active_events, self.events_ical)
        self.pyganizer.execute()

    def initUI(self):

        QToolTip.setFont(QFont('SansSerif', 10))        
        self.setToolTip('This is <b>Pyganizer</b>.')
       
        self.prepare_tasks_UI()
        self.prepare_events_UI()

        self.prepare_geometry()
        self.center()

        self.load_tasks()
        self.load_events()

        self.show()

    def prepare_tasks_UI(self):
        self.task_line_edit_fields()
        self.tasks_table()
        self.task_date_time_edit()

        self.task_id_label()
        self.task_id_line_edit()
        self.remove_task_button()
        self.change_priority_button()
        self.change_progress_button()

        self.task_name_label()
        self.task_message_label()
        self.task_completeness_label()
        self.task_priority_label()
        self.task_datetime_label()
        self.task_completeness_label()
        self.task_priority_label()
        self.task_add_progress_label()
        self.task_add_priority_label()

        self.task_combo_text = 'local'
        self.task_combo()
        self.task_combo_label()

        self.tasks_ical_export_button()
        self.task_refresh_button()
        self.add_task_button()

    def prepare_events_UI(self):
        self.event_line_edit_fields()
        self.events_table()
        self.event_start_date_time_edit()
        self.event_end_date_time_edit()

        self.event_name_label()
        self.event_message_label()
        self.event_start_datetime_label()
        self.event_end_datetime_label()
        self.remove_event_button()

        self.event_combo_text = 'local'
        self.event_combo()
        self.event_combo_label()

        self.events_ical_export_button()
        self.event_refresh_button()
        self.add_event_button()

    def tasks_table(self):
        self.task_table = QTextBrowser(self)
        self.task_table.setReadOnly(True)
        self.task_table.move(self.horizontal_offset+200, 40)
        self.task_table.resize(400, 180)
        self.task_table.setText(" TASKS TABLE Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed lacus urna, semper sit amet metus eu, vestibulum tempus arcu. Curabitur ornare condimentum massa id consectetur. Curabitur volutpat odio sollicitudin quam venenatis, sed ornare justo auctor. Aenean aliquet metus non nulla dignissim, sed pellentesque lacus sollicitudin. Etiam interdum quis odio eget. ")

    def task_date_time_edit(self):
        self.task_date_time_edit = QDateTimeEdit(self)
        self.task_date_time_edit.setDate(QDate(self.now.day, self.now.month, self.now.year))
        self.task_date_time_edit.setTime(QTime(self.now.hour, self.now.minute))
        self.task_date_time_edit.resize(self.task_date_time_edit.sizeHint())
        self.task_date_time_edit.move(self.horizontal_offset, 70)

    def task_line_edit_fields(self):
        self.task_name = QLineEdit('task_name', self)
        self.task_name.resize(self.task_name.sizeHint())
        self.task_name.move(self.horizontal_offset, 10)

        self.task_message = QLineEdit('task_message', self)
        self.task_message.resize(self.task_message.sizeHint())
        self.task_message.move(self.horizontal_offset, 40)

        self.task_completeness = QLineEdit('100', self)
        self.task_completeness.setGeometry(QtCore.QRect(10, 70, 13, 27))
        self.task_completeness.resize(self.task_completeness.sizeHint())
        self.task_completeness.move(self.horizontal_offset, 130)

        self.task_priority = QLineEdit('1', self)
        self.task_priority.resize(self.task_priority.sizeHint())
        self.task_priority.move(self.horizontal_offset, 100)

        self.task_add_priority_line_edit()
        self.task_add_progress_line_edit()

    def tasks_ical_export_button(self):
        self.tasks_export_button = QPushButton('ical export', self)
        self.tasks_export_button.setToolTip('<b>Refresh ical file.</b>')
        self.tasks_export_button.clicked.connect(self.export_tasks_ical)
        self.tasks_export_button.resize(self.tasks_export_button.sizeHint())
        self.tasks_export_button.move(self.horizontal_offset+300, 10)

    def task_refresh_button(self):
        self.refresh_button = QPushButton('refresh', self)
        self.refresh_button.setToolTip('<b>Refresh tasks</b>')
        self.refresh_button.clicked.connect(self.load_tasks)
        self.refresh_button.resize(self.refresh_button.sizeHint())
        self.refresh_button.move(self.horizontal_offset+200, 10)

    def add_task_button(self):
        self.task_button = QPushButton('AddTask', self)
        self.task_button.setToolTip('<b>AddTask</b>')
        self.task_button.clicked.connect(self.add_task_func)
        self.task_button.resize(self.task_button.sizeHint())
        self.task_button.move(self.horizontal_offset, 190)

    def events_table(self):
        self.event_table = QTextBrowser(self)
        self.event_table.setReadOnly(True)
        self.event_table.move(self.horizontal_offset+200, 450)
        self.event_table.resize(400, 180)
        self.event_table.setText(" EVENTS TABLELorem ipsum dolor sit amet, consectetur adipiscing elit. Sed lacus urna, semper sit amet metus eu, vestibulum tempus arcu. Curabitur ornare condimentum massa id consectetur. Curabitur volutpat odio sollicitudin quam venenatis, sed ornare justo auctor. Aenean aliquet metus non nulla dignissim, sed pellentesque lacus sollicitudin. Etiam interdum quis odio eget. ")

    def event_start_date_time_edit(self):
        self.event_start_date_time_edit = QDateTimeEdit(self)
        self.event_start_date_time_edit.setDate(QDate(self.now.day, self.now.month, self.now.year))
        self.event_start_date_time_edit.setTime(QTime(self.now.hour, self.now.minute))
        self.event_start_date_time_edit.resize(self.event_start_date_time_edit.sizeHint())
        self.event_start_date_time_edit.move(self.horizontal_offset, 420)

    def event_end_date_time_edit(self):
        self.event_end_date_time_edit = QDateTimeEdit(self)
        self.event_end_date_time_edit.setDate(QDate(self.now.day, self.now.month, self.now.year))
        self.event_end_date_time_edit.setTime(QTime(self.now.hour, self.now.minute))
        self.event_end_date_time_edit.resize(self.event_end_date_time_edit.sizeHint())
        self.event_end_date_time_edit.move(self.horizontal_offset, 450)

    def event_line_edit_fields(self):
        self.event_name = QLineEdit('event_name', self)
        self.event_name.resize(self.event_name.sizeHint())
        self.event_name.move(self.horizontal_offset, 480)

        self.event_message = QLineEdit('event_message', self)
        self.event_message.resize(self.event_message.sizeHint())
        self.event_message.move(self.horizontal_offset, 510)

        self.event_id_line_edit()
        self.event_id_label()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def events_ical_export_button(self):
        self.events_export_button = QPushButton('ical export', self)
        self.events_export_button.setToolTip('<b>Refresh ical file.</b>')
        self.events_export_button.clicked.connect(self.export_events_ical)
        self.events_export_button.resize(self.events_export_button.sizeHint())
        self.events_export_button.move(self.horizontal_offset+300, 420)
    
    def event_refresh_button(self):
        self.event_refresh_button = QPushButton('refresh', self)
        self.event_refresh_button.setToolTip('<b>Refresh events</b>')
        self.event_refresh_button.clicked.connect(self.load_events)
        self.event_refresh_button.resize(self.refresh_button.sizeHint())
        self.event_refresh_button.move(self.horizontal_offset+200, 420) 

    def add_event_button(self):
        self.event_button = QPushButton('AddEvent', self)
        self.event_button.setToolTip('<b>AddEvent</b>')
        self.event_button.clicked.connect(self.add_event_func)
        self.event_button.resize(self.event_button.sizeHint())
        self.event_button.move(self.horizontal_offset, 570)

    def task_add_priority_line_edit(self):
        self.add_priority_line_edit = QLineEdit('pri', self)
        self.add_priority_line_edit.resize(40, 25)
        self.add_priority_line_edit.move(self.horizontal_offset+70, self.vertical_offset+60)

    def task_add_progress_line_edit(self):
        self.add_progress_line_edit = QLineEdit('pro', self)
        self.add_progress_line_edit.resize(40, 25)
        self.add_progress_line_edit.move(self.horizontal_offset+70, self.vertical_offset+30)

    def task_id_label(self):
        self.id_label = QLabel('Enter task id:', self)
        self.id_label.resize(self.id_label.sizeHint())
        self.id_label.move(self.horizontal_offset, self.vertical_offset-25)

    def task_add_progress_label(self):
        self.add_progress_label = QLabel('Progress:', self)
        self.add_progress_label.resize(self.add_progress_label.sizeHint())
        self.add_progress_label.move(self.horizontal_offset, self.vertical_offset+30)

    def task_add_priority_label(self):
        self.add_priority_label = QLabel('Priority:', self)
        self.add_priority_label.resize(self.add_priority_label.sizeHint())
        self.add_priority_label.move(self.horizontal_offset, self.vertical_offset+60)

    def task_name_label(self):
        self.task_name_label = QLabel('Name:', self)
        self.task_name_label.resize(self.task_name_label.sizeHint())
        self.task_name_label.move(self.label_x_offset, 10)

    def task_message_label(self):
        self.task_message_label = QLabel('Message:', self)
        self.task_message_label.resize(self.task_message_label.sizeHint())
        self.task_message_label.move(self.label_x_offset, 40)

    def task_datetime_label(self):
        self.task_datetime_label = QLabel('Datetime:', self)
        self.task_datetime_label.resize(self.task_datetime_label.sizeHint())
        self.task_datetime_label.move(self.label_x_offset, 70)

    def task_priority_label(self):
        self.task_message_label = QLabel('Priority:', self)
        self.task_message_label.resize(self.task_message_label.sizeHint())
        self.task_message_label.move(self.label_x_offset, 100)

    def task_completeness_label(self):
        self.task_message_label = QLabel('Comleteness:', self)
        self.task_message_label.resize(self.task_message_label.sizeHint())
        self.task_message_label.move(self.label_x_offset, 130)

    def event_name_label(self):
        self.event_name_label = QLabel('Name:', self)
        self.event_name_label.resize(self.event_name_label.sizeHint())
        self.event_name_label.move(self.label_x_offset, 480)

    def event_message_label(self):
        self.event_message_label = QLabel('Message:', self)
        self.event_message_label.resize(self.task_message_label.sizeHint())
        self.event_message_label.move(self.label_x_offset, 510)

    def event_start_datetime_label(self):
        self.event_sdatetime_label = QLabel('Alert datetime:', self)
        self.event_sdatetime_label.resize(self.event_sdatetime_label.sizeHint())
        self.event_sdatetime_label.move(self.label_x_offset, 420)

    def event_end_datetime_label(self):
        self.event_edatetime_label = QLabel('End datetime:', self)
        self.event_edatetime_label.resize(self.event_edatetime_label.sizeHint())
        self.event_edatetime_label.move(self.label_x_offset, 450)

    def task_id_line_edit(self):
        self.task_id_line_edit = QLineEdit('id', self)
        self.task_id_line_edit.resize(self.task_id_line_edit.sizeHint())
        self.task_id_line_edit.move(self.horizontal_offset+120, self.vertical_offset-30)

    def event_id_label(self):
        self.event_id_label = QLabel('Enter event id:', self)
        self.event_id_label.resize(self.event_id_label.sizeHint())
        self.event_id_label.move(self.horizontal_offset, 670)

    def event_id_line_edit(self):
        self.event_id_line_edit = QLineEdit('id', self)
        self.event_id_line_edit.resize(self.event_id_line_edit.sizeHint())
        self.event_id_line_edit.move(self.horizontal_offset+120, 670)

    def remove_event_button(self):
        self.remove_event_button = QPushButton('remove_event', self)
        self.remove_event_button.setToolTip('<b>Remove event</b>')
        self.remove_event_button.clicked.connect(self.remove_event_func)
        self.remove_event_button.resize(self.remove_event_button.sizeHint())
        self.remove_event_button.move(self.horizontal_offset+120, 700)

    def remove_task_button(self):
        self.remove_task_button = QPushButton('remove_task', self)
        self.remove_task_button.setToolTip('<b>Remove task</b>')
        self.remove_task_button.clicked.connect(self.remove_task_func)
        self.remove_task_button.resize(self.remove_task_button.sizeHint())
        self.remove_task_button.move(self.horizontal_offset+120, self.vertical_offset)

    def change_priority_button(self):
        self.change_priority_button = QPushButton('change_task_priority', self)
        self.change_priority_button.setToolTip('<b>Change priority</b>')
        self.change_priority_button.clicked.connect(self.change_priority_func)
        self.change_priority_button.resize(self.change_priority_button.sizeHint())
        self.change_priority_button.move(self.horizontal_offset+120, self.vertical_offset+60)

    def change_progress_button(self):
        self.change_progress_button = QPushButton('add_task_progress', self)
        self.change_progress_button.setToolTip('<b>Add progress to the task</b>')
        self.change_progress_button.clicked.connect(self.change_progress_func)
        self.change_progress_button.resize(self.change_progress_button.sizeHint())
        self.change_progress_button.move(self.horizontal_offset+120, self.vertical_offset+30)

    def prepare_geometry(self):
        self.setGeometry(300, 300, 725, 768)
        self.setWindowTitle('Pyganizer!')
        self.setWindowIcon(QIcon('1440359594_document_text_edit.ico')) 

    def add_task_func(self):
        name = self.task_name.text()
        message = self.task_message.text()
        comleteness = self.task_completeness.text()
        priority = self.task_priority.text()

        if name == '' or message == '' or not comleteness.isnumeric() or not priority.isnumeric():
                self.alert("Incorrect input!")
        else:
            comleteness = int(comleteness)
            priority = int(priority)

            current_date = self.task_date_time_edit.date()
            current_time = self.task_date_time_edit.time()
            timezone = self.task_combo_text

            start_date = self.get_arrow_datetime(current_date, current_time, timezone)

            self.pyganizer.add_task(start_date, name, message, comleteness, priority, timezone)
            self.alert("Successfully added the task")

        self.task_priority.setText("") 
        self.task_completeness.setText("")
        self.task_message.setText("")
        self.task_name.setText("")
        self.task_date_time_edit.setDate(QDate(self.now.day, self.now.month, self.now.year))
        self.task_date_time_edit.setTime(QTime(self.now.hour, self.now.minute))

    def add_event_func(self):
        name = self.event_name.text()
        message = self.event_message.text()

        if name == '' or message == '':
                self.alert("Incorrect input!")
        else:
            start_date = self.event_start_date_time_edit.date()
            start_time = self.event_start_date_time_edit.time()
            end_date = self.event_end_date_time_edit.date()
            end_time = self.event_end_date_time_edit.time()
            timezone = self.event_combo_text

            start_datetime = self.get_arrow_datetime(start_date, start_time, timezone)
            end_datetime = self.get_arrow_datetime(end_date, end_time, timezone)     

            try:
                self.pyganizer.add_event(start_datetime, end_datetime, name, message, timezone)
                self.alert("Successfully added the event.")
            except InvalidDateError:
                self.alert("You entered incorrect datetimes.")

        self.event_message.setText("")
        self.event_name.setText("")
        self.event_start_date_time_edit.setDate(QDate(self.now.day, self.now.month, self.now.year))
        self.event_start_date_time_edit.setTime(QTime(self.now.hour, self.now.minute))
        self.event_end_date_time_edit.setDate(QDate(self.now.day, self.now.month, self.now.year))
        self.event_end_date_time_edit.setTime(QTime(self.now.hour, self.now.minute))

    def get_arrow_datetime(self, current_date, current_time, timezone):
        arrow_datetime = arrow.Arrow(current_date.year(), current_date.month(),
                current_date.day(), current_time.hour(),
                current_time.minute(), current_time.second(), tzinfo=timezone)
        # arrow_datetime.to(timezone)
        print(timezone)
        return arrow_datetime

    def load_tasks(self):
        with open("work_files/active_tasks.txt", "r") as f:
            active_tasks = f.readlines()
            self.expose_tasks(active_tasks)

    def expose_tasks(self, lines):
        display_content = ''        
        for line in lines:
            task = Task.decode(line)
            display_content = '{}{}\n'.format(display_content, task)
        self.task_table.setText(display_content)

    def load_events(self):
        with open("work_files/active_events.txt", "r") as f:
            active_events = f.readlines()
            self.expose_events(active_events)

    def expose_events(self, lines):
        display_content = ''        
        for line in lines:
            event = Event.decode(line)
            display_content = '{}{}\n'.format(display_content, event)
        self.event_table.setText(display_content)

    def export_tasks_ical(self):
        self.pyganizer.export_tasks_ical()
        self.alert("Successfully exported to {}".format(self.tasks_ical))

    def export_events_ical(self):
        self.pyganizer.export_events_ical()
        self.alert("Successfully exported to {}".format(self.events_ical))

    def change_progress_func(self):
        progress = self.add_progress_line_edit.text()
        target_id = self.task_id_line_edit.text()

        if not target_id.isnumeric() or not progress.isnumeric():
            self.alert("Incorrect input! Progress should be numeric.")
        else: 
            target_id = int(target_id)
            progress = int(progress)
            result = self.pyganizer.add_task_progress(target_id, progress)
            if not result:
                self.alert("No such id!")
            else:
                self.load_tasks()

        self.task_id_line_edit.setText("")
        self.add_progress_line_edit.setText("")

    def change_priority_func(self):
        priority = self.add_priority_line_edit.text()
        target_id = self.task_id_line_edit.text()

        if not target_id.isnumeric() or not priority.isnumeric():
            self.alert("Incorrect input! Priority should be numeric.")
        else:
            priority = int(priority)
            target_id = int(target_id)
            result = self.pyganizer.set_task_priority(target_id, priority)
            if not result:
                self.alert("No such id!")
            else:
                self.load_tasks()

        self.task_id_line_edit.setText("")
        self.add_priority_line_edit.setText("")

    def remove_task_func(self):
        target_id = self.task_id_line_edit.text()

        if not target_id.isnumeric():
            self.alert("Incorrect input!")
        else:
            target_id = int(target_id)
            result = self.pyganizer.remove_task(target_id)
            self.load_tasks()
            if not result:
                self.alert("No such id!")

        self.task_id_line_edit.setText("")

    def remove_event_func(self):
        target_id = self.event_id_line_edit.text()

        if not target_id.isnumeric():
            self.alert("Incorrect input!")
        else:
            target_id = int(target_id)
            result = self.pyganizer.remove_event(target_id)
            self.load_events()
            if not result:
                self.alert("No such id!")

        self.event_id_line_edit.setText("")

    def alert(self, alert_message):
        QMessageBox.information(self, "Info Box",
                                alert_message)

    def task_combo_label(self):
        self.task_combo_label = QLabel('Timezone:', self)
        self.task_combo_label.resize(self.task_combo_label.sizeHint())
        self.task_combo_label.move(self.label_x_offset, 160)

    def task_combo(self):
        self.task_combo = QComboBox(self)
        self.task_combo.addItem('local')
        self.task_combo.addItem('utc')
        self.task_combo.addItem('US/Pacific')
        self.task_combo.addItem('Europe/Berlin')

        self.task_combo.move(self.horizontal_offset, 160)

        self.task_combo.activated[str].connect(self.onTaskComboActivated)                
        
    def onTaskComboActivated(self, text):
        self.task_combo_text = text

    def event_combo_label(self):
        self.event_combo_label = QLabel('Timezone:', self)
        self.event_combo_label.resize(self.event_combo_label.sizeHint())
        self.event_combo_label.move(self.label_x_offset, 540)

    def event_combo(self):
        self.event_combo = QComboBox(self)
        self.event_combo.addItem('local')
        self.event_combo.addItem('utc')
        self.event_combo.addItem('US/Pacific')
        self.event_combo.addItem('Europe/Berlin')

        self.event_combo.move(self.horizontal_offset, 540)

        self.event_combo.activated[str].connect(self.onEventComboActivated)                
        
    def onEventComboActivated(self, text):
        self.event_combo_text = text

'''
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QMessageBox.Yes | 
            QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.pyganizer.terminate()
            event.accept()
        else: 
            event.ignore()
            # event.ignore()
'''

if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = IconWidget()
    sys.exit(app.exec_())