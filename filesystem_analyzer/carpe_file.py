from __future__ import print_function
import sys
import re
import pdb
class Carpe_File(object):
	def __init__(self):
		super(Carpe_File, self).__init__()
		self._id = 0
		self._p_id = ""
		#self._attr_type = 0
		#self._attr_id = 0
		self._inode = ""
		self._name = ""
		self._file_id = 0
		self._meta_seq = 0
		self._type = 0
		self._dir_type = 0
		self._meta_type = 0
		self._meta_flags = 0
		self._size = 0
		self._mtime = 0
		self._atime = 0
		self._ctime = 0
		self._etime = 0
		self._mtime_nano = 0
		self._atime_nano = 0
		self._ctime_nano = 0
		self._etime_nano = 0
		self._additional_mtime = 0
		self._additional_atime = 0
		self._additional_ctime = 0
		self._additional_etime = 0		
		self._additional_mtime_nano = 0
		self._additional_atime_nano = 0
		self._additional_ctime_nano = 0
		self._additional_etime_nano = 0
		self._mode = 0
		self._uid = 0
		self._gid = 0
		self._md5 = ""
		self._sha1 = ""
		self._sha3 = ""
		self._parent_path = ""
		self._parent_id = 0
		self._extension = ""
		self._bookmark = False

	def toTuple(self):
		var_list = sorted([x for x in dir(self) if (re.match(r'(^[_][a-z])', x))])
		temp = self.__dict__
		ret = []
		for i in var_list:
			if(type(temp[i]) is int):
				ret.append(int(str(temp[i]).rstrip("L")))
			else :
				ret.append(temp[i])
		return tuple(ret)
