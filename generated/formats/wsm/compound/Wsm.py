import numpy
import typing
from generated.array import Array
from generated.formats.ovl_base.compound.GenericHeader import GenericHeader
from generated.formats.wsm.compound.WsmHeader import WsmHeader


class Wsm(GenericHeader):

	def __init__(self, context, arg=None, template=None):
		self.name = ''
		super().__init__(context, arg, template)
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.header = WsmHeader(self.context, None, None)

		# xyz
		self.locs = numpy.zeros((self.header.frame_count, 3), dtype='float')

		# xyzw
		self.quats = numpy.zeros((self.header.frame_count, 4), dtype='float')
		self.set_defaults()

	def set_defaults(self):
		self.header = WsmHeader(self.context, None, None)
		self.locs = numpy.zeros((self.header.frame_count, 3), dtype='float')
		self.quats = numpy.zeros((self.header.frame_count, 4), dtype='float')

	def read(self, stream):
		self.io_start = stream.tell()
		super().read(stream)
		self.header = stream.read_type(WsmHeader, (self.context, None, None))
		self.locs = stream.read_floats((self.header.frame_count, 3))
		self.quats = stream.read_floats((self.header.frame_count, 4))

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		super().write(stream)
		stream.write_type(self.header)
		stream.write_floats(self.locs)
		stream.write_floats(self.quats)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'Wsm [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += super().get_fields_str()
		s += f'\n	* header = {self.header.__repr__()}'
		s += f'\n	* locs = {self.locs.__repr__()}'
		s += f'\n	* quats = {self.quats.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
