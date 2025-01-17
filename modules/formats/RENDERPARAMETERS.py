import logging
import struct

from modules.formats.BaseFormat import BaseFile

"""
        RenderParameterType_Bool = 0,
        RenderParameterType_Float = 1,
        RenderParameterType_Int = 2,
        RenderParameterType_UInt = 3,
        RenderParameterType_Vector2 = 4,
        RenderParameterType_Vector3 = 5,
        RenderParameterType_Vector4 = 6,
        RenderParameterType_Colour = 7,
        RenderParameterType_ColourHDR = 8,
        RenderParameterType_String = 9,
"""        


class RenderParametersLoader(BaseFile):

    def create(self):
        #ss, buffer_0 = self._get_data(self.file_entry.path)
        #self.sized_str_entry = self.create_ss_entry(self.file_entry)
        #self.write_to_pool(self.sized_str_entry.pointers[0], 4, ss)
        #self.create_data_entry(self.sized_str_entry, (buffer_0,))
        pass

    def load(self, file_path):
        #ss, buffer_0 = self._get_data(file_path)
        #self.sized_str_entry.data_entry.update_data((buffer_0,))
        #self.sized_str_entry.pointers[0].update_data(ss, update_copies=True)
        pass

    def collect(self):
        self.assign_ss_entry()
        print(f"Collecting {self.sized_str_entry.name}")
        # offset  x0: ptr to string
        # offset  x8: ptr to list of ptrs to data entries
        # offset x10: count of data entries
        # offset x14: not used? (count could be int64)
        # offset x18: not used? padding?
        # offset x1c: not used? padding?
        ss_ptr = self.sized_str_entry.pointers[0]
        _,_,count,_ = struct.unpack("<4Q", ss_ptr.data)
        self.sized_str_entry.count = count

        self.sized_str_entry.curve_name = self.get_str_at_offset(0)
        print(f"rpc : {count} : {self.sized_str_entry.curve_name}")

        if count:
            list_frag = self.ovs.frag_at_pointer(self.sized_str_entry.pointers[0], offset=8)
            tmp_fragments = self.ovs.frags_from_pointer(list_frag.pointers[1], count)
            for frag in tmp_fragments:
                # frag is a ptr to the entry data
                entry_fragment = self.ovs.frag_at_pointer(frag.pointers[0], offset=0)
                # data entries:
                # offset  x0: strz attribute name (Atmospherics.Lights.IrradianceScatterIntensity, ...)
                # offset  x8: int  dtype1   (1, 3, 5, 7...)
                # offset  xc: int  dtype2   unused (probably type is int64)
                # offset x10: float/int (with dtype1 == 3 this type might be int)
                # offset x14: float/int 
                # offset x18: float/int (could be min, max or def)
                # offset x1c: float?  (probaby unused, padding?)
                _,dtype1,dtype2,ffloat1, ffloat2,fdefault1, fdefault2 = struct.unpack("<QIIffff", entry_fragment.pointers[1].data)
                print(f"dtype1 {dtype1} dtype2 {dtype2} ffloat1: {ffloat1} ffloat2: {ffloat2} fdefault1: {fdefault1} fdefault2: {fdefault2}")

                attrib_name = self.ovs.frag_at_pointer(entry_fragment.pointers[1], offset=0)
                if attrib_name:
                    name = self.p1_ztsr(attrib_name)
                    print(f"attrib: {name}")

        pass



    def extract(self, out_dir, show_temp_files, progress_callback):
        #name = self.sized_str_entry.name
        #logging.info(f"Writing {name}")
        #out_path = out_dir(name)
        #buffers = self.sized_str_entry.data_entry.buffer_datas
        #with open(out_path, 'wb') as outfile:
        #    for buff in buffers:
        #        outfile.write(buff)
        #return [out_path]
        pass

    def _get_data(self, file_path):
        """Loads and returns the data for a GFX"""
        #buffer_0 = self.get_content(file_path)
        #ss = struct.pack("<QQQQ", 0, len(buffer_0), 0, 0)
        #return ss, buffer_0
        pass
