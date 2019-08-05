from defines         import *
from interface       import ModuleComponentInterface

import os,sys
import signal
import argparse
import importlib

# @Gibartes

class Actuator(object):
    def __init__(self):
        self.id = ModuleID.ACTUATOR
        self.init()

    def __del__(self):
        self.clear()

    def __str__(self):
        return (ModuleID.ACTUATOR,
                "Module Component {0}".format(self.__class__.__name__))

    # <--------------------------------
    # @ Module Executor
    def open(self,key,id,value):
        obj = self.__objectTbl.get(key)
        if(obj==None):
            return False
        return obj.module_open(id,value)

    def close(self,key,id,value):
        obj = self.__objectTbl.get(key)
        if(obj==None):
            return False
        return obj.module_close(id)

    # Get (a) module parameter(s)
    def get(self,key,attr):
        obj = self.__objectTbl.get(key)
        if(obj==None):
            return False
        return obj.get_attrib(attr)

    # Set (a) module parameter(s)
    def set(self,key,attr,value):
        obj = self.__objectTbl.get(key)
        if(obj==None):
            return False
        obj.set_attrib(attr,value)
        return True

    # Start Activity
    def call(self,key,cmd,option):
        obj = self.__objectTbl.get(key)
        if(obj==None):
            return [(False,0,ModuleConstant.INVALID)]
        return obj.execute(cmd,option)

    # -------------------------------->

    # <--------------------------------
    # @ Module Loader
    def init(self):
        self.__objectTbl = {}
        self.__importTbl = {}

    def clear(self):
        keylist = self.__objectTbl.copy().keys()
        for k in keylist:
            self.unloadObject(k)

        keylist = self.__importTbl.copy().keys()
        for k in keylist:
            self.unloadModule(k)
        
    # Load/Unload a python package
    def loadModule(self,module):
        try:
            tmp = importlib.import_module(module)
            self.__importTbl.update({module:tmp})
            return tmp
        except:return None

    def loadModuleAs(self,module,alias):
        try:
            tmp = importlib.import_module(module)
            self.__importTbl.update({alias:tmp})
            return tmp
        except:return None

    def unloadModule(self,module):
        tmp = self.__importTbl.pop(module,None)
        if(tmp!=None):
            try:del tmp
            except:pass
            return
        return tmp

    def getModuleHandle(self,module):
        return self.__importTbl.get(module,None)

    # Load/Unload a module
    def loadObject(self,name,module):
        self.__objectTbl.update({name:module})

    def unloadObject(self,name):
        tmp = self.__objectTbl.pop(name,None)
        if(tmp!=None):
            try:del tmp
            except:pass
            return
        return tmp

    # Check
    def checkModuleLoaded(self,module):
        return (True if module in self.__importTbl.keys() else False)

    def getLoadedModuleList(self):
        return self.__importTbl.copy()

    def checkObjectLoaded(self,name):
        return (True if name in self.__objectTbl.keys() else False)

    def getLoadedObjectList(self):
        return self.__objectTbl.copy()

    # load("module_name","class_name")
    def load(self,module,clss):
        if(self.checkModuleLoaded(module)==False):
            if(self.loadModule(module)==None):
                return None
        try:
            ClassObject = getattr(self.getModuleHandle(module),clss)
            Object      = ClassObject()
            self.loadObject(module,Object)
            return True
        except:
            return False

    # loadClass("module_name","class_name")
    def loadClass(self,module,clss):
        if(self.checkModuleLoaded(module)==False):
            return False
        try:
            ClassObject = getattr(self.getModuleHandle(module),clss)
            Object      = ClassObject()
            self.loadObject(module,Object)
            return True
        except:
            return False

    # loadLibrary("module_name")
    def loadLibrary(self,module):
        if(self.checkModuleLoaded(module)==False):
            if(self.loadModule(module)==None):
                return None
            return True
        return False

    # loadLibraryAs("module_name","namespace")
    def loadLibraryAs(self,module,alias):
        if(self.checkModuleLoaded(alias)==True):
            return False
        if(self.checkModuleLoaded(module)==False):
            if(self.loadModuleAs(module,alias)==None):
                return None
            return True
        return False

    # unloadLibrary("module_name")
    def unloadLibrary(self,module):
        if(self.checkModuleLoaded(module)==False):
            return False
        return self.unloadModule(module)

    # loadModuleClassAs("module_name","class_name","namespace")
    def loadModuleClassAs(self,module,cls,alias=None):
        if(alias!=None):
            self.loadLibraryAs(module,alias)
            return self.loadClass(alias,cls)
        else:
            self.loadLibrary(module)
            return self.loadClass(module,cls)

    # -------------------------------->


if __name__ == '__main__':

    def signal_handler(signal,frame):
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    # python .\actuator.py -t module_bmp -f '.\sample\img.bmp' -i module_bmp -c ModuleBMP
    mod    = Actuator()
    parser = argparse.ArgumentParser(description="select run mode")
    parser.add_argument("-t",action="store",dest="target",type=str,default='n',     required=True)
    parser.add_argument("-f",action="store",dest="file",type=str,default='n',       required=True)
    parser.add_argument("-e",action="store",dest="encode",type=str,default='euc-kr',required=False)
    parser.add_argument("-b",action="store",dest="block",type=int,default=1024,     required=False)
    parser.add_argument("-from",action="store",dest="start",type=int,default=0,     required=False)
    parser.add_argument("-to",action="store",dest="end",type=int,default=0,         required=False)
    parser.add_argument("-cmd",action="store",dest="cmd",type=str,default=None,     required=False)
    parser.add_argument("-opt",action="store",dest="option",type=bool,default=True, required=False)
    parser.add_argument("-i",action="store",dest="lib",type=str,default=None,       required=False)
    parser.add_argument("-c",action="store",dest="cls",type=str,default=None,       required=False)

    args = parser.parse_args()

    _request  = args.target
    _file     = args.file
    _encode   = args.encode
    _base     = args.start
    _last     = args.end
    _block    = args.block
    _cmd      = args.cmd
    _opt      = args.option
    _lib      = args.lib
    _cls      = args.cls

    if(_block<=0):
        print("[!] Error")
        sys.exit(0)
    
    if(_lib!=None and _cls!=None):
        mod.load(_lib,_cls)

    if(_request not in mod.getLoadedObjectList().keys()):
        print("[!] Unsupport type")
        sys.exit(0)

    print("[*] Start to verify type of the file.")

    mod.set(_request,ModuleConstant.FILE_ATTRIBUTE,_file)          # File to carve
    mod.set(_request,ModuleConstant.IMAGE_BASE,_base)              # Set start offset of the file base
    mod.set(_request,ModuleConstant.IMAGE_LAST,_last)              # Set last offset of the file base
    mod.set(_request,ModuleConstant.ENCODE,_encode)                # Set encode type
    mod.set(_request,ModuleConstant.CLUSTER_SIZE,_block)           # Set cluster size

    cret = mod.call(_request,_cmd,_opt)

    print("[*] Result :\n(Start offset, Valid size, Record Type)")
    print(cret)

    sys.exit(0)
