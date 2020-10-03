class MotionGraphVarsStrData:

	"""
	per attribute
	"""

	# 4 in driver
	unknown_0: int

	# 0 in driver
	unknown_1: int

	def __init__(self, arg=None, template=None):
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.unknown_0 = 0
		self.unknown_1 = 0

	def read(self, stream):

		io_start = stream.tell()
		self.unknown_0 = stream.read_uint()
		self.unknown_1 = stream.read_uint()

		self.io_size = stream.tell() - io_start

	def write(self, stream):

		io_start = stream.tell()
		stream.write_uint(self.unknown_0)
		stream.write_uint(self.unknown_1)

		self.io_size = stream.tell() - io_start

	def __repr__(self):
		s = 'MotionGraphVarsStrData [Size: '+str(self.io_size)+']'
		s += '\n	* unknown_0 = ' + self.unknown_0.__repr__()
		s += '\n	* unknown_1 = ' + self.unknown_1.__repr__()
		s += '\n'
		return s