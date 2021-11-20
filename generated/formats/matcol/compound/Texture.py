from generated.context import ContextReference


class Texture:

	"""
	each texture = three fragments of format: data0 = 8 bytes zeros | data1 = null terminating string (scale texture name)
	"""

	context = ContextReference()

	def __init__(self, context, arg=None, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0
		self.fgm_name = ''
		self.texture_suffix = ''
		self.texture_type = ''
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.fgm_name = ''
		self.texture_suffix = ''
		self.texture_type = ''

	def read(self, stream):
		self.io_start = stream.tell()
		self.fgm_name = stream.read_zstring()
		self.texture_suffix = stream.read_zstring()
		self.texture_type = stream.read_zstring()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):
		self.io_start = stream.tell()
		stream.write_zstring(self.fgm_name)
		stream.write_zstring(self.texture_suffix)
		stream.write_zstring(self.texture_type)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'Texture [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* fgm_name = {self.fgm_name.__repr__()}'
		s += f'\n	* texture_suffix = {self.texture_suffix.__repr__()}'
		s += f'\n	* texture_type = {self.texture_type.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
