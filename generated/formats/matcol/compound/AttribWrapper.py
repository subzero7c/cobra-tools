from generated.context import ContextReference
from generated.formats.matcol.compound.Attrib import Attrib


class AttribWrapper:

	context = ContextReference()

	def __init__(self, context, arg=None, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.attrib = Attrib(self.context, None, None)
		self.name = ''
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.attrib = Attrib(self.context, None, None)
		self.name = ''

	def read(self, stream):
		self.io_start = stream.tell()
		self.attrib = stream.read_type(Attrib, (self.context, None, None))
		self.name = stream.read_zstring()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		stream.write_type(self.attrib)
		stream.write_zstring(self.name)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'AttribWrapper [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* attrib = {self.attrib.__repr__()}'
		s += f'\n	* name = {self.name.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
