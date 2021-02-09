import typing
from generated.array import Array
from generated.formats.ms2.compound.LodInfo import LodInfo
from generated.formats.ms2.compound.LodInfoZT import LodInfoZT
from generated.formats.ms2.compound.Material0 import Material0
from generated.formats.ms2.compound.Material1 import Material1
from generated.formats.ms2.compound.PcModelData import PcModelData
from generated.formats.ms2.compound.ZTPreBones import ZTPreBones
from generated.formats.ms2.compound.ZtModelData import ZtModelData


class PcModel:

	def __init__(self, arg=None, template=None):
		self.name = ''
		self.arg = arg
		self.template = template
		self.io_size = 0
		self.io_start = 0

		# uses uint here, two uints elsewhere
		self.materials_0 = Array()
		self.lod_infos = Array()
		self.lod_infos = Array()
		self.materials_1 = Array()
		self.model_data = Array()
		self.model_data = Array()
		self.ztuac_pre_bones = ZTPreBones()

	def read(self, stream):

		self.io_start = stream.tell()
		self.materials_0.read(stream, Material0, self.arg.mat_count, None)
		if stream.version == 17:
			self.lod_infos.read(stream, LodInfoZT, self.arg.lod_count, None)
		if stream.version == 18:
			self.lod_infos.read(stream, LodInfo, self.arg.lod_count, None)
		self.materials_1.read(stream, Material1, self.arg.mat_1_count, None)
		if stream.version == 18:
			self.model_data.read(stream, PcModelData, self.arg.model_count, None)
		if stream.version == 17:
			self.model_data.read(stream, ZtModelData, self.arg.model_count, None)
			self.ztuac_pre_bones = stream.read_type(ZTPreBones)

		self.io_size = stream.tell() - self.io_start

	def write(self, stream):

		self.io_start = stream.tell()
		self.materials_0.write(stream, Material0, self.arg.mat_count, None)
		if stream.version == 17:
			self.lod_infos.write(stream, LodInfoZT, self.arg.lod_count, None)
		if stream.version == 18:
			self.lod_infos.write(stream, LodInfo, self.arg.lod_count, None)
		self.materials_1.write(stream, Material1, self.arg.mat_1_count, None)
		if stream.version == 18:
			self.model_data.write(stream, PcModelData, self.arg.model_count, None)
		if stream.version == 17:
			self.model_data.write(stream, ZtModelData, self.arg.model_count, None)
			stream.write_type(self.ztuac_pre_bones)

		self.io_size = stream.tell() - self.io_start

	def get_info_str(self):
		return f'PcModel [Size: {self.io_size}, Address: {self.io_start}] {self.name}'

	def get_fields_str(self):
		s = ''
		s += f'\n	* materials_0 = {self.materials_0.__repr__()}'
		s += f'\n	* lod_infos = {self.lod_infos.__repr__()}'
		s += f'\n	* materials_1 = {self.materials_1.__repr__()}'
		s += f'\n	* model_data = {self.model_data.__repr__()}'
		s += f'\n	* ztuac_pre_bones = {self.ztuac_pre_bones.__repr__()}'
		return s

	def __repr__(self):
		s = self.get_info_str()
		s += self.get_fields_str()
		s += '\n'
		return s
