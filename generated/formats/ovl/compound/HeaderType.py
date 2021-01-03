class HeaderType:

	"""
	Located at start of deflated archive stream
	"""

	def __init__(self, arg=None, template=None):
		self.name = ''
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# Type of the headers that follow
		self.type = 0

		# Amount of the headers of that type that follow the headers block
		self.num_headers = 0

	def read(self, stream):

		self.io_start = stream.tell()
		self.type = stream.read_ushort()
		self.num_headers = stream.read_ushort()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_ushort(self.type)
		stream.write_ushort(self.num_headers)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'HeaderType [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* type = {self.type.__repr__()}'
		s += f'\n	* num_headers = {self.num_headers.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
