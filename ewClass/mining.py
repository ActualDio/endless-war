

class EwMineGrid:
	grid_type = ""
	
	grid = []

	message = ""
	wall_message = ""

	times_edited = 0

	time_last_posted = 0

	cells_mined = 0

	def __init__(self, grid = [], grid_type = ""):
		self.grid = grid
		self.grid_type = grid_type
		self.message = ""
		self.wall_message = ""
		self.times_edited = 0
		self.time_last_posted = 0
		self.cells_mined = 0
