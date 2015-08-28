import sys

class FileWorker():
	def __init__(self, general_file, events_file, tasks_file):
		self.general = general_file
        self.events = events_file
        self.tasks = tasks_file