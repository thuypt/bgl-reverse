import io
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
        self.param={}
        self.property={}
        self.srcCharset="latin1"
        self.targCharset="latin1"
        return
    
    def moveForward(self):
        while True:
            self.current=readRecord(self)
            if self.current==None:
                return False
            elif self.current[0]==0:
                if len(self.current[1])>0:
                    (k,v)=parseGLSParam(self.current[1])
                    self.setProperty(k,v)
            elif self.current[0]==3:
                if len(self.current[1])>0:
                    (k,v)=parseGLSProperty(self.current[1])
                    self.setProperty(k,v)
            else:
                return True

    def setProperty(self,k,v):
        self.property[k]=v
        if k==0x1A:
            self.srcCharset=gls.CHARSET[v]
        elif k==0x1B:
            self.targCharset=gls.CHARSET[v]

    def setParam(self,k,v):
        self.property[k]=v
    
    def parseAsResource(self):
        resdata=parseRecordBlock(self.current[1],1)
        return gls.GlsResource(resdata[0].decode('utf-8'),resdata[1])

    def parseAsTerm(self):
        data=self.current[1]
        if self.current[0]==gls.RC_GLSTERM1 or self.current[0]==gls.RC_GLSTERMA:
            (title,data)=parseRecordBlock(data,1)
        else:
            (title,data)=parseRecordBlock(data,2)
        
        (termbody,data)=parseRecordBlock(data,2)
        if len(data)>0:
            termtail=parseRecordBlock(data,1)[0]
        else:
            termtail=b''
        title=title.decode(self.srcCharset)
        (definition,*data)=termbody.split(b'\x14',1)        
        if len(data)>0:
            termprop=data[0]
        else:
            termprop=b''
        return gls.GlsTerm(
            title,
            decode(definition,self.targCharset),
            parseTermProperty(termprop,self.srcCharset),
            decode(termtail,self.srcCharset))

def readRecord(f):
    """read a record from a bglr file, return (rec_type,data), None if eof"""
    hdr=f.read(1)
    if len(hdr)>0:
        hdr=hdr[0]
    else:
        # eof
        return None
    high_nibble=hdr>>4
    rec_type=hdr&0x0F
    if high_nibble>=4:
        rec_len=high_nibble-4
    else:
        rec_len=parseInt(f.read(high_nibble+1))
    return (rec_type,f.read(rec_len))

def parseRecordBlock(data,x):
    """return a tuple (blockdata,tail)"""
    length=parseInt(data[0:x])
    return (data[x:x+length],data[x+length:])

def parseTermProperty(rawprop,charset):
    """return a dict"""
    prop={}
    while len(rawprop)>1:
        spec=rawprop[0]
        if spec<0x10:
            prop[spec&0x0F]=rawprop[1]
            rawprop=rawprop[2:]
        elif spec<0x40:            
            (prop[spec&0x0F],rawprop)=parseRecordBlock(rawprop[1:],(spec>>4))
        elif (spec&0xF0)==0x40:
            newspec=rawprop[1]
            prop[newspec]=rawprop[2:(spec&0x0F)+1+2]
            rawprop=rawprop[(spec&0x0F)+1+2:]
        elif spec>=0x50:
            newspec=rawprop[1]
            (prop[newspec],rawprop)=parseRecordBlock(rawprop[2:],(spec>>4)-4)
        else:
            raise Exception([rawprop,prop,spec])
    if 0x1b in prop.keys():
        prop[0x1b]=prop[0x1b].decode(charset) #transcription
    if 0x08 in prop.keys():
        prop[0x08]=prop[0x08].decode(charset) #display name
    return prop

def parseGLSProperty(data,charset="latin1"):
    k=parseInt(data[0:2])
    v=data[2:]
    if k in set([0x01,0x02,0x03,0x04,0x09]):
        return (k,v.decode(charset))
    elif k in set([0x07,0x08,0x0C,0x1A,0x1B,0x33,0x1C]):
        return (k,parseInt(v))
    else:
        return (k,v)

def parseGLSParam(data):
    return (parseInt(data[0:1]),data[1:])


