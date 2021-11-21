import numpy
from generated.context import ContextReference
from generated.formats.dds.bitstruct.Caps1 import Caps1
from generated.formats.dds.bitstruct.Caps2 import Caps2
from generated.formats.dds.bitstruct.HeaderFlags import HeaderFlags
from generated.formats.dds.compound.FixedString import FixedString
from generated.formats.dds.struct.Dxt10Header import Dxt10Header
from generated.formats.dds.struct.PixelFormat import PixelFormat


class Header:

	context = ContextReference()

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# DDS
		self.header_string = FixedString(self.context, 4, None)

		# Always 124 + 4 bytes for headerstring, header ends at 128.
		self.size = 124
		self.flags = HeaderFlags(self.context, 0, None)

		# The texture height.
		self.height = 0

		# The texture width.
		self.width = 0
		self.linear_size = 0
		self.depth = 0
		self.mipmap_count = 0
		self.reserved_1 = numpy.zeros((11,), dtype=numpy.dtype('uint32'))
		self.pixel_format = PixelFormat(self.context, 0, None)
		self.caps_1 = Caps1(self.context, 0, None)
		self.caps_2 = Caps2(self.context, 0, None)
		self.caps_3 = 0
		self.caps_4 = 0
		self.unused = 0
		self.dx_10 = Dxt10Header(self.context, 0, None)
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.header_string = FixedString(self.context, 4, None)
		self.size = 124
		self.flags = HeaderFlags(self.context, 0, None)
		self.height = 0
		self.width = 0
		self.linear_size = 0
		self.depth = 0
		self.mipmap_count = 0
		self.reserved_1 = numpy.zeros((11,), dtype=numpy.dtype('uint32'))
		self.pixel_format = PixelFormat(self.context, 0, None)
		self.caps_1 = Caps1(self.context, 0, None)
		self.caps_2 = Caps2(self.context, 0, None)
		self.caps_3 = 0
		self.caps_4 = 0
		self.unused = 0
		if self.pixel_format.four_c_c == 808540228:
			self.dx_10 = Dxt10Header(self.context, 0, None)

	def read(self, stream):
		self.io_start = stream.tell()
		self.read_fields(stream, self)
		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		self.write_fields(stream, self)
		self.io_size = stream.tell() - self.io_start

	@classmethod
	def read_fields(cls, stream, instance):
		instance.header_string = FixedString.from_stream(stream, instance.context, 4, None)
		instance.size = stream.read_uint()
		instance.flags = HeaderFlags.from_stream(stream, instance.context, 0, None)
		instance.height = stream.read_uint()
		instance.width = stream.read_uint()
		instance.linear_size = stream.read_uint()
		instance.depth = stream.read_uint()
		instance.mipmap_count = stream.read_uint()
		instance.reserved_1 = stream.read_uints((11,))
		instance.pixel_format = PixelFormat.from_stream(stream, instance.context, 0, None)
		instance.caps_1 = Caps1.from_stream(stream, instance.context, 0, None)
		instance.caps_2 = Caps2.from_stream(stream, instance.context, 0, None)
		instance.caps_3 = stream.read_uint()
		instance.caps_4 = stream.read_uint()
		instance.unused = stream.read_uint()
		if instance.pixel_format.four_c_c == 808540228:
			instance.dx_10 = Dxt10Header.from_stream(stream, instance.context, 0, None)

	@classmethod
	def write_fields(cls, stream, instance):
		FixedString.to_stream(stream, instance.header_string)
		stream.write_uint(instance.size)
		HeaderFlags.to_stream(stream, instance.flags)
		stream.write_uint(instance.height)
		stream.write_uint(instance.width)
		stream.write_uint(instance.linear_size)
		stream.write_uint(instance.depth)
		stream.write_uint(instance.mipmap_count)
		stream.write_uints(instance.reserved_1)
		PixelFormat.to_stream(stream, instance.pixel_format)
		Caps1.to_stream(stream, instance.caps_1)
		Caps2.to_stream(stream, instance.caps_2)
		stream.write_uint(instance.caps_3)
		stream.write_uint(instance.caps_4)
		stream.write_uint(instance.unused)
		if instance.pixel_format.four_c_c == 808540228:
			Dxt10Header.to_stream(stream, instance.dx_10)

	@classmethod
	def from_stream(cls, stream, context, arg=0, template=None):
		instance = cls(context, arg, template, set_default=False)
		instance.io_start = stream.tell()
		cls.read_fields(stream, instance)
		instance.io_size = stream.tell() - instance.io_start
		return instance

	@classmethod
	def to_stream(cls, stream, instance):
		instance.io_start = stream.tell()
		cls.write_fields(stream, instance)
		instance.io_size = stream.tell() - instance.io_start
		return instance

	def get_info_str(self):
		return f'Header [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* header_string = {self.header_string.__repr__()}'
		s += f'\n	* size = {self.size.__repr__()}'
		s += f'\n	* flags = {self.flags.__repr__()}'
		s += f'\n	* height = {self.height.__repr__()}'
		s += f'\n	* width = {self.width.__repr__()}'
		s += f'\n	* linear_size = {self.linear_size.__repr__()}'
		s += f'\n	* depth = {self.depth.__repr__()}'
		s += f'\n	* mipmap_count = {self.mipmap_count.__repr__()}'
		s += f'\n	* reserved_1 = {self.reserved_1.__repr__()}'
		s += f'\n	* pixel_format = {self.pixel_format.__repr__()}'
		s += f'\n	* caps_1 = {self.caps_1.__repr__()}'
		s += f'\n	* caps_2 = {self.caps_2.__repr__()}'
		s += f'\n	* caps_3 = {self.caps_3.__repr__()}'
		s += f'\n	* caps_4 = {self.caps_4.__repr__()}'
		s += f'\n	* unused = {self.unused.__repr__()}'
		s += f'\n	* dx_10 = {self.dx_10.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
