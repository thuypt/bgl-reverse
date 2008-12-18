import io
import os
import gzip
from util import *
import gls

class BGL(gzip.GzipFile):
    def __init__(self,path):
        fo=io.FileIO(path,'r')
        spec=parseInt(fo.read(4))
        if spec==0x12340001:
            fo.seek(0x47)
        elif spec==0x12340002:
            fo.seek(0x69)
        else:
            raise IOError("not a bgl file: {0:#x}".format(spec))
        gzip.GzipFile.__init__(self,fileobj=fo)

    def readRecord(self):
        """read a record from a bgr file, return (rec_type,data), None if eof"""
        hdr=self.read(1)
        if len(hdr)>0:
            hdr=hdr[0]
        else:
            return None
        
        high_nibble=hdr>>4
        rec_type=hdr&0x0F
    
        if high_nibble>=4:
            rec_len=high_nibble-4
        else:
            rec_len=parseInt(self.read(high_nibble+1))
        return (rec_type,self.read(rec_len))


def parseBlkA(data,n):
    "parse a Block_A: n bytes of length indicator and data next, returns (parsed, unparsed)"
    blk_len=parseInt(data[0:n])
    return (data[n:n+blk_len],data[n+blk_len:])

def parseBlkB(data,size):
    """parse a Block_B: 1 byte specifier and data next,returns (spec,parsed,unparsed)"""
    return (data[0],data[1:size+1],data[size+1:])

def parseTranscription(data):
    """data should be a Block_A"""
    parseInt(data[0:2])

def parseTermProp(rawprop,tail):
    """return a dict"""
    prop={}
    
    return deftail

def parseGLSProp(data):
    return (parseInt(data[0:2]),data[2:])

def parseGLSParam(data):
    return (parseInt(data[0:1]),data[1:])

def parseTerm(data):
    
    (title,data)=parseBlkA(data,1)
    (termbody,data)=parseBlkA(data,2)
    if len(data)>0:
        termtail=parseBlkA(data,1)[0]
    else:
        termtail=b''
    
    (definition,*data)=termbody.split(b'\x14',1)
    if len(data)>0:
        termprop=data[0]
    else:
        termprop=b''
    return (title,definition,termprop,termtail)

def parseResource(data):
    resdata=parseBlkA(data,1)
    return Resource(resdata[0],resdata[1])


class BGR(BGL):
    """a base class that is capable of reading records"""
    def __init__(self,path):
        """create a BGR reader"""
        BGL.__init__(self,path)
        return

    def readTerm(self):
        pass

    def readParam(self):
        pass

    def readProp(self):
        pass

    def readnparse(self):
        rec=self.read()
        if rec==None:
            return
        if rec[0]==RC_ENTRY_1:
            ent=parseEntry(rec[1])
            phon=ent[2].get(0x1B)
            if phon!=None:
                ent[2][0x1B]=replaceCharsetTag(replaceHTMLEntity(phone),"ISO-8859-1")
            return (
                replaceCharsetTag(ent[0],self.info["Source Encoding"]),
                replaceCharsetTag(ent[1],self.info["Target Encoding"]),
                ent[2],
                replaceCharsetTag(ent[3],self.info["Source Encoding"]))
            return ent
        
        if rec[0]==RC_RES:
            return parseResource(rec[1])
        return rec

    def parseInfo(self):
        rawparam=self.rawparam
        rawprop=self.rawprop
        info={}
        info["Default Encoding"]=CHARSET[parseInt(rawmeta[0x08])]
        info["Glossary Name"]=rawinfo[0x01].decode(info["Default Encoding"])
        info["Author"]=rawinfo[0x02].decode(info["Default Encoding"])
        info["Author Email"]=rawinfo.get(0x03,b'').decode(info["Default Encoding"])
        info["Copyright"]=rawinfo[0x04].decode(info["Default Encoding"])
        info["Source Language"]=LANGUAGE[parseInt(rawinfo[0x07])]
        info["Target Language"]=LANGUAGE[parseInt(rawinfo[0x08])]
        info["Description"]=rawinfo[0x09].decode(info["Default Encoding"])
        info["Entry Count"]=parseInt(rawinfo[0x0C])
        info["Source Encoding"]=CHARSET[parseInt(rawinfo[0x1A])]
        info["Target Encoding"]=CHARSET[parseInt(rawinfo[0x1B])]
        return info


