
import io
from generated.io import BinaryStream
from modules.formats.shared import assign_versions, get_padding


from generated.context import ContextReference


class HeaderPointer:

	"""
	Not standalone, used by SizedStringEntry, Fragment and DependencyEntry
	8 bytes
	"""

	context = ContextReference()

	def set_defaults(self):
		self.pool_index = 0
		self.data_offset = 0

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
		instance.pool_index = stream.read_int()
		instance.data_offset = stream.read_uint()

	@classmethod
	def write_fields(cls, stream, instance):
		stream.write_int(instance.pool_index)
		stream.write_uint(instance.data_offset)

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
		return f'HeaderPointer [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* pool_index = {self.pool_index.__repr__()}'
		s += f'\n	* data_offset = {self.data_offset.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s


	def __init__(self, context, arg=0, template=None, set_default=True):
		self.name = ''
		self._context = context
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# The index of the MemPool this one relates to; OR, for entries referred to from AssetEntries: -1 (FF FF FF FF)
		self.pool_index = 0

		# the byte offset relative to the start of the header entry data
		self.data_offset = 0

		# define this already
		self.padding = b""
		self.pool = None

	def read_data(self):
		"""Load data from archive header data readers into pointer for modification and io"""
		if self.pool_index == -1:
			self.data = None
		else:
			self.data = self.read_from_pool(self.data_size)

	def read_from_pool(self, data_size):
		self.pool.data.seek(self.data_offset)
		return self.pool.data.read(data_size)

	def write_data(self, update_copies=False):
		"""Write data to header data, update offset, also for copies if told"""

		if self.pool_index != -1:
			# update data offset
			self.data_offset = self.pool.data.tell()
			if update_copies:
				for other_pointer in self.copies:
					other_pointer.data_offset = self.pool.data.tell()
			# write data to io, adjusting the cursor for that header
			self.pool.data.write(self.data + self.padding)

	def strip_zstring_padding(self):
		"""Move surplus padding into the padding attribute"""
		# the actual zstring content + end byte
		data = self.data.split(b"\x00")[0] + b"\x00"
		# do the split itself
		self.split_data_padding(len(data))

	def split_data_padding(self, cut):
		"""Move a fixed surplus padding into the padding attribute"""
		_d = self.data + self.padding
		self.padding = _d[cut:]
		self.data = _d[:cut]

	def link_to_pool(self, pools):
		"""Link this pointer to its pool"""

		if self.pool_index != -1:
			# get pool
			self.pool = pools[self.pool_index]
			if self.data_offset not in self.pool.pointer_map:
				self.pool.pointer_map[self.data_offset] = []
			self.pool.pointer_map[self.data_offset].append(self)

	def update_pool_index(self, pools_lut):
		"""Changes self.pool_index according to self.pool in pools_lut"""

		if self.pool:
			self.pool_index = pools_lut[self.pool]
		else:
			self.pool_index = -1

	def update_data(self, data, update_copies=False, pad_to=None, include_old_pad=False):
		"""Update data and size of this pointer"""
		self.data = data
		# only change padding if a new alignment is given
		if pad_to:
			len_d = len(data)
			# consider the old padding for alignment?
			if include_old_pad:
				len_d += len(self.padding)
			new_pad = get_padding(len_d, pad_to)
			# append new to the old padding
			if include_old_pad:
				self.padding = self.padding + new_pad
			# overwrite the old padding
			else:
				self.padding = new_pad
		self.data_size = len(self.data + self.padding)
		# update other pointers if asked to by the injector
		if update_copies and self.pool_index != -1:
			for other_pointer in self.copies:
				if other_pointer is not self:
					other_pointer.update_data(data, pad_to=pad_to, include_old_pad=include_old_pad)

	def load_as(self, cls, num=1, version_info={}, args=()):
		"""Return self.data as codegen cls
		version_info must be a dict that has version & user_version attributes"""
		with BinaryStream(self.data) as stream:
			assign_versions(stream, version_info)
			insts = []
			for i in range(num):
				inst = cls(self.context, *args)
				inst.read(stream)
				insts.append(inst)
		return insts

	def remove(self, archive):
		"""Remove this pointer from suitable header entry"""

		if self.pool_index == -1:
			pass
		else:
			# get header entry
			entry = archive.pools[self.pool_index]
			if self.data_offset in entry.pointer_map:
				entry.pointer_map.pop(self.data_offset)

	def __eq__(self, other):
		if isinstance(other, HeaderPointer):
			return self.data_offset == other.data_offset and self.pool_index == other.pool_index


