from generated.context import ContextReference


class ByteColor4:

	"""
	A color with alpha (red, green, blue, alpha).
	"""

	context = ContextReference()

	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# Red color component.
		self.r = 0

		# Green color component.
		self.g = 0

		# Blue color component.
		self.b = 0

		# Alpha color component.
		self.a = 0
		if set_default:
			self.set_defaults()

	def set_defaults(self):
		self.r = 0
		self.g = 0
		self.b = 0
		self.a = 0

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
		instance.r = stream.read_ubyte()
		instance.g = stream.read_ubyte()
		instance.b = stream.read_ubyte()
		instance.a = stream.read_ubyte()

	@classmethod
	def write_fields(cls, stream, instance):
		stream.write_ubyte(instance.r)
		stream.write_ubyte(instance.g)
		stream.write_ubyte(instance.b)
		stream.write_ubyte(instance.a)

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
		return f'ByteColor4 [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* r = {self.r.__repr__()}'
		s += f'\n	* g = {self.g.__repr__()}'
		s += f'\n	* b = {self.b.__repr__()}'
		s += f'\n	* a = {self.a.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
