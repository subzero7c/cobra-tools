
import struct
import math
import numpy as np
from generated.formats.ms2.compound.packing_utils import *
from utils.tristrip import triangulate
import typing
from generated.array import Array
from generated.formats.ms2.bitfield.ModelFlag import ModelFlag


class ZtModelData:

	"""
	Defines one model's data. Both LODs and mdl2 files may contain several of these.
	This is a fragment from headers of type (0,0)
	If there is more than one of these, the fragments appear as a list according to
	"""

	def __init__(self, arg=None, template=None):
		self.name = ''
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# index into streamed buffers
		self.stream_index = 0

		# always zero
		self.zeros_a = Array()

		# repeat
		self.tri_index_count = 0

		# vertex count of model
		self.vertex_count = 0

		# stores count, -1 as ints
		self.tri_info_offset = 0

		# stores count, -1 as ints
		self.vert_info_offset = 0

		# x*16 = offset in buffer 2
		self.known_ff_0 = 0

		# relative to start of buffer[i]'s tris section start, blocks of 2 bytes (ushort), tri index count
		self.tri_offset = 0

		# relative to start of buffer[i], blocks of 8 bytes, count vertex_count
		self.uv_offset = 0

		# relative to start of buffer[i], blocks of 24 bytes, count vertex_count
		self.vert_offset = 0

		# x*16 = offset in buffer 2
		self.known_ff_1 = 0

		# x*16 = offset in buffer 2
		self.one_0 = 0

		# ?
		self.one_1 = 0

		# ?
		self.poweroftwo = 0

		# power of 2 increasing with lod index
		self.poweroftwo = 0

		# always zero
		self.zero = 0

		# some floats
		self.unknown_07 = 0

		# bitfield
		self.flag = ModelFlag()

		# always zero
		self.zero_uac = 0

	def read(self, stream):

		self.io_start = stream.tell()
		self.stream_index = stream.read_uint()
		self.zeros_a = stream.read_uints((3))
		self.tri_index_count = stream.read_uint()
		self.vertex_count = stream.read_uint()
		self.tri_info_offset = stream.read_uint()
		self.vert_info_offset = stream.read_uint()
		self.known_ff_0 = stream.read_int()
		self.tri_offset = stream.read_uint()
		self.uv_offset = stream.read_uint()
		self.vert_offset = stream.read_uint()
		self.known_ff_1 = stream.read_short()
		self.one_0 = stream.read_ushort()
		self.one_1 = stream.read_ushort()
		if stream.version == 17:
			self.poweroftwo = stream.read_ushort()
		if stream.version == 18:
			self.poweroftwo = stream.read_uint()
			self.zero = stream.read_uint()
			self.unknown_07 = stream.read_float()
		self.flag = stream.read_type(ModelFlag)
		if stream.version == 17:
			self.zero_uac = stream.read_uint()

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		stream.write_uint(self.stream_index)
		stream.write_uints(self.zeros_a)
		stream.write_uint(self.tri_index_count)
		stream.write_uint(self.vertex_count)
		stream.write_uint(self.tri_info_offset)
		stream.write_uint(self.vert_info_offset)
		stream.write_int(self.known_ff_0)
		stream.write_uint(self.tri_offset)
		stream.write_uint(self.uv_offset)
		stream.write_uint(self.vert_offset)
		stream.write_short(self.known_ff_1)
		stream.write_ushort(self.one_0)
		stream.write_ushort(self.one_1)
		if stream.version == 17:
			stream.write_ushort(self.poweroftwo)
		if stream.version == 18:
			stream.write_uint(self.poweroftwo)
			stream.write_uint(self.zero)
			stream.write_float(self.unknown_07)
		stream.write_type(self.flag)
		if stream.version == 17:
			stream.write_uint(self.zero_uac)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'ZtModelData [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* stream_index = {self.stream_index.__repr__()}'
		s += f'\n	* zeros_a = {self.zeros_a.__repr__()}'
		s += f'\n	* tri_index_count = {self.tri_index_count.__repr__()}'
		s += f'\n	* vertex_count = {self.vertex_count.__repr__()}'
		s += f'\n	* tri_info_offset = {self.tri_info_offset.__repr__()}'
		s += f'\n	* vert_info_offset = {self.vert_info_offset.__repr__()}'
		s += f'\n	* known_ff_0 = {self.known_ff_0.__repr__()}'
		s += f'\n	* tri_offset = {self.tri_offset.__repr__()}'
		s += f'\n	* uv_offset = {self.uv_offset.__repr__()}'
		s += f'\n	* vert_offset = {self.vert_offset.__repr__()}'
		s += f'\n	* known_ff_1 = {self.known_ff_1.__repr__()}'
		s += f'\n	* one_0 = {self.one_0.__repr__()}'
		s += f'\n	* one_1 = {self.one_1.__repr__()}'
		s += f'\n	* poweroftwo = {self.poweroftwo.__repr__()}'
		s += f'\n	* zero = {self.zero.__repr__()}'
		s += f'\n	* unknown_07 = {self.unknown_07.__repr__()}'
		s += f'\n	* flag = {self.flag.__repr__()}'
		s += f'\n	* zero_uac = {self.zero_uac.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s

	def populate(self, ms2_file, ms2_stream, start_buffer2, bone_names=[], base=512):
		self.streams = ms2_file.pc_buffer1.buffer_info_pc.streams
		self.stream_info = self.streams[self.stream_index]
		self.stream_offset = 0
		for s in self.streams[:self.stream_index]:
			self.stream_offset += s.vertex_buffer_length + s.tris_buffer_length + s.next_buffer_length
		self.start_buffer2 = start_buffer2
		self.ms2_file = ms2_file
		self.base = base
		self.bone_names = bone_names
		self.read_verts(ms2_stream)
		self.read_tris(ms2_stream)

	def init_arrays(self, count):
		self.vertex_count = count
		self.vertices = np.empty((self.vertex_count, 3), np.float32)
		self.normals = np.empty((self.vertex_count, 3), np.float32)
		self.tangents = np.empty((self.vertex_count, 3), np.float32)
		try:
			uv_shape = self.dt_uv["uvs"].shape
			self.uvs = np.empty((self.vertex_count, *uv_shape), np.float32)
		except:
			self.uvs = None
		try:
			colors_shape = self.dt["colors"].shape
			self.colors = np.empty((self.vertex_count, *colors_shape), np.float32)
		except:
			self.colors = None
		self.weights = []

	def update_dtype(self):
		"""Update ModelData.dt (numpy dtype) according to ModelData.flag"""
		# basic shared stuff
		dt = [
			# ("pos", np.uint64),
			# ("normal", np.ubyte, (3,)),
			# ("unk", np.ubyte),
			# ("tangent", np.ubyte, (3,)),
			# ("bone index", np.ubyte),

			# ("bones", np.uint64),
			("bone ids", np.ubyte, (4,)),
			("bone weights", np.ubyte, (4,)),
			("pos", np.float16, (3,)),
			("unk", np.ushort, (5,)),
			# ("bone index", np.ubyte),
		]
		dt_uv = [
			("uvs", np.ushort, (1, 2)),
		]
		# bone weights
		# if self.flag in (529, 533, 885, 565, 1013, 528, 821):
		dt_w = [
			("bone ids", np.ubyte, (4,)),
			("bone weights", np.ubyte, (4,)),
		]
		self.dt = np.dtype(dt)
		self.dt_uv = np.dtype(dt_uv)
		self.dt_w = np.dtype(dt_w)
		print("PC size of vertex:", self.dt.itemsize)
		print("PC size of uv:", self.dt_uv.itemsize)
		print("PC size of weights:", self.dt_w.itemsize)

	def read_tris(self, stream):
		# read all tri indices for this model
		stream.seek(self.start_buffer2 + self.stream_offset + self.stream_info.vertex_buffer_length + self.tri_offset)
		print("tris offset", stream.tell())
		# read all tri indices for this model segment
		self.tri_indices = list(struct.unpack(str(self.tri_index_count) + "H", stream.read(self.tri_index_count * 2)))
		print(self.tri_indices)

	@property
	def tris(self, ):
		# tri strip
		return triangulate((self.tri_indices,))

	def read_verts(self, stream):
		# get dtype according to which the vertices are packed
		self.update_dtype()
		# create arrays for the unpacked ms2_file
		self.init_arrays(self.vertex_count)
		# read a vertices of this model
		stream.seek(self.start_buffer2 + self.stream_offset + self.vert_offset)
		print("VERTS", stream.tell())
		self.verts_data = np.fromfile(stream, dtype=self.dt, count=self.vertex_count)
		stream.seek(self.start_buffer2 + self.stream_offset + self.stream_info.vertex_buffer_length + self.stream_info.tris_buffer_length + self.uv_offset)
		print("UV", stream.tell())
		# self.uv_data = np.fromfile(stream, dtype=self.dt_uv, count=self.vertex_count)
		# stream.seek(self.start_buffer2 + (self.weights_offset * 16))
		# print("WEIGHtS", stream.tell())
		# self.weights_data = np.fromfile(stream, dtype=self.dt_w, count=self.vertex_count)
		# # print(self.verts_data)
		# # first cast to the float uvs array so unpacking doesn't use int division
		# if self.uvs is not None:
		# 	self.uvs[:] = self.uv_data[:]["uvs"]
		# 	# unpack uvs
		# 	self.uvs = (self.uvs - 32768) / 2048
		# if self.colors is not None:
		# 	# first cast to the float colors array so unpacking doesn't use int division
		# 	self.colors[:] = self.verts_data[:]["colors"]
		# 	self.colors /= 255
		# self.normals[:] = self.verts_data[:]["normal"]
		# self.tangents[:] = self.verts_data[:]["tangent"]
		self.vertices[:] = self.verts_data[:]["pos"]
		# self.normals = (self.normals - 128) / 128
		# self.tangents = (self.tangents - 128) / 128
		for i in range(self.vertex_count):
		# 	in_pos_packed = self.verts_data[i]["pos"]
		# 	vert, residue = unpack_longint_vec(in_pos_packed, self.base)
			self.vertices[i] = unpack_swizzle(self.vertices[i])
		# 	self.normals[i] = unpack_swizzle(self.normals[i])
		# 	self.tangents[i] = unpack_swizzle(self.tangents[i])
			self.weights.append(unpack_weights(self, i, 0, extra=False))
		# print(self.verts_data)
		# print(self.vertices)
		# print(self.weights)

	@staticmethod
	def get_weights(bone_ids, bone_weights):
		return [(i, w / 255) for i, w in zip(bone_ids, bone_weights) if w > 0]

	@property
	def lod_index(self, ):
		try:
			lod_i = int(math.log2(self.poweroftwo))
		except:
			lod_i = 0
			print("EXCEPTION: math domain for lod", self.poweroftwo)
		return lod_i

	@lod_index.setter
	def lod_index(self, lod_i):
		self.poweroftwo = int(math.pow(2, lod_i))
