
class PyganizerError(Exception):
	def __init__(self):
		self.message = "PyganizerError"

class TodoNameExistsError(PyganizerError):
	def __init__(self):
		super().__init__()
		self.message = "TodoNameExistsError"

class InvalidDateError(PyganizerError):
    def __init__(self):
        super().__init__()
        self.message = "InvalidDateError"