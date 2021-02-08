import typing
from generated.array import Array


class ZTPreBones:

	def __init__(self, arg=None, template=None):
		self.name = ''
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.zeros = Array()
		self.unks = Array()
		self.zeros_3 = Array()
		self.unks_2 = Array()
		self.floats = Array()
		self.unks_3 = Array()

	def read(self, stream):

		self.io_start = stream.tell()
		self.zeros = stream.read_uint64s((2))
		self.unks = stream.read_uints((4))
		self.zeros_3 = stream.read_uint64s((2))
		self.unks_2 = stream.read_uints((10))
		self.floats = stream.read_floats((4))
		self.unks_3 = stream.read_uints((2))

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uint64s(self.zeros)
		stream.write_uints(self.unks)
		stream.write_uint64s(self.zeros_3)
		stream.write_uints(self.unks_2)
		stream.write_floats(self.floats)
		stream.write_uints(self.unks_3)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'ZTPreBones [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* zeros = {self.zeros.__repr__()}'
		s += f'\n	* unks = {self.unks.__repr__()}'
		s += f'\n	* zeros_3 = {self.zeros_3.__repr__()}'
		s += f'\n	* unks_2 = {self.unks_2.__repr__()}'
		s += f'\n	* floats = {self.floats.__repr__()}'
		s += f'\n	* unks_3 = {self.unks_3.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s