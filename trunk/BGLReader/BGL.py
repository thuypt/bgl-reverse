from util import *
from bgrformat import *

def readRecord(f):
    hdr=f.read(1)[0]
    high_nibble=hdr>>4
    rec_type=hdr&0x0F
    
    if high_nibble>=4:
        rec_len=high_nibble-4
    else:
        rec_len=parseInt(f.read(high_nibble+1))
    return (rec_type,f.read(rec_len))

def parseBlock_A(data,size):
    blk_len=parseInt(data[0:size])
    return (data[size:size+blk_len],data[size+blk_len:])

def parseBlock_B(data,size):
    """return a tuple (spec,parsed,unparsed)"""
    return (data[0],data[1:size+1],data[size+1:])

def parseDefinitionTail(tail):
    """return a tuple (word_class,display_name,word_variation, alternatives)"""
    deftail={}
    tailbackup=tail
    while len(tail)>0:
        spec=tail[0]
        if (spec == 0x06) or (spec == 0x02):
            deftail[spec]=tail[1]
            tail=tail[2:]
            continue
        elif spec == 0x13: # unknown, only found in eng-eng dictionary
            deftail[spec]=tail[1]
            tail=tail[2:]
            continue
        elif spec == 0xC7: # unknown, only found in eng-eng dictionary
            deftail[spec]=None
            tail=tail[1:]
        elif spec == 0x50:
            spec = tail[1]
            (deftail[spec],tail)=parseBlock_A(tail[2:],1)
            continue
        elif spec == 0x60:
            spec = tail[1]
            (deftail[spec],tail)=parseBlock_A(tail[2:],2)
        elif spec == 0x18: # display name
            (deftail[spec],tail)=parseBlock_A(tail[1:],1)
            continue
        elif (spec>>4)==4:
            (spec,data,tail)=parseBlock_B(tail[1:],(spec&0x0F)+1)
            deftail[0x4000+spec]=data
            continue
        else:
            print([tailbackup,tail])
            raise Exception("unknown data: "+str(spec)+"\n")
    return deftail

def parseInfo(data):
    return (util.parseInt(data[0:2]),data[2:])

def parseMeta(data):
    return (util.parseInt(data[0:1]),data[1:])

def parseEntry(data):
    (hw,data)=parseBlock_A(data,1)
    (defs,data)=parseBlock_A(data,2)
    if len(data)>0:
        entry_tail=parseBlock_A(data,1)[0]
    else:
        entry_tail=b''
    
    (def_text,*def_tail)=defs.split(b'\x14',1)
    if len(def_tail)>0:
        def_tail=def_tail[0]
    else:
        def_tail=b''
    return (hw,def_text,parseDefinitionTail(def_tail),entry_tail)

class BGR:
    def __init__(self,path):
        self.file=open(path,"rb")
        self.eof=False
        rawinfo={}
        rawmeta={}
        while True:
            rec=self.read()
            if rec[0]==RC_NULL_1:
                break
            if rec[0]==RC_META:
                (meta,data)=parseMeta(rec[1])
                rawmeta[meta]=data
                continue
            elif rec[0]==RC_INFO:
                (info,data)=parseInfo(rec[1])
                rawinfo[info]=data
                continue
        
        self.rawinfo=rawinfo
        self.rawmeta=rawmeta
        self.info=self.parseInfo()
        return

    def read(self):
        rec=readRecord(self.file)
        if rec[0]==RC_EOF:
            self.eof=True
        return rec

    def readnparse(self):
        rec=self.read()
        if rec[0]==RC_ENTRY_1:
            ent=parseEntry(rec[1])
            phone=ent[2].get(0x1B)
            if phone!=None:
                ent[2][0x1B]=replaceCharsetTag(replaceHTMLEntity(phone),"ISO-8859-1")
            return (
                replaceCharsetTag(ent[0],self.info["Source Encoding"]),
                replaceCharsetTag(ent[1],self.info["Target Encoding"]),
                ent[2],
                replaceCharsetTag(ent[3],self.info["Source Encoding"]))

    def parseInfo(self):
        rawmeta=self.rawmeta
        rawinfo=self.rawinfo
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


